# ucvm_metadata_utilities
This repo contains scripts for working with ucvm metadata files.

# Introduction
UCVM metadata files are produced by the UCVM website.
They are also produced by the UCVM plotting routines.

# Use Case
These scripts read the UCVM metadata files and convert them to simpler text file formats.
Two cases are currently support:
1. Convert vertical profiles data (json) and metadata (json) files to a CSV file.
2. Convert a vertical cross section data (binary) and metadata (json) file to a CSV file.
3. Convert a horizontal slice data (binary) and metadata (json) file to a CSV file.

In both cases, the UCVM Files are converted into panda dataframes and then written out as CSV files.

# Example Usage:
The following examples will input data files in the repository.
1. 
2. ucvm_cross_section2csv.py 2ddata/cross-cvmsi_data.bin 2ddata/cross-cvmsi_meta.json
3. ucvm_horizontal_slice2csv.py 2ddata/cvms_poisson_map_data.bin 2ddata/cvms_poisson_map_meta.json

# Support
Please send questions/issue to software (at) scec.org
