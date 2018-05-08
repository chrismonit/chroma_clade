from Tkinter import *
import tkFileDialog
import os.path
from check_input import Input, InputError
import chroma_clade

class GuiInput():
    
    MAX_FILE_LEN = 20
    tree_choices = ["Newick", "Nexus"]
    align_choices = ["Fasta", "Nexus"]
    save_choices = ["Figtree", "XML"]
    default_str = ""
    initial_directory = os.path.expanduser("~") # should be platform independent, home directory

    def __init__(self):
        self.colour_branches = BooleanVar()
        self.colour_branches.set(False)

        self.tree_file = StringVar() # for display only
        self.tree_file.set("") # keep label empty at first
        self.tree_path = StringVar()
        self.tree_path.set(GuiInput.default_str)

        self.tree_format = StringVar()
        self.tree_format.set(GuiInput.tree_choices[0])
        
        self.align_format = StringVar()
        self.align_format.set(GuiInput.align_choices[0])

        self.save_format = StringVar()
        self.save_format.set(GuiInput.save_choices[0])

        self.align_file = StringVar() # for display only
        self.align_file.set("") # keep label empty at first
        self.align_path = StringVar()
        self.align_path.set(GuiInput.default_str)

        self.save_path = StringVar()
        self.save_path.set(GuiInput.default_str)
        self.save_file = StringVar()
        self.save_file.set(GuiInput.default_str)
        
        self.message = StringVar()
        self.message.set("")

    def set_tree(self):
        filepath = tkFileDialog.askopenfilename(initialdir=GuiInput.initial_directory)
        self.tree_path.set(filepath)
        filename = os.path.split(filepath)[1]
        if len(filename) <= GuiInput.MAX_FILE_LEN:
            self.tree_file.set( filename )
        else:
            self.tree_file.set( filename[:GuiInput.MAX_FILE_LEN] + "..." )
    
    def set_align(self):
        filepath = tkFileDialog.askopenfilename(initialdir=GuiInput.initial_directory)
        self.align_path.set(filepath)
        filename = os.path.split(filepath)[1]
        if len(filename) <= GuiInput.MAX_FILE_LEN:
            self.align_file.set( filename )
        else:
            self.align_file.set( filename[:GuiInput.MAX_FILE_LEN] + "..." )


    def set_save(self):
        filepath = tkFileDialog.asksaveasfilename(initialdir=GuiInput.initial_directory)
        self.save_path.set(filepath)
        filename = os.path.split(filepath)[1]
        if len(filename) <= GuiInput.MAX_FILE_LEN:
            self.save_file.set( filename )
        else:
            self.save_file.set( filename[:GuiInput.MAX_FILE_LEN] + "..." )

    def set_message(self, value): self.message.set(value)

    def get_tree_format(self): return self.tree_format
    def get_align_format(self): return self.align_format
    def get_save_format(self): return self.save_format

    def get_tree_file(self): return self.tree_file
    def get_tree_path(self): return self.tree_path

    def get_align_file(self): return self.align_file
    def get_align_path(self): return self.align_path
    
    def get_colour_branches(self): return self.colour_branches

    def get_save_file(self): return self.save_file
    def get_save_path(self): return self.save_path
    
    def get_message(self): return self.message

    def __str__(self):
        labels = ["tree_path", "tree_file", "align_path", "align_file", "save_path", "save_file",
                "colour_branches", "tree_format", "align_format", "save_format", "message"
                ]
        values = [self.get_tree_path().get(), self.get_tree_file().get(), self.get_align_path().get(), self.get_align_file().get(), self.get_save_path().get(), self.get_save_file().get(),
                self.get_colour_branches().get(), self.get_tree_format().get(), self.get_align_format().get(), self.get_save_format().get(), self.get_message().get()
                ]
        values = [str(v) for v in values]
        return "\n".join( ["%s:%s" % tup for tup in zip(labels, values)])

    def get_input(self):
        values = [self.get_tree_path().get(), self.get_align_path().get(), self.get_colour_branches().get(), self.get_tree_format().get(), self.get_align_format().get(), self.get_save_path().get(), self.get_save_format().get(), None, None ]
        try: 
            return Input(*values)
        except InputError as e:
            self.message.set(str(e))
            return None

root = Tk()

gui = GuiInput()

def go():
    user_input = gui.get_input()
    if user_input == None: # invalid input provided, do not proceed. Error message will be updated by GuiInput
        return
    else:
        try:
            chroma_clade.run(user_input)
        except Exception as e:
            err_msg = "Oops an error occured, please check input options and try again"
            gui.set_message(err_msg)
            #print str(e) # debug only
        gui.set_message("Done!")

root.title("ChromaClade")

WIDTH = 600.
HEIGHT = WIDTH*1.2 

root.geometry("%dx%d"%(round(WIDTH), round(HEIGHT)))
root.configure(bg="gray")

# TODO
# icon image
#root.wm_iconbitmap("icon_image_filename.ico")

# ================ window layout ===============
f_title = Frame(root, height=HEIGHT*0.1, width=WIDTH*1.0, bg="darkred")
f_input = Frame(root, height=HEIGHT*0.4, width=WIDTH*0.5, bg="white") # nice pale cyan: 
f_image = Frame(root, height=HEIGHT*0.4, width=WIDTH*0.5, bg="white") # nice pale cyan: #9BFBFB
f_messages = Frame(root, height=HEIGHT*0.1, width=WIDTH*1.0, bg="orange")

