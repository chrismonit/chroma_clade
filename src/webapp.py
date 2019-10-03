from flask import Flask, render_template, request, send_from_directory, current_app, redirect, flash, session
from werkzeug.utils import secure_filename
import os
import random
import uuid
from check_input import Input, InputError
import chroma_clade

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "write")
TREE_FOLDER = "tree"
ALIGNMENT_FOLDER = "align"
OUTPUT_FOLDER = "output"
ALIGNMENT_FILE_EXTENSIONS = ("txt", "nexus", "nex", "fasta", "fas", "fa")
TREE_FILE_EXTENSIONS = ("txt", "tre", "tree", "xml", "nex", "nexus", "new", "nwk", "newick")
MAX_FILE_SIZE_MB = 50
OUTPUT_FILE_PREIX = "col."
# identifier for option to make coloured trees for all sites. Declared here to avoid hard coding in html:
ALL_SITES_ID = "ALL_SITES"
UNIQUE_ID_LENGTH = 36  # == len(str(uuid.uuid4()))

app = Flask(__name__)

# TODO could be in config file
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["TREE_FOLDER"] = os.path.join(UPLOAD_FOLDER, TREE_FOLDER)
app.config["ALIGNMENT_FOLDER"] = os.path.join(UPLOAD_FOLDER, ALIGNMENT_FOLDER)
app.config["OUTPUT_FOLDER"] = os.path.join(UPLOAD_FOLDER, OUTPUT_FOLDER)
app.config["TREE_FILE_EXTENSIONS"] = TREE_FILE_EXTENSIONS
app.config["ALIGNMENT_FILE_EXTENSIONS"] = ALIGNMENT_FILE_EXTENSIONS
app.config["MAX_FILENAME_LENGTH"] = 255 - UNIQUE_ID_LENGTH  # apparently 255 chars is a common upper limit

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"  # TODO change!!!
# TODO we may need a privacy policy if using cookies


def save_file(input_file, destination, identifier, file_extensions, identifier_delimiter="."):
    if not input_file:
        raise ValueError("No file given")
    if not input_file.filename:
        raise ValueError("No filename given")
    if len(input_file.filename) > app.config["MAX_FILENAME_LENGTH"]:
        raise ValueError(f"Length of filename ({input_file.filename}) above max ({app.config['MAX_FILENAME_LENGTH']})")
    if not ('.' in input_file.filename and
            input_file.filename.rsplit('.', 1)[1].lower() in file_extensions):
        raise ValueError("Filename does not have acceptable file extension")
    saved_name = secure_filename(input_file.filename)  # ensure filename is not dangerous
    saved_name = f"{identifier}{identifier_delimiter}{saved_name}"
    if os.path.exists(os.path.join(destination, saved_name)):  # check it is unique
        raise ValueError("Same filename found on system")  # we're using UUID identifiers, so this shouldn't happen
    saved_path = os.path.join(destination, saved_name)
    input_file.save(saved_path)
    return saved_path  # return path so it can be accessed later


#  TODO include file names to send back to user?
# TODO should this stuff go in session object?
class FormData:
    TREE_IN_FORMATS = ("newick", "nexus")
    ALIGNMENT_IN_FORMATS = ("fasta", "nexus")
    TREE_OUT_FORMATS = ("figtree", "xml")
    DEFAULT_SITES_STRING = ""
    def __init__(self, branches=False, tree_in_format="newick", alignment_in_format="fasta", tree_out_format="figtree",
                 all_sites=True, sites_string=DEFAULT_SITES_STRING):

        # NB this is not for validating user input, just ensuring values provided are acceptable
        if tree_in_format not in FormData.TREE_IN_FORMATS:
            raise ValueError("Tree format not acceptable")
        if alignment_in_format not in FormData.ALIGNMENT_IN_FORMATS:
            raise ValueError("Alignment format not acceptable")
        if tree_out_format not in FormData.TREE_OUT_FORMATS:
            raise ValueError("Output format not acceptable")

        self.data = dict()
        self.data["branches"] = "checked" if branches else ""

        for tree_format in FormData.TREE_IN_FORMATS:
            self.data[f"tree_in_format_{tree_format}"] = "selected" if tree_in_format == tree_format else ""

        for alignment_format in FormData.ALIGNMENT_IN_FORMATS:
            self.data[f"alignment_format_{alignment_format}"] = "selected" if alignment_in_format == alignment_format else ""

        for out_format in FormData.TREE_OUT_FORMATS:
            self.data[f"tree_out_format_{out_format}"] = "selected" if tree_out_format == out_format else ""

        self.data["choose_sites_all"] = "checked" if all_sites else ""
        self.data["choose_sites_range"] = "checked" if not all_sites else ""
        self.data["sites_string"] = sites_string

    def get(self):
        return self.data

    def get_value(self, key):
        return self.data[key]


