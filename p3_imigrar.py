import datetime
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
import mysql.connector

app = Flask(__name__)

if os.name == "nt":
  print(" Windows")
  os.system("cls")
else:
  print("Linux ou outro sistema Unix-like")
  os.system("clear")

print('Iniciando ....')

CORS(app)  # This will enable CORS for all routes

@app.route('/submit', methods=['POST'])

################################# F U N Ç Õ E S (Inicio)

def submit():
    if request.method == 'POST':
        data = request.get_json()  # Assuming data is sent as JSON
        cidade_1 = data['cidade1']
        rendimento1 = float(data['valor1'])
        cidade_2 = data['cidade2']
        rendimento2 = float(data['valor2'])
        print("Received JSON data:", data)  # Print JSON data to console
        
        vLiq_1 = 0
        vLiq_2 = 0
        periodo1 = ''
        periodo2 = ''

################################# Procura as cidade nas listas e chama a funcao correspondente

        if cidade_1 in lisBRA:
            vLiq_1 = faz_Brasil(rendimento1)
            # Considerando que para o Brasil o valor é mensal e existe o 13º, o valor deve ser multipicado por 13
            vLiq_1 *= 13
            tipoMoeda1 = 'R$'
            periodo1 = ' (mensal)'
        elif cidade_1 in lisALE:
            vLiq_1 = faz_Alemanha(rendimento1)
            tipoMoeda1 = '€'
        elif cidade_1 in lisEUA:
            vLiq_1 = faz_EUA(rendimento1,cidade_1)
            tipoMoeda1 = 'US$'
        elif cidade_1 in lisITA:
            vLiq_1 = faz_Italia(rendimento1,cidade_1)
            tipoMoeda1 = '€'
        else:
            print('Sem pais!')

        if cidade_2 in lisBRA:
            vLiq_2 = faz_Brasil(rendimento2)
            # Considerando que para o Brasil o valor é mensal e existe o 13º, o valor deve ser multipicado por 13
            vLiq_2 *= 13
            tipoMoeda2 = 'R$'
            periodo2 = ' (mensal)'
        elif cidade_2 in lisALE:
            vLiq_2 = faz_Alemanha(rendimento2)
            tipoMoeda2 = '€'
        elif cidade_2 in lisEUA:
            vLiq_2 = faz_EUA(rendimento2,cidade_2)
            tipoMoeda2 = 'US$'
        elif cidade_2 in lisITA:
            vLiq_2 = faz_Italia(rendimento2,cidade_2)
            tipoMoeda2 = '€'
        else:
            print('Sem pais!')


        data['varliq1'] = f"{vLiq_1:.2f}"  # Usando f-string (Python 3.6+)
        data['varliq2'] = f"{vLiq_2:.2f}"  # Usando f-string (Python 3.6+)

        #prepara nome de arquivo
        now=datetime.datetime.now()
        string_i_want=('%04d-%02d-%02d'%(now.year,now.month,now.day) + '_' + '%02d'%(now.hour) + 'h' + '%02d'%(now.minute) + 'm' + '%02d'%(now.second) + 's')
        nomearquivo = '/var/www/p_3/html/outputs/' + string_i_want + '.json'
        
        arq_results = '/var/www/p_3/html/resultado.txt'
        
        # Prepara lista 3 moedas para mostra no resultado
        lisRes1 = converter_moeda(tipoMoeda1, vLiq_1)
        lisRes2 = converter_moeda(tipoMoeda2, vLiq_2)

        # Gravando arquivo com os resultados
        file = open(arq_results,'w+') #criando o arquivo (Se o arquivo existir, vai sobreescrever)
        # print('Iniciando a inserção de linhas para formação do arquivo de resultados!')
        file.write(f'Cidade 1: {cidade_1} - Salário Bruto{periodo1}: {tipoMoeda1} {rendimento1:.2f}\n\n')
        file.write(f'Valor líquido (Anual): R$ {lisRes1[0]:.2f} / US$ {lisRes1[1]:.2f} / {lisRes1[2]:.2f} €\n\n\n\n') # inserindo 2a linha

        file.write(f'Cidade 2: {cidade_2} - Salário Bruto{periodo2}: {tipoMoeda2} {rendimento2:.2f}\n\n')
        file.write(f'Valor líquido (Anual): R$ {lisRes2[0]:.2f} / US$ {lisRes2[1]:.2f} / {lisRes2[2]:.2f} €\n') # inserindo 4a linha

        file.close()

        #Gravando arquivo com os resultados
        # Write data to the JSON file
        with open(nomearquivo, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        #print("Data has been written to ", nomearquivo)
        return jsonify({'message': 'Data processed successfully'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405

def trib_tab (parametro,tabela):
        for linha in tabela:
                # Verificar as condições
                if linha[0] < parametro and linha[1] >= parametro:
                        # Usa o parametro1 (valor bruto), o dado da 3º coluna (alíquota) e da 4ª coluna (desconto)
                        # Para calcular o valor do tributo
                        return (linha[2]*parametro - linha[3])

def faz_Brasil (parametro):
        global INSS
        global BRA
        tabela = INSS
        val_INSS = trib_tab(parametro,tabela)
        BC_IRPF = parametro - val_INSS
        tabela = BRA
        val_IRPF = trib_tab(BC_IRPF,tabela)
        return (parametro - val_INSS - val_IRPF)

def faz_Alemanha (parametro):
        global ALE
        tabela = ALE
        val_IR = trib_tab(parametro,tabela)

        global CUIDADOS
        tabela = CUIDADOS
        val_cuidados = trib_tab(parametro,tabela)

        global DESEMPREGO
        tabela = DESEMPREGO
        val_desemprego = trib_tab(parametro,tabela)

        global PREV_ALE
        tabela = PREV_ALE
        val_prev = trib_tab(parametro,tabela)

        global SAUDE
        tabela = SAUDE
        val_saude = trib_tab(parametro,tabela)

        return (parametro - val_IR - val_cuidados - val_desemprego - val_prev - val_saude)


def faz_EUA (parametro,city):
        global USA
        tabela = USA
        val_IR = trib_tab(parametro,tabela)

        global PREV_USA
        tabela = PREV_USA
        val_Prev = trib_tab(parametro,tabela)

        global MEDICARE
        tabela = MEDICARE
        val_Saude = trib_tab(parametro,tabela)

        val_State = 0
        val_City = 0

        if city == 'Houston':
            print('Houston nao tem tributacao adicional.')
        elif city == 'Chicago':
            global Illinois_State
            tabela = Illinois_State
            val_State = trib_tab(parametro,tabela)
        elif city == 'Los Angeles':
            global California_State
            tabela = California_State
            val_State = trib_tab(parametro,tabela)
        elif city == 'Phoenix':
            global Arizona_State
            tabela = Arizona_State
            val_State = trib_tab(parametro,tabela)
        elif city == 'Nova iorque':
            global NewYork_State
            tabela = NewYork_State
            val_State = trib_tab(parametro,tabela)
            global NYC
            tabela = NYC
            val_City = trib_tab(parametro,tabela)

        return (parametro - val_IR - val_Prev - val_Saude - val_State - val_City)

def faz_Italia (parametro,citta):
        global ITA
        tabela = ITA
        val_IR = trib_tab(parametro,tabela)

        global PREV_ITA
        tabela = PREV_ITA
        val_Prev = trib_tab(parametro,tabela)

        val_State = 0
        val_City = 0

        if citta == 'Roma':
            global Roma
            tabela_C = Roma
            global Lazio
            tabela_S = Lazio
        elif citta == 'Milão':
            global Milao
            tabela_C = Milao
            global Lombardia
            tabela_S = Lombardia
        elif citta == 'Nápoles':
            global Napoles
            tabela_C = Napoles
            global Campania
            tabela_S = Campania
        elif citta == 'Turim':
            global Turim
            tabela_C = Turim
            global Piemonte
            tabela_S = Piemonte
        elif citta == 'Palermo':
            global Palermo
            tabela_C = Palermo
            global Sicilia
            tabela_S = Sicilia
            
        val_City = trib_tab(parametro,tabela_C)
        val_State = trib_tab(parametro,tabela_S)

        return (parametro - val_IR - val_Prev - val_State - val_City)


def converter_moeda(tipo_moeda, valor):
    # Mapeando os símbolos para os códigos da API
    simbolos_para_codigos = {"R$": "BRL", "US$": "USD", "€": "EUR"}
    
    if tipo_moeda not in simbolos_para_codigos:
        return "Tipo de moeda inválido"
    
    codigo_moeda = simbolos_para_codigos[tipo_moeda]
    
    api_key = "fcff24c4c9199ff0f979669c"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{codigo_moeda}"

    response = requests.get(url)
    if response.status_code != 200:
        return f"Erro ao acessar a API de câmbio: {response.status_code}"

    dados = response.json()
    taxas = dados["conversion_rates"]

    lista = [
        round(valor * (taxas["BRL"] / taxas[codigo_moeda]), 2),
        round(valor * (taxas["USD"] / taxas[codigo_moeda]), 2),
        round(valor * (taxas["EUR"] / taxas[codigo_moeda]), 2),
    ]

    return lista        

def gerar_lista_da_tabela(nome_tabela):
    # Conectar ao banco de dados MySQL

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='imigrar',
        auth_plugin='mysql_native_password'   # só é preciso se trocou o plugin
    )
    
    cursor = conexao.cursor()
    
    # Verificar se a tabela existe
    cursor.execute("SHOW TABLES LIKE %s", (nome_tabela,))
    tabela_existe = cursor.fetchone()
    
    if tabela_existe:
        # Selecionar todo o conteúdo da tabela
        cursor.execute(f"SELECT * FROM {nome_tabela}")

        conteudo_tabela = cursor.fetchall()  # Retorna uma lista de tuplas
        
        # Fechar a conexão
        conexao.close()
        
        # Converter tuplas para listas
        lista_conteudo = [list(linha) for linha in conteudo_tabela]
        lista_convertida = [[float(valor) for valor in sublista] for sublista in lista_conteudo]        
        return lista_convertida
    else:
        conexao.close()
        return f"Tabela '{nome_tabela}' não encontrada no banco de dados."

################################# F U N Ç Õ E S (Termino)

################################# L I S T A S (Inicio)

lisALE = ["Berlim","Hamburgo","Munique","Colônia","Frankfurt"]
  
lisBRA = ["São Paulo","Rio de Janeiro","Brasília","Fortaleza","Salvador"]
    
lisEUA =["Nova Iorque","Los Angeles","Chicago","Houston","Phoenix"]
      
lisITA =["Roma","Milão","Nápoles","Turim","Palermo"]

INSS = gerar_lista_da_tabela('INSS')
BRA = gerar_lista_da_tabela('BRA')

ALE = gerar_lista_da_tabela('ALE')
CUIDADOS = gerar_lista_da_tabela('CUIDADOS')
DESEMPREGO = gerar_lista_da_tabela('DESEMPREGO')
PREV_ALE = gerar_lista_da_tabela('PREV_ALE')
SAUDE = gerar_lista_da_tabela('SAUDE')

USA = gerar_lista_da_tabela('USA')
PREV_USA = gerar_lista_da_tabela('PREV_USA')
MEDICARE = gerar_lista_da_tabela('MEDICARE')
NewYork_State = gerar_lista_da_tabela('NewYork_State')
NYC = gerar_lista_da_tabela('NYC')
California_State = gerar_lista_da_tabela('California_State')
Illinois_State = gerar_lista_da_tabela('Illinois_State')
Arizona_State = gerar_lista_da_tabela('Arizona_State')

ITA = gerar_lista_da_tabela('ITA')
PREV_ITA = gerar_lista_da_tabela('PREV_ITA')

Lazio = gerar_lista_da_tabela('Lazio')
Roma = gerar_lista_da_tabela('Roma')

Lombardia = gerar_lista_da_tabela('Lombardia')
Milao = gerar_lista_da_tabela('Milao')

Campania = gerar_lista_da_tabela('Campania')
Napoles = gerar_lista_da_tabela('Napoles')

Piemonte = gerar_lista_da_tabela('Piemonte')
Turim = gerar_lista_da_tabela('Turim')

Sicilia = gerar_lista_da_tabela('Sicilia')
Palermo = gerar_lista_da_tabela('Palermo')

################################# L I S T A S (Termino)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
