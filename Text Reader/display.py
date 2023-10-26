import tkinter as tk
from tkinter import Text, messagebox
import pyttsx3
from googletrans import Translator
from tkinter.ttk import Combobox, Separator
import sqlite3



"""MODEL"""
def Create_Table():
    connection = sqlite3.connect('TEXT_READER')
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS Text(Text_ID INTEGER PRIMARY KEY AUTOINCREMENT, Text_Block TEXT, Text_Name TEXT)')
        connection.commit()
    except:
        messagebox.showerror('Error', 'It was an error: Table did not created')


def Save_Text():
    connection = sqlite3.connect('TEXT_READER')
    cursor = connection.cursor()

    text_name = save_name()

    if text_name == '':
        messagebox.showwarning('Text Name', 'Text name field have not be empty')
    else: 
        text_name_exists = cursor.execute('SELECT * FROM Text WHERE Text_Name = ?', (text_name,)).fetchone()
        if text_name_exists is not None:
            messagebox.showwarning('Save Text', 'The current Text name is already in use, use another Text name please.')
        else:
            cursor.execute('INSERT INTO Text(Text_Block, Text_Name) VALUES(?, ?)', (save_text(), save_name()))
            messagebox.showinfo('Save Text', 'Text saved succesfully!')

    connection.commit()
    connection.close()

    reload_text_list()

def Select_Text_Names():
    connection = sqlite3.connect('TEXT_READER')
    cursor = connection.cursor()
    Create_Table()

    cursor.execute('SELECT Text_Name FROM Text')
    text_names_tuples = cursor.fetchall()

    text_names = [name_tuple[0] for name_tuple in text_names_tuples]

    connection.commit()
    connection.close()
    
    return text_names


def Select_Text():
    connection = sqlite3.connect('TEXT_READER')
    cursor = connection.cursor()

    selected_text_name = texts_list.get()

    cursor.execute('SELECT Text_Block FROM Text WHERE Text_Name = ?', (selected_text_name,))
    text_block_tuple = cursor.fetchone()

    connection.commit()
    connection.close()

    if text_block_tuple:
        text_block = text_block_tuple[0]
        return text_block
    else:
        return ''

    return text_block





"""VIEW"""
root = tk.Tk()
root.iconbitmap('C:/Users/raven/OneDrive/Escritorio/PYTHON/MY PROJECTS/Text Reader/images/microphone.ico')
root.title('READEXT')
root.geometry('1360x690+0+0')
root.config(bg = "LightSkyBlue")
root.resizable(0, 0)

Create_Table()


#Frames
base_frame = tk.Frame(root, bg = "Gray30", width = 1260, height = 690)
base_frame.place(x = 50, y = 50)

menu_frame = tk.Frame(root, bg = 'Gray20', width = 1360, height = 50)
menu_frame.place(x = 0, y = 0)

#Labels
shell_label = tk.Label(base_frame, bg = 'Snow', width = 171, height = 40)
shell_label.place(x = 25, y = 15)

load_text_label = tk.Label(menu_frame, text = 'Load text:', font = ('Times', '12', 'bold'), bg = 'Gray20', fg = 'Snow')
load_text_label.place(x = 680, y = 0)

text_name_entry_label = tk.Label(menu_frame, text = 'Text name:', font = ('Times', '12', 'bold'), bg = "Gray20", fg = 'Snow')
text_name_entry_label.place(x = 890, y = 0)

select_language_label = tk.Label(menu_frame, text = 'Select language:', font = ('Times', '12', 'bold'), bg = 'Gray20', fg = "Snow")
select_language_label.place(x = 1100, y = 0)

font_size_label = tk.Label(menu_frame, text = 'Font size:', font = ('Times', '12', 'bold'), bg = 'Gray20', fg = 'Snow')
font_size_label.place(x = 370, y = 0)

#Write Shell
write_shell = tk.Text(base_frame, bg = "Snow", width = 140, height = 30, font = ('Times', '12', 'bold'))
write_shell.place(x = 65, y = 25)

#Methods
def translate_text():
    text_block = write_shell.get('1.0', 'end')
    translator = Translator()

    language_to_translate = translation_languages_list.get()
    if language_to_translate == 'English':
        traduction = translator.translate(text_block, dest='en').text
    elif language_to_translate == 'Spanish':
        traduction = translator.translate(text_block, dest='es').text
    elif language_to_translate == 'Francais':
        traduction = translator.translate(text_block, dest='fr').text
    elif language_to_translate == 'Rusian':
        traduction = translator.translate(text_block, dest='ru').text
    else:
        traduction = translator.translate(text_block, dest='es').text

    return traduction

def read_text():
    text_block = translate_text()
    engine = pyttsx3.init()
    engine.say(text_block)
    engine.runAndWait()
    print(text_block)

def save_name():
    text_name = text_name_entry.get()
    return text_name

def save_text():
    text_block = translate_text()
    return text_block
        
def open_text():    
    clean_shell()
    text_block = Select_Text()    
    write_shell.insert(tk.END, text_block)

