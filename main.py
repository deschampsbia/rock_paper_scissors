#importação e inicialização
from flask import Flask, render_template, request, redirect, url_for
from random import choice

# Criação da instância da aplicação Flask
app = Flask(__name__)

# Definição de variáveis
acoes_permitidas = ['pedra', 'papel', 'tesoura']  # Opções de movimentos permitidos
pontos = {'AI': 0, 'Usuario': 0}  # Dicionário para armazenar os pontos dos jogadores
rodadas = 0  # Contador de rodadas

# Rota principal (/)
@app.route('/', methods=['GET', 'POST'])
def index():
    global rodadas  # Permite modificar a variável global 'rodadas'
    
    # Lógica do jogo e processamento de formulário
    if request.method == 'POST':
        movimento_usuario = request.form['movimento']  # Movimento do usuário a partir do formulário
        movimento_ai = choice(acoes_permitidas)  # Movimento aleatório da AI

        # Lógica do jogo para determinar o resultado
        if movimento_usuario == movimento_ai:
            resultado = 'Empate!'  # Empate
        elif (movimento_ai == 'pedra' and movimento_usuario == 'tesoura') or \
             (movimento_ai == 'tesoura' and movimento_usuario == 'papel') or \
             (movimento_ai == 'papel' and movimento_usuario == 'pedra'):
            pontos['AI'] += 1  # Aumenta os pontos da AI
            resultado = 'AI ganhou!'  # Mensagem de vitória da AI
        else:
            pontos['Usuario'] += 1  # Aumenta os pontos do usuário
            resultado = 'Usuário ganhou!'  # Mensagem de vitória do usuário

        rodadas += 1  # Incrementa o contador de rodadas

        # Redirecionamento ou renderização do resultado
        if rodadas >= 3:
            return redirect(url_for('resultado'))  # Redireciona para a página de resultado após 3 rodadas

        # Renderiza a página principal com os resultados atuais
        return render_template('index.html', movimento_ai=movimento_ai, movimento_usuario=movimento_usuario, resultado=resultado, pontos=pontos)

    # Renderiza a página inicial se não houver um POST
    return render_template('index.html', pontos=pontos)

# Rota de resultado
@app.route('/resultado')
def resultado():
    # Renderiza a página de resultado final
    return render_template('resultado.html', pontos=pontos)

# Execução final da aplicação
if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor em modo de depuração