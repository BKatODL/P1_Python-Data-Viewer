
from csv_reader import file_to_dic
import json


def csv_to_json(name):
    raw_data = file_to_dic(name)
    raw_data_json = json.dumps(raw_data)
    return raw_data_json

def main():
    file_name = "./Raw_Data/SB1in-23_J1-1_22x64_angle-cut-cover-cap.csv"
    file_name_spilt = file_name.split(".")
    new_file_name = ''
    for i in range(0,len(file_name_spilt)-1):
        new_file_name = new_file_name+file_name_spilt[i]
        new_file_name = new_file_name+"."
    new_file_name = new_file_name + 'json'

    json_data = csv_to_json(file_name)
    with open(new_file_name,'w') as f:
        f.write(json_data)
    print("done")

if __name__ == "__main__":
    main()
