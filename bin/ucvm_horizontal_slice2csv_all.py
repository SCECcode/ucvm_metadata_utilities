#!/usr/bin/env python3
"""
ucvm_horizontal_slice2csv_all.py:

This script takes 3 sets of metadata (json) and binary data (bin) files produced from
the UCVM plotting routines when doing a horizontal slice plot. This then outputs
to a csv file format.

lon lat val

"""
import json
import sys
import numpy as np

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

    if len(sys.argv) != 7:
        raise ValueError("Usage:\n"
                         " ./ucvm_horizontal_slice2csv_all.py vp_data.bin vp_meta.json vs_data.bin vs_meta.json density_data.bin density_meta.json")

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
    ['num_y', 'lat1', 'data_type', 'lat2', 'color', 'max',
     'title', 'spacing', 'configfile', 'lon_list', 'num_x',
     'outfile', 'depth', 'cvm', 'min', 'datapoints', 'lon1',
     'lat_list', 'lon2', 'installdir', 'mean']
    """
    depth = vp_obj["depth"]
    latlist = vp_obj["lat_list"]
    lonlist = vp_obj["lon_list"]
    npts = vp_obj["datapoints"]
    num_x = vp_obj["num_x"]
    num_y = vp_obj["num_y"]

    #
    total_pts = len(lonlist) * len(latlist)

    vp_datalist = import_np_float_array(vp_data_file,len(lonlist), len(latlist))
    vs_datalist = import_np_float_array(vs_data_file,len(lonlist), len(latlist))
    density_datalist = import_np_float_array(density_data_file,len(lonlist), len(latlist))

    # Use shape to return the dimensions of the np array that is returned
    # We assume it is 2D array
    vp_datasizes = vp_datalist.shape
    if npts != (vp_datasizes[0] * vp_datasizes[1]) :
        raise Exception("Number of depth points does not each number of 1ddata points. Exiting", npts, vp_datasizes[0] * vp_datasizes[1])

    if len(lonlist) * len(latlist) != npts:
        print("Error: Total points should equal the number of lats times the number of lons",
              len(lonlist) * len(latlist),npts)
        sys.exit(0)
    #
    # Make properties type
    vp_propstr = "Vp(m/s)"
    vs_propstr = "Vs(m/s)"
    density_propstr = "Density(kg/m^3)"

    #
    # Create output file name
    # Example filename: input_data_file = "cross-cvmsi_meta.json"
    # cross-cvmsi_data.bin cross-cvmsi_meta.json
    output_file_name = vp_data_file.replace("vp_data.bin","all_data.csv")
    print("\nWriting CSV file: ", output_file_name)
    f = open(output_file_name, "w")

    header_str = '''\
# Title: {0}
# CVM(abbr): {1}
# Data_type: vp,vs,density 
# Depth(m): {2} 
# Spacing(degree): {3}
# Lon_pts: {4} 
# Lat_pts: {5} 
# Total_pts: {6}
# vp Min_v: {7}
# vp Max_v: {8}
# vp Mean_v: {9}
# vs Min_v: {10}
# vs Max_v: {11}
# vs Mean_v: {12}
# density Min_v: {13}
# density Max_v: {14}
# density Mean_v: {15}
# Lat1: {16}
# Lon1: {17}
# Lat2: {18}
# Lon2: {19}
# Lon,Lat,{20},{21},{22}
'''.format(vp_obj["title"],
           vp_obj["cvm"],
           vp_obj["depth"],
           vp_obj["spacing"],
           len(lonlist),
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

    for i in range(len(lonlist)):
        for j in range(len(latlist)):
            vp=vp_datalist[j][i]
            if(vp == -1) :
              vp="nan"
            vs=vs_datalist[j][i]
            if(vs == -1) :
              vs="nan"
            density=density_datalist[j][i]
            if(density == -1) :
              density="nan"
            f.write('{0},{1},{2},{3},{4}\n'.format(lonlist[i],latlist[j],vp,vs,density));

    f.close()
    sys.exit(True)
