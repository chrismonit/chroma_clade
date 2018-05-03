from Tkinter import *
import tkFileDialog
import os.path

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
        self.save_file.set( os.path.split(filepath)[1] )

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

    def __str__(self):
        labels = ["tree_path", "tree_file", "align_path", "align_file", "save_path", "save_file",
                "colour_branches", "tree_format", "align_format", "save_format"
                ]
        values = [self.get_tree_path().get(), self.get_tree_file().get(), self.get_align_path().get(), self.get_align_file().get(), self.get_save_path().get(), self.get_save_file().get(),
                self.get_colour_branches().get(), self.get_tree_format().get(), self.get_align_format().get(), self.get_save_format().get()
                ]
        values = [str(v) for v in values]
        return "\n".join( ["%s:%s" % tup for tup in zip(labels, values)])

root = Tk()

gui = GuiInput()
root.title("ChromaClade")

WIDTH = 600.
HEIGHT = WIDTH*1.2 

root.geometry("%dx%d"%(round(WIDTH), round(HEIGHT)))
root.configure(background="gray")
#root.resizable(width=False, height=False) # are we sure about this?
# TODO may want to set a minimum size: https://stackoverflow.com/questions/10448882/how-do-i-set-a-minimum-window-size-in-tkinter

# TODO
# icon image
#root.wm_iconbitmap("icon_image_filename.ico")

# background image
#bg_image = PhotoImage(file="/Users/cmonit1/Desktop/coloured_trees/chroma_clade/pic/tmp.darwin.gif")
#image_lbl = Label(root, image=bg_image)
##image_lbl.pack() # dont mix pack and grid in same window


# ================ window layout ===============
f_title = Frame(root, height=HEIGHT*0.1, width=WIDTH*1.0, background="darkred")
f_input = Frame(root, height=HEIGHT*0.4, width=WIDTH*0.5, background="darkblue")
#f_left_input = Frame(f_input, background="darkorange")
#f_right_input = Frame(f_input, background="purple")
f_space = Frame(root, height=HEIGHT*0.1, width=WIDTH*1.0, background="yellow")
f_options = Frame(root, height=HEIGHT*0.3, width=WIDTH*1.0, background="darkgreen")
f_messages = Frame(root, height=HEIGHT*0.1, width=WIDTH*1.0, background="orange")

root.grid_rowconfigure(0, weight=1) 
root.grid_rowconfigure(1, weight=1) 
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

# place large frames on root grid
f_title.grid(column=0, row=0, sticky="nesw")
f_input.grid(column=0, row=1, sticky="nesw")
f_space.grid(column=0, row=2, sticky="nesw")
f_options.grid(column=0, row=3, sticky="nesw")
f_messages.grid(column=0, row=4, sticky="nesw")

propagate = False
f_title.grid_propagate(propagate)
f_input.grid_propagate(propagate)
f_space.grid_propagate(propagate)
f_options.grid_propagate(propagate)
f_messages.grid_propagate(propagate)

# ================ title ===============
f_title.grid_rowconfigure(0, weight=1)
f_title.grid_columnconfigure(0, weight=1)

l_title = Label(f_title, text="ChromaClade", background="red")
l_title.grid(column=0, row=0, sticky="nsew")

# ================ file input ===============
# two columns in f_input, for tree and alignment panels

for i in range(5):
    f_input.grid_rowconfigure(i, weight=1)
    for j in range(9):
        f_input.grid_columnconfigure(j, weight=1)

L_COL = 3
B_COL = L_COL + 1
F_COL = B_COL + 1

# CHOOSE TREE
l_tree = Label(f_input, text="Tree:", background="cyan")
l_tree.grid(column=L_COL, row=0, sticky="")

b_tree = Button(f_input, text="Choose file", command=gui.set_tree)
b_tree.grid(column=B_COL, row=0, sticky="")

l_tree_file = Label(f_input, textvariable=gui.get_tree_file(), background="cyan", width=GuiInput.MAX_FILE_LEN) # TODO initial text could be blank, then updated when file is selected
l_tree_file.grid(column=F_COL, row=0, sticky="")

# TREE FORMAT
l_tree_format = Label(f_input, text="Tree format:", background="cyan")
l_tree_format.grid(column=L_COL, row=1, sticky="")

o_tree_format = OptionMenu(f_input, gui.get_tree_format(), *gui.tree_choices) 
o_tree_format.grid(column=B_COL, row=1)

# column 2, row 1 is empty

# all row 2 is empty

# CHOOSE ALIGN
l_align = Label(f_input, text="Alignment:", background="cyan")
l_align.grid(column=L_COL, row=3, sticky="")

b_align = Button(f_input, text="Choose file", command=gui.set_align)
b_align.grid(column=B_COL, row=3)

# TODO could make text a different colour to make it clearer
l_align_file = Label(f_input, textvariable=gui.get_align_file(), background="cyan", width=GuiInput.MAX_FILE_LEN) # TODO initial text could be blank, then updated when file is selected
l_align_file.grid(column=F_COL, row=3, sticky="")

l_align_format = Label(f_input, text="Alignment format:", background="cyan")
l_align_format.grid(column=L_COL, row=4, sticky="")

o_align = OptionMenu(f_input, gui.get_align_format(), *gui.align_choices) 
o_align.grid(column=B_COL, row=4)

# ================ options ===============
for i in range(6):
    f_options.grid_rowconfigure(i, weight=1)
    for j in range(9):
        f_options.grid_columnconfigure(j, weight=1)

B_COL = 4
L_COL = B_COL + 1

#l_blank = Label(f_options, text="", background="pink")
#l_blank.grid(column=B_COL-1, row=0, sticky="ew")

cb_branches = Checkbutton(f_options, text="Colour branches", background="red", variable=gui.get_colour_branches())
cb_branches.grid(column=B_COL, row=0, sticky="")

# TODO choose range of sites, check button and text box
# rows 1 and 2

# output format
o_out_format = OptionMenu(f_options, gui.get_save_format(), *GuiInput.save_choices) 
o_out_format.grid(column=B_COL, row=3)

l_out_format = Label(f_options, text="Output file format", background="cyan")
l_out_format.grid(column=L_COL, row=3, sticky="")

# output file
b_outfile = Button(f_options, text="Save as", command=gui.set_save)
b_outfile.grid(column=B_COL, row=4, sticky="")

l_outfile = Label(f_options, text="Output file", background="cyan")
l_outfile.grid(column=L_COL, row=4, sticky="")

# go button
b_run = Button(f_options, text="Go")
b_run.grid(column=B_COL, row=5, sticky="")

# ================ messages ===============

f_messages.grid_columnconfigure(0, weight=1)
for i in range(1):
    f_messages.grid_rowconfigure(i, weight=1)

l_messages = Label(f_messages, text="[message]", background="firebrick")
l_messages.grid(column=0, row=0, sticky="news")



#event loop
root.mainloop()

print str(gui)

#print tree_var.get(),  align_var.get(),  colour_branches.get(),  out_format_var.get()