def clean_shell():
    write_shell.delete('1.0', 'end')

def update_traducted_text():
    text_block = write_shell.get('1.0', 'end')
    translator = Translator()

    language_to_translate = translation_languages_list.get()
    if language_to_translate == 'English':
        traduction = translator.translate(text_block, dest='en').text
    elif language_to_translate == 'Spanish':
        traduction = translator.translate(text_block, dest='es').text
    elif language_to_translate == 'Francais':
        traduction = translator.translate(text_block, dest='fr').text
    elif language_to_translate == 'Rusian':
        traduction = translator.translate(text_block, dest='ru').text
    else:
        traduction = translator.translate(text_block, dest='es').text
    
    write_shell.delete('1.0', 'end')

    write_shell.insert(tk.END, traduction)

def reload_text_list():
    texts_list = Combobox(menu_frame, values = Select_Text_Names())
    texts_list.place(x = 680, y = 20)

def update_font_size():
    text_block = write_shell.get('1.0', 'end')

    if font_size_list.get() == 'Small':
        write_shell.config(font = ('Times', '8', 'bold'), width = 187, height = 44)
    elif font_size_list.get() == 'Medium':
        write_shell.config(font = ('Times', '12', 'bold'), width = 140, height = 30)
    elif font_size_list.get() == 'Large':
        write_shell.config(font = ('Times', '22', 'bold'), width = 75, height = 18)
    else:
        write_shell.config(font = ('Times', '12', 'bold'), width = 140, height = 30)
    
    write_shell.delete('1.0', 'end')
    write_shell.insert(tk.END, text_block)




#Images
read_image = tk.PhotoImage(file='C:/Users/raven/OneDrive/Escritorio/PYTHON/MY PROJECTS/Text Reader/images/read.png')
save_image = tk.PhotoImage(file='C:/Users/raven/OneDrive/Escritorio/PYTHON/MY PROJECTS/Text Reader/images/save.png')
open_image = tk.PhotoImage(file='C:/Users/raven/OneDrive/Escritorio/PYTHON/MY PROJECTS/Text Reader/images/open.png')
clean_image = tk.PhotoImage(file='C:/Users/raven/OneDrive/Escritorio/PYTHON/MY PROJECTS/Text Reader/images/clean.png')
traduct_image = tk.PhotoImage(file='C:/Users/raven/OneDrive/Escritorio/PYTHON/MY PROJECTS/Text Reader/images/traduct.png')
font_image = tk.PhotoImage(file='C:/Users/raven/OneDrive/Escritorio/PYTHON/MY PROJECTS/Text Reader/images/font.png')

#Buttons
read_button = tk.Button(menu_frame, bg = "Gray30", image = read_image, width = 30, height = 31, command = lambda: read_text())
read_button.place(x = 1060, y = 5)

save_text_button = tk.Button(menu_frame, bg = 'Gray30', image = save_image, width = 30, height = 31, command = lambda: Save_Text())
save_text_button.place(x = 850, y = 5)

open_text_button = tk.Button(menu_frame, bg = 'Gray30', image = open_image, width = 30, height = 31, command = lambda: open_text())
open_text_button.place(x = 640, y = 5)

clean_text_button = tk.Button(menu_frame, bg = 'Gray30', image = clean_image, width = 30, height = 31, command = lambda: clean_shell())
clean_text_button.place(x = 590, y = 5)

traduction_button = tk.Button(menu_frame, bg = 'Gray30', image = traduct_image, width = 30, height = 31, command = lambda: update_traducted_text())
traduction_button.place(x = 540, y = 5)

font_button = tk.Button(menu_frame, bg = 'Gray30', image = font_image, width = 30, height = 31, command = lambda: update_font_size())
font_button.place(x = 330, y = 5)

#Separators
horizontal_line_1 = Separator(menu_frame, orient = 'vertical', style = 'TSeparator', takefocus = 1, cursor = 'man').grid(row = 1, column = 1, ipady = 22, padx = 300, pady = 0)

horizontal_line_2 = Separator(menu_frame, orient = 'vertical', style = 'TSeparator', takefocus = 1, cursor = 'man').grid(row = 1, column = 2, ipady = 22, padx = 230, pady = 0)

horizontal_line_3 = Separator(menu_frame, orient = 'vertical', style = 'TSeparator', takefocus = 1, cursor = 'man').grid(row = 1, column = 3, ipady = 22, padx = 350, pady = 0)

#Entrys
text_name_entry = tk.Entry(menu_frame, font = ('Times', '10', 'bold'))
text_name_entry.place(x = 890, y = 20)

#Lists
translation_languages_list = Combobox(menu_frame, values = ['English', 'Spanish', 'Francais', 'Rusian'])
translation_languages_list.place(x = 1100, y = 20)

texts_list = Combobox(menu_frame, values = Select_Text_Names())
texts_list.place(x = 680, y = 20)

font_size_list = Combobox(menu_frame, values = ['Small', 'Medium', 'Large'])
font_size_list.place(x = 370, y = 20)


root.mainloop()