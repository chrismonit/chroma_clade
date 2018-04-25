from Tkinter import *

root = Tk()
root.title("My first window")

root.geometry("200x100")


app = Frame(root)
app.grid()

button1 = Button(app, text="This is button 1")
button1.grid()

button2 = Button(app)
button2.grid()
button2.configure(text="New text for button 2")

button3 = Button(app)
button3.grid()
button3["text"] = "Text for button 3"


#event loop
root.mainloop()



