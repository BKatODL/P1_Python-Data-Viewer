from asyncio.windows_events import NULL
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from csv_reader import file_to_dic
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class data_veiwer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
                # Initialize root parameters
        self.parent = parent
        self.screen_w = int(self.winfo_screenwidth())
        self.screen_h = int(self.winfo_screenheight())
        self.default_geometry = str(int(self.screen_w/2))+"x"+str(int(self.screen_h/2))+"+"+str(int(self.screen_w/4))+"+"+str(int(self.screen_h/4))
        #self.parent.geometry(self.default_geometry)
        #self.parent.state('zoomed')
        self.parent.wm_title("Data visualizer")
        self.parent.protocol('WM_DELETE_WINDOW', self.exit)
        self.data_set_viewer = self.file_handler(self.parent,self.new_data_selected) 
        self.run_veiwer = self.data_set_handler(self.parent,self.new_runs_selected)
        self.graph_element = self.graph_handler(self.parent)

        self.data_set_viewer.frame.grid(row = 0,column = 0)
        self.run_veiwer.frame.grid(row = 1,column = 0)
        self.graph_element.frame.grid(row = 0,column = 1,rowspan = 2,columnspan = 2)


        # self.data_set_viewer.frame.place(relx = .01,rely = .01,relwidth = .08, relheight = .18)
        # self.run_veiwer.frame.place(relx = .01,rely = .21,relwidth = .08, relheight = .18)
        # self.graph_element.frame.place(relx = .11,rely = .01,relwidth = .78, relheight = .48)

    def new_runs_selected(self,data):
        self.graph_element.clear_graph()
        if data != None:
            for i in data:
                self.graph_element.graph(i["time(ms)"],i["h (enc)"])

    
    def new_data_selected(self,data,name):
        self.run_veiwer.add_runs(data,name)


    class graph_handler:
        def __init__(self,parent):
            self.frame = tk.LabelFrame(parent,text = "graph")
            self.fig = Figure()
            self.ax1 = self.fig.add_subplot(111)

            self.graph_canvas = FigureCanvasTkAgg(self.fig, self.frame)  # A tk.DrawingArea.
            self.graph_canvas.draw()
            self.graph_canvas.get_tk_widget().pack()

            self.graph_toolbar = NavigationToolbar2Tk(self.graph_canvas, self.frame)
            self.graph_toolbar.update()
            self.graph_canvas.get_tk_widget().pack()
        def clear_graph(self):
            self.ax1.clear()
        def graph(self,x_data,y_data):
            self.ax1.plot(x_data,y_data)
            self.graph_canvas.draw()


    class data_set_handler:
        def __init__(self,parent,data_cb):
            self.data_cb = data_cb
            self.frame = tk.LabelFrame(parent,text = "runs")
            self.runs = tk.Listbox(self.frame,selectmode = MULTIPLE)
            self.runs.bind("<<ListboxSelect>>", self.new_data_entry)
            self.data_set_label = tk.Label(self.frame,text="Selected: none")
            self.clear_selected = tk.Button(self.frame,text = "clear",command = self.unselect_all)
            self.do_rl = IntVar()
            self.do_tilt = IntVar()
            self.rl_filter_check = tk.Checkbutton(self.frame,text = "rl",variable=self.do_rl,onvalue=1,offvalue=0,height=2,width=1)
            self.tile_filter_check = tk.Checkbutton(self.frame,text = "tilt",variable=self.do_tilt,onvalue=1,offvalue=0,height=2,width=1)
            self.rl_filter_check.select()
            self.tile_filter_check.select()
            self.do_rl.trace_add("write",self.update_check_selection)
            self.do_tilt.trace_add("write",self.update_check_selection)

            self.data_set_label.grid(row = 0,column = 0,columnspan=2)
            self.runs.grid(row = 1, column = 0,columnspan=2)
            self.clear_selected.grid(row = 2, column = 0,columnspan=2)
            self.rl_filter_check.grid(row = 3,column=0)
            self.tile_filter_check.grid(row=3,column=1)
            self.tile_filter_check = tk.Checkbutton(self.frame,text = "tilt",variable=self.do_tilt,onvalue=1,offvalue=0,height=5,width=20)
            self.run_data = []
            self.selected_data = ''
            
            
            


        def update_check_selection(self, *args):
            self.runs.delete(0,END)
            self.add_selected_runs()


        def add_selected_runs(self):
            for i,item in enumerate(self.run_data):
                if((item["command_type"] == "rl" and self.do_rl.get()) or (item["command_type"] == "tilt" and self.do_tilt.get())):
                    self.runs.insert(i,item["name"])

        def unselect_all(self):
            self.runs.delete(0,END)
            self.add_selected_runs()
            self.data_cb(None)




        def add_runs(self,new_data,name):
            self.rl_filter_check.select()
            self.tile_filter_check.select()
            self.runs.delete(0,END)
            self.run_data = new_data
            self.data_set_label.configure(text = "Selected: "+name)
            self.add_selected_runs()
            


        def new_data_entry(self,event):
            selected_index = self.runs.curselection()
            runs_to_return = []
            #print(selected_index)
            if selected_index:
                for i in selected_index:
                    #print(i)
                    selection_string = self.runs.get(i)
                    for j in self.run_data:
                        if j["name"] == selection_string:
                            runs_to_return.append(j)
                self.data_cb(runs_to_return)

    
    class file_handler:
        def __init__(self,parent,new_data_set_cb):
            self.new_data_cb = new_data_set_cb
            self.frame = tk.LabelFrame(parent,text = "data sets")
            self.files_to_work_with = tk.Listbox(self.frame)
            self.files_to_work_with.bind("<<ListboxSelect>>", self.new_selected_data)
            self.select_folder_button = tk.Button(self.frame,text = "select data",command = self.load_data_sets)
            self.files_to_work_with.grid(row = 0, column = 0, pady = 2)
            self.select_folder_button.grid(row = 1, column = 0, pady = 2)
            self.selected_data = ''
            self.files_loaded = []

        def load_data_sets(self):
            self.files_loaded =  tk.filedialog.askopenfilenames()
            self.files_to_work_with.delete(0,self.files_to_work_with.size())
            for i,item in enumerate(self.files_loaded):
                if(item.split('/')[-1].split('.')[-1] == "csv"):
                    self.files_to_work_with.insert(i,item.split('/')[-1].split('.')[0])
            #print(folder_to_load)

        def new_selected_data(self,data):
            selected_index = self.files_to_work_with.curselection()
            selected_data = []
            if selected_index:
                selection_string = self.files_to_work_with.get(selected_index[0])
                print(selection_string)
                if(self.selected_data != selection_string):
                    self.selected_data = selection_string
                    for i in self.files_loaded:
                        if i.split('/')[-1].split('.')[0] == selection_string:
                            new_data_set = file_to_dic(i)
                            self.new_data_cb(new_data_set,selection_string)
                    




    def exit(self):
        self.destroy()
        self.parent.destroy()



def main():
    root = tk.Tk()
    data_veiwer(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()