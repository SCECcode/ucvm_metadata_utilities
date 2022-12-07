#!/usr/bin/env python
"""
read_ucvm_vert_profile.py: this script inputs the files produced from the UCVM web viewer
when doing a vertical profile. The script includes two input files include metadata file, and a 1ddata file,
both in json format. This then outputs the pandadata frame to a csv file format.
"""
import pandas as pd
import json
import sys

def read_ucvm_vert_data():
    """
    :return: This returns a list of values as a dict, with vp, vs, density keys
    """
    with open(input_data_file) as json_data:
        obj = json.load(json_data)
        #
        # vertical profile 1ddata is a list of objects, each object has vp, vs, rho
        #
        list_of_vals = obj["matprops"]
        return list_of_vals


def read_ucvm_metadata():
    """
    :return: cvm_name, lat, lon, starting_depth, ending_depth, spacing, list of depth points
    """
    with open(input_metadata_file) as json_data:
        obj = json.load(json_data)
        cvm_name = obj["comment"]
        cvm_abbr = obj["cvm"]
        lat = obj["lat1"]
        lon = obj["lon1"]
        starting_depth = obj['starting_depth']
        ending_depth = obj['ending_depth']
        vspacing = obj["vertical_spacing"]
        ldlist = obj["depth"]
        return cvm_name, cvm_abbr, lat, lon, starting_depth, ending_depth, vspacing, ldlist


if __name__ == '__main__':
    """
    :input: UCVM_*_vertical_meta.json file UCVM_*_vertical_matprops.json file
    :return: UCVM_*.csv file
    
    example input_metadata_file = "UCVM_1663883162439vertical_meta.json"
    example input_data_file = "UCVM_1663883162439vertical_matprops.json"
    Reads file names from header of this file.
    Outputs a CSV file with header and
    depth, vs, vp, rho columns
    """

    if len(sys.argv) != 3:
        raise ValueError("Please provide arguments: ucvm1d2csv.py UCVM_data_file UCVM_metadata_file.\n"
                         "e.g. ucvm1d2csv.py UCVM_1663883162439vertical_matprops.json UCVM_1663883162439vertical_meta.json")

    input_data_file = sys.argv[1]
    input_metadata_file = sys.argv[2]
    metadepthlist = read_ucvm_metadata()
    #
    # The return values here are
    # 0 cvm_name
    # 1 cvm_abbr
    # 2 lat
    # 3 lon
    # 4 start_depth
    # 5 end_depth
    # 6 vert_spacing
    # 7 list of depth values

    datalist = read_ucvm_vert_data()

    if len(metadepthlist[7]) != len(datalist):
        raise Exception("Number of depth points does not each number of 1ddata points. Exiting",
                        len(metadepthlist[7]), len(datalist))

    merged_list = {}
    dlist = []
    vplist = []
    vslist = []
    denlist = []
    for idx in range(len(metadepthlist[7])):
        dlist.append(metadepthlist[7][idx])
        vplist.append(datalist[idx]["vp"]/1000.0)
        vslist.append(datalist[idx]["vs"]/1000.0)
        denlist.append(datalist[idx]["density"])

    merged_list = {"# Depth(m)": dlist, "Vp(km/s)": vplist, "Vs(km/s)": vslist, "Density(kg/m^3)": denlist}
    #
    # convert to dataframes
    #
    df = pd.DataFrame(merged_list)
    #
    # Create output file name
    # Example filename: input_data_file = "UCVM_1618866062727vertical_matprops.json"
    filevals = input_data_file.split("_")
    output_file_name = filevals[0] + filevals[1] + ".csv"
    print("Writing CSV file: ", output_file_name)
    f = open(output_file_name, "w")
    header_str = '''\
# Input Data files: {0} {1}
# CVM_name: {2} (abbr: {3})
# Lat: {4} Long: {5} Start_depth(m): {6} End_depth(m): {7} Vert_spacing(m): {8}
# Depth(m)  Vp(km/s)  Vs(km/s)  Density(kg/m^3)\n'''.format(input_data_file,input_metadata_file,
                metadepthlist[0],
                metadepthlist[1],
                metadepthlist[2],
                metadepthlist[3],
                metadepthlist[4],
                metadepthlist[5],
                metadepthlist[6])
    print(header_str)
    f.write(header_str)
    df.to_csv(f, header=False,float_format='{:5.4f}'.format, index=False, mode="a")
    f.close()
    sys.exit(True)