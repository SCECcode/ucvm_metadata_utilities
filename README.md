# ucvm_metadata_utilities
Scripts for working with ucvm metadata files.
UCVM metadata files are produced by the UCVM website.
They are also produced by the UCVM plotting routines.
These scripts read the UCVM metadata files and convert them to simpler text file formats.
Two cases are currentl support:
(1) Convert vertical profiles data (json) and metadata (json) files to a CSV file.
(2) Convert a vertical profile data (binary) and metadata (json) file to a CSV file.
In both cases, the UCVM Files are converted into panda dataframes and then written out as CSV files.
