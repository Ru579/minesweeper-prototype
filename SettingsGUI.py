from tkinter import *
from PIL import Image, ImageTk

class SettingsGUI:
    def __init__(self, settings, window):
        self.settings_data = settings

        self.main_menu = None
        self.window = window

        # creating frames
        self.settings_frame = Frame(self.window)
        self.settings_switches_frame = Frame(self.settings_frame)

        # getting images
        self.on = Image.open("Images/on_switch.png")
        self.on = self.on.resize((80, 30))
        self.on = ImageTk.PhotoImage(self.on)

        self.off = Image.open("Images/off_switch.png")
        self.off = self.off.resize((80, 30))
        self.off = ImageTk.PhotoImage(self.off)

        #switches
        self.switches = {}



    def create_settings_window(self, main_menu):
        self.main_menu = main_menu
        self.main_menu.forget()
        self.settings_frame = Frame(self.window)
        self.settings_frame.pack()

        # title
        Label(self.settings_frame, text="Settings", font=("Calibri Bold", 24), bg="white", fg="grey").grid(row=0, column=0)

        # creating close button
        Button(self.settings_frame, text="X", font=("Calibri Bold", 30), bg="white", fg="red",
               command=lambda: self.close_window()).grid(row=0,column=2)

        # creating frame that stores the switches that change settings
        self.settings_switches_frame = Frame(self.settings_frame)
        self.settings_switches_frame.grid(row=1, column=1)

        self.create_settings_switches()


    def create_settings_switches(self):
        for i, setting_name in enumerate(self.settings_data.user_bool_settings):
            setting_name_frame = Frame(self.settings_switches_frame, width=1000)
            setting_name_frame.grid(row=i, column=0)
            Label(setting_name_frame, text=setting_name, font=("Calibri Bold", 20), pady=30).pack(side=LEFT)
            Button(setting_name_frame, text="i", font=("Calibri", 15), fg="grey",
                   command=lambda: self.popup_info_window(setting_name)).pack(side=RIGHT, padx=15)

            self.switches[setting_name] = Button(self.settings_switches_frame,
                                                 image = self.on if self.settings_data.user_bool_settings[setting_name] else self.off,
                                                 command = lambda current_setting = setting_name: self.switch_state(current_setting))
            self.switches[setting_name].grid(row=i, column=1, padx=40)
         # add code for dealing with variable settings

    def switch_state(self, setting):
        # switches the Boolean value of the current switch and any linked switches, then returns the linked switch's name
        corresponding_setting = self.settings_data.switch(setting)
        if self.settings_data.user_bool_settings[setting]:
            self.switches[setting].config(image = self.on)
            if corresponding_setting is not None:
                self.switches[corresponding_setting].config(image = self.on)
        else:
            self.switches[setting].config(image = self.off)
            #if setting in self.settings_data.linked_settings:
            #    #self.switch_state(self.switches[self.settings_data.linked_settings[setting]])
            #    self.switches[self.settings_data.linked_settings[setting]].config(image = self.off)
            if corresponding_setting is not None:
                self.switches[corresponding_setting].config(image = self.off)


    def popup_info_window(self, setting):
        pass


    def close_window(self):
        self.settings_data.save_settings()
        self.settings_frame.destroy()
        self.main_menu.pack()

