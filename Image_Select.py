from tkinter import *
from PIL import ImageTk
import tkinter.filedialog
from PIL import Image
import cv2
import math
import imutils
from EXIF_Data import Intencive
import os
from sensor import Sensor
from matrix import Matrix
from coordinate_cal import Newcoordinate

Radius = 6378.1

# master = ['X', 'Y']

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field[0]+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,field[1])
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

def destroy_root(root):
	root.destroy()


def select_image():

    path = tkinter.filedialog.askopenfilename()
    if len(path) > 0:
        image = ImageTk.PhotoImage(Image.open(path))
        # process_image(path)
        obj = Intencive(path)
        ob2=Sensor(obj)
        mat=Matrix(ob2)
        a, b, c, w, h, log1, lat1 = ob2.overall(path)

        m = mat.intensive_matrix(a, w, h)
        dist_mat = mat.distance_mat(b)
        pos_m = mat.pos_mat()
        neg_m = mat.neg_mat(c)

        mat.set_mat_maul(dist_mat, pos_m)
        mat.set_mat_maul2(neg_m)
        mat.set_mat_mul3(m)
        # mat.calculate_inverse_matrix()

        # print('inverse matreix======',mat.ainv)
        cord = Newcoordinate(mat)

        m1 = cord.pixel_to_world(0, 0, mat.mat_mul3)
        m2 = cord.pixel_to_world(w, 0, mat.mat_mul3)
        m3 = cord.pixel_to_world(w, h, mat.mat_mul3)
        m4 = cord.pixel_to_world(0, h, mat.mat_mul3)
        m5 = cord.pixel_to_world(w / 2, h / 2, mat.mat_mul3)

        print('m1==', m1)
        print('m2==', m2)
        print('m3==', m3)
        print('m4==', m4)
        print('m5==', m5)

        d1 = cord.eq_distance(m1, m2)
        print(d1)
        d2 = cord.eq_distance(m2, m3)
        print(d2)
        d3 = cord.eq_distance(m3, m4)
        print(d3)
        d4 = cord.eq_distance(m4, m1)
        print(d4)
        d5 = cord.eq_distance(m1, m3)
        print(d5)
        d6 = cord.eq_distance(m2, m4)
        print(d6)
        d7 = cord.eq_distance(m2, m5)
        print(d7)
        d8 = cord.eq_distance(m1, m5)
        print(d8)
        d9 = cord.eq_distance(m3, m5)
        print(d9)
        d10 = cord.eq_distance(m4, m5)
        print(d10)

        # km = cord.div()
        dis_km_25 = cord.div(d7)
        print('distance of m2,m5 in km',dis_km_25 )
        dis_km_15 = cord.div(d8)
        print('distance of m1,m5 in km',dis_km_15 )
        dis_km_35 = cord.div(d9)
        print('distance of m3,m5 in km',dis_km_35 )
        dis_km_45 = cord.div(d10)
        print('distance of m4,m5 in km',dis_km_45 )
        # ang = cord.angle_calculation()

        value_of_angle1 = cord.angle_calculation(m5,m1)
        print('angle value for m5,m1  ===>',value_of_angle1)
        value_of_angle2 =cord.angle_calculation(m5,m2)
        print('angle value for m5,m2  ===>',value_of_angle2)
        value_of_angle3 = cord.angle_calculation(m5,m3)
        print('angle value for m5,m3  ===>',value_of_angle3)
        value_of_angle4 = cord.angle_calculation(m5,m4)
        print('angle value for m5,m4  ===>',value_of_angle4)

        new_cod_val =  cord.coordinate_angle(value_of_angle1, dis_km_15, lat1, log1, Radius)
        print(new_cod_val)

        new_cod_val =  cord.coordinate_angle(value_of_angle2, dis_km_25, lat1, log1, Radius)
        print(new_cod_val)
        #
        new_cod_val =  cord.coordinate_angle(value_of_angle3, dis_km_35, lat1, log1, Radius)
        print(new_cod_val)

        new_cod_val =  cord.coordinate_angle(value_of_angle4, dis_km_45, lat1, log1, Radius)
        print(new_cod_val)

        def every_pixel_cord(x, y):
            world_cord = cord.pixel_to_world(x, y, mat.mat_mul3)
            print('x value=-==', x)
            print('y value is ===', y)
            # print('world coordinate', wc)
            dist_to_center = cord.eq_distance(m5, world_cord)
            # print(di)
            dist_km = cord.div(dist_to_center)
            # print('division', dv)
            angle = cord.angle_calculation(m5,world_cord)
            # print('angle',angle)
            latitude, longitude = cord.coordinate_angle(angle, dist_km, lat1, log1, Radius)
            print('latitude,longitude', latitude, longitude)
            return (latitude, longitude)


        frame = Frame(root, bd=2, relief=SUNKEN)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E+W)

        yscrollbar = Scrollbar(frame)
        yscrollbar.grid(row=0, column=1, sticky=N+S)

        canvas = Canvas(frame, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set,width = 800, height = 500)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)
        
        canvas.create_image(0,0,image=image, anchor="nw")
        canvas.config(scrollregion=canvas.bbox(ALL))

        xscrollbar.config(command=canvas.xview)
        yscrollbar.config(command=canvas.yview)
        def printcoords(event):
            x = event.x
            y = event.y
            latitude, longitude = every_pixel_cord(x, y)
            fields = ('X', 'Y', 'latitude', 'longitude')
            root1 = Tk()
            input_val = [("X", x), ("Y", y), ("latitude", latitude), ("longitude", longitude)]
            ents = makeform(root1, input_val)
            b3 = Button(root1, text='Quit', command=(lambda e=root1: destroy_root(e)))
            b3.pack(side=LEFT, padx=5, pady=5)

            root1.mainloop()
        canvas.bind("<Button 1>", printcoords)

        frame.pack()
        root.mainloop()
root = Tk()

if __name__=='__main__':
    btn = Button(root, text="Select an image",command=select_image)
    btn.pack(side="bottom", fill="both", expand="yes", padx="50", pady="50")

root.mainloop()