root.grid_rowconfigure(0, weight=1) 
root.grid_rowconfigure(1, weight=1) 
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# place large frames on root grid
f_title.grid(column=0, row=0, sticky="nesw")
f_input.grid(column=0, row=1, sticky="nesw")
f_image.grid(column=0, row=2, sticky="nesw")
f_messages.grid(column=0, row=3, sticky="nesw")

propagate = False
f_title.grid_propagate(propagate)
f_input.grid_propagate(propagate)
f_image.grid_propagate(propagate)
f_messages.grid_propagate(propagate)

# ================ title ===============
f_title.grid_rowconfigure(0, weight=1)
f_title.grid_columnconfigure(0, weight=1)

l_title = Label(f_title, text="ChromaClade", bg="#9BFBFB")
l_title.grid(column=0, row=0, sticky="nsew")

# ================ file input ===============
# two columns in f_input, for tree and alignment panels

for i in range(13):
    f_input.grid_rowconfigure(i, weight=1)
    for j in range(9):
        f_input.grid_columnconfigure(j, weight=1)

#L, M, R = left, middle, right
L_COL = 3
M_COL = L_COL + 1
R_COL = M_COL + 1

L_BG = "white" # label background colour
L_FG = "blue" # label text colour for file choices

# CHOOSE TREE
l_tree = Label(f_input, text="Tree:", bg=L_BG)
l_tree.grid(column=L_COL, row=0, sticky="")

b_tree = Button(f_input, text="Choose file", command=gui.set_tree)
b_tree.grid(column=M_COL, row=0, sticky="")

l_tree_file = Label(f_input, textvariable=gui.get_tree_file(), fg=L_FG, bg=L_BG, width=GuiInput.MAX_FILE_LEN) # TODO initial text could be blank, then updated when file is selected
l_tree_file.grid(column=R_COL, row=0, sticky="")

# TREE FORMAT
l_tree_format = Label(f_input, text="Tree format:", bg=L_BG)
l_tree_format.grid(column=L_COL, row=1, sticky="")

o_tree_format = OptionMenu(f_input, gui.get_tree_format(), *gui.tree_choices) 
o_tree_format.grid(column=M_COL, row=1)

# column 2, row 1 is empty

# all row 2 is empty

# CHOOSE ALIGN
l_align = Label(f_input, text="Alignment:", bg=L_BG)
l_align.grid(column=L_COL, row=3, sticky="")

b_align = Button(f_input, text="Choose file", command=gui.set_align)
b_align.grid(column=M_COL, row=3)

l_align_file = Label(f_input, textvariable=gui.get_align_file(), fg=L_FG, bg=L_BG, width=GuiInput.MAX_FILE_LEN) # TODO initial text could be blank, then updated when file is selected
l_align_file.grid(column=R_COL, row=3, sticky="")

l_align_format = Label(f_input, text="Alignment format:", bg=L_BG)
l_align_format.grid(column=L_COL, row=4, sticky="")

o_align = OptionMenu(f_input, gui.get_align_format(), *gui.align_choices) 
o_align.grid(column=M_COL, row=4)

# ================ options ===============
# rows 5, 6, 7 blank

cb_branches = Checkbutton(f_input, text="Colour branches", bg="white", variable=gui.get_colour_branches())
cb_branches.grid(column=M_COL, row=8, sticky="")

# TODO choose range of sites, check button and text box
# rows 1 and 2

# output format
o_out_format = OptionMenu(f_input, gui.get_save_format(), *GuiInput.save_choices) 
o_out_format.grid(column=M_COL, row=11)

l_out_format = Label(f_input, text="Output file format:", bg=L_BG)
l_out_format.grid(column=L_COL, row=11, sticky="")

# output file
b_outfile = Button(f_input, text="Save as", command=gui.set_save)
b_outfile.grid(column=M_COL, row=12, sticky="")

l_outfile = Label(f_input, text="Output destination:", bg=L_BG)
l_outfile.grid(column=L_COL, row=12, sticky="")

l_outfile = Label(f_input, textvariable=gui.get_save_file(), fg=L_FG, bg=L_BG, width=GuiInput.MAX_FILE_LEN)
l_outfile.grid(column=R_COL, row=12, sticky="")

# go button
b_run = Button(f_input, text="Go", command=go)
b_run.grid(column=M_COL, row=13, sticky="")

# ================ image ===============
f_image.grid_rowconfigure(0, weight=1)
f_image.grid_columnconfigure(0, weight=1)
#
## background image
bg_image = PhotoImage(file="/Users/cmonit1/Desktop/coloured_trees/chroma_clade/pic/tree.gif")
l_image = Label(f_image, image=bg_image)
l_image.grid(column=0, row=0, sticky="nesw")

# ================ messages ===============

f_messages.grid_columnconfigure(0, weight=1)
for i in range(1):
    f_messages.grid_rowconfigure(i, weight=1)

l_messages = Label(f_messages, font=("Helvetica", 16), textvariable=gui.get_message(), bg="#9BFBFB")
l_messages.grid(column=0, row=0, sticky="news")


#event loop
root.mainloop()


#print tree_var.get(),  align_var.get(),  colour_branches.get(),  out_format_var.get()
