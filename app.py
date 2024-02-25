import tkinter as tk
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from dijkstra import *
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(v1,v2):
    R = 6371.0
    lat1 = v1[0]
    lon1 =v1[1]
    lat2 = v2[0]
    lon2 = v2[1]
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate the differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula to calculate distance
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

po1=""
po2=""
def on_marker_click(marker_id , name):
    global po1 , po2

    if name ==  po1 or name ==po2:
        canvas.itemconfig(marker_id, image=img)
        if name ==  po1 :
             source_combobox.set("")     
             po1=""
        else:
            po2=""
            target_combobox.set("")     
        return
    if po1!="" and po2!="":
        messagebox.showerror("marke","You have chose 2 item")
        return
    if(po1==""):
         canvas.itemconfig(marker_id, image=Nimg)
         source_combobox.set(name)
         po1=name
    else:
        target_combobox.set(name)
        po2=name
        canvas.itemconfig(marker_id, image=Endimg)

def on_source_combobox_change(event):
    global po1 
    if po1!="" :
        index = list(listofpoint).index(po1)
        canvas.itemconfig(markers[index], image=img)
        po1=""
    po=source_var.get()
    if po == po2:
        source_combobox.set("")
        messagebox.showerror("marke","You have chose this point")

        return

    po1=po
    index = list(listofpoint).index(po)
    canvas.itemconfig(markers[index], image=Nimg)



def on_target_combobox_change(event):
    global  po2
    if po2!="" :
        index = list(listofpoint).index(po2)
        canvas.itemconfig(markers[index], image=img)
        po2=""
    po=target_var.get()
    if po == po1:
        target_combobox.set("")
        messagebox.showerror("marke","You have chose this point")
        return
    po2=po
    index = list(listofpoint).index(po)
    canvas.itemconfig(markers[index], image=Endimg)


def getX(l): 

        l = float(l)
        minLon =34.199874448407934
        maxL =34.60789839066584
        # XperL=900/(maxL-minLon)
        # diff =l-minLon
        # return diff*XperL
        return (l-minLon)/(maxL-minLon)*900
def getY(l):
        l = float(l)
        minLon =31.218168572415646
        maxL =31.617160373220266
        # YperL=650/(maxL-minLon)
        # diff =maxL-l
        # return diff*YperL
        return (maxL-l)/(maxL-minLon)*650

def clear_all_lines():
    for line_id in lines:
        canvas.delete(line_id)

lines = []

def run():
    distance_entry.configure(state="normal")
    path_entry.configure(state="normal")
    distance_entry.delete(0, tk.END)
    path_entry.delete("0.0",tk.END)
    
    if po1=="" or po2 =="" :
        messagebox.showerror("marke","Please chose 2 point")
        return
    path , c = dijkstra(g , po1,po2) 
    path.reverse()


    if c !=float("inf"):
        c = "{:.2f}".format(c)
        distance_entry.insert(0, c+" KM")
        xpath=""
        for p in path :
            xpath+= p+" - > "
        if len(xpath) >= 2:
            new_text = xpath[:-4]
            path_entry.delete(tk.END)
            path_entry.insert("0.0", new_text)    
        prev=""
        clear_all_lines()
        for point in path:
            if prev !="" :
                x1 = getX(listofpoint[prev][1])
                y1 = getY(listofpoint[prev][0])
                x2 = getX(listofpoint[point][1])
                y2 = getY(listofpoint[point][0])
                line = canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
                lines.append(line)
            prev=point    
            distance_entry.configure(state="readonly")
            path_entry.configure(state="disabled")
    else:
        messagebox.showerror("marke",f"cant go to {po2} from {po1}")
#X1,Y1,X2,Y2    

root = tk.Tk()
root.title("GAZA Map !")
root.geometry("500x500")
root.state('zoomed')  #make screen full
mark = tk.PhotoImage(file="marker.png")
Nimg = tk.PhotoImage(file="start.png")
Endimg = tk.PhotoImage(file="end.png")

left_frame = ctk.CTkFrame(master=root)
left_frame.grid(row=0, column=0)

