#xkcd API Teste
import os
from bottle import request, template, route, run
import requests
from random import randint

#Seleciona o número da história mais recente
id_ultima_historia = int(requests.get('https://xkcd.com/info.0.json').json().get("num"))

#Seleciona o ano da história mais recente & cria uma lista de anos de 2006 até esse último ano
ultimo_ano = int(requests.get('https://xkcd.com/info.0.json').json().get("year"))
todos_os_anos = [n for n in range(2006, ultimo_ano+1)]
todos_os_anos.reverse()

#Lista da primeira história de cada ano
lista_primeira_historia_ano = [[2006, 1], [2007, 204], [2008, 365], [2009, 525], [2010, 683], [2011, 842], [2012, 998], [2013, 1155], [2014, 1311], [2015, 1468],
                             [2016, 1624], [2017, 1780], [2018, 1936], [2019, 2093], [2020, 2249], [2021, 2406], [2022, id_ultima_historia+1]]

#A operação de '\n'.join([...]) dentro do return de inicio é para converter a lista dos anos em uma lista HTML
@route('/')
def inicio():
    return '''
        <h1>Histórias XKCD</h1>
        <h3>Selecione uma das opções abaixo</h3>
        <a href=historia?tipo=aleatoria>Ver Histórias Aleatórias</a><br><br>
        Ver Histórias do Seguinte Ano:
        <form action="/historia" method="GET">
        <select name="ano" id="tipo">
        ''' + '\n'.join(['<option value="' + str(ano) + '">' + str(ano) + '</option>' for ano in todos_os_anos]) + '''
        </select>
        <input value="Enviar" type="submit" />
        </form>
        '''

@route('/historia', method='GET')
def exibir_imagem():
    tipo = str(request.params.get('tipo'))
    
    if 'aleatoria' in tipo:
        resposta = requests.get('https://xkcd.com/' + str(randint(1, id_ultima_historia)) + '/info.0.json')

        titulo = resposta.json().get("safe_title")
        imagem = resposta.json().get("img")
        comentario = resposta.json().get("alt")

        return template("<h3>{{titulo_}}</h3> \
                        <img src=\"{{imagem_}}\" alt=''><br> \
                        <p>{{comentario_}}<br><br> \
                        <a href=\"/historia?tipo=aleatoria\">Gerar Nova História!</a><br> \
                        <a href=\"/\">Voltar à Página Inicial</a><br><br>",
                        titulo_=titulo, imagem_=imagem, comentario_=comentario)
        
    else:
        ano = int(request.params.get('ano'))

        try:
            id_relativo_historia_atual = int(request.params.get('id_historia'))
        except:
            id_relativo_historia_atual = 1

        if id_relativo_historia_atual < 1 or id_relativo_historia_atual > lista_primeira_historia_ano[(ano+1)-2006][1] - lista_primeira_historia_ano[ano-2006][1]:
            return ("<p>Não foi possível encontrar a história indicada.</p>\
                            <a href=\"/\">Voltar à Página Inicial</a><br><br>")
        
        resposta = requests.get('https://xkcd.com/' + str(lista_primeira_historia_ano[ano-2006][1] + id_relativo_historia_atual - 1) + '/info.0.json')

        titulo = resposta.json().get("safe_title")
        imagem = resposta.json().get("img")
        comentario = resposta.json().get("alt")
        id_historia = resposta.json().get("num")

        botoes_para_adicionar = ''

        if id_historia + 1 < lista_primeira_historia_ano[(ano+1)-2006][1]:
            botoes_para_adicionar += '<a href=\"/historia?ano=' + str(ano) + '&id_historia=' + str(id_relativo_historia_atual + 1) + '\">História Seguinte</a><br>'

        if id_historia - 1 >= lista_primeira_historia_ano[ano-2006][1]:
            botoes_para_adicionar += '<a href=\"/historia?ano=' + str(ano) + '&id_historia=' + str(id_relativo_historia_atual - 1) + '\">História Anterior</a><br>'

        return template("<h3>{{titulo_}}</h3> \
                        <img src=\"{{imagem_}}\" alt=''><br> \
                        <p>{{comentario_}}<br><br> \
                        " + botoes_para_adicionar + " \
                        <a href=\"/\">Voltar à Página Inicial</a><br><br>",
                        titulo_=titulo, imagem_=imagem, comentario_=comentario)

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
