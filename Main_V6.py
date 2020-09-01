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
        self.start_game = Button(self.main_frame, text = "Start Game", font =('Century Gothic', 16), pady = 5, padx = 10, command = self.close_main)
        self.start_game.grid(row=3, column=0)    

        #Making the how to button
        self.EditButton = Button(self.main_frame, text = "Edit Words", font =('Century Gothic', 16), pady = 5, padx = 10, command = self.edit_words)
        self.EditButton.grid(row=3, column=3)   

        self.howToPlayButton = Button(self.main_frame, text = "How to play", font =('Century Gothic', 16), pady = 5, padx = 10, command = self.HowToPlayFrame)
        self.howToPlayButton.grid(row=3, column=1)                


    def HowToPlayFrame(self):

        self.howToPlayButton.config(state = DISABLED)


        #Setting up the help_box window
        self.how_to_frame = Toplevel(pady = 10, padx = 10, bg = background)


        #Set up heading of the how to box frame
        self.help_heading = Label(self.how_to_frame, text = "Settings",
                                  font = ("Lottes Handwriting", 60, "bold"),
                                  bg = background, fg = foreground)    
        self.help_heading.grid(row=1)

        self.how_to_frame.protocol('WM_DELETE_WINDOW', partial(self.close_HowTo))



    def close_HowTo(self):

        #Put history button back to normal...
        self.howToPlayButton.config(state = NORMAL)
        self.how_to_frame.destroy() 

    def close_main(self):



        #Closes the mainFrame Class and opens the GameFrame class 
        self.parent.destroy()  
        MainGame()

    #making the edit words screen    

    def edit_words(self):#arema ###################################################################################################
        self.EditButton.config(state = DISABLED)
        
        self.words_edit_screen= Toplevel(pady = 10, bg= background)
        self.words_edit_screen.grid()   

        self.edit_words_label = Label(self.words_edit_screen, text="ID", width = 10, font = ("Arial", "14", "bold"), bg = background)
        self.edit_words_label.grid(row = 0, column = 1)

        self.edit_words_label2 = Label(self.words_edit_screen, text="Word", width = 10, font = ("Arial", "14", "bold"), bg = background)
        self.edit_words_label2.grid(row = 0, column = 3)        

        self.edit_words_label3 = Label(self.words_edit_screen, text="", width = 10, font = ("Arial", "14", "bold"), bg = background)
        self.edit_words_label3.grid(row = 0, column = 2)        
        
        self.edit_words_label4 = Label(self.words_edit_screen, text="\nEdit: To edit an existing word, enter its id\n in the entry box\n and enter the updated value in the\n popup window. Press finished\nwhen done", width = 40, font = ("Arial", "10"), bg = background)
        self.edit_words_label4.grid(row = 1, column = 2)            
        
        self.edit_words_label5 = Label(self.words_edit_screen, text="\nDelete: Enter the Id into the entry box\n and then click delete", width = 40, font = ("Arial", "10"), bg = background)
        self.edit_words_label5.grid(row = 2, column = 2)  
        
        self.edit_words_label6 = Label(self.words_edit_screen, text="\nAdd: Enter the word into the entry box\n and then click add", width = 40, font = ("Arial", "10"), bg = background)
        self.edit_words_label6.grid(row = 3, column = 2)         
        #MADE THIS SO THE SCREEN REFRESHES
        def refresh_words():
            self.words_edit_screen.destroy()
            self.edit_words()
        with db_conn:
            db_conn.row_factory = sqlite3.Row
            the_cursor = db_conn.cursor()
            the_cursor.execute("SELECT * FROM hangManTB")
            rows = the_cursor.fetchall()
            rowcounter = 1
            for row in rows:

                rowthing = ("{}".format(row["name"]))  
                idrowthing = ("{}".format( row["ID"]))

                Label(self.words_edit_screen, text=idrowthing, width = 10, font =('Century Gothic', 16), bg= background).grid(row=rowcounter, column=1)
                Label(self.words_edit_screen, text=rowthing, width = 10,font =('Century Gothic', 16), bg = background).grid(row=rowcounter, column=3)
                rowcounter+=1   
        def adding_words_button_action():

            global userInput
            self.newWordsList = []
            self.userInput =""

            userInput = self.edit_words_entry.get() #get word from form
        # print(self.userInput)#print the user input
            insert_Value(userInput)
            refresh_words()



        def edit_words_button_action():
            self.edit_words_button_frame = Toplevel(pady = 10, bg= background)
            self.edit_words_button_frame.grid()  
            self.edit_words_button.config(state = DISABLED)

            self.edit_words_button_entry = Entry(self.edit_words_button_frame, font =('Century Gothic', 16))
            self.edit_words_button_entry.grid(row=0, column=1)              
            editWordsInput = self.edit_words_entry.get()

            def edit_them():
                
                thenewvalue = self.edit_words_button_entry.get()
                try:
                    db_conn.execute("UPDATE hangmanTb SET name = ? WHERE ID = ?",(thenewvalue,editWordsInput,))
                    db_conn.commit()

                    refresh_words()
                    self.edit_words_button_frame.destroy()
                    self.edit_words_button.config(state = NORMAL)
                except sqlite3.OperationalError:
                    messagebox.showinfo("Oh no", "It didnt work")
            self.edit_value_button = Button(self.edit_words_button_frame, text = "Finished", font =('Century Gothic', 16), pady = 5, padx = 10, command = edit_them)
            self.edit_value_button.grid(row=0, column=2)                  
        def delete_words_button_action():
            try:
                editWordsInput = self.edit_words_entry.get()
                db_conn.execute("DELETE FROM hangmanTB WHERE ID = ?",(editWordsInput,))
                db_conn.commit()
                refresh_words()
                self.edit_words_button_frame.destroy()
            except sqlite3.OperationalError:
                messagebox.showinfo("Oh no", "It didnt work")
        def correct(inp):
            if inp == " ":
                print(inp)
                return False
            elif inp == "":
                print(inp)
                return True
            elif inp.isdigit():
                print(inp)
                return False
            elif inp.isalpha():
                return True
            else:
                return False
        
        reg = root.register(correct)
        
        self.edit_words_entry = Entry(self.words_edit_screen, font =('Century Gothic', 16), text="test", )
        self.edit_words_entry.grid(row=900, column=2)    
        
        self.edit_words_entry.config(validate="key", validatecommand=(reg, '%P'))

        self.edit_words_button = Button(self.words_edit_screen, text = "Edit words", font =('Century Gothic', 16), pady = 5, padx = 10, command = edit_words_button_action)
        self.edit_words_button.grid(row=901, column=1)            

        self.delete_words_button = Button(self.words_edit_screen, text = "Delete words", font =('Century Gothic', 16), pady = 5, padx = 10, command = delete_words_button_action)
        self.delete_words_button.grid(row=901, column=2) 

        self.add_words_button = Button(self.words_edit_screen, text = "Add words", font =('Century Gothic', 16), pady = 5, padx = 10, command = adding_words_button_action)
        self.add_words_button.grid(row=901, column=3)          





        #THIS IS HOW THE AUTO INCREMENT INSERT WORKS
#def insert_Value(koko):
    #c0bj.execute("INSERT INTO arema(name) VALUES(?)", (koko))
    #con.commit()  

def insert_Value(koko):
    #c0bj.execute("INSERT INTO arema(name) VALUES("|| koko ||"jn o )")
    #con.commit()     
    print(koko)

    # To insert data into a table we use INSERT INTO
    # followed by the table name and the item name
    # and the data to assign to those items
    db_conn.execute("INSERT INTO hangManTB(name) VALUES (?)",(koko,))
    db_conn.commit()
    print("Your word has successfuly Entered")    

    #INTO COMPANY (NAME,AGE,ADDRESS,SALARY)
    #VALUES ( 'Paul', 32, 'California', 20000.00 )    



    #def insertWords(self):
        #filename = "words.txt"

        ##open file to hold data
        #f = open(filename, "a")
        #print(self.newWordsList)
        ##Add a comma after each item.
        #for item in self.newWordsList:
            #f.write(item + ",")


        #close file
        #f.close()

#this code is just testing. will connect the game and main components in the final version
if __name__ == "__main__":
    root=Tk()
    root.title("Fleur")
    something = mainFrame(root)
    root.mainloop()