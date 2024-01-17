from tkinter import *
import matplotlib

root = Tk()
# Grid system, to anchor to parts of the grid
Label(root, text="Hello World!").grid(row=0, column=0)
Label(root, text="My name is newton long").grid(row=1, column=5)

root.mainloop()


