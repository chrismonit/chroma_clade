from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

import check_input


#  tree_path, align_path, branches, tree_in_format,
#             align_in_format, colour_file_path, output_path=None, tree_out_format=None,
#             sites_string=""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tree = request.form['tree_file']
        alignment = request.form['alignment_file']
        branches = request.form["branches"]
        align_in_format = request.form["alignment_format"]
        tree_in_format = request.form["tree_format"]

        tree_out_format = request.form["output_format"]
        choose_sites = request.form["choose_sites"]
        sites_range = request.form["sites_range"]
    # return render_template('index.html', items=shopping_list)
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)
