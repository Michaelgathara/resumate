from flask import Flask, render_template, redirect

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return render_template("base.html")
 
# main driver function
if __name__ == '__main__':
    app.run(host = '0.0.0.0')
    