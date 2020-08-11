# This lesson will add a
# scrollable area for the
# quotes text.
# Final version of the app.

from kivy.app import App
# Used to link the design.kv file
# with main.py
from kivy.lang import Builder
# Used for the different screens in the app
# e.g. log in screen, signup screen etc.
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
# Allows us to hover over icons
from hoverable import HoverBehavior
# Used for hover button image
from kivy.uix.image import Image
# Used for hover function
from kivy.uix.behaviors import ButtonBehavior
# Used to read the users.json
import json
import glob
# Used to read {feelings}.txt
from pathlib import Path
# Used for the time created key in users
# dictionary
from datetime import datetime
# Used to get random happy or sad quote
import random

# Gets the kv file
Builder.load_file('design.kv')


# Need to create a class for each widget
class LoginScreen(Screen):
    def sign_up(self):
        # Self accesses manager from Screen class
        # which is used to set the current
        # screen as the signup screen
        self.manager.current = "sign_up_screen"

    # Checks if details provided
    # match details in users.json
    def login(self, uname, pword):
        with open("users.json", 'r') as file:
            users = json.load(file)
        # If details provided are correct, show login screen success
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"


# Used to add users
class SignUpScreen(Screen):
    # Gets username and password
    # from signup page
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        # Creates a dictionary for new
        # users with time created as string
        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        # Creates new file with previous users
        # and current users
        with open("users.json", 'w') as file:
            json.dump(users, file)

        # Used to change to successful sign up screen
        self.manager.current = "sign_up_screen_success"


# Displayed if new user's data was
# added successfully
class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        # Page moves right as if going back to
        # login page
        self.manager.transition.direction = 'right'
        # Goes to login screen when user presses
        # login button
        self.manager.current = "login_screen"


# Displayed when user has entered their
# details correctly
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        # Convert feeling to lowercase
        # to match the text files
        feel = feel.lower()
        # Gets all .txt files from quotes folder
        available_feelings = glob.glob("quotes/*txt")
        print(available_feelings)

        # Gets the .stem of the filename
        # i.e. sad in sad.txt
        available_feelings = [
            Path(filename).stem for filename in available_feelings]

        # Checks if feeling exists in quotes folder
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf-8") as file:
                # Reads content of .txt file
                quotes = file.readlines()
            # Reads random quote if feeling is in
            # one of the text files
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"


# Used for the dynamic hover button
# Following order is needed for button to work as log out
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


# This includes all the screens from
# the RootWidget rule
class RootWidget(ScreenManager):
    pass


# And another class for the
# main app itself
class MainApp(App):
    def build(self):
        # Initialises the root widget
        return RootWidget()


# Used to call the app and run
if __name__ == "__main__":
    MainApp().run()
