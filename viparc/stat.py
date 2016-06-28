# coding: utf-8

'''
stat.py - Vipar's statistic module

+ developer: Akio Taniguchi (IoA, UTokyo)
+ contact: taniguchi@ioa.s.u-tokyo.ac.jp
'''

# common preamble
import os
import sys
import inspect
import numpy as np

# unique preamble
import pyfits as fits
from copy import deepcopy
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter


class PCA:
    def __init__(self, scan):
        scan = np.asarray(scan)
        self.U, self.d, self.Vt = np.linalg.svd(scan, full_matrices=False)

        self.eigen = self.d**2
        self.sumvariance = np.cumsum(self.eigen)
        self.sumvariance /= self.sumvariance[-1]

        for d in self.d:
            if d > self.d[0] * 1e-6:
                self.dinv = np.array([1/d])
            else:
                self.dinv = np.array([0])

    def reconstruct(self, fraction):
        npc = np.searchsorted(self.sumvariance, fraction) + 1
        scan = np.dot(self.U[:,:npc], np.dot(np.diag(self.d[:npc]), self.Vt[:npc]))
        self.npc_last = npc
        return scan


class CheckConvergence(object):
    def __init__(self, N_max=10, threshold=0.01):
        self.N_max = N_max
        self.N_call = 0
        self.threshold = threshold

    def __call__(self, *p_now):
        if self.N_call == 0:
            p_now = np.array(p_now)
            self.p_prev = p_now
            self.N_call += 1
            return False

        elif 1 <= self.N_call <= self.N_max:
            p_now = np.array(p_now)
            p_diff = (p_now-self.p_prev)/self.p_prev
            d_diff = np.linalg.norm(p_diff)
            print('{0}: {1}'.format(self.N_call, d_diff)) # debug
            self.p_prev = p_now
            self.N_call += 1
            return d_diff <= self.threshold

        else:
            raise Exception


