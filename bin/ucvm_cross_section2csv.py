#!/usr/bin/env python3
"""
ucvm_cross_section2csv.py:
This script inputs the metadata (json) and data (bin) files produced from the UCVM plotting routines
when doing a vertical cross section plot. This then outputs the panda data frame to a csv file format.
       column => (lat,lon),....
       row => depth[m]
       
"""
import pandas as pd
import json
import sys
import numpy as np
import pdb

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
    :input: c_data.bin c_meta.json 
    :return: c_data.csv file
    
    example input_metadata_file = "cross-cvmsi_meta.json"
    example input_data_file = "cross-cvmsi_data.bin"
    Reads file names from header of this file.
    Outputs a CSV file with header:
    # cvm (abbr) : string
    # data_type : string
    # datapoints (# rows) : XX
    # starting_depth : XX 
    # ending_depth: XX
    # horizontal_spacing: XX
    # vertical_spacing: XX
    # starting_lat_lon: lat1,lon1
    # ending_lat_lon: lat2, lon2
    #
    depth, lat_lon, vp, rho columns
    """

    if len(sys.argv) != 3:
        raise ValueError("Please provide arguments: ucvm_cross_section2csv.py c_data.bin c_meta.json.\n"
                         "e.g. ./ucvm_cross_section2csv.py c_data.bin c_meta.json")

    input_data_file = sys.argv[1]
    input_metadata_file = sys.argv[2]
    with open(input_metadata_file) as json_data:
        obj = json.load(json_data)

    #
    # The return values here are
    """
    ['depth_list', 'color', 'horizontal_spacing', 'datapoints',
     'starting_depth', 'title', 'vertical_spacing', 'data_type', 'max', 'outfile', 
    'lat1', 'lat2', 'ending_depth', 'lon_list', 'num_x', 'num_y', 'cvm', 'min', 'lon1', 'lat_list', 'lon2', 'mean'])
    """
    depthlist = obj["depth_list"]
    latlist = obj["lat_list"]
    lonlist = obj["lon_list"]
    npts = obj["datapoints"]
    # This assumes lat_list and lon_list are the same length. We can use either in this calc
    # which can be restated as # of x_pts * # of y_pts
    # The lat and lon lists are the same length, so we iterate through one, and use the index to
    # create a point string for the query point
    if  len(lonlist) != len(latlist):
        print("Error: lat and lon lists are not the same list, which is assumption for these data files")
        sys.exit(0)
    #
    total_pts = len(depthlist) * len(latlist)
    datalist = import_np_float_array(len(lonlist), len(depthlist))
    # Use shape to return the dimensions of the np array that is returned
    # We assume it is 2D array
    datasizes = datalist.shape
    if npts != datasizes[0] * datasizes[1]:
        raise Exception("Number of depth points does not each number of 1ddata points. Exiting",
                        npts, datasizes[0] * datasizes[1])
    #
    # Combine the
    mystrlist = []
    for i in range(len(latlist)):
        mystr = "(" + str(latlist[i]) + "," + str(lonlist[i]) + ")"
        mystrlist.append(mystr)

    if len(mystrlist) * len(depthlist) != npts:
        print("Error: Total points should equal the number of latlons times the number of data points",
              len(mystrlist) * len(depthlist),npts)
        sys.exit(0)

    #
    # Find properties type
    proptype = obj["data_type"]
    if proptype == "vp":
        propstr = "Vp(km/s)"
    elif proptype == "vs":
        propstr = "Vs(km/s)"
    elif proptype == "density":
        propstr = "Density(kg/m^3)"
    elif proptype == "poisson":
        propstr = "PoissionRatio"
    else:
        raise Exception("Unknown propertype type error type:",proptype)

    dlist = []
    # Create a dataframe with one columen of Depths values
    for idx in range(len(depthlist)):
        dlist.append(depthlist[idx])

    #Convert it to dataframe
    df = pd.DataFrame(dlist,columns=["Depths[m]"])

    # Add each latlon point as a column. Each lat/long column
    # is expected to be same length as existing column of depths
    for indx in range(len(latlist)):
        colstr = mystrlist[indx]
        vals = []
        for d in range(len(depthlist)):
            vals.append(datalist[d][indx])
        df[colstr] = vals
 
    #
    # Create output file name
    # Example filename: input_data_file = "cross-cvmsi_meta.json"
    # cross-cvmsi_data.bin cross-cvmsi_meta.json
    output_file_name = input_data_file.replace(".bin",".csv")
    print("\nWriting CSV file: ", output_file_name)
    f = open(output_file_name, "w")

    """
    ['depth_list', 'color', 'horizontal_spacing', 'datapoints',
     'starting_depth', 'title', 'vertical_spacing', 'data_type', 'max', 'outfile', 
    'lat1', 'lat2', 'ending_depth', 'lon_list', 'num_x', 'num_y', 'cvm', 'min', 'lon1', 'lat_list', 'lon2', 'mean'])
    """

    header_str = '''\
# Title: {10}
# CVM(abbr): {2}
# Data_type: {3}
# Start_depth(m): {4} 
# End_depth(m): {5} 
# Vert_spacing(m): {6}
# Depth_pts: {7} 
# Horizontal_pts: {8} 
# Total_pts: {9}
# Min_v: {11}
# Max_v: {12}
# Mean_v: {13}
# Num_x: {14}
# Num_y: {15}
# Lat1: {16}
# Lon1: {17}
# Lat2: {18}
# Lon2: {19}
'''.format(input_data_file,input_metadata_file,
                obj["cvm"],
                obj["data_type"],
                obj["starting_depth"],
                obj["ending_depth"],
                obj["vertical_spacing"],
                len(depthlist),
                len(latlist),
                npts,
                obj["title"],
                obj["min"],
                obj["max"],
                obj["mean"],
                obj["num_x"],
                obj["num_y"],
                obj["lat1"],
                obj["lon1"],
                obj["lat2"],
                obj["lon2"]
           )

    print(header_str)
    f.write(header_str)
    df.to_csv(f, float_format='{:5.4f}'.format, index=False, mode="a")
    # This version will remove the column name headers
    #  df.to_csv(f, header=False,float_format='{:5.4f}'.format, index=False, mode="a")
    f.close()
    sys.exit(True)
