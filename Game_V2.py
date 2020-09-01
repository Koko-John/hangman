from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
import random
import sqlite3


background = "#EECFBB"
foreground = "#FAF0E4"

#Creates a database called hangman.db
db_conn = sqlite3.connect('HangMan.db')
#If it worked, it will print this.
print("Database Created")

# A cursor is used to traverse the records of a result
the_cursor = db_conn.cursor()

#Creates a table to store the words. Works like a list.
try:
    db_conn.execute("CREATE TABLE IF NOT EXISTS hangManTB(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT);")
    db_conn.commit()
    print("hangManTB Table has created")
except sqlite3.OperationalError as e:
    print("Table couldn't be created :", str(e))

class MainGame:
    def __init__(self):
        #setting up game frame.
  
        self.game_frame= Frame(pady = 10, bg= background)
        self.game_frame.grid()
        global word_list
        
            
        #photos for the hangman pic
        global photos
        photos = [PhotoImage(file="hang0.png"), PhotoImage(file="hang1.png"), PhotoImage(file="hang2.png"), PhotoImage(file="hang3.png"),
                  PhotoImage(file="hang4.png"), PhotoImage(file="hang5.png"), PhotoImage(file="hang6.png"), PhotoImage(file="hang7.png"),
                  PhotoImage(file="hang8.png"), PhotoImage(file="hang9.png"), PhotoImage(file="hang10.png"), PhotoImage(file="hang11.png")]
        
        #Creates the start photo 
        self.imgLabel=Label(self.game_frame)
        self.imgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=40)
        self.imgLabel.config(image=photos[0])
        

        
        #Make the letter buttons
        n=0
        for c in ascii_uppercase:
            self.theLetters = Button(self.game_frame, text=c, font=("Helvetica 18"), width=4).grid(row=1+n//9, column=n%9)
            n+=1    

         
        
if __name__ == "__main__":
    root=Tk()
    root.title("Fleur")
    something = MainGame()
    root.mainloop()