class Gaussian2D(object):
    def __init__(self, b_0=23.0, pm='auto', threshold=5.0):
        '''Gaussian 2D fit class.

        Args:
        - b_0 (float): typical beam size for initial guess [arcsec]
        - pm (str): +/- of Gaussian peak
        - threshold (float): threshold of S/N
        '''
        self.b_0 = float(b_0)
        self.pm = pm
        self.threshold = threshold

    def __call__(self, mg_daz, mg_del, mp_data):
        '''Fit 2D Gaussian to a map.

        Args:
        - mg_daz (2D array): meshgrid of dAz [arcsec]
        - mg_del (2D array): meshgrid of dEl [arcsec]
        - mp_data (2D array): data map [arbitrary unit]

        Returns:
        - hd_fit (Header): FITS header object containing the results of fit
        - mp_fit (2D array): fit map [arbitrary unit]
        '''
        # preprocessing
        mp_data = deepcopy(mp_data)
        mp_data[np.isnan(mp_data)] = np.nanmedian(mp_data)
        self.mg_daz, self.mg_del = mg_daz, mg_del
        self.mp_data = mp_data

        # step 1: initial parameters (*_0)
        bmaj_0, bmin_0, pa_0 = self.b_0, self.b_0, 0.0

        gridsize = [np.mean(np.diff(mg)) for mg in (mg_daz, mg_del)]
        sigma = self.b_0 / (2*np.sqrt(np.log(2))) / np.linalg.norm(gridsize)
        mp_gauss = gaussian_filter(mp_data, sigma)
        if pm == 'auto':
            peak_pos = np.max(mp_gauss) - np.median(mp_gauss)
            peak_neg = np.median(mp_gauss) - np.min(mp_gauss)
            argfunc = np.argmax if peak_pos > peak_neg else np.argmin
        elif pm == 'positive':
            argfunc = np.argmax
        elif pm == 'negative':
            argfunc = np.argmin

        j, i = np.unravel_index(argfunc(mp_gauss), mp_gauss.shape)
        xp_0, yp_0 = mg_daz[j,i], mg_del[j,i]

        f = self.partial(xp=xp_0, yp=yp_0, bmaj=bmaj_0, bmin=bmin_0, pa=pa_0)
        popt, pcov = curve_fit(f, (mg_daz, mg_del), mp_data.flatten())
        ampl_0, offset_0 = popt

        # step 2: if initial S/N<threshold, then stop fitting
        sd_0 = self._estimate_sd(xp_0, yp_0, bmaj_0, bmin_0)
        sn_0 = np.abs(ampl_0/sd_0)
        if sn_0 < threshold:
            return self._failed_results()

        # step 3: iterative fit
        cc = CheckConvergence()
        try:
            while not cc(xp_0, yp_0, bmaj_0, bmin_0, pa_0, ampl_0, offset_0):
                # bmaj, bmin, pa
                f = self.partial(xp=xp_0, yp=yp_0, ampl=ampl_0, offset=offset_0)
                pinit = [bmaj_0, bmin_0, pa_0]
                popt, pcov = curve_fit(f, (mg_daz, mg_del), mp_data.flatten(), pinit)

                bmaj_0, bmin_0, pa_0 = popt
                bmaj_e, bmin_e, pa_e = np.sqrt(np.diag(pcov))
                if bmaj_0 < bmin_0:
                    bmaj_0, bmin_0 = bmin_0, bmaj_0
                    bmaj_e, bmin_e = bmin_e, bmaj_e
                    pa_0 += 90.0

                pa_0 %= 180.0

                # xp, yp
                f = self.partial(bmaj=bmaj_0, bmin=bmin_0, pa=pa_0, ampl=ampl_0, offset=offset_0)
                pinit = [xp_0, yp_0]
                popt, pcov = curve_fit(f, (mg_daz, mg_del), mp_data.flatten(), pinit)

                xp_0, yp_0 = popt
                xp_e, yp_e = np.sqrt(np.diag(pcov))

                # ampl, offset
                f = self.partial(xp=xp_0, yp=yp_0, bmaj=bmaj_0, bmin=bmin_0, pa=pa_0)
                pinit = [ampl_0, offset_0]
                popt, pcov = curve_fit(f, (mg_daz, mg_del), mp_data.flatten(), pinit)

                ampl_0, offset_0 = popt
                ampl_e, offset_e = np.sqrt(np.diag(pcov))

        except:
            return self._failed_results()

        # step 4: fit all parameters
        try:
            f = self.partial()
            pinit = np.array([xp_0, yp_0, bmaj_0, bmin_0, pa_0, ampl_0, offset_0])
            popt, pcov = curve_fit(f, (mg_daz, mg_del), mp_data.flatten(), pinit)
        except:
            return self._failed_results()

        xp, yp, bmaj, bmin, pa, ampl, offset = popt
        xp_e, yp_e, bmaj_e, bmin_e, pa_e, ampl_e, offset_e = np.sqrt(np.diag(pcov))
        if bmaj < bmin:
            bmaj, bmin = bmin, bmaj
            bmaj_e, bmin_e = bmin_e, bmaj_e
            pa += 90.0

        pa %= 180.0

        # step 5: if S/N<threshold, then return failed results
        sd = self._estimate_sd(xp, yp, bmaj, bmin)
        sn = np.abs(ampl/sd)
        if np.ma.is_masked(sn):
            return self._failed_results()
        elif sn < threshold:
            return self._failed_results()
        else:
            mp_fit = f((mg_daz, mg_del), *popt).reshape(mp_data.shape)
            chi2 = np.sum(((mp_data-mp_fit)/sd)**2) / mp_data.size
            hd_fit = fits.Header()
            hd_fit['FIT_FUNC'] = 'Gaussian2D', 'fitting function'
            hd_fit['FIT_STAT'] = 'success', 'fiting status'
            hd_fit['FIT_CHI2'] = chi2, 'reduced Chi^2 (no unit)'
            hd_fit['FIT_SD']   = sd, 'S.D. of map (no unit)'
            hd_fit['FIT_SN']   = sn, 'S/N of amplitude (no unit)'
            hd_fit['PAR_DAZ']  = xp, 'offset in dAz (arcsec)'
            hd_fit['PAR_DEL']  = yp, 'offset in dEl (arcsec)'
            hd_fit['PAR_BMAJ'] = bmaj, 'major beamsize (arcsec)'
            hd_fit['PAR_BMIN'] = bmin, 'minor beamsize (arcsec)'
            hd_fit['PAR_PA']   = pa, 'position angle (degree)'
            hd_fit['PAR_AMPL'] = ampl, 'amplitude (no unit)'
            hd_fit['PAR_OFFS'] = offset, 'offset (no unit)'
            hd_fit['ERR_DAZ']  = xp_e, 'offset in dAz (arcsec)'
            hd_fit['ERR_DEL']  = yp_e, 'offset in dEl (arcsec)'
            hd_fit['ERR_BMAJ'] = bmaj_e, 'major beamsize (arcsec)'
            hd_fit['ERR_BMIN'] = bmin_e, 'minor beamsize (arcsec)'
            hd_fit['ERR_PA']   = pa_e, 'position angle (degree)'
            hd_fit['ERR_AMPL'] = ampl_e, 'amplitude (no unit)'
            hd_fit['ERR_OFFS'] = offset_e, 'offset (no unit)'

            return hd_fit, mp_fit

    @staticmethod
    def func((x, y), xp, yp, bmaj, bmin, pa, ampl, offset):
        '''Return 2D Gaussian as a flat array.

        Args:
        - (x, y) (array, array) : Input map coordinates [arbitrary unit]
        - xp (float): Peak x (dAz) position of 2D Gaussian [arbitrary unit]
        - yp (float): Peak y (dEl) position of 2D Gaussian [arbitrary unit]
        - bmaj (float): Major beam size of 2D Gaussian [arbitrary unit]
        - bmin (float): Minor beam size of 2D Gaussian [arbitrary unit]
        - pa (float): Position angle of 2D Gaussian [degree]
        - ampl (float): Amplitude of 2D Gaussian [arbitrary unit]
        - offset (float): Baseline offset of 2D Gaussian [arbitrary unit]

        Returns:
        - Gaussian (1D array): Flatten 2D Gaussian [arbitrary unit]
        '''
        xp, yp = float(xp), float(yp)
        bmaj, bmin, pa = float(bmaj), float(bmin), float(pa)
        ampl, offset = float(ampl), float(offset)

        sigx = np.sqrt(2*np.log(2))*bmaj/2
        sigy = np.sqrt(2*np.log(2))*bmin/2
        theta = np.deg2rad(-pa+90.0)

        a = (np.cos(theta)**2)/(2*sigx**2) + (np.sin(theta)**2)/(2*sigy**2)
        b = -(np.sin(2*theta))/(4*sigx**2) + (np.sin(2*theta))/(4*sigy**2)
        c = (np.sin(theta)**2)/(2*sigx**2) + (np.cos(theta)**2)/(2*sigy**2)
        g = offset + ampl * np.exp(-(a*(x-xp)**2-2*b*(x-xp)*(y-yp)+c*(y-yp)**2))

        return g.flatten()

    def partial(self, **kwargs):
        '''Return a new function with some args fixed.

        Args:
        - kwargs: Args and fixed values

        Returns:
        - func (function): A new function with some args fixed
        '''
        args = inspect.getargspec(self.func).args
        args.pop(0) # ('x', 'y')

        args_fnew = list(args)
        for key in kwargs.keys():
            args_fnew.remove(key)

        args_f = []
        for arg in args:
            if arg in kwargs.keys():
                args_f.append('{0}={1}'.format(arg, kwargs[arg]))
            else:
                args_f.append('{0}={1}'.format(arg, arg))

        args_fnew = ','.join(args_fnew)
        args_f = ','.join(args_f)

        func_str = 'lambda (x,y),{0}: self.func((x,y),{1})'
        func = eval(func_str.format(args_fnew, args_f), locals())

        return func

    def _estimate_sd(self, xp, yp, bmaj, bmin):
        '''Estimate S.D. of data using current fit parameters.

        Args:
        - xp (float): Peak x (dAz) position of 2D Gaussian [arbitrary unit]
        - yp (float): Peak y (dEl) position of 2D Gaussian [arbitrary unit]
        - bmaj (float): Major beam size of 2D Gaussian [arbitrary unit]
        - bmin (float): Minor beam size of 2D Gaussian [arbitrary unit]

        Returns:
        - sd_est (float): Estimated S.D. of data [arbitrary unit]
        '''
        width = bmaj + bmin
        mp_mask_daz = (self.mg_daz>xp-width) & (self.mg_daz<xp+width)
        mp_mask_del = (self.mg_del>yp-width) & (self.mg_del<yp+width)
        mp_noise = np.ma.array(self.mp_data, mask=(mp_mask_daz & mp_mask_del))
        sd_est = np.std(mp_noise)

        return sd_est

    def _failed_results(self):
        '''Return results in case of failed fit.

        Args:
        this method requires no arguments.

        Returns:
        - hd_fit (Header): FITS header object containing the results of fit
        - mp_fit (2D array): map with nan values [arbitrary unit]
        '''
        mp_fit = np.full(self.mp_data.shape, np.nan)
        hd_fit = fits.Header()
        hd_fit['FIT_FUNC'] = 'Gaussian2D', 'fitting function'
        hd_fit['FIT_STAT'] = 'failed', 'fiting status'

        return hd_fit, mp_fit
