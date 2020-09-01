from functools import partial #To prevent unwanted windows
from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
import random
import sqlite3

background = "#EECFBB"
foreground = "#FAF0E4"

#*******************************************DATABASE SQLITE3 START****************************************************************
##DATABASE SECTION
#con = sqlite3.connect('hangman.db')
#c0bj= con.cursor()

# connect() will open an SQLite database, or if it
# doesn't exist it will create it
# The file appears in the same directory as this
# Python file
db_conn = sqlite3.connect('HangMan.db')
print("Database Created")

# A cursor is used to traverse the records of a result
the_cursor = db_conn.cursor()

#c0bj.execute("CREATE TABLE IF NOT EXISTS hangManTB(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT);")
#con.commit() 
#print("hangManTB Table has created")

## execute() executes a SQL command
# We organize our data in tables by defining their
# name and the data type for the data

# We define the table name
# A primary key is a unique value that differentiates
# each row of data in our table
# The primary key will auto increment each time we
# add a new Employee
# If a piece of data is marked as NOT NULL, that means
# it must have a value to be valid

# NULL is NULL and stands in for no value
# INTEGER is an integer
# TEXT is a string of variable length
# REAL is a float
# BLOB is used to store binary data

# You can delete a table if it exists like this
# db_conn.execute("DROP TABLE IF EXISTS Employees")
# db_conn.commit()
try:
    db_conn.execute("CREATE TABLE IF NOT EXISTS hangManTB(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT);")
    db_conn.commit()
    print("hangManTB Table has created")
except sqlite3.OperationalError as e:
    print("Table couldn't be created :", str(e))

# To insert data into a table we use INSERT INTO
# followed by the table name and the item name
# and the data to assign to those items
#db_conn.execute("INSERT INTO employees(f_name, l_name, age, address, salary, hire_date) VALUES ('Derek', 'Banas', 43, '123 Main St', 500000, date('now'));")
#db_conn.commit()
#print("Employee Entered")







    
    
    
#*******************************************DATABASE SQLITE3 END*********************************************************

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
        
       
    def changeTheme(self):
        global background
        background = "#aec6cf"
        self.parent.destroy
        mainFrame(self)
        
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
        
        self.words_edit_screen= Toplevel(pady = 10, bg= background)
        self.words_edit_screen.grid()   
        
        self.edit_words_label = Label(self.words_edit_screen, text="ID", width = 10, font = ("Arial", "14", "bold"), bg = background)
        self.edit_words_label.grid(row = 0, column = 1)
        
        self.edit_words_label2 = Label(self.words_edit_screen, text="Word", width = 10, font = ("Arial", "14", "bold"), bg = background)
        self.edit_words_label2.grid(row = 0, column = 3)        
        
        self.edit_words_label3 = Label(self.words_edit_screen, text="", width = 10, font = ("Arial", "14", "bold"), bg = background)
        self.edit_words_label3.grid(row = 0, column = 2)        
        
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
                except sqlite3.OperationalError:
                    messagebox.showinfo("Oh no", "It didnt work")
            self.edit_value_button = Button(self.edit_words_button_frame, text = "Edit words", font =('Century Gothic', 16), pady = 5, padx = 10, command = edit_them)
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
        self.edit_words_entry = Entry(self.words_edit_screen, font =('Century Gothic', 16), text="test", )
        self.edit_words_entry.grid(row=900, column=2)        
        
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

class MainGame:
    def __init__(self):
        background = "#EECFBB"
        
        self.game_frame= Frame(pady = 10, bg= background)
        self.game_frame.grid()
        global word_list
        
            
        
        global photos
        photos = [PhotoImage(file="hang0.png"), PhotoImage(file="hang1.png"), PhotoImage(file="hang2.png"), PhotoImage(file="hang3.png"),
                  PhotoImage(file="hang4.png"), PhotoImage(file="hang5.png"), PhotoImage(file="hang6.png"), PhotoImage(file="hang7.png"),
                  PhotoImage(file="hang8.png"), PhotoImage(file="hang9.png"), PhotoImage(file="hang10.png"), PhotoImage(file="hang11.png")]
        
        self.imgLabel=Label(self.game_frame)
        self.imgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=40)
        self.imgLabel.config(image=photos[0])
        
        global lblWord
        
        #THIS ONE GETS ALL THE INFO FROM THE DATABASE AND PUTS IT INTO THE LIST THATI WILL USE FOR THE GAME
        with db_conn:
            db_conn.row_factory = sqlite3.Row
            the_cursor = db_conn.cursor()
            the_cursor.execute("SELECT * FROM hangManTB")
            rows = the_cursor.fetchall()
            rowcounter = 1
            word_list = []
            for row in rows:
                
                rowthing = ("{}".format(row["name"]))  
                word_list.append(rowthing)    
            print(word_list)
        #my_file = open("words.txt", "r")
        #content = my_file.read()        
        #word_list = content.split(",")
        #print(word_list)
        #my_file.close()      
        
        
        word_list = [x.upper() for x in word_list] 
        
        print(word_list)
        
        lblWord=StringVar()
        self.theWord = Label(self.game_frame, textvariable=lblWord, font=("Consolas 24 bold")).grid(row=0, column=3, columnspan=6, padx=10)
        
        n=0
        for c in ascii_uppercase:
            self.theLetters = Button(self.game_frame, text=c, command=lambda c=c: self.guess(c), font=("Helvetica 18"), width=4).grid(row=1+n//9, column=n%9)
            n+=1    
            
        global the_word_withSpaces
        global numberOfGuesses
        numberOfGuesses=0
        self.imgLabel.config(image=photos[0])
        the_word=random.choice(word_list)
        the_word_withSpaces=" ".join(the_word)
        lblWord.set(" ".join("_"*len(the_word)))         
        
        
  
       
               
        
    def guess(self, letter):
        global numberOfGuesses
        if numberOfGuesses<11:
            txt=list(the_word_withSpaces)
            guessed=list(lblWord.get())
            if the_word_withSpaces.count(letter)>0:
                for c in range(len(txt)):
                    if txt[c]==letter:
                        guessed[c]=letter
                    lblWord.set("".join(guessed))
                    #WHEN THE THING FINISHED IT KEPT LOOPING THIS MESSAGER BOX. I BACKSPACED TO KEEP IT FROM REPEATING
                if lblWord.get()==the_word_withSpaces:
                    self.restart_frame = Toplevel(bg = background, pady=10, padx=20)
                    self.play_again_button = Button(self.restart_frame, text="Play Again", command=self.close_game ,font=("Consolas 24 bold")).grid(row=0, column=3, columnspan=6, padx=10)
                   
                    
            else:
                numberOfGuesses+=1
                self.imgLabel.config(image=photos[numberOfGuesses])
                if numberOfGuesses==11:
                    messagebox.showwarning("Hangman", "GameOver")            
    
    def close_game(self):
        self.game_frame.destroy()  
        MainGame() 
    
     
if __name__ == "__main__":
    root=Tk()
    root.title("Fleur")
    something = mainFrame(root)
    root.mainloop()