#!/usr/bin/env python3
"""
ucvm_cross_section2csv_line.py:
This script inputs the metadata (json) and data (bin) files produced from the UCVM plotting routines
when doing a vertical cross section plot. This then outputs to a csv file format.

lon lat depth val
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
    :input: c_data.bin c_meta.json 
    :return: c_data.csv file
    
    example input_metadata_file = "cross-cvmsi_meta.json"
    example input_data_file = "cross-cvmsi_data.bin"
    Reads file names from header of this file.
  "starting_depth": "0",
  "horizontal_spacing": "852",
  "data_type": "vs",
  "cvm": "sfcvm",
  "color": "sd",
  "outfile": "../result/CVM_1730414702834_c.png",
  "configfile": "/usr/local/share/ucvm/install/conf/ucvm.conf",
  "installdir": "/usr/local/share/ucvm/install",
  "vertical_spacing": "50",
  "lat1": "37.5783",
  "lon1": "-122.658",
  "lat2": "37.7505",
  "lon2": "-121.1362",
  "ending_depth": "5000",
  "title": "sfcvm Cross Section from (-122.66, 37.58) to (-121.14, 37.75)",
  "num_x": 160,
  "num_y": 101,
  "datapoints": 16160,
  "max": 3.454256057739258,
  "min": 0.08067899942398071,
  "mean": 2.3316869735717773,
  "lon_list": ..
  "lat_list": ..
  "depth_list": ..
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

    if total_pts != npts:
        print("Error: Total points should equal the number of latlons times the number of data points",
              total_pts,npts)
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
# min_v: {11}
# max_v: {12}
# mean_v: {13}
# num_x: {14}
# num_y: {15}
# lat1: {16}
# lon1: {17}
# lat2: {18}
# lon2: {19}
# lon,lat,{2}
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

    for i in range(len(latlist)):
        for d in range(len(depthlist)):
            v=datalist[d][i]
            f.write('{0},{1},{2}\n'.format(lonlist[i],latlist[i],v));

 
    f.close()
    sys.exit(True)