canvas = tk.Canvas(left_frame, width=900, height=656, bg="#00b4d8")
canvas.pack(side="top", fill="both", expand=True)
image_path = "map.png"  # Replace with the path to your image file
map_img = tk.PhotoImage(file="map.png")
ma =canvas.create_image(0,0, anchor=tk.NW, image=map_img)
listofpoint ={}
listofcity=[]
g={}
image_path = "marker.png" 
img = tk.PhotoImage(file=image_path)
markers=[]
with open("city.txt", "r") as input_file:
        line = input_file.readline()
        line = line.replace("\n", "")
        info = line.split(",")
        numofve=int(info[0])
        numofed=int(info[1])

        for i in  range(numofve):
            line = input_file.readline()
            line = line.replace("\n", "")
            info = line.split(",")
            if(int(info[3]) ==1):
                vertex = Vertex( info[0], float(info[2]), float(info[1]))
                listofpoint[vertex.name] = (vertex.y, vertex.x)
                g[vertex.name]=[]
            else:
                vertex = Vertex( info[0], float(info[2]), float(info[1]))
                listofcity.append(vertex.name)
                listofpoint[vertex.name] = (vertex.y, vertex.x)
                g[vertex.name]=[]

                tid=canvas.create_text(getX(vertex.x),  getY(vertex.y)-40, text=vertex.name, fill="black") # write the number of led and battery on screen
                marker_id = canvas.create_image(getX(vertex.x)-25, getY(vertex.y)-35,anchor=tk.NW, image=img )
                canvas.tag_bind(marker_id, '<Button-1>', lambda event,vertex=vertex, marker_id=marker_id: on_marker_click(marker_id , vertex.name))
                markers.append(marker_id)

        for i in  range(numofed):
            line = input_file.readline()
            line = line.replace("\n", "")
            info = line.split(",")
            g[info[0]].append((info[1],haversine_distance((listofpoint[info[0]][0],listofpoint[info[0]][1]),(listofpoint[info[1]][0],listofpoint[info[1]][1]))))



right_frame = ctk.CTkFrame(master=root, width=400,fg_color="#c1121f")
right_frame.grid(row=0, column=1,sticky="nesw")

# make the frames expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# Create a label For soucre
source_label = ctk.CTkLabel(right_frame, text="Source : " , font=("Arial",18))
source_label.place(x=10,y=10)

# Create a variable to hold the selected source
source_var = tk.StringVar()

# Create a Combobox (Dropdown) for source selection
source_combobox = ctk.CTkComboBox(right_frame, variable=source_var, values=listofcity ,command=on_source_combobox_change)
source_combobox.place(x=100,y=10)
source_combobox.set("")  # Set the default value

# Create a label for target
terget_label = ctk.CTkLabel(master=right_frame, text="Target : " , font=("Arial",18))
terget_label.place(x=10,y=50)

# Create a variable to hold the selected source
target_var = tk.StringVar()

# Create a Combobox (Dropdown) for source selection
target_combobox = ctk.CTkComboBox(right_frame, variable=target_var, values=listofcity , state="readonly" , command=on_target_combobox_change)
target_combobox.place(x=100,y=50)
target_combobox.set("")  # Set the default value
# target_combobox.bind("<<ComboboxSelected>>", on_target_combobox_change)


runBTN = ctk.CTkButton(right_frame,text="RUN !" , command=run,width=100)
runBTN.place(x=50 , y=100)


# Create a label for path
path_label = ctk.CTkLabel(master=right_frame, text="Path : " , font=("Arial",18))
path_label.place(x=10,y=180)
path_entry = ctk.CTkTextbox(right_frame ,width=300,height=200,wrap=tk.WORD)
path_entry.place(x=10,y=220)

# Create a label for Distance
distance_label = ctk.CTkLabel(master=right_frame, text="Distance : " , font=("Arial",18))
distance_label.place(x=10,y=430)
distance_entry = ctk.CTkEntry(right_frame, placeholder_text="" , state="readonly" ,width=200,height=50)
distance_entry.place(x=10,y=460)



# Run the Tkinter event loop
root.mainloop()