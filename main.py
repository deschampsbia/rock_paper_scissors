from flask import Flask, render_template, request, redirect, url_for
from random import choice

app = Flask(__name__)

acoes_permitidas = ['pedra', 'papel', 'tesoura']
pontos = {'AI': 0, 'Usuario': 0}
rodadas = 0
vitoria_necessaria = 3  # Número de vitórias necessárias para reiniciar o jogo

@app.route('/', methods=['GET', 'POST'])
def index():
    global rodadas
    
    if request.method == 'POST':
        movimento_usuario = request.form['movimento']
        movimento_ai = choice(acoes_permitidas)

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
        
        # Verifica se algum jogador ganhou mais de 3 vezes
        if pontos['AI'] > vitoria_necessaria or pontos['Usuario'] > vitoria_necessaria:
            return redirect(url_for('resultado'))  # Redireciona para a página de resultado após a vitória

        if rodadas >= 3:
            return redirect(url_for('resultado'))

        return render_template('index.html', movimento_ai=movimento_ai, movimento_usuario=movimento_usuario, resultado=resultado, pontos=pontos)

    return render_template('index.html', pontos=pontos)

@app.route('/resultado')
def resultado():
    global pontos, rodadas
    resultado_final = ""
    
    # Verifica quem venceu
    if pontos['AI'] > pontos['Usuario']:
        resultado_final = "AI venceu o jogo!"
    elif pontos['Usuario'] > pontos['AI']:
        resultado_final = "Usuário venceu o jogo!"
    else:
        resultado_final = "O jogo terminou em empate!"

    # Reinicia os pontos e rodadas
    pontos = {'AI': 0, 'Usuario': 0}
    rodadas = 0

    return render_template('resultado.html', pontos=pontos, resultado_final=resultado_final)

if __name__ == '__main__':
    app.run(debug=True)