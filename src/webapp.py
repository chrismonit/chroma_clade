from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from check_input import Input
import random

UPLOAD_FOLDER = '/path/to/the/uploads'
ALIGNMENT_FILE_EXTENSIONS = {'txt', 'nex', 'fasta', 'fas', 'fa'}
TREE_FILE_EXTENSIONS = {'txt', 'tre', 'tree', 'xml', 'nex', 'nexus', 'new', 'newick'}

app = Flask(__name__)

# TODO could be in config file
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALIGNMENT_FILE_EXTENSIONS'] = ALIGNMENT_FILE_EXTENSIONS
app.config['TREE_FILE_EXTENSIONS'] = TREE_FILE_EXTENSIONS


# TODO may be unclear what the output file name should be
# TODO enforce max file size
def save_file(input_file, file_extensions):
    if not input_file:
        raise ValueError("No file name given")
    if not ('.' in input_file.filename and \
            input_file.filename.rsplit('.', 1)[1].lower() in file_extensions):
        raise ValueError("Filename does not have acceptable file extension")

    save_path = secure_filename(input_file.filename)  # ensure filename is not dangerous
    if os.path.exists(app.config['UPLOAD_FOLDER'], save_path):  # if a file with this name already exists in tmp storage
        save_path = "-".join([str(random.randint(0, 1000)), save_path])  # make name unique
        if os.path.exists(app.config['UPLOAD_FOLDER'], save_path):  # check it actually is unique
            raise ValueError(
                "Same filename found on system")  # very unlikely to happen by chance, possible security issue
    input_file.save(save_path)
    return save_path  # return path so it can be accessed later


# TODO could have separate function for after job has finished?
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tree_file = request.files["tree_file"]
        tree_path = save_file(tree_file)
        alignment_file = request.files["alignment_file"]
        alignment_path = save_file(alignment_file)


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

        usr_input = Input(tree_path, alignment_path, branches, tree_in_format, align_in_format,
                          colour_file_path=colour_file, tree_out_format=tree_out_format, sites_string=sites_string)
    # return render_template('index.html', items=shopping_list)
    return render_template('index.html')  # TODO update page content to show job has finished


if __name__ == '__main__':
    app.run(debug=True)
