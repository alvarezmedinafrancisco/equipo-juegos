from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/memorama')
def memorama():

    return render_template('memorama.html')

@app.route('/gato')
def gato():
  
    return render_template('gato.html')

if __name__ == '__main__':
    
    print("\n[INFO] Ejecutando Flask en modo simple. http://127.0.0.1:5000/memorama\n")
    app.run(debug=True)