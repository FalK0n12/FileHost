from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)

fileDirectory = os.path.join(os.getcwd(), "files")
os.makedirs(fileDirectory, exist_ok=True)

@app.route("/")
def Index():
    items = os.listdir(fileDirectory)
    return render_template('index.html', ITEMS=items)

@app.route("/Upload", methods=["GET","POST"])
def Upload():
    if request.method == "POST":
        if "File" not in request.files:
            return "No file part"
        file = request.files["File"]
        if file.filename == "":
            return "No selected file"

        # save the file
        filepath = os.path.join(fileDirectory, file.filename)
        file.save(filepath)
        return f"File saved at {filepath}"
    else:
        return render_template('index.html')
    
@app.route("/Download/<fileName>")
def Download(fileName: str):
    filepath = os.path.join(fileDirectory, fileName)
    if os.path.exists(filepath):
        return send_from_directory(fileDirectory, fileName, as_attachment=True)
    else:
        return "No such file exists"

if __name__ == '__main__':
    app.run(debug=True)