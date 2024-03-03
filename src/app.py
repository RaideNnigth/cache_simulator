from ast import List
from tkinter.messagebox import RETRY
from flask import Flask, render_template, url_for, request, jsonify, flash, redirect
# import the cache simulator
from cache_simulator import simulate_cache

from sim_cache.file_reader import read_file
from werkzeug.utils import secure_filename

import os

# Define the log file path
LOG_FILE = '.\\log.txt'

# Define the upload folder
UPLOAD_FOLDER = '..\\uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create the Flask app
app = Flask(__name__)

host = "0.0.0.0" # Change to your IP address


# Define the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Replace this with your own secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  

# Header table data
headings = ("Address", "Tag", "Index", "Hit/Miss")

# Cache table data
data = []

# Home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', headings=headings)


@app.route('/submit_cache', methods=['GET', 'POST'])
def submit_cache():
    if request.method == 'POST':

        # Check if any log file exists, if so delete it
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

        # Get the parameters from the form
        nsets = int(request.form['nsets'])
        bsize = int(request.form['bsize'])
        assoc = int(request.form['assoc'])
        subs_method = request.form['subs_method']
        output_flag = request.form['output_flag']

        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash('ERROR:: No file part, call admin!', 'error')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('ERROR:: No selected file, please select a .bin file', 'error')
            return redirect(request.url)

        if file:
            # Secure filename and save it to the upload folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Read the uploaded file
            try:
                file_data = read_file(file_path)
            except Exception as e:
                flash('ERROR:: Invalid file. Please try again.', 'error')
                return redirect(request.url)
            
            # Call the cache simulator with the file data
            try:
                simulate_cache(nsets, bsize, assoc, subs_method, output_flag, file_path)
            except Exception as e:
                flash('ERROR:: in cache simulation. Please try again. Error: ' + str(e), 'error')
                return redirect(request.url)

            # Flash success message
            flash('File Submited and ready to simulate', 'success')


            # Check if the log file exists
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r') as file:
                    # Get the last line from the log file
                    log_lines = file.readlines()
            else:
                flash('ERROR:: No Log file found. Please make sure to submit a file first.', 'error')
                return render_template('home.html', headings=headings, error="No Log file found. Please make sure to submit a file first.")

            # For each line in the log file, add it to the data list
            for line in log_lines:
                data.append(line.split(','))

            return redirect(request.url)
        else:
            flash('ERROR:: No file uploaded. Please try again.', 'error')
            return redirect(request.url)
    else:
        return render_template('home.html', headings=headings)

@app.route('/sim_cache', methods=['GET', 'POST'])
def sim_cache():
    if request.method == 'POST':
        # Return the home page with the data
        flash('Cache simulation successful!', 'success')
        return render_template('home.html', headings=headings)
    else:
        return render_template('home.html', headings=headings)
    
@app.route('/process_sim_cache', methods=['GET', 'POST'])
def process_sim_cache():
    global data
    if request.method == 'POST':
        if len(data) == 0:
            return jsonify({'success': False,
                    'data': data})
        
        # Return the home page with the data
        return jsonify({'success': True,
                    'data': data})
    else:
        return jsonify({'success': False,
                    'data': data})

@app.route('/process_clean_cache', methods=['GET', 'POST'])
def process_clean_cache():
    if request.method == 'POST':
        # Clear the data list
        data.clear()

        # Check if the log file exists
        if os.path.exists(LOG_FILE):
            # Delete the log file
            os.remove(LOG_FILE)

        # Return the home page with the data
        return jsonify({'success': True,
                    'data': data})
    else:
        return jsonify({'success': False,
                    'data': data})


@app.route('/clean_cache', methods=['GET', 'POST'])
def clean_cache():
    # Clear the data list
    data.clear()

    # Check if the log file exists
    if os.path.exists(LOG_FILE):
        # Delete the log file
        os.remove(LOG_FILE)

    # Return the home page with the data
    flash('Cache cleared!', 'success')
    return render_template('home.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run(debug=True, host=host)
