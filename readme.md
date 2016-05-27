# Vipar - Visualization and Imaging Package for ASTECAM Reduction

+ version: 0.1.0 (alpha)
+ author: Akio Taniguchi (IoA, UTokyo)

## Summary

Vipar is a visualization and imaging package for ASTECAM reduction.

## Dependencies

+ CASA - Common Astronomy Software Application
    - we recommend to use CASA whose release is >= 4.5.0

In the case of Mac OSX, FITS I/O package `pyfits` is not included in CASA 4.6.0.
We don't know the reason (any mistake?) and now asking for ALMA Helpdesk.
Anyway please use Vipar with CASA < 4.6.0 for a while.

## Installation

1. Install [CASA (>= 4.5)][casa] and type `!create-symlinks` on a CASA prompt
1. Execute `setup.sh` on a terminal
1. Now you can use Vipar tasks whose name begin with mb* on a CASA prompt.

[casa]: https://casa.nrao.edu/casa_obtaining.shtml
[casa-python]: https://github.com/radio-astro-tools/casa-python
