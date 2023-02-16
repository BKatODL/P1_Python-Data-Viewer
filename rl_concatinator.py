


from platform import mac_ver
from csv_reader import file_to_dic
import json

import matplotlib.pyplot as plt


def set_ratio(data):
    max_val = max(data)
    if max_val == 0:
        max_val = 1
    new_data = []
    for i in data:
        new_data.append(i/max_val)
    return new_data


file_name = "./DataAnalaysisTool/Raw_Data/ten_to_ninety.csv"




if(file_name.split(".")[-1] == "csv"):
    raw_data = file_to_dic(file_name)
else:
    with open(file_name,'r') as f:
        json_data = f.read()
        raw_data = json.loads(json_data)


# #
# with open(file_name,'r') as f:
#     json_data = f.read()
#     raw_data = json.loads(json_data)

t_actual = []
t_last = 0
t_counts = []
run_n = []
count = 0
current = []
quarter = []
t_run = []
rl = []
rl_d = []
out = []
target = []
dif = []
energy = []
rl_last = raw_data[0]["h (enc)"][0]
for i in raw_data:
    if i["command_type"] == "rl":
        for j in i["time(ms)"]:
            t_actual.append(t_last+j)
            t_run.append(j)
            count += 1
            t_counts.append(count)
        for j in i["h (enc)"]:
            rl.append(j)
            rl_d.append(rl[-1]-rl_last)
            rl_last = rl[-1]
        for j in i["I (uA)"]:
            current.append(j)
        for j in i["Q"]:
            quarter.append(float(j))
        for j in i["O"]:
            out.append(j)
        for j in i["T"]:
            target.append(j)
        for j in i["E (mJ)"]:
            energy.append(j)

        t_last = t_actual[-1]


for i in range(0,len(rl)):
    dif.append(target[i]-rl[i])

for index,i in enumerate(out):
    if i > 100:
        out[index] = 100


# t_run = set_ratio(t_run)
rl = set_ratio(rl)
target = set_ratio(target)
# dif = set_ratio(dif)

#quarter = set_ratio(quarter)
# current = set_ratio(current)
# rl_d    = set_ratio(rl_d)
out = set_ratio(out)

quater_floored = []
for i in quarter:
    #quater_floored.append(float(i)/100)
    quater_floored.append(float(i)*1000)
#plt.plot(rl,current)

# plt.plot(t_counts,rl,marker='o')
# plt.plot(t_counts,current)
# plt.plot(t_counts,target,marker='o')
# 

plt.plot(t_counts,rl)
plt.plot(t_counts,out)
plt.plot(t_counts,target)
# plt.plot(t_counts,energy)


plt.show()
