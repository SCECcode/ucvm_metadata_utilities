# ucvm_metadata_utilities
This repo contains scripts for working with ucvm metadata files. UCVM plotting routines, query UCVM and output PNG files produced using matplotlib. UCVM plotting also outputs the data, and metadata files used to created the PNG files. These utilities scripts are useful for users that want to use the data shown in the PNG plots created by UCVM plotting routintes.

# Introduction
UCVM metadata files are produced by the UCVM website. They are also produced by the UCVM plotting routines. Three types of UCVM plotting queries are currently supported including vertical profile plots, vertical cross section plots, and horizontal slice plots. The data directories in this repo contain examples of these plots, as png files, and the associated data and metadata files that contain the data used to create the pngs. 

# Python3 versus Python2
These scripts use Python3. The UCVM plotting scripts use Python2. The plotting scripts have not been updated to Python3 because some of the required libraries (basemap) are not available for Python3, so the upgrade to Python3 will take substantial time. We typically recommend using Anaconda virtual enviroments for working with UCVM plotting. This will allow users to change between a python2 and python3 environment easily. 

Core UCVM is a C-language program and does not require a specific Python. UCVM_Plotting is a Python2 language program, so if you are using the UCVM plotting scripts directly, you should setup a Python2 environment as the base environment.
The following example shows how users can change between a Python2 environment (for generating the UCVM plots, data, and metadata files), and a Python3 environment for running these metadata utility scripts. This assumes your Python2 environment is active, and a Python3 environment called python3.

- % conda deactivate
- Run UCVM_Plotting scripts

- % conda activate python3
- Run these ucvm metadata utility scripts


# Use Case
These scripts read the UCVM metadata files and convert them to simpler text file formats. Three cases are currently support:

1. Convert vertical profiles data (json) and metadata (json) files to a CSV file.
2. Convert a vertical cross section data (binary) and metadata (json) file to a CSV file.
3. Convert a horizontal slice data (binary) and metadata (json) file to a CSV file.

In both cases, the UCVM Files are converted into panda dataframes and then written out as CSV files.

# Example Usage:
The following examples call the conversion scripts and input the example input data files in this repository. These example input data files were produced by running the UCVM_Plotting scripts.

1. ucvm_profile2csv.py 1ddta/UCVM_1618866062727vertical_matprops.json 1ddata/UCVM_1618866062727vertical_meta.json
2. ucvm_cross_section2csv.py 2ddata/cross-cvmsi_data.bin 2ddata/cross-cvmsi_meta.json
3. ucvm_horizontal_slice2csv.py 2ddata/cvms_poisson_map_data.bin 2ddata/cvms_poisson_map_meta.json

# Documentation:
- [UCVM metadata utilities Wiki](https://github.com/SCECcode/ucvm_metadata_utilities/wiki)

# Support
Please send questions/issue to software (at) scec.org
