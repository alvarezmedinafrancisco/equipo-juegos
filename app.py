from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def memorama():

    images = [
        "static/aguacate.jpg",
        "static/almendra.jpg", 
        "static/arandanos.jpg",  
        "static/avena.jpg", 
        "static/brocoli.jpg",  
        "static/ensalada.jpg",  
        "static/yougurt.jpg",  
        "static/salmon.jpg"    
    ]

    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)
