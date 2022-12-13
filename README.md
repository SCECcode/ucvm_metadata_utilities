# ucvm_metadata_utilities
This repo contains scripts for working with ucvm metadata files. UCVM plotting routines, query UCVM and output PNG files produced using matplotlib. UCVM plotting also outputs the data, and metadata files used to created the PNG files. These utilities scripts are useful for users that want to use the data shown in the PNG plots created by UCVM plotting routintes.

# Introduction
UCVM metadata files are produced by the UCVM website. They are also produced by the UCVM plotting routines. Three types of UCVM plotting queries are currently supported including vertical profile plots, vertical cross section plots, and horizontal slice plots. The data directories in this repo contain examples of these plots, as png files, and the associated data and metadata files that contain the data used to create the pngs. 

# Use Case
These scripts read the UCVM metadata files and convert them to simpler text file formats. Three cases are currently support:

1. Convert vertical profiles data (json) and metadata (json) files to a CSV file.
2. Convert a vertical cross section data (binary) and metadata (json) file to a CSV file.
3. Convert a horizontal slice data (binary) and metadata (json) file to a CSV file.

In both cases, the UCVM Files are converted into panda dataframes and then written out as CSV files.

# Example Usage:
The following examples will input data files in the repository.
- ucvm_profile2csv.py
- ucvm_cross_section2csv.py 2ddata/cross-cvmsi_data.bin 2ddata/cross-cvmsi_meta.json
- ucvm_horizontal_slice2csv.py 2ddata/cvms_poisson_map_data.bin 2ddata/cvms_poisson_map_meta.json

# Support
Please send questions/issue to software (at) scec.org
