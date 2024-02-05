from tkinter import *
import pandas
import random
from tkinter import messagebox
BACKGROUND_COLOR = "#B1DDC6"
### Count Down ###
timer = None
def countDown(count, translate):
    global timer
    timer = window.after(1000, countDown, count-1, translate)
    if count == 0:
        card.itemconfig(cardFace, image = backCardImage)
        card.itemconfig(wordText, fill = 'white')
        card.itemconfig(langText, fill = 'white')
        card.itemconfig(wordText, text = translate)
        card.itemconfig(langText, text = 'English')

### Word Generation ###
needToLearnCsv = pandas.read_csv('TkinterProjects\FlashCardProject\data\\NeedToLearn.csv')
needToLearnDict = pandas.DataFrame(needToLearnCsv).to_dict(orient='records')
word = ''
italianWord = ''
translation = ''
knownWords = []
   

def generateWords():
    global word
    global knownWords
    global needToLearnDict
    try:
        if type(needToLearnDict) != list:
            needToLearnCsv = pandas.read_csv('TkinterProjects\FlashCardProject\data\\NeedToLearn.csv')
            needToLearnDict = pandas.DataFrame(needToLearnCsv).to_dict(orient='records')
    except pandas.errors.EmptyDataError:
        reset()
        correct()
        messagebox.showinfo(title="Flashcards", message="Congrats!\nYou learned all the words")
    else:
        if type(knownWords) != list:
            kw = pandas.read_csv('TkinterProjects\FlashCardProject\data\\AlreadyKnow.csv')
            knownWords = pandas.DataFrame(kw).to_dict(orient='records')
        word = random.choice(needToLearnDict)
        try:         
            window.after_cancel((timer))
        except ValueError:
            pass
        card.itemconfig(cardFace, image = frontCardImage)
        card.itemconfig(wordText, fill = 'black')
        card.itemconfig(langText, fill = 'black')
        card.itemconfig(langText, text = 'Italian')
        italianWord = word['Italian']
        translation = word['English']
        card.itemconfig(wordText, text=italianWord)
        countDown(3, translation)

def correct():
    global knownWords
    global word, needToLearnDict
    knownWords.append(word)
    knownWords = pandas.DataFrame(knownWords).to_csv('TkinterProjects\FlashCardProject\data\AlreadyKnow.csv', index=False)
    needToLearnDict.remove(word)
    needToLearnDict = pandas.DataFrame(needToLearnDict).to_csv('TkinterProjects\FlashCardProject\data\\NeedToLearn.csv', index=False)
    generateWords()
    
def wrong():
    generateWords()

def reset():
    global needToLearnDict, knownWords
    needToLearnCsv = pandas.read_csv('TkinterProjects\FlashCardProject\data\ItalianToEnglishTranslations.csv')
    needToLearnDict = pandas.DataFrame(needToLearnCsv).to_dict(orient='records')
    knownWords = []
    knownWords = pandas.DataFrame(knownWords).to_csv('TkinterProjects\FlashCardProject\data\AlreadyKnow.csv', index=False)
    knownWords = []

### Creating the UI ###
# Window creation
window = Tk()
window.title('Flashcards')
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
frontCardImage = PhotoImage(file='TkinterProjects\FlashCardProject\images\card_front.png')
backCardImage = PhotoImage(file='TkinterProjects\FlashCardProject\images\card_back.png')
card = Canvas(width=800,height=528, highlightthickness=0, bg=BACKGROUND_COLOR)
cardFace = card.create_image(410,264,image = frontCardImage)
langText = card.create_text(400,150, text='Italian', font=('Ariel', 40, 'italic'))
wordText = card.create_text(400,263, text=italianWord, font=('Ariel', 60, 'bold'))
card.grid(row=0,column=0, columnspan=2)
generateWords()
# Button creation
checkImage = PhotoImage(file='TkinterProjects\FlashCardProject\images\\right.png')
xImage = PhotoImage(file='TkinterProjects\FlashCardProject\images\wrong.png')
resetImage = PhotoImage(file='TkinterProjects\FlashCardProject\images\\reset.png')
checkButton = Button(image = checkImage, highlightthickness=0, command=correct)
xButton = Button(image=xImage, highlightthickness=0, command=wrong)
checkButton.grid(row=1,column=1)
xButton.grid(row=1,column=0)
resetButton = Button(image = resetImage, highlightthickness=0, command=reset, bg=BACKGROUND_COLOR)
resetButton.grid(row=1,column=0,columnspan=2)
window.mainloop()
