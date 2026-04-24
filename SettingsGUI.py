from tkinter import *
from PIL import Image, ImageTk
from Settings import Settings

class SettingsGUI:
    def __init__(self, settings: Settings, main_window):
        self.settings_data = settings
        
        self.main_menu = Frame()
        self.main_window = main_window

        # creating frames
        self.settings_frame = Frame(self.main_window)
        self.settings_switches_frame = Frame(self.settings_frame)

        # importing images
        self.on_image = Image.open("Images/on_switch.png")
        self.on_image = self.on_image.resize((80, 30))
        self.on_image = ImageTk.PhotoImage(self.on_image)

        self.off_image = Image.open("Images/off_switch.png")
        self.off_image = self.off_image.resize((80, 30))
        self.off_image = ImageTk.PhotoImage(self.off_image)

        # dictionary of all switch widgets in the menu
        self.switches = {}
    
    def create_settings_window(self, main_menu):
        # switching frames
        self.main_menu = main_menu
        self.main_menu.forget()
        self.settings_frame = Frame(self.main_window)
        self.settings_frame.pack()

        # title
        Label(self.settings_frame, text="Settings", font=("Calibri Bold", 24), bg="white", fg="grey").grid(row=0, column=0)

        # creating close button
        Button(self.settings_frame, text="X", font=("Calibri Bold", 30), bg="white", fg="red",
               command=lambda: self.close_window()).grid(row=0,column=2)

        # creating frame that stores the switch widgets
        self.settings_switches_frame = Frame(self.settings_frame)
        self.settings_switches_frame.grid(row=1, column=1)

        self.create_settings_switches()
    
    def create_settings_switches(self):
        # iterating through each setting and creating its switch
        for i, setting_name in enumerate(self.settings_data.user_settings):
            name_of_setting_frame = Frame(self.settings_switches_frame, width=1000)
            name_of_setting_frame.grid(row=i, column=0)
            # creating the name of the setting
            Label(name_of_setting_frame, text=setting_name, font=("Calibri Bold", 20), pady=30).pack(side=LEFT)
            # creating the information button
            Button(name_of_setting_frame, text="i", font=("Calibri", 15), fg="grey",
                   command=lambda: self.popup_info_window(setting_name)).pack(side=RIGHT, padx=15)
            # creating the switch
            self.switches[setting_name] = Button(self.settings_switches_frame,
                                                 image = self.on_image if self.settings_data.user_settings[setting_name] else self.off_image,
                                                 command = lambda current_setting = setting_name: self.switch_state(current_setting))
            self.switches[setting_name].grid(row=i, column=1, padx=40)
    
    def switch_state(self, setting):
        # switches the Boolean value of the current switch and any linked switches
        corresponding_setting = self.settings_data.switch_setting(setting)
        
        if self.settings_data.user_settings[setting]: # if setting is now True
            self.switches[setting].config(image = self.on_image)
            # switching linked setting to True if there is one
            if corresponding_setting is not None:
                self.switches[corresponding_setting].config(image = self.on_image)
        else:
            self.switches[setting].config(image = self.off_image)
            # switching linked setting to False if there is one
            if corresponding_setting is not None:
                self.switches[corresponding_setting].config(image = self.off_image)
    
    def close_window(self):
        self.settings_data.update_settings_file()
        self.settings_frame.destroy()
        self.main_menu.pack()
