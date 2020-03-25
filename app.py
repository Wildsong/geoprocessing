from flask import Flask
app = Flask(__name__)

# I could build up a little web site here
# and have each Python geoprocessing command
# run from a button click
# but I have not done that yet

@app.route("/")
def hello():
    print("Here be a console message.")
    return app.send_static_file("index.html")
