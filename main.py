from flask import Flask, render_template
import matplotlib.pyplot as plt
from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence
import random
import string
import json
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/gerados')
def gerados():
    cssgerado = "style1010.css"
    jssgerado = "script1010.js"
    audios = "audios/musica2.wav"
    return render_template('gerados/index.html', audios=audios,cssgerado=cssgerado,jssgerado=jssgerado)

@app.route('/acordes')
def acordes():
    files_to_extract_from = [
        '/home/c1158/Documentos/projeto_acordes/musica2.wav'
    ]

    timestamps = []
    acordes = []

    # Função para atualizar a linha do tempo
    def update_timeline(chord, timestamp):
        timestamps.append(timestamp)
        acordes.append(chord)

    def salva_acorde(results: LabelledChordSequence):
        for chord_change in results.sequence:
            chord = chord_change.chord
            timestamp = chord_change.timestamp

            #print(f"Acordes: {chord}, Tempo: {timestamp}")
            # chamamos a função para atualizar a linha do tempo
            update_timeline(chord, timestamp)

    chordino = Chordino()

    # Optionally clear cache of file conversions (e.g. wav files that have been converted from midi)
    clear_conversion_cache()

    # Run bulk extraction
    res = chordino.extract_many(files_to_extract_from, callback=salva_acorde, num_extractors=2,
                                num_preprocessors=2, max_files_in_cache=10, stop_on_error=False)

    acorde = []
    tempo = []
    # Desenhar a linha do tempo com os acordes
    for i in range(len(acordes)-1):
        chord = acordes[i]
        acorde.append(chord)
        timestamp = timestamps[i]
        next_timestamp = timestamps[i + 1]
        #calcula a duracao para milissigundos e arredonda para inteiro mais proximo com int(round(numero)) 
        tempo.append(int(round((next_timestamp - timestamp)*1000)))

    print(acorde, tempo)
    
    def gerar_nome_arquivo(): 
       caracteres = string.ascii_letters + string.digits 
       nome_arquivo = ''.join(random.choices(caracteres, k=10)) + '.js' 
       return nome_arquivo
     
    def criar_arquivo_js(nome_arquivo, codigo_js): 
        with open(nome_arquivo, 'w') as arquivo: 
            arquivo.write(codigo_js)
     
    acordes = json.dumps(acorde)
    duracao = json.dumps(tempo)
    # Exemplo de uso 
    codigo_exemplo = "\n const chords =" + acordes + "\n const duracao = " + duracao + ''' 
    const chordBox = document.getElementById('chord-box');
     
    function showChord(index) {
    chordBox.style.left = `${index * 50}px`; // Ajuste o valor do espaçamento conforme necessário
    chordBox.innerText = chords[index]; }
     
    function playTimeline() {
    let index = 0;

    function playNextChord() {
    showChord(index);
    index++;

    if (index >= chords.length) {
      clearInterval(interval);
      return;
    }

    interval = setTimeout(playNextChord, duracao[index]);  }

    playNextChord(); }
    playTimeline();
     
    playTimeline(); '''      
    nome_arquivo = gerar_nome_arquivo() 
    criar_arquivo_js(nome_arquivo, codigo_exemplo) 
    print(f'Arquivo JavaScript criado: {nome_arquivo   }') 

    
    return render_template('index.html')

#def teste():
#    return "teste"
#app.add_url_rule("/andre","teste",teste)



if __name__ == '__main__':
    app.run()
