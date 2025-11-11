from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)

app.secret_key = 'tu_clave_secreta_aqui'
API = ""https://pokeapi.co/api/v2/pokemon/"
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.route(debug=True)


@app.route('/pokemon',methodS =['POST'])
def search_pokemon():
    pokemon_name = request.form.get('pokemon')

if not pokemon_name:
    flash('por favor ingresa un nombre vlaido')
    return redirect(url_for('index'))


try: 


    resp = request.get(f"{API}{pokemon_name}")
    if resp.status_code == 200:
    pokemon_data = resp.json()
    return render_template('pokemon.html', pokemon)






