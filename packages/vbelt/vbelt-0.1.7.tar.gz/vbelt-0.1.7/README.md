# vbelt

## About

vbelt is a library and a collection of scripts to manipulate VASP output files.

## Script

Available scripts:

- `chgsum`: combine two CHGCAR
- `chgx`: extract channels from CHGCAR
- `ckconv`: check a single-point computation converged
- `ckend`: check the computation ended normally
- `ckforces`: check the forces are converged in an optimization calculation
- `jobtool`: precompute and predict some infos on a job
- `poscartool`: manipulate POSCAR files
- `termdos`: plot a DoS in terminal (WIP)

Run the scripts with `--help` to check for subcommands and options.

## Modules

Available modules:

- `charge_utils`: read and manipulate CHGCAR
- `forces`: extract forces from OUTCAR
- `gencalc`: facilities to generate input files
- `incar`: parse INCAR
- `jobtool`: facilities to predict some job characteristics
- `outcar`: parse some informations from OUTCAR
- `poscar`: read and write POSCAR
- `potcar`: parse some informations from POTCAR

## Installation

Most features only requires numpy, however `gencalc` also requires tc-pysh, chevron and ase.

To install all the optional dependencies use `pip install vbelt[gencalc]`.
For a minimal installation `pip install vbelt`.
