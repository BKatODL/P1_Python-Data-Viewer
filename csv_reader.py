

import sys


def file_to_dic(file_name):

    valid_headers = ['Cycle,Time (ms),h (enc),t (enc),I (uA),P (mW),E (mJ),Q','Cycle,Time (ms),h (enc),t (enc),I (uA),P (mW),E (mJ),Q,O','Cycle,Time (ms),h (enc),t (enc),I (uA),P (mW),E (mJ),Q,O,T']

    if(file_name.split('.')[-1] != 'csv'):
        raise Exception("File not csv")
    with open(file_name,'r') as f:
        raw_text = f.read()
    lines = raw_text.split('\n')
    lines.pop(0) #clear first line as its not filled
    if not (lines[0] in valid_headers):
        raise Exception("file not odl data file")
    data_sets = []
    lines.pop(0) #if we have made it here were in the data set
    if(lines[0].split(',')[0].isnumeric()):
        raise Exception("File error")
    last_command = ''
    cycle = []
    t = []
    h = []
    t_en = []
    I = []
    p = []
    e = []
    q = []
    o = []
    T = []
    command_num = 0
    #yes I know that this is like the slowest way to do this but this is python so.....
    for i in lines:
        rows = i.split(',')
        if(not rows[0].isnumeric()):
            if(last_command):
                command_type = ''
                
                if(last_command.split(" ")[0] == "blind_h"):
                    command_type = "rl"
                    target = int(last_command.split(" ")[1])
                elif(last_command.split(" ")[0] == "blind_t"):
                    command_type = "tilt"
                    target = int(last_command.split(" ")[1])
                else:
                    command_type = "other"
                    target = 0
                if(len(cycle)):
                    data_sets.append({"name":last_command + " -" + str(command_num),"command": last_command,"command_type": command_type,"target":target,"Cycle":cycle[0],"time(ms)":t,"h (enc)":h,"t (enc)":t_en,"I (uA)":I,"P (mW)":p,"E (mJ)":e,"Q":q,"O":o,"T":T})
                    command_num += 1
                cycle = []
                t = []
                h = []
                t_en = []
                I = []
                p = []
                e = []
                q = []
                o = []
                T = []
            last_command = rows[0]

        elif (len(rows) >= 8) and (len(rows) <= 10):
            cycle.append(int(rows[0]))
            t.append(float(rows[1]))
            h.append(float(rows[2]))
            t_en.append(float(rows[3]))
            I.append(float(rows[4]))
            p.append(float(rows[5]))
            e.append(float(rows[6]))
            q.append(int(rows[7]))
            if len(rows) >= 9:
                o.append(float(rows[8]))
            else:
                o.append(0.0)
            if len(rows) >= 10:
                T.append(float(rows[9]))
            else:
                T.append(0.0)



        else:
            raise Exception("File error")
            
    return data_sets