# coding: utf-8

import numpy as np

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