#  TODO apparent bug whereby on invalid form submission, options are returned to populate the form,
#  TODO but if user then corrects the problem and resubmits, the input is not accepted and the previous
#  TODO invalid options are returned
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            identifier = uuid.uuid4()
            print(identifier)
            print(request.form)
            branches = (request.form.get("branches") is not None)
            align_in_format = request.form["alignment_format"]
            tree_in_format = request.form["tree_format"]
            tree_out_format = request.form["output_format"]
            input_sites_string = request.form["sites_range"] if not request.form["choose_sites"] == ALL_SITES_ID else ""

            def format_file_error_message(file_type, max_len, file_extensions):
                ext_list = f"{', '.join('.'+ext for ext in file_extensions[:-1])} or .{file_extensions[-1]}"
                return f"Oops: Please ensure {file_type} file name is less than {max_len} characters and ends with {ext_list}"
            try:
                tree_file = request.files["tree_file"]
                tree_path = save_file(tree_file, app.config["TREE_FOLDER"], identifier, app.config["TREE_FILE_EXTENSIONS"])
            except ValueError:
                raise InputError(format_file_error_message("tree", app.config["MAX_FILENAME_LENGTH"], TREE_FILE_EXTENSIONS))
            try:
                alignment_file = request.files["alignment_file"]
                alignment_path = save_file(alignment_file, app.config["ALIGNMENT_FOLDER"], identifier, app.config["ALIGNMENT_FILE_EXTENSIONS"])
            except ValueError:
                raise InputError(format_file_error_message("alignment", app.config["MAX_FILENAME_LENGTH"], ALIGNMENT_FILE_EXTENSIONS))

            colour_file = os.path.join(os.path.dirname(__file__), Input.DEFAULT_COL_FILE)  # TODO allow user to upload one/pick colours

            out_name = os.path.basename(tree_path)
            out_name = OUTPUT_FILE_PREIX + out_name
            out_path = os.path.join(os.path.join(app.config["OUTPUT_FOLDER"], out_name))

            usr_input = Input(tree_path, alignment_path, branches, tree_in_format, align_in_format,
                              colour_file_path=colour_file, output_path=out_path, tree_out_format=tree_out_format,
                              sites_string=input_sites_string)
        except InputError as e:
            print(e)
            # TODO want to keep reference to uploaded files too if upload successful and they are validated
            flash(str(e), category="warning")
            submitted_data = FormData(
                branches=branches, alignment_in_format=align_in_format, tree_in_format=tree_in_format,
                tree_out_format=tree_out_format,
                sites_string=(FormData.DEFAULT_SITES_STRING if request.form["choose_sites"] == ALL_SITES_ID else request.form["sites_range"]),
                all_sites=(request.form["choose_sites"] == ALL_SITES_ID))
            return render_template("index.html", form=submitted_data.get())
        except Exception as e:
            print(e)  # could save message to a log file for bug checking in future?
            flash("Oops: Something went wrong, please check the options and try again", "warning")
            if os.path.exists(tree_path):  # remove any uploaded files to avoid cluttering
                os.remove(tree_path)
            if os.path.exists(alignment_path):
                os.remove(alignment_path)
            return render_template('index.html', form=FormData().get(), all_sites_id=ALL_SITES_ID)  # TODO inefficient if making new instance every time

        chroma_clade.run(usr_input)
        os.remove(tree_path)
        os.remove(alignment_path)

        return render_template("result.html", out_name=out_name)
    return render_template('index.html', form=FormData().get(), all_sites_id=ALL_SITES_ID)  # TODO inefficient if making new instance every time


@app.route('/result/<filename>')
def download(filename):

    out_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)
    # make the output file download and remove it from server;
    # https://stackoverflow.com/questions/40853201/remove-file-after-flask-serves-it

    # TODO this implementation does not work. Need to find a way to handle FileNotFoundError if
    # TODO users has already downloaded the file
    # TODO may be best to achieve this by changing the interface once download is clicked, ie with javascript
    def generate():
        with open(out_path) as f:
            yield from f
        os.remove(out_path)

    r = current_app.response_class(generate(), mimetype='text/csv')
    r.headers.set('Content-Disposition', 'attachment', filename=filename)
    return r


if __name__ == '__main__':
    import pytz
    from datetime import datetime
    london = pytz.timezone("Europe/London")

    try:
        app.run(port=8080) # may need to add host and port fields here, and remove debug setting for deployment
    except Exception as e:
        with open("log_web.txt", "a") as f:
            f.write(str(datetime.now(tz=timezone)), str(e))
            
