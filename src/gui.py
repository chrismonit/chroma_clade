from Tkinter import *
import tkFileDialog
import os.path

class GuiInput():

    tree_choices = ["Newick", "Nexus"]
    align_choices = ["Fasta", "Nexus"]
    save_choices = ["Figtree", "XML"]
    default_str = ""
    initial_directory = os.path.expanduser("~") # should be platform independent, home directory

    def __init__(self):
        self.colour_branches = BooleanVar()
        self.colour_branches.set(False)

        self.tree_file = StringVar()
        self.tree_file.set("") # keep label empty at first
        self.tree_path = StringVar()
        self.tree_path.set(GuiInput.default_str)

        self.tree_format = StringVar()
        self.tree_format.set(GuiInput.tree_choices[0])
        
        self.align_format = StringVar()
        self.align_format.set(GuiInput.align_choices[0])

        self.save_format = StringVar()
        self.save_format.set(GuiInput.save_choices[0])

        self.align_file = StringVar()
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
        self.tree_file.set( os.path.split(filepath)[1] )
    
    def set_align(self):
        filepath = tkFileDialog.askopenfilename(initialdir=GuiInput.initial_directory)
        self.align_path.set(filepath)
        self.align_file.set( os.path.split(filepath)[1] )

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

WIDTH = 500.
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
f_title = Frame(root, height=HEIGHT*0.2, width=WIDTH*1.0, background="darkred")
f_inputs = Frame(root, height=HEIGHT*0.4, width=WIDTH*0.5, background="darkblue")
#f_left_input = Frame(f_inputs, background="darkorange")
#f_right_input = Frame(f_inputs, background="purple")
f_options = Frame(root, height=HEIGHT*0.3, width=WIDTH*1.0, background="darkgreen")
f_messages = Frame(root, height=HEIGHT*0.1, width=WIDTH*1.0, background="orange")

root.grid_rowconfigure(0, weight=1) 
root.grid_rowconfigure(1, weight=1) 
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# place large frames on root grid
f_title.grid(column=0, row=0, sticky="nesw")
f_inputs.grid(column=0, row=1, sticky="nesw")
f_options.grid(column=0, row=2, sticky="nesw")
f_messages.grid(column=0, row=3, sticky="nesw")

propagate = False
f_title.grid_propagate(propagate)
f_inputs.grid_propagate(propagate)
f_options.grid_propagate(propagate)
f_messages.grid_propagate(propagate)

# ================ title ===============
f_title.grid_rowconfigure(0, weight=1)
f_title.grid_columnconfigure(0, weight=1)

l_title = Label(f_title, text="ChromaClade", background="red")
l_title.grid(column=0, row=0, sticky="nsew")

# ================ file input ===============
# two columns in f_inputs, for tree and alignment panels
f_inputs.grid_columnconfigure(0, weight=1)
f_inputs.grid_columnconfigure(1, weight=1)
f_inputs.grid_rowconfigure(0, weight=1)

# ==== left panel: choose tree =====
f_left_input = Frame(f_inputs, bg="orange", width=WIDTH*0.5, bd=1, relief=RAISED)
f_left_input.grid(column=0, row=0, sticky="nsew")

f_left_input.grid_columnconfigure(0, weight=1)

for i in range(9): # create lots of rows, so we can have some widgets closer together than others
    f_left_input.grid_rowconfigure(i, weight=1)

f_left_input.grid_propagate(propagate)

b_tree = Button(f_left_input, text="Choose tree", command=gui.set_tree)
b_tree.grid(column=0, row=2)

bl_left_input = Label(f_left_input, textvariable=gui.get_tree_file(), background="cyan") # TODO initial text could be blank, then updated when file is selected
bl_left_input.grid(column=0, row=3, sticky="")

o_tree = OptionMenu(f_left_input, gui.get_tree_format(), *gui.tree_choices) 
o_tree.grid(column=0, row=5)

ol_left_input = Label(f_left_input, text="Tree format", background="cyan")
ol_left_input.grid(column=0, row=6, sticky="")

# ==== right panel: choose alignment =====
f_right_input = Frame(f_inputs, bg="pink", width=WIDTH*0.5, bd=1, relief=RAISED)
f_right_input.grid(column=1, row=0, sticky="nsew")

f_right_input.grid_columnconfigure(0, weight=1)

for i in range(9): # create lots of rows, so we can have some widgets closer together than others
    f_right_input.grid_rowconfigure(i, weight=1)

f_right_input.grid_propagate(propagate)

b_align = Button(f_right_input, text="Choose alignment", command=gui.set_align)
b_align.grid(column=0, row=2)


bl_right_input = Label(f_right_input, textvariable=gui.get_align_file(), background="cyan") # TODO initial text could be blank, then updated when file is selected
bl_right_input.grid(column=0, row=3, sticky="")

o_align = OptionMenu(f_right_input, gui.get_align_format(), *gui.align_choices) 
o_align.grid(column=0, row=5)

ol_right_input = Label(f_right_input, text="Alignment format", background="cyan")
ol_right_input.grid(column=0, row=6, sticky="")

# ================ options ===============
for i in range(3):
    f_options.grid_columnconfigure(i, weight=1)
    f_options.grid_rowconfigure(i, weight=1)

cb_branches = Checkbutton(f_options, text="Colour branches", background="red", variable=gui.get_colour_branches())
cb_branches.grid(column=1, row=1)

# choose output file
b_outfile = Button(f_options, text="Save as", command=gui.set_save)
b_outfile.grid(column=0, row=0)

# output format label
#bl_outfile = Label(f_options, text="z", background="cyan")
#bl_outfile.grid(column=0, row=2, sticky="")

# output format
o_out_format = OptionMenu(f_options, gui.get_save_format(), *GuiInput.save_choices) 
o_out_format.grid(column=2, row=0)

# output format label
#ol_out_format = Label(f_options, text="Output format", background="cyan")
#ol_out_format.grid(column=0, row=4, sticky="")

# go button
b_run = Button(f_options, text="Go")
b_run.grid(column=1, row=2)

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
