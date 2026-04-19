class DatabaseHandler:
    def __init__(self):
        self.user_signed_in = False

        # profile information
        self.username = ""

        # temporary sign in information- used during login
        self.temp_username = ""

    def find_user_file(self, username_input):
        self.temp_username = username_input
        return True
    
    def check_pword(self, pword_input):
        return True
    
    def sign_in_user(self):
        print(f"signed in {self.temp_username}")