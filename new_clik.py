import sys
import cv2
from Tkinter import *
import Image, ImageTk
imgCV = cv2.imread('0002_C.jpg')
print(imgCV.shape)
root = Tk()
geometry = "%dx%d+0+0"%(imgCV.shape[0], imgCV.shape[1])
root.geometry()
def leftclick(event):
    print("left")
    print('===============')
    #print root.winfo_pointerxy()
    print (event.x, event.y)
    #print("BGR color")
    print (imgCV[event.x, event.y])
    # convert color from BGR to HSV color scheme
    hsv = cv2.cvtColor(imgCV, cv.COLOR_BGR2HSV)
    print("HSV color")
    print (hsv[event.x, event.y])
# import image
img = ImageTk.PhotoImage(Image.open('0002_C.jpg'))
panel = Label(root, image = img)
panel.bind("<Button-1>", leftclick)
#panel.pack(side = "bottom", fill = "both", expand = "no")
panel.pack(fill = "both", expand = 1)
root.mainloop()