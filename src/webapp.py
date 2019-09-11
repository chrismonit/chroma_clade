from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from check_input import Input, InputError
import random
import chroma_clade

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "storage")
ALIGNMENT_FILE_EXTENSIONS = {"txt", "nex", "fasta", "fas", "fa"}
TREE_FILE_EXTENSIONS = {"txt", "tre", "tree", "xml", "nex", "nexus", "new", "newick"}
MAX_FILE_SIZE_MB = 50
OUTPUT_FILE_PREIX = "col."

app = Flask(__name__)

# TODO could be in config file
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALIGNMENT_FILE_EXTENSIONS"] = ALIGNMENT_FILE_EXTENSIONS
app.config["TREE_FILE_EXTENSIONS"] = TREE_FILE_EXTENSIONS
app.config["MAX_FILENAME_LENGTH"] = 200  # apparently 255 chars is a common upper limit

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024


def save_file(input_file, file_extensions):
    if not input_file:
        raise ValueError("No file given")
    if not input_file.filename:
        raise ValueError("No filename given")
    if len(input_file.filename) > app.config["MAX_FILENAME_LENGTH"]:
        raise ValueError(f"Length of filename ({input_file.filename}) above max ({app.config['MAX_FILENAME_LENGTH']})")
    if not ('.' in input_file.filename and \
            input_file.filename.rsplit('.', 1)[1].lower() in file_extensions):
        raise ValueError("Filename does not have acceptable file extension")

    saved_name = secure_filename(input_file.filename)  # ensure filename is not dangerous
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], saved_name)):  # if a file with this name already exists in tmp storage
        saved_name = "-".join([str(random.randint(0, 10000)), saved_name])  # make name unique # TODO use UUID instead?
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], saved_name)):  # check it actually is unique
            raise ValueError(
                "Same filename found on system")  # very unlikely to happen by chance, possible security issue
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_name)
    input_file.save(saved_path)
    return saved_path  # return path so it can be accessed later


# TODO could have separate function for after job has finished?
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # TODO may want to have seperate destinations for alignments, trees and coloured trees for clarity

        tree_file = request.files["tree_file"]
        tree_path = save_file(tree_file, app.config["TREE_FILE_EXTENSIONS"])
        alignment_file = request.files["alignment_file"]
        alignment_path = save_file(alignment_file, app.config["ALIGNMENT_FILE_EXTENSIONS"])


        branches = (request.form.get("branches") is not None)
        align_in_format = request.form["alignment_format"]
        tree_in_format = request.form["tree_format"]
        tree_out_format = request.form["output_format"]
        sites_string = request.form["sites_range"] if request.form["choose_sites"] else ""

        # print("tree", tree)
        # print("alignment", alignment)
        print("branches", branches)
        print("align_in_format", align_in_format)
        print("tree_in_format", tree_in_format)
        print("tree_out_format", tree_out_format)
        print("sites_range", sites_string)

        colour_file = os.path.join(os.path.dirname(__file__), Input.DEFAULT_COL_FILE)

        out_dir, out_name = os.path.split(tree_path)
        out_name = OUTPUT_FILE_PREIX + out_name
        out_path = os.path.join(os.path.join(out_dir, out_name))
        print(tree_path)

        try:
            usr_input = Input(tree_path, alignment_path, branches, tree_in_format, align_in_format,
                              colour_file_path=colour_file, output_path=out_path, tree_out_format=tree_out_format,
                              sites_string=sites_string)
        except InputError as e:
            pass  # TODO
        chroma_clade.run(usr_input)
        return send_from_directory(app.config["UPLOAD_FOLDER"], out_name, as_attachment=True)

        # TODO remove files from storage
        # TODO clear form
    # return render_template('index.html', items=shopping_list)
    return render_template('index.html')  # TODO update page content to show job has finished

# TODO must clear files at some point
if __name__ == '__main__':
    app.run(debug=True)
