# Data provenance

Derived daily statistics from Réunion TCCON GGG2020 R0, 2015-03-01 to 2020-07-18.
Source DOI: https://doi.org/10.14291/tccon.ggg2020.reunion01.R0
Original file: ra20150301_20200718.public.qc.nc, downloaded 2026-10-09.
Source contact: Martine De Mazière, Royal Belgian Institute for Space Aeronomy.
The observations were collected by TCCON investigators, not by this project's author.
Dataset citation and terms: https://tccondata.org/ and
https://tccon-wiki.caltech.edu/Network_Policy/Data_Use_Policy
Retain the original dataset attribution; this project's MIT code license does not
relicense the measurements. Consult the DOI record before using data in a publication.

Bundled CSV is a derived daily summary, with no gap filling. The full source file is
downloaded separately using scripts/prepare_data.py. CO2 is already ppm; CO is already
ppb; CH4 is supplied in ppm and multiplied by 1000 to obtain ppb. Input is the public
quality-controlled product; no extra unverified instrument flag is assumed.
