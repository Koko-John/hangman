from functools import partial #To prevent unwanted windows
from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
import random
import sqlite3

background = "#EECFBB"
foreground = "#FAF0E4"



#Connecting to database
db_conn = sqlite3.connect('HangMan.db')
print("Database Created")

background = "#EECFBB"
foreground = "#FAF0E4"

# A cursor is used to traverse the records of a result
the_cursor = db_conn.cursor()

#the table has been made so this code isn't needed. Im keeping it here for reference later
##c0bj.execute("CREATE TABLE IF NOT EXISTS hangManTB(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT);")
##con.commit() 
##print("hangManTB Table has created")
class mainFrame:
    def __init__(self, parent):
        global background
        self.parent = parent



        #Am making the window
        self.main_frame = Frame(bg = background, pady = 50, padx = 20)
        self.main_frame.grid()            

        #Making the label
        self.__main_label= Label(self.main_frame, text = "Fleur", fg = foreground, bg = background, font=("Lottes Handwriting", 60, "bold"),
                                 pady=10, padx=10)
        self.__main_label.grid(row = 1, column=1)        

        #Making the start button
        self.start_game = Button(self.main_frame, text = "Start Game", font =('Century Gothic', 16), pady = 5, padx = 10)
        self.start_game.grid(row=3, column=0)    

        #Making the how to button
        self.settingsButton = Button(self.main_frame, text = "Settings", font =('Century Gothic', 16), pady = 5, padx = 10, command = self.settingsBox)
        self.settingsButton.grid(row=3, column=2)        
        
    def settingsBox(self):
        
        self.settingsButton.config(state = DISABLED)
       
       
        #Setting up the help_box window
        self.how_to_frame = Toplevel(pady = 10, padx = 10, bg = background)
       
        
          
        
        self.change_theme_button = Button(self.how_to_frame, text = "How to play", font =('Century Gothic', 16), pady = 5, padx = 10)
        self.change_theme_button.grid(row=2, column=0)    
        
        self.Edit_words_button = Button(self.how_to_frame, text = "Edit words", font =('Century Gothic', 16), pady = 5, padx = 10)
        self.Edit_words_button.grid(row=4, column=0)    
        
        
        
        #Set up heading of the how to box frame
        self.help_heading = Label(self.how_to_frame, text = "Settings",
                                  font = ("Lottes Handwriting", 60, "bold"),
                                          bg = background, fg = foreground)    
        self.help_heading.grid(row=1)
        
        self.how_to_frame.protocol('WM_DELETE_WINDOW', partial(self.close_Settings))
        
    def close_Settings(self):

        #Put history button back to normal...
        self.settingsButton.config(state = NORMAL)
        self.how_to_frame.destroy() 
if __name__ == "__main__":
    root=Tk()
    root.title("Fleur")
    something = mainFrame(root)
    root.mainloop()