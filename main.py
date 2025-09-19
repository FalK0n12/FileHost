from flask import Flask, request, render_template, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

fileDirectory = os.path.join(os.getcwd(), "files")
os.makedirs(fileDirectory, exist_ok=True)

backgrounds = ["02.jpg", "04.jpg", "23.jpg", "37.jpg"]

def get_current_background():
    current_hour = datetime.now().hour
    background_index = current_hour % len(backgrounds)
    return backgrounds[background_index]

@app.route("/")
def Index():
    items = os.listdir(fileDirectory)
    current_bg = get_current_background()
    return render_template('index.html', ITEMS=items, background=current_bg)

@app.route("/Upload", methods=["GET","POST"])
def Upload():
    current_bg = get_current_background()
    if request.method == "POST":
        if "File" not in request.files:
            return "No file part"
        file = request.files["File"]
        if file.filename == "":
            return "No selected file"
        items = os.listdir(fileDirectory)
        if file.filename in items:
            return render_template('index.html', ITEMS=items, ERROR="error", background=current_bg)
        filepath = os.path.join(fileDirectory, file.filename)
        file.save(filepath)
        items = os.listdir(fileDirectory)
        return render_template('index.html', ITEMS=items, filename=file.filename, background=current_bg)
    else:
        items = os.listdir(fileDirectory)
        return render_template('index.html', ITEMS=items, background=current_bg)
    
@app.route("/download/<fileName>")
def Download(fileName: str):
    filepath = os.path.join(fileDirectory, fileName)
    if os.path.exists(filepath):
        return send_from_directory(fileDirectory, fileName, as_attachment=True)
    else:
        return "No such file exists"

if __name__ == '__main__':
    app.run(debug=True)