from Tkinter import *
import tkFileDialog
import os.path
from check_input import Input, InputError
import chroma_clade

# colour choices:
#https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/

class GuiInput():
    
    MAX_FILE_LEN = 20
    tree_choices = ["Newick", "Nexus"]
    align_choices = ["Fasta", "Nexus"]
    save_choices = ["Figtree", "XML"]
    default_str = ""
    initial_directory = os.path.expanduser("~") # should be platform independent, home directory
    EXAMPLE_SITES_STR = "e.g. 1-5, 8, 11-13"

    def __init__(self):
        self.colour_branches = BooleanVar()
        self.colour_branches.set(False)

        self.tree_file = StringVar() # for display only
        self.tree_file.set("(No file selected)") # keep label empty at first
        self.tree_path = StringVar()
        self.tree_path.set(GuiInput.default_str)

        self.tree_format = StringVar()
        self.tree_format.set(GuiInput.tree_choices[0])
        
        self.align_format = StringVar()
        self.align_format.set(GuiInput.align_choices[0])

        self.save_format = StringVar()
        self.save_format.set(GuiInput.save_choices[0])

        self.align_file = StringVar() # for display only
        self.align_file.set("(No file selected)") # keep label empty at first
        self.align_path = StringVar()
        self.align_path.set(GuiInput.default_str)

        self.save_path = StringVar()
        self.save_path.set(GuiInput.default_str)
        self.save_file = StringVar()
        self.save_file.set(GuiInput.default_str)
        
        self.all_sites = BooleanVar()
        self.all_sites.set(True)

        self.site_range_str = StringVar()
        self.site_range_str.set(GuiInput.EXAMPLE_SITES_STR)

        self.message = StringVar()
# get path for dir containing image files
        self.message.set("")
        
        # py2app saves data files in "<project>.app/Contents/Resources/", which is also where app's main file resides
        # therefore we can use the path to this file to get the path to the data files
        # this will work also for CLI version, since the data files reside in same dir as source code
        self.colour_file_path = os.path.join(os.path.split(__file__)[0], Input.DEFAULT_COL_FILE)

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
    
    def set_all_sites(self, value): self.all_sites.set(value)
    def set_site_range_str(self, value): self.site_range_str.set(value)

    def set_message(self, value): self.message.set(value)

    def set_colour_file_path(self, value): raise NotImplementedError("Haven't implemented optional colours!")

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
    
    def get_all_sites(self): return self.all_sites
    def get_site_range_str(self): return self.site_range_str

    def get_message(self): return self.message

    def get_colour_file_path(self): return self.colour_file_path

    def __str__(self):
        labels = ["tree_path", "tree_file", "align_path", "align_file", "save_path", "save_file",
                "colour_branches", "tree_format", "align_format", "save_format", "all_sites", 
                "site_range_str", "message", "colour_file_path"
                ]
        values = [self.get_tree_path().get(), self.get_tree_file().get(), self.get_align_path().get(), 
                self.get_align_file().get(), self.get_save_path().get(), self.get_save_file().get(),
                self.get_colour_branches().get(), self.get_tree_format().get(), self.get_align_format().get(), 
                self.get_save_format().get(), self.get_all_sites().get(), self.get_site_range_str().get(), 
                self.get_message().get(), self.get_colour_file_path()
                ]
        values = [str(v) for v in values]
        return "\n".join( ["%s:%s" % tup for tup in zip(labels, values)])

    def get_input(self):
        sites_str = None if self.get_all_sites().get() else self.get_site_range_str().get() 
        values = [self.get_tree_path().get(), self.get_align_path().get(), self.get_colour_branches().get(), 
                self.get_tree_format().get(), self.get_align_format().get(), self.get_colour_file_path(),
                self.get_save_path().get(), self.get_save_format().get(), sites_str]
        try: 
            return Input(*values)
        except InputError as e:
            self.message.set(str(e))
            return None

root = Tk()

gui = GuiInput()

def go():
    try:
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
    except Exception as e:
        gui.set_message("Oops: an unknown error occured, please check input files and try again.\nIf the problem persists, please contact the author.")


# assuming that the data/image files are in the same directory as this script
image_dir = os.path.split(__file__)[0]

root.title("ChromaClade")

WIDTH = 500.
HEIGHT = WIDTH*1.5 
#root.minsize(int(WIDTH), int(HEIGHT))
root.resizable(False, False)

root.geometry("%dx%d"%(round(WIDTH), round(HEIGHT)))
root.configure(bg="gray")

# TODO
# icon image
#root.wm_iconbitmap("icon_image_filename.ico")

# ================ window layout ===============
f_title = Frame(root, height=HEIGHT*0.1, width=WIDTH*1.0, bg="darkred")
f_input = Frame(root, height=HEIGHT*0.45, width=WIDTH*0.5, bg="white") # nice pale cyan: 
f_image = Frame(root, height=HEIGHT*0.35, width=WIDTH*0.5, bg="white") # nice pale cyan: #9BFBFB
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


