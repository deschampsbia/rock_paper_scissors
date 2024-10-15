from flask import Flask, render_template, request, redirect, url_for
from random import choice

app = Flask(__name__)

acoes_permitidas = ['pedra', 'papel', 'tesoura']
pontos = {'AI': 0, 'Usuario': 0}
rodadas = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global rodadas
    if request.method == 'POST':
        movimento_usuario = request.form['movimento']
        movimento_ai = choice(acoes_permitidas)

        # Lógica do jogo
        if movimento_usuario == movimento_ai:
            resultado = 'Empate!'
        elif (movimento_ai == 'pedra' and movimento_usuario == 'tesoura') or \
             (movimento_ai == 'tesoura' and movimento_usuario == 'papel') or \
             (movimento_ai == 'papel' and movimento_usuario == 'pedra'):
            pontos['AI'] += 1
            resultado = 'AI ganhou!'
        else:
            pontos['Usuario'] += 1
            resultado = 'Usuário ganhou!'

        rodadas += 1

        if rodadas >= 3:
            return redirect(url_for('resultado'))

        return render_template('index.html', movimento_ai=movimento_ai, movimento_usuario=movimento_usuario, resultado=resultado, pontos=pontos)

    return render_template('index.html', pontos=pontos)

@app.route('/resultado')
def resultado():
    return render_template('resultado.html', pontos=pontos)

if __name__ == '__main__':
    app.run(debug=True)
