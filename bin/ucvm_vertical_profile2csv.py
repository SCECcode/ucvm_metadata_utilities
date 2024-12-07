#!/usr/bin/env python
"""

ucvm_vertical_profile2csv.py v_matprops.json v_meta.json

this script inputs the files produced from the UCVM web viewer
when doing a vertical profile. The script includes two input 
files include metadata file, and a data file, both in json format. 
and outputs the panda data frame to a csv file format.

"""
import pandas as pd
import json
import sys

def read_ucvm_vert_data(file):
    """
    :return: This returns a list of values as a dict, with vp, vs, density keys
    """
    with open(file) as json_data:
        obj = json.load(json_data)
        #
        # vertical profile data is a list of objects, each object has vp, vs, rho
        #
        list_of_vals = obj["matprops"]
        return list_of_vals


def read_ucvm_metadata(file):
    """
    :return: cvm_name, lat, lon, starting_depth, ending_depth, spacing, list of depth points
    """
    with open(file) as json_data:
        obj = json.load(json_data)
        return obj


if __name__ == '__main__':
    """
    :input: v_matprops.json v_meta.json
    :return: v_data.csv file
    
    Reads file names from header of this file.
    Outputs a CSV file with header and
    depth, vs, vp, rho columns
    """

    if len(sys.argv) != 3:
        raise ValueError("Please provide arguments: ucvm_vertical_profile2csv.py v_matprops.json v_meta.json.\n"
                         "e.g. ./ucvm_vertial_profile2csv.py v_matprops.json v_meta.json")

    input_data_file = sys.argv[1]
    input_metadata_file = sys.argv[2]
    datalist=read_ucvm_vert_data(input_data_file)
    mobj=read_ucvm_metadata(input_metadata_file)


    cvm_name = mobj["cvm"]
    lat = mobj["lat1"]
    lon = mobj["lon1"]

    isDepth=0;
    if 'starting_depth' in mobj :
       starting_depth = mobj['starting_depth']
       ending_depth = mobj['ending_depth']
       ldlist = mobj["depth"]
       isDepth=1;
    else:
       starting_elevation = mobj['starting_elevation']
       ending_elevation = mobj['ending_elevation']
       ldlist = mobj["elevation"]


    vspacing = mobj["vertical_spacing"]
    dtype = mobj["data_type"]


    if len(ldlist) != len(datalist):
        raise Exception("Number of depth points does not each number of data points. Exiting",
                        len(ldlist), len(datalist))

    merged_list = {}
    dlist = []
    vplist = []
    vslist = []
    denlist = []
    for idx in range(len(ldlist)):
        dlist.append(ldlist[idx])
        vplist.append(datalist[idx]["vp"])
        vslist.append(datalist[idx]["vs"])
        denlist.append(datalist[idx]["density"])

    merged_list = {"# Depth(m)": dlist, "Vp(m)": vplist, "Vs(m)": vslist, "Density(kg/m^3)": denlist}
    #
    # convert to dataframes
    #
    df = pd.DataFrame(merged_list)
    #
    # Create output file name
    # Example filename: input_data_file = "UCVM_1618866062727vertical_matprops.json"
    output_file_name = input_data_file.replace(".json",".csv")
    print("\nWriting CSV file: ", output_file_name)
    f = open(output_file_name, "w")

    if isDepth :
      if "comment" not in mobj:
        header_str = '''\
# Title:{6}
# CVM(abbr):{0} 
# Lat:{1}
# Lon:{2}
# Start_depth(m):{3}
# End_depth(m):{4} 
# Vert_spacing(m):{5}
'''.format(
      mobj["cvm"],
      mobj["lat1"],
      mobj["lon1"],
      mobj['starting_depth'],
      mobj['ending_depth'],
      mobj["vertical_spacing"],
      output_file_name)
      else:
        header_str = '''\
# Title:{7}
# CVM(abbr):{0} 
# Lat:{1}
# Lon:{2}
# Start_depth(m):{3}
# End_depth(m):{4}  
# Vert_spacing(m):{5}
# Comment:{6}
'''.format(
      mobj["cvm"],
      mobj["lat1"],
      mobj["lon1"],
      mobj['starting_depth'],
      mobj['ending_depth'],
      mobj["vertical_spacing"],
      mobj["comment"],
      output_file_name)
    else: # not isDepth 
      if "comment" not in mobj:
        header_str = '''\
# Title:{6}
# CVM(abbr):{0} 
# Lat:{1}
# Lon:{2}
# Start_elevation(m):{3}
# End_elevation(m):{4} 
# Vert_spacing(m):{5}
'''.format(
      mobj["cvm"],
      mobj["lat1"],
      mobj["lon1"],
      mobj['starting_elevation'],
      mobj['ending_elevation'],
      mobj["vertical_spacing"],
      output_file_name)
      else:
        header_str = '''\
# Title:{7}
# CVM(abbr):{0} 
# Lat:{1}
# Lon:{2}
# Start_elevation(m):{3}
# End_elevation(m):{4}  
# Vert_spacing(m):{5}
# Comment:{6}
'''.format(
      mobj["cvm"],
      mobj["lat1"],
      mobj["lon1"],
      mobj['starting_elevation'],
      mobj['ending_elevation'],
      mobj["vertical_spacing"],
      mobj["comment"],
      output_file_name)

    print(header_str)
    f.write(header_str)
    df.to_csv(f, index=False, mode="a")
    f.close()
    sys.exit(True)
