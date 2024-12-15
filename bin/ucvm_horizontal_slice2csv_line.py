#!/usr/bin/env python3
"""
ucvm_horizontal_slice2csv_line.py h_data.bin h_meta.json

This script inputs the metadata (json) and data (bin) files produced from the UCVM plotting routines
when doing a horizontal slice plot. This then outputs in csv file format.

lon lat val

skipped outputing row that has val=0.0

"""
import json
import sys
import numpy as np

# import raw floats array data from the external file into
# numpy array
def import_np_float_array(num_x, num_y):
    global fh
    try:
        fh = open(input_data_file, 'rb')
    except:
        print("ERROR: binary np float array data does not exist.")
        exit(1)

    floats = np.load(fh)
    fh.close()
    return floats

if __name__ == '__main__':
    """
    :input: h_data.bin h_meta.json
    :return: h_data.csv file
    
    example input_metadata_file = "h_meta.json"
    example input_data_file = "h_data.bin"
    Reads file names from header of this file.
    Outputs a CSV file with header:
        
# Title: horizontal vs sfcvm
# CVM(abbr): sfcvm
# Data_type: vs
# Depth(m): 0 
# Spacing(degree): 0.01
# Lon_pts: 762 
# Lat_pts: 649 
# Title: 494538
# min_v: 0.0
# max_v: 3502.5
# mean_v: 386.0216979980469
# lat1: 35.02
# lon1: -126.4
# lat2: 41.50
#lon,lat,vs
    """

    if len(sys.argv) != 3:
        raise ValueError("Please provide arguments: ucvm_horizontal_slice2csv.py h_data.bin h_meta.json.\n"
                         "e.g. ./ucvm_horizontal_slice2csv.py h_data.bin h_meta.json")

    input_data_file = sys.argv[1]
    input_metadata_file = sys.argv[2]
    with open(input_metadata_file) as json_data:
        obj = json.load(json_data)

    #
    # The return values here are
    """
    ['num_y', 'lat1', 'data_type', 'lat2', 'color', 'max',
     'title', 'spacing', 'configfile', 'lon_list', 'num_x',
     'outfile', 'depth', 'cvm', 'min', 'datapoints', 'lon1',
     'lat_list', 'lon2', 'installdir', 'mean']
    """
    depth = obj["depth"]
    latlist = obj["lat_list"]
    lonlist = obj["lon_list"]
    npts = obj["datapoints"]
    num_x = obj["num_x"]
    num_y = obj["num_y"]

    #
    total_pts = len(lonlist) * len(latlist)
    datalist = import_np_float_array(len(lonlist), len(latlist))
    # Use shape to return the dimensions of the np array that is returned
    # We assume it is 2D array
    datasizes = datalist.shape
    if npts != (datasizes[0] * datasizes[1]) :
        raise Exception("Number of depth points does not each number of 1ddata points. Exiting", npts, datasizes[0] * datasizes[1])

    if len(lonlist) * len(latlist) != npts:
        print("Error: Total points should equal the number of lats times the number of lons",
              len(lonlist) * len(latlist),npts)
        sys.exit(0)
    #
    # Find properties type
    proptype = obj["data_type"]
    if proptype == "vp":
        propstr = "Vp(m/s)"
    elif proptype == "vs":
        propstr = "Vs(m/s)"
    elif proptype == "density":
        propstr = "Density(kg/m^3)"
    elif proptype == "poisson":
        propstr = "PoissionRatio"
    else:
        raise Exception("Unknown propertype type error type:",proptype)

    #
    # Create output file name
    # Example filename: input_data_file = "cross-cvmsi_meta.json"
    # cross-cvmsi_data.bin cross-cvmsi_meta.json
    output_file_name = input_data_file.replace(".bin",".csv")
    print("\nWriting CSV file: ", output_file_name)
    f = open(output_file_name, "w")

    header_str = '''\
# Title: {9}
# CVM(abbr): {2}
# Data_type: {3}
# Depth(m): {4} 
# Spacing(degree): {5}
# Lon_pts: {6} 
# Lat_pts: {7} 
# Total_pts: {8}
# Min_v: {10}
# Max_v: {11}
# Mean_v: {12}
# Lat1: {13}
# Lon1: {14}
# Lat2: {15}
# Lon2: {16}
# Lon,Lat,{17}
'''.format(
                input_data_file,
                input_metadata_file,
                obj["cvm"],
                obj["data_type"],
                obj["depth"],
                obj["spacing"],
                len(lonlist),
                len(latlist),
                npts,
                obj["title"],
                obj["min"],
                obj["max"],
                obj["mean"],
                obj["lat1"],
                obj["lon1"],
                obj["lat2"],
                obj["lon2"],
                propstr
                )

    print(header_str)
    f.write(header_str)

    # Add each lonlist point as a column.
    for i in range(len(lonlist)):
        for j in range(len(latlist)):
            v=datalist[j][i]
            if(v == -1):
                f.write('{0},{1},nan\n'.format(lonlist[i],latlist[j]));
            else:
                f.write('{0},{1},{2}\n'.format(lonlist[i],latlist[j],v));

    f.close()
    sys.exit(True)
