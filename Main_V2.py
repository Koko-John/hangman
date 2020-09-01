from tkinter import *
import random
import sqlite3


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
        self.settingsButton = Button(self.main_frame, text = "Settings", font =('Century Gothic', 16), pady = 5, padx = 10)
        self.settingsButton.grid(row=3, column=2)        
        
      


if __name__ == "__main__":
    root=Tk()
    root.title("Fleur")
    something = mainFrame(root)
    root.mainloop()