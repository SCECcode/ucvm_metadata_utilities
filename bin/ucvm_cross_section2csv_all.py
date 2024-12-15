#!/usr/bin/env python3
"""
ucvm_cross_section2csv_all.py:

This script takes 3 sets of metadata (json) and binary data (bin) files produced from
the UCVM plotting routines when doing a vertical cross section plot. This then outputs 
to a csv file format.

lon lat depth vp vs density
"""
import json
import sys
import numpy as np

import pdb

# import raw floats array data from the external file into
# numpy array
def import_np_float_array(datafile, num_x, num_y):
    global fh
    try:
        fh = open(datafile, 'rb')
    except:
        print("ERROR: binary np float array data does not exist.")
        exit(1)

    floats = np.load(fh)
    fh.close()
    return floats


if __name__ == '__main__':
    """
    :input: vp_data.bin vp_meta.json vs_data.bin vs_meta.json density_data.bin density_meta.json 
    :return: all_data.csv file
    
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

    if len(sys.argv) != 7:
        raise ValueError("Usage:\n"
                         "  ./ucvm_cross_section2csv_all.py vp_data.bin vp_meta.json vs_data.bin vs_meta.json density_data.bin density_meta.json")

    vp_data_file = sys.argv[1]
    vp_metadata_file = sys.argv[2]
    vs_data_file = sys.argv[3]
    vs_metadata_file = sys.argv[4]
    density_data_file = sys.argv[5]
    density_metadata_file = sys.argv[6]
    with open(vp_metadata_file) as json_data:
        vp_obj = json.load(json_data)
    with open(vs_metadata_file) as json_data:
        vs_obj = json.load(json_data)
    with open(density_metadata_file) as json_data:
        density_obj = json.load(json_data)

    #
    # The return values here are
    """
    ['depth_list', 'color', 'horizontal_spacing', 'datapoints',
     'starting_depth', 'title', 'vertical_spacing', 'data_type', 'max', 'outfile', 
    'lat1', 'lat2', 'ending_depth', 'lon_list', 'num_x', 'num_y', 'cvm', 'min', 'lon1', 'lat_list', 'lon2', 'mean'])
    """
    depthlist = vp_obj["depth_list"]
    latlist = vp_obj["lat_list"]
    lonlist = vp_obj["lon_list"]
    npts = vp_obj["datapoints"]
    # This assumes lat_list and lon_list are the same length. We can use either in this calc
    # which can be restated as # of x_pts * # of y_pts
    # The lat and lon lists are the same length, so we iterate through one, and use the index to
    # create a point string for the query point
    if  len(lonlist) != len(latlist):
        print("Error: lat and lon lists are not the same list, which is assumption for these data files")
        sys.exit(0)
    #

    total_pts = len(depthlist) * len(latlist)
    vp_datalist = import_np_float_array(vp_data_file, len(lonlist), len(depthlist))
    vs_datalist = import_np_float_array(vs_data_file, len(lonlist), len(depthlist))
    density_datalist = import_np_float_array(density_data_file, len(lonlist), len(depthlist))

    # Use shape to return the dimensions of the np array that is returned
    # We assume it is 2D array

    vp_datasizes = vp_datalist.shape
    if npts != vp_datasizes[0] * vp_datasizes[1]:
        raise Exception("Number of depth points does not each number of 1ddata points. Exiting",
                        npts, vp_datasizes[0] * vp_datasizes[1])
    #

    if total_pts != npts:
        print("Error: Total points should equal the number of latlons times the number of data points",
              total_pts,npts)
        sys.exit(0)
    #
    # Make properties type
    vp_propstr = "Vp(m/s)"
    vs_propstr = "Vs(m/s)"
    density_propstr = "Density(kg/m^3)"

    #
    # Create output file name
    # Example filename: ipnput_data_file = "cross-cvmsi_meta.json"
    # cross-cvmsi_data.bin cross-cvmsi_meta.json
    output_file_name = vp_data_file.replace("vp_data.bin","all_data.csv")

    print("\nWriting CSV file: ", output_file_name)
    f = open(output_file_name, "w")

    """
    """

    header_str = '''\
# Title: {0}
# CVM(abbr): {1}
# Data_type: vp,vs,density
# Start_depth(m): {2} 
# End_depth(m): {3} 
# Vert_spacing(m): {4}
# Horizontal_spacing(m): {5}
# Depth_pts: {6} 
# Horizontal_pts: {7} 
# Total_pts: {8}
# vp Min_v: {9}
# vp Max_v: {10}
# vp Mean_v: {11}
# vs Min_v: {12}
# vs Max_v: {13}
# vs Mean_v: {14}
# density Min_v: {15}
# density Max_v: {16}
# density Mean_v: {17}
# Num_x: {18}
# Num_y: {19}
# Lat1: {20}
# Lon1: {21}
# Lat2: {22}
# Lon2: {23}
# Lon,Lat,Depth(m),{24},{25},{26}
'''.format(vp_obj["title"],
           vp_obj["cvm"],
           vp_obj["starting_depth"],
           vp_obj["ending_depth"],
           vp_obj["vertical_spacing"],
           vp_obj["horizontal_spacing"],
           len(depthlist),
           len(latlist),
           npts,
           vp_obj["min"],
           vp_obj["max"],
           vp_obj["mean"],
           vs_obj["min"],
           vs_obj["max"],
           vs_obj["mean"],
           density_obj["min"],
           density_obj["max"],
           density_obj["mean"],
           vp_obj["num_x"],
           vp_obj["num_y"],
           vp_obj["lat1"],
           vp_obj["lon1"],
           vp_obj["lat2"],
           vp_obj["lon2"],
           vp_propstr,
           vs_propstr,
           density_propstr
          )

    print(header_str)
    f.write(header_str)

    for i in range(len(latlist)):
        for d in range(len(depthlist)):
            vp=vp_datalist[d][i]
            if(vp == -1) :
              vp="nan"
            vs=vs_datalist[d][i]
            if(vs == -1) :
              vs="nan"
            density=density_datalist[d][i]
            if(density == -1) :
              density="nan"
            f.write('{0},{1},{2},{3},{4},{5}\n'.format(lonlist[i],latlist[i],depthlist[d],vp,vs,density));

 
    f.close()
    sys.exit(True)
