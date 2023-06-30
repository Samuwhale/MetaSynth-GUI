from flask import Flask, url_for, render_template, request, redirect
import polars as pl

from markupsafe import escape


app = Flask(__name__)
dataframe = None  # global variable to store our dataframe


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    global dataframe
    if request.method == 'POST':
        csv_file = request.files['file']
        dataframe = pl.read_csv(csv_file.stream)
        return redirect(url_for('view_dataframe'))
    return render_template('upload_csv.html')

@app.route('/dataframe')
def view_dataframe():
    global dataframe
    if dataframe is not None:
        return dataframe.to_pandas().to_html()
    else:
        return "No dataframe loaded"

if __name__ == '__main__':
    app.run(debug=True)