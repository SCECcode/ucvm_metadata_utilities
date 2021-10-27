#!/usr/bin/env python
"""
read_ucvm_vert_profile.py: this script inputs the files produced from the UCVM web viewer
when doing a vertical profile. The script includes two input files include metadata file, and a data file,
both in json format. This then outputs the pandadata frame to a csv file format.

"""
import pandas as pd
import json
import sys

input_metadata_file = "UCVM_1618866062727vertical_meta.json"
input_data_file = "UCVM_1618866062727vertical_matprops.json"


def read_ucvm_vert_data():
    """

    :return: This returns a list of values as a dict, with vp, vs, density keys
    """
    with open(input_data_file) as json_data:
        obj = json.load(json_data)
        #
        # vertical profile data is a list of objects, each object has vp, vs, rho
        #
        list_of_vals = obj["matprops"]
        return list_of_vals


def read_ucvm_metadata():
    """
    :return: cvm_name, lat, lon, starting_depth, ending_depth, spacing, list of depth points
    """
    with open(input_metadata_file) as json_data:
        obj = json.load(json_data)
        cvm_name = obj["cvm"]
        lat = obj["lat1"]
        lon = obj["lon1"]
        starting_depth = obj['starting_depth']
        ending_depth = obj['ending_depth']
        vspacing = obj["vertical_spacing"]
        ldlist = obj["depth"]
        return cvm_name, lat, lon, starting_depth, ending_depth, vspacing, ldlist


if __name__ == '__main__':
    """
    Reads file names from header of this file.
    Outputs a CSV file with header and
    depth, vs, vp, rho columns
    """
    metadepthlist = read_ucvm_metadata()
    #
    # The return values here are
    # 0 cvm_name
    # 1 lat
    # 2 lon
    # 3 start_depth
    # 4 end_depth
    # 5 vert_spacing
    # 6 list of depth values

    datalist = read_ucvm_vert_data()

    if len(metadepthlist[6]) != len(datalist):
        raise Exception("Number of depth points does not each number of data points. Exiting",
                        len(metadepthlist[6]), len(datalist))

    merged_list = {}
    dlist = []
    vplist = []
    vslist = []
    denlist = []
    for idx in range(len(metadepthlist[6])):
        dlist.append(metadepthlist[6][idx])
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
    filevals = input_data_file.split("_")
    output_file_name = filevals[0] + filevals[1] + ".csv"
    print("Writing CSV file: ", output_file_name)
    f = open(output_file_name, "w")
    header_str = "# CVM_name:{0} Lat:{1} Long:{2} Start_depth(m):{3} End_depth(m):{4} Vert_spacing(m):{5}\n".format(
        metadepthlist[0],
        metadepthlist[1],
        metadepthlist[2],
        metadepthlist[3],
        metadepthlist[4],
        metadepthlist[5])
    print(header_str)
    f.write(header_str)
    df.to_csv(f, index=False, mode="a")
    f.close()
    sys.exit(True)