title_image = PhotoImage(file=os.path.join(image_dir, "title.gif"))
l_title = Label(f_title, image=title_image, bg="cyan") # #9BFBFB
#l_title = Label(f_title, text="title", bg="cyan") # #9BFBFB
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
L_FG = "darkgray" # label text colour for file choices

# CHOOSE TREE
l_tree = Label(f_input, text="Tree:", bg=L_BG)
l_tree.grid(column=L_COL, row=0, sticky="")

b_tree = Button(f_input, text="Choose file", command=gui.set_tree)
b_tree.grid(column=M_COL, row=0, sticky="")

l_tree_file = Label(f_input, textvariable=gui.get_tree_file(), fg=L_FG, bg=L_BG, width=GuiInput.MAX_FILE_LEN)
l_tree_file.grid(column=R_COL, row=0, sticky="")

# TREE FORMAT
l_tree_format = Label(f_input, text="Tree format:", bg=L_BG)
l_tree_format.grid(column=L_COL, row=1, sticky="")

o_tree_format = OptionMenu(f_input, gui.get_tree_format(), *gui.tree_choices) 
o_tree_format.grid(column=M_COL, row=1)

# BLANK ROW
Label(f_input, text="").grid(column=M_COL, row=2, sticky="nesw")

# CHOOSE ALIGN
l_align = Label(f_input, text="Alignment:", bg=L_BG)
l_align.grid(column=L_COL, row=3, sticky="")

b_align = Button(f_input, text="Choose file", command=gui.set_align)
b_align.grid(column=M_COL, row=3)

l_align_file = Label(f_input, textvariable=gui.get_align_file(), fg=L_FG, bg=L_BG, width=GuiInput.MAX_FILE_LEN)
l_align_file.grid(column=R_COL, row=3, sticky="")

l_align_format = Label(f_input, text="Alignment format:", bg=L_BG)
l_align_format.grid(column=L_COL, row=4, sticky="")

o_align = OptionMenu(f_input, gui.get_align_format(), *gui.align_choices) 
o_align.grid(column=M_COL, row=4)

# ================ image ===============
f_image.grid_rowconfigure(0, weight=1)
f_image.grid_columnconfigure(0, weight=1)

plain_image = PhotoImage(file=os.path.join(image_dir, "tree.gif"))
col_image = PhotoImage(file=os.path.join(image_dir, "col.tree.gif"))
l_image = Label(f_image, image=plain_image)
l_image.grid(column=0, row=0, sticky="nesw")


# ================ options ===============

# BLANK ROW
Label(f_input, text="").grid(column=M_COL, row=5, sticky="nesw")

# COLOUR BRANCHES
def image_callback():
	if gui.get_colour_branches().get():
		l_image.configure(image=col_image)
	else:
		l_image.configure(image=plain_image)

cb_branches = Checkbutton(f_input, text="Colour branches", bg="white", command=image_callback, variable=gui.get_colour_branches())
cb_branches.grid(column=M_COL, row=6, sticky="w")

# BLANK ROW
Label(f_input, text="").grid(column=M_COL, row=7, sticky="nesw")

# CHOOSE ALIGNMENT SITES
e_sites = Entry(f_input, textvariable=gui.get_site_range_str(), state="disabled", fg="gray")
e_sites.grid(column=R_COL, row=9)

def clear_site_example(): # prepare for user entering text
    gui.set_site_range_str("")
    e_sites.focus() # take keyboard focus, meaning cursor will blink and text can be entered immediately
    e_sites.configure(state="normal", fg="black")

def restore_site_example():
    gui.set_site_range_str(GuiInput.EXAMPLE_SITES_STR)
    root.focus() # give keyboard focus to root widget, thereby removing focus from entry widget
    e_sites.configure(state="disabled", fg="gray")

r_all_sites = Radiobutton(f_input, text="All sites", variable=gui.get_all_sites(), value=True, command=restore_site_example)
r_all_sites.grid(column=M_COL, row=8, sticky="w")

r_range_sites = Radiobutton(f_input, text="Choose sites:", variable=gui.get_all_sites(), value=False, command=clear_site_example)
r_range_sites.grid(column=M_COL, row=9, sticky="w")

# BLANK ROW
Label(f_input, text="").grid(column=M_COL, row=10, sticky="nesw")

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


# ================ messages ===============

f_messages.grid_columnconfigure(0, weight=1)
for i in range(1):
    f_messages.grid_rowconfigure(i, weight=1)

l_messages = Label(f_messages, font=("Helvetica", 16), textvariable=gui.get_message(), bg="cyan") # #9BFBFB
l_messages.grid(column=0, row=0, sticky="news")


print "run main loop:"
#event loop
root.mainloop()
