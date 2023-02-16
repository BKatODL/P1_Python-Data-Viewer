

from csv_reader import file_to_dic
import matplotlib.pyplot as plt
import json



#file_name = "./Raw_Data/SB1in-23_J1-1_22x64.json"
#file_name = "./Raw_Data/Big_Blind.json"
#file_name = "./DataAnalaysisTool/Raw_Data/Big_Blind.json"
#file_name = "./Raw_Data/Big_Blind.csv"
#file_name = "./Raw_Data/SB1in-23_J1-1_22x64_angle-cut-cover-cap"
file_name = "./Raw_Data/IBS2023-D_Fatigue-Log_500-1000.csv"
#file_name = "./Cal-15_Several-Fails_Several-Deads.csv"
#file_name = "C:\Users\bkaterberg\OneDrive - ODL, Incorporated\2_Powering ODL\2_Data Collection Tools\Phase1 - Blind Cycle Data Logger\BCM Issues Log\Cal-15_Several-Fails_Several-Deads.csv"
#file_name = "./Raw_Data/ten_to_ninety.csv"


if(file_name.split(".")[-1] == "csv"):
    raw_data = file_to_dic(file_name)
else:
    with open(file_name,'r') as f:
        json_data = f.read()
        raw_data = json.loads(json_data)


selected_sets = []

# for i in raw_data:
#    if i["command_type"] == "rl" and i["target"] == 1000:
#        selected_sets.append(i)

# for i in raw_data:
#    if i["command_type"] == "rl" and i["target"] > 500:
#        selected_sets.append(i)

# for i in raw_data:
#    if i["command_type"] == "rl":
#        selected_sets.append(i)

for i in raw_data:
   if i["command_type"] == "rl" and i["target"] > 500:
       selected_sets.append(i)
   if i["command_type"] == "rl" and i["target"] <= 500:
       selected_sets.append(i)

#for i in raw_data:
#   if i["command_type"] == "rl" and i["target"] == 1000:
#       selected_sets.append(i)
#   if i["command_type"] == "rl" and i["target"] == 0:
#       selected_sets.append(i)


delta_t = []
for i in selected_sets:
    delta = []
    t_last = i["h (enc)"][0]
    for j in i["h (enc)"]:
        delta.append(j-t_last)
        t_last = j
    delta_t.append(delta)

##### To display the current ["I (uA)"] as "negative" to be similar to other efforts plotting we have done.
for i in selected_sets:
    if i["target"] <= 500:
        i["I (uA)"] = [-x for x in i["I (uA)"]]


x_axis = "h (enc)" # "time(ms)" # 
y_axis = "I (uA)" # "O" # "h (enc)"

for index,i in enumerate(selected_sets):
    plt.plot(i[x_axis],i[y_axis])

    # plt.plot(i["time(ms)"],i["h (enc)"])
	#plt.plot(i["time(ms)"],i["I (uA)"])
    #plt.plot(i["time(ms)"],i["I (uA)"])
    #plt.plot(i["h (enc)"],i["I (uA)"])
    # plt.plot(selected_sets[i]["h (enc)"],delta_t[i])
    # plt.plot(selected_sets[i]["h (enc)"])
    # plt.plot(i["h (enc)"],i["O"])

plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.show()
#plt.savefig("plot.png")