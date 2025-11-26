from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jose_memorama_123'  # pon la que quieras

IMAGES = [
    "static/aguacate.jpg",
    "static/almendra.jpg",
    "static/arandanos.jpg",
    "static/avena.jpg",
    "static/brocoli.jpg",
    "static/ensalada.jpg",
    "static/yougurt.jpg",
    "static/salmon.jpg"
]


def start_game():
    """Inicializa un nuevo juego en la sesión."""
    cards = IMAGES * 2  # duplicamos para hacer parejas
    random.shuffle(cards)

    session['cards'] = cards          # lista de imágenes mezcladas
    session['flipped'] = []           # índices de cartas volteadas (máx 2)
    session['matched'] = []           # índices de cartas ya acertadas
    session['matched_pairs'] = 0      # número de parejas acertadas


@app.route("/", methods=["GET", "POST"])
def memorama():

    if 'cards' not in session:
        start_game()

    # -----------------------------
    # MANEJO DE PETICIÓN POST
    # -----------------------------
    if request.method == "POST":
        action = request.form.get('action')

        if action == 'reset':
            start_game()
            return redirect(url_for('memorama'))

        # Se hizo clic en una carta
        index_str = request.form.get('card')
        if index_str is not None:
            try:
                index = int(index_str)
            except ValueError:
                return redirect(url_for('memorama'))

            cards = session.get('cards', [])
            flipped = session.get('flipped', [])
            matched = session.get('matched', [])
            matched_pairs = session.get('matched_pairs', 0)

            # Si ya había 2 volteadas sin resolver, las "volteamos boca abajo"
            if len(flipped) == 2:
                flipped = []

            # Si la carta no está ya volteada ni acertada, la volteamos
            if index not in flipped and index not in matched and 0 <= index < len(cards):
                flipped.append(index)

                # Si ahora hay 2 volteadas, revisamos si hacen pareja
                if len(flipped) == 2:
                    i, j = flipped
                    if cards[i] == cards[j]:
                        # Pareja acertada
                        matched.extend(flipped)
                        matched_pairs += 1
                        flipped = []  # Se vacía porque ya son permanentes

            session['flipped'] = flipped
            session['matched'] = matched
            session['matched_pairs'] = matched_pairs

        return redirect(url_for('memorama'))

    # -----------------------------
    # MANEJO GET: mostrar estado actual del juego
    # -----------------------------
    cards = session.get('cards', [])
    flipped = session.get('flipped', [])
    matched = session.get('matched', [])
    matched_pairs = session.get('matched_pairs', 0)
    total_pairs = len(cards) // 2 if cards else 0
    won = matched_pairs == total_pairs and total_pairs > 0

    # Construimos una lista con info para cada carta
    card_states = []
    for idx, img in enumerate(cards):
        visible = (idx in flipped) or (idx in matched)
        card_states.append({
            'index': idx,
            'img': img,
            'visible': visible,
            'matched': idx in matched
        })

    return render_template(
        "index.html",
        cards=card_states,
        matched_pairs=matched_pairs,
        total_pairs=total_pairs,
        won=won
    )


if __name__ == "__main__":
    app.run(debug=True)
