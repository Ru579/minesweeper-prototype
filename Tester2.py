#from tkinter import *
#from PIL import Image, ImageTk
#
#def on_button_toggle():
#        if var.get() == 1:
#                print("Checkbutton is selected")
#        else:
#                print("Unselected")
#
#root = Tk()
#
#var = IntVar()
#my_button = Checkbutton(root, text="Hello!", variable=var, image=ImageTk.PhotoImage(Image.open("on_switch.png")), onvalue=1 ,offvalue=0,
#                        command = lambda: on_button_toggle())
#my_button.pack()
#my_button.flash()
#
#mainloop()

#from tkinter import *
#from PIL import Image, ImageTk
#
#def switch():
#        if Checkbutton1.get()==1:
#                Button1.config(image = on)
#        else:
#                Button1.config(image = off)
#
#root = Tk()
#root.geometry("1000x1000")
#
#w = Label(root, text='GeeksForGeeks', font="50")
#w.pack()
#
#Checkbutton1 = IntVar()
#Checkbutton2 = IntVar()
#Checkbutton3 = IntVar()
#image = Image.open("off_switch.png")
#off = ImageTk.PhotoImage(image)
#image = Image.open("on_switch.png")
#on = ImageTk.PhotoImage(image)
#
#Button1 = Checkbutton(root, text="Tutorial",
#                      variable=Checkbutton1,
#                      onvalue=1,
#                      offvalue=0,
#                      height=400,
#                      width=400,
#                      image = off,
#                      command=lambda: switch())
#
#Button2 = Checkbutton(root, text="Student",
#                      variable=Checkbutton2,
#                      onvalue=1,
#                      offvalue=0,
#                      height=2,
#                      width=10)
#
#Button3 = Checkbutton(root, text="Courses",
#                      variable=Checkbutton3,
#                      onvalue=1,
#                      offvalue=0,
#                      height=2,
#                      width=10)
#
#Button1.pack()
#Button2.pack()
#Button3.pack()
#
#mainloop()

#data = []
#with open("ms_user_data/Classic/Beginner/123_ClBeginner.txt") as file:
#    for i in range(2):
#        data.append(file.readline())
#    file.close()
#print(data)



#def create_settings_switches(self):
#    for i, setting_name in enumerate(self.settings_data.user_bool_settings):
#        #row_frame = Frame(self.settings_switches_frame, width=1000)
#        #row_frame.grid(row=i, column=0)
#        #Label(row_frame, text=setting_name, font=("Calibri Bold", 20), pady=30).pack(side=LEFT)
#        #Button(row_frame, text="i", font=("Calibri", 15), fg="grey",
#        #       command=lambda: self.popup_info_window(setting_name)).pack(side=LEFT)
#
#        #self.switches[setting_name] = Button(row_frame,
#        #                                     image = self.on if self.settings_data.user_bool_settings[setting_name] else self.off,
#        #                                     command = lambda: self.switch_state(self.switches[setting_name]))
#        #self.switches[setting_name].pack(side=RIGHT)#