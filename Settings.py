from Widget import *

class Settings:
    def __init__(self, minesweeper_window):
        self.volume=50
        self.fifty_fifty_on = False
        #self.create_game_finished_window = True
        self.settings_window = Frame(minesweeper_window)
        self.on = PhotoImage(file="on_switch.png", master=self.settings_window)
        self.off = PhotoImage(file="off_switch.png", master=self.settings_window)
        self.user_settings={}
        with open("user_settings.txt", "r") as file:
            for line in file:
                record = line.split(":")
                if record[1].strip("\n")=="True":
                    self.user_settings[record[0]] = True
                elif record[1].strip("\n")=="False":
                    self.user_settings[record[0]] = False


    def create_settings_window(self, main_menu, window):
        main_menu.forget()
        self.settings_window = Frame(window)
        self.settings_window.pack()

        #title
        Label(self.settings_window, text="Settings", font=("Calibri", 24), bg="white", fg="grey").grid(row=0, column=1)

        #creating close button
        Button(self.settings_window, text="X", font=("Calibri", 30), bg="white", fg="red", command=lambda: self.close_window(self.settings_window, main_menu)).grid(row=0, column=2)

        settings_options=Frame(self.settings_window)
        settings_options.grid(row=1,column=1)

        #creating options in settings_options window
        create_gfw_button = Button(settings_options,
                                   image=self.get_switch_status("create_game_finished_window"),
                                   command=lambda: self.switch(create_gfw_button,
                                                               self.user_settings["create_game_finished_window"],
                                                               "create_game_finished_window"))
        if create_gfw_button.cget("image")==self.on:
            print("Button is on")
        elif create_gfw_button.cget("image")==self.off:
            print("Button is off")
        create_gfw_button.grid(row=0,column=0)

    def get_switch_status(self, attribute):
        if self.user_settings[attribute]:
            return self.on
        elif not self.user_settings[attribute]:
            return self.off


    def switch(self, button, status, attribute):
        if not status:
            self.user_settings[attribute] = True
            button.config(image=self.on)
        elif status:
            self.user_settings[attribute] = False
            button.config(image=self.off)

    def close_window(self, settings_window, main_menu):
        with open("user_settings.txt","w") as file:
            for a,b in self.user_settings.items():
                file.write(f"{a}:{b}\n")
        settings_window.destroy()
        main_menu.pack()

        #use user_settings.txt to, during initialisation, create a dictionary of the names of settings and their values
        #then, set each of the attributes of the Settings object to the value in the dictionary:
        # eg. self.create_game_finished_window = settings_map[create_game_finished_window]


#need to add more options, also need to add text for what each option is
#need to resize images of switches

#class Settings:
#    def __init__(self, window):
#        self.user_settings={"create_game_finished_window":True}
#
#    def create_settings_window(self,a,b):
#        pass