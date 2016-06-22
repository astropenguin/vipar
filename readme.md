# Vipar - Visualization and Imaging Package for ASTE/TESCAM Reduction

+ version: 0.2.2 (alpha)
+ author: Akio Taniguchi (IoA, UTokyo)

## Summary

Vipar is a visualization and imaging package for ASTE/TESCAM reduction.

## Dependencies

+ CASA - Common Astronomy Software Application
    - we recommend to use CASA >= 4.5.0

In the case of Mac OSX El Capitan, FITS I/O package `pyfits` is not included in CASA 4.6.0.
This is a bug and reported to CASA developers by sending a ticket to ALMA Helpdesk.
So please use Vipar with CASA < 4.6.0 for a while.

## Installation

1. Install [CASA (>= 4.5)][casa] and type `!create-symlinks` on a CASA prompt
1. Execute `setup.sh` on a terminal

## How to use

+ to use Vipar in CASA, execute vipar.py on a CASA prompt:
    - e.g. `CASA <2>: execfile('/path/to/Vipar/vipar.py')`

(only for development use)

+ to use Vipar outside CASA, execute vipardev.py on a (I)Python prompt:
    - e.g. `>>> execfile('/path/to/Vipar/vipardev.py')`

[casa]: https://casa.nrao.edu/casa_obtaining.shtml
