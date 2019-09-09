from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

import check_input

@app.route('/', methods=['GET', 'POST'])
def index():
    global shopping_list
    if request.method == 'POST':
        shopping_list.append(request.form['item'])
    return render_template('index.html', items=shopping_list)


if __name__=='__main__':
    app.run(debug=True)
