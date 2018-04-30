from Tkinter import *
import tkFileDialog

root = Tk()
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


# define frames which determine layout
f_title = Frame(root, height=HEIGHT*0.2, width=WIDTH*1.0, background="darkred")
f_inputs = Frame(root, height=HEIGHT*0.4, width=WIDTH*0.5, background="darkblue")
#f_left_input = Frame(f_inputs, background="darkorange")
#f_right_input = Frame(f_inputs, background="purple")
f_options = Frame(root, height=HEIGHT*0.2, width=WIDTH*1.0, background="darkgreen")
f_messages = Frame(root, height=HEIGHT*0.2, width=WIDTH*1.0, background="orange")

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

# make title
f_title.grid_rowconfigure(0, weight=1)
f_title.grid_columnconfigure(0, weight=1)

l_title = Label(f_title, text="ChromaClade", background="red")
l_title.grid(column=0, row=0, sticky="nsew")

#make input panels

# two columns in f_inputs
f_inputs.grid_columnconfigure(0, weight=1)
f_inputs.grid_columnconfigure(1, weight=1)
f_inputs.grid_rowconfigure(0, weight=1)

#f_inputs.grid_rowconfigure(0, weight=1)
#f_inputs.grid_columnconfigure(0, weight=1)
#f_inputs.grid_columnconfigure(1, weight=1)

f_left_input = Frame(f_inputs, bg="orange", width=WIDTH*0.5, bd=1, relief=RAISED)
f_left_input.grid(column=0, row=0, sticky="nsew")

f_left_input.grid_columnconfigure(0, weight=1)

for i in range(9): # create lots of rows, so we can have some widgets closer together than others
    f_left_input.grid_rowconfigure(i, weight=1)

f_right_input = Frame(f_inputs, bg="pink", width=WIDTH*0.5, bd=1, relief=RAISED)
f_right_input.grid(column=1, row=0, sticky="nsew")

f_right_input.grid_columnconfigure(0, weight=1)
f_right_input.grid_rowconfigure(0, weight=1)

f_left_input.grid_propagate(propagate)
f_right_input.grid_propagate(propagate)

# left widgets
b_tree = Button(f_left_input, text="Choose tree")
b_tree.grid(column=0, row=2)

bl_left_input = Label(f_left_input, text="x", background="cyan") # TODO initial text could be blank, then updated when file is selected
bl_left_input.grid(column=0, row=3, sticky="")

tree_var = StringVar(f_left_input)
tree_choices = ["Newick", "Nexus"]
tree_var.set(tree_choices[0])
o_tree = OptionMenu(f_left_input, tree_var, *tree_choices) 
o_tree.grid(column=0, row=5)

ol_left_input = Label(f_left_input, text="Tree format", background="cyan")
ol_left_input.grid(column=0, row=6, sticky="")

# right widgets
l_right_input = Label(f_right_input, text="rrrrrrrrrrrrrrr", background="cyan")
l_right_input.grid(column=0, row=0, sticky="ns")


# populate frames

#def choose_file(f):
#    f = tkFileDialog.askopenfilename()

# title
#title_colour = "red"
#f_title2 = Frame(f_title, height=HEIGHT*0.2, width=WIDTH*1.0, background=title_colour)
#f_title2.grid()
#
#l_title = Label(f_title, text="ChromaClade", background=title_colour )
#l_title.grid(column=0, row=0, sticky="nesw")
#
## left panel # height=HEIGHT*0.4, width=WIDTH*0.5, 
#f_left_input2 = Frame(f_left_input, background="yellow")
#f_left_input2.grid(column=0, row=0, sticky="ns")
#f_left_input2.columnconfigure(0, weight=10)
#
##f_left_input.columnconfigure(0, weight=100)
#
#b_tree = Button(f_left_input, text="Choose tree")
#b_tree.grid(column=0, row=0)
#
#l_tree = Label(f_left_input, text="[tree file text]")
#l_tree.grid(column=0, row=1)
#
#tree_var = StringVar(f_left_input)
#tree_choices = ["Newick", "Nexus"] # TODO get full list of acceptable file types
#tree_var.set(tree_choices[0])
#o_tree = OptionMenu(f_left_input, tree_var, *tree_choices) 
#o_tree.grid(column=0, row=2)
#
#
## right panel
#f_right_input2 = Frame(f_right_input, height=HEIGHT*0.4, width=WIDTH*0.5, background="cyan")
#f_right_input2.grid(column=0, row=0)
#
#b_align = Button(f_right_input, text="Choose alignment")
#b_align.grid(column=0, row=0)
#
#l_align = Label(f_right_input, text="[align file text]")
#l_align.grid(column=0, row=1)
#
#align_var = StringVar(f_right_input)
#align_choices = ["Fasta", "Nexus"] # TODO get full list of acceptable file types
#align_var.set(align_choices[0])
#o_align = OptionMenu(f_right_input, align_var, *align_choices) 
#o_align.grid(column=0, row=2)
#
#

# lower panel




#event loop
root.mainloop()



