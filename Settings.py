from Widget import *

class Settings:
    def __init__(self):
        self.volume=50
        self.fifty_fifty_on = False
        self.create_game_finished_window = True
        self.on = PhotoImage(file="on_switch.png")
        self.off = PhotoImage(file="off_switch.png")

    def create_settings_window(self, main_menu, window):
        main_menu.forget()
        settings_window = Frame(window)
        settings_window.pack()

        #title
        Label(settings_window, text="Settings", font=("Calibri", 24), bg="white", fg="grey").grid(row=0, column=1)

        #creating close button
        Button(settings_window, text="X", font=("Calibri", 30), bg="white", fg="red", command=lambda: self.close_window(settings_window, main_menu)).grid(row=0, column=2)

        settings_options=Frame(settings_window)
        settings_options.grid(row=1,column=1)

        #creating options in settings_options window
        create_gfw_button = Button(settings_options, image=self.on, command=lambda: self.switch(create_gfw_button, self.create_game_finished_window, "create_game_finished_window"))
        print(self.create_game_finished_window)
        create_gfw_button.grid(row=0,column=0)


    def switch(self, button, status, attribute):
        if not status:
            setattr(self, attribute, True)
            button.config(image=self.on)
            print("Button now on")
        elif status:
            setattr(self, attribute, False)
            button.config(image=self.off)
            print("Button now off")

    def close_window(self, settings_window, main_menu):
        settings_window.destroy()
        main_menu.pack()

        #use user_settings.txt to, during initialisation, create a dictionary of the names of settings and their values
        #then, set each of the attributes of the Settings object to the value in the dictionary:
        # eg. self.create_game_finished_window = settings_map[create_game_finished_window]


#need to add more options, also need to add text for what each option is
#need to resize images of switches