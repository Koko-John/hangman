
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


the_cursor.execute(
"CREATE TABLE IF NOT EXISTS hangmanDB(ID INTEGER PRIMARY KEY  NOT NULL, name TEXT PRIMARY KEY NOT NULL );")
db_conn.commit() 
print("hangmanDB Table has created")
class mainFrame:
    def __init__(self, parent):
        global background
        self.parent = parent
        
        word1= "hangman"
        word2= "fleur"
        word3= "John"
        
        #starter words for the game
        db_conn.execute("INSERT OR REPLACE INTO hangmanDB(name) VALUES (?)", (word1,))
        db_conn.commit()
        db_conn.execute("INSERT OR REPLACE INTO hangmanDB(name) VALUES (?)", (word2,))
        db_conn.commit()
        db_conn.execute("INSERT OR REPLACE INTO hangmanDB(name) VALUES (?)", (word3,))
        db_conn.commit()

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
        self.help_heading = Label(self.how_to_frame, text = "How to play",
                                  font = ("Lottes Handwriting", 30, "bold"),
                                  bg = background, fg =foreground)    
        self.help_heading.grid(row=1)
        
        self.help_heading = Label(self.how_to_frame, text = "The underscores represent"\
                                  "\nthe number of letters in the word.\n Press the"\
                                  "buttons to guess",
                                  font = ("Century Gothic", 20),
                                  bg = background, )    
        self.help_heading.grid(row=2)
        

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
            the_cursor.execute("SELECT * FROM hangManTable")
            rows = the_cursor.fetchall()
            rowcounter = 1
            for row in rows:

                rowthing = ("{}".format(row["name"]))  
                idrowthing = ("{}".format( row["ID"]))

                Label(self.words_edit_screen, text=idrowthing, width = 10, font =('Century Gothic', 16), bg= background).grid(row=rowcounter, column=1)
                Label(self.words_edit_screen, text=rowthing, width = 10,font =('Century Gothic', 16), bg = background).grid(row=rowcounter, column=3)
                rowcounter+=1   
        def adding_words_button_action():
            self.adding_words_button_frame = Toplevel(pady = 10, bg= background)
            self.adding_words_button_frame.grid()  
            self.edit_words_button.config(state = DISABLED)
            self.delete_words_button.config(state= DISABLED)
            self.add_words_button.config(state= DISABLED)            
            def correct(inp):
                if inp == " ":
                    messagebox.showwarning("Error", "Spaces are not allowed")  
                    return False
                elif inp == "":
                    print(inp)
                    return False
                elif inp.isdigit():
                    messagebox.showwarning("Error", "Numbers are not allowed")  
                    return False
                elif inp.isalpha():
                    return True
                else:
                    messagebox.showwarning("Error", "Special chracters are not allowed")  
                    return False

            reg = root.register(correct)

            global userInput
            self.newWordsList = []
            self.userInput =""
            self.new_words = Entry(self.adding_words_button_frame, font =('Century Gothic', 16))
            self.new_words.grid(row=0, column=1)              

            self.new_words.config(validate="key", validatecommand=(reg, '%P'))
            def enter_new_word_db():
                userInput = self.new_words.get() #get word from form
                    
                if len(userInput)== 0:
                    messagebox.showwarning("Error", "empty words are not allowed") 
                    refresh_words()
                    self.adding_words_button_frame.destroy()
                else:
                    insert_Value(userInput) 
                    refresh_words()    
                    self.adding_words_button_frame.destroy()                                
                
            self.adding_words_button_frame.protocol('WM_DELETE_WINDOW', partial(self.close_add_words))
            
            self.new_word_button = Button(self.adding_words_button_frame, text = "Add", font =('Century Gothic', 16), pady = 5, padx = 10, command = enter_new_word_db)
            self.new_word_button.grid(row=0, column=2)  
            
            
        





        def edit_words_button_action():
            self.edit_words_button_frame = Toplevel(pady = 10, bg= background)
            self.edit_words_button_frame.grid()  
            self.edit_words_button.config(state = DISABLED)
            self.delete_words_button.config(state= DISABLED)
            self.add_words_button.config(state= DISABLED)

            self.edit_words_button_entry = Entry(self.edit_words_button_frame, font =('Century Gothic', 16))
            self.edit_words_button_entry.grid(row=0, column=1)              
            editWordsInput = self.edit_words_entry.get()

            def edit_them():

                thenewvalue = self.edit_words_button_entry.get()
                if len(thenewvalue)== 0:
                    messagebox.showwarning("Error", "empty words are not allowed") 
                    refresh_words()
                    self.edit_words_button_frame.destroy()
                    self.edit_words_button.config(state = NORMAL)  
                else:
                    db_conn.execute("UPDATE hangManTable SET name = ? WHERE ID = ?",(thenewvalue,editWordsInput,))
                    db_conn.commit()
                    refresh_words()    
                    self.edit_words_button_frame.destroy()
                    self.edit_words_button.config(state = NORMAL)                 
                


            self.edit_value_button = Button(self.edit_words_button_frame, text = "Finished", font =('Century Gothic', 16), pady = 5, padx = 10, command = edit_them)
            self.edit_value_button.grid(row=0, column=2)    
            self.edit_words_button_frame.protocol('WM_DELETE_WINDOW', partial(self.close_edit_words))
        def delete_words_button_action():
            try:
                editWordsInput = self.edit_words_entry.get()
                db_conn.execute("DELETE FROM hangManTable WHERE ID = ?",(editWordsInput,))
                db_conn.commit()
                refresh_words()

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

        self.words_edit_screen.protocol('WM_DELETE_WINDOW', partial(self.close_Settings))

    def close_Settings(self):
        self.EditButton.config(state = NORMAL)
               
        self.words_edit_screen.destroy() 
    def close_add_words(self):
        self.edit_words_button.config(state = NORMAL)
        self.delete_words_button.config(state= NORMAL)
        self.add_words_button.config(state= NORMAL)
        self.adding_words_button_frame.destroy()   
    def close_edit_words(self):
        self.edit_words_button.config(state = NORMAL)
        self.delete_words_button.config(state= NORMAL)
        self.add_words_button.config(state= NORMAL)
        self.edit_words_button_frame.destroy()           
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
    db_conn.execute("INSERT OR REPLACE INTO hangManTable(name) VALUES (?)",(koko,))
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
class MainGame:
    def __init__(self):
        #setting up game frame.

        self.game_frame= Frame(pady = 10, bg= background)
        self.game_frame.grid()
        global word_list
        global lblWord

        #photos for the hangman pic
        global photos
        photos = [PhotoImage(file="hang0.png"), PhotoImage(file="hang1.png"), PhotoImage(file="hang2.png"), PhotoImage(file="hang3.png"),
                  PhotoImage(file="hang4.png"), PhotoImage(file="hang5.png"), PhotoImage(file="hang6.png"), PhotoImage(file="hang7.png"),
                  PhotoImage(file="hang8.png"), PhotoImage(file="hang9.png"), PhotoImage(file="hang10.png"), PhotoImage(file="hang11.png")]

        #Creates the start photo 
        self.imgLabel=Label(self.game_frame)
        self.imgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=40)
        self.imgLabel.config(image=photos[0])



        with db_conn:
            db_conn.row_factory = sqlite3.Row
            the_cursor = db_conn.cursor()
            the_cursor.execute("SELECT * FROM hangManTable")
            rows = the_cursor.fetchall()
            rowcounter = 1
            word_list = []
            for row in rows:

                rowthing = ("{}".format(row["name"]))  
                word_list.append(rowthing)    
            print(word_list)

            #Makes all the letters uppercase in the program
        word_list = [x.upper() for x in word_list] 
        print(word_list)  

        #Creates the letters at the top
        lblWord=StringVar()
        self.theWord = Label(self.game_frame, textvariable=lblWord, font=("Consolas 24 bold")).grid(row=0, column=3, columnspan=6, padx=10)


        #Make the letter buttons
        n=0
        for c in ascii_uppercase:
            self.theLetters = Button(self.game_frame, text=c, command=lambda c=c: self.guess(c), font=("Helvetica 18"), width=4).grid(row=1+n//9, column=n%9)
            n+=1    

        #Makes the letters at the top turn into underscores if not guessed yet
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
                if lblWord.get()==the_word_withSpaces:
                    self.restart_frame = Toplevel(bg = background, pady=10, padx=10)

                    self.play_again_button = Button(self.restart_frame, text="Play Again", command=self.close_game ,font=("Consolas 24 bold")).grid(row=0, column=3, columnspan=6, padx=10)
            else:
                numberOfGuesses+=1
                self.imgLabel.config(image=photos[numberOfGuesses])
                if numberOfGuesses==11:
                    messagebox.showwarning("Fleur", "GameOver")     
    def close_game(self):
        self.restart_frame.destroy()
        self.game_frame.destroy()  
        MainGame()     
#this code is just testing. will connect the game and main components in the final version
if __name__ == "__main__":
    root=Tk()
    root.title("Fleur")
    something = mainFrame(root)
    root.mainloop()

