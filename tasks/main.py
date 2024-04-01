import requests
import pandas as pd
from reusable_code import log_to_file

lista_localidade = [] 
lista_status = []
lista_mensagem = []

# Leitura dos dados
dados = pd.read_excel('files/ceps-BKP.xlsx')
log_to_file.info('Leitura da planilha realizada com sucesso', 'logs/teste.txt')

for i, row in dados.iterrows():

    # verbo utilizado: get
    resposta = requests.get(url=f'http://viacep.com.br/ws/{row['CEP']}/json/')

    if resposta.status_code >= 200 and resposta.status_code <= 299:
        
        # Mostrando retorno
        print('Status Code', resposta.status_code)
        print('Reason', resposta.reason)
        print(resposta.json())
        dados_resposta = resposta.json()

        # No caso do get, ele não gera erro, caso não existe a chave, apenas retorna 'None' dai podemos tratar ou retornr uma mensagem
        erro = dados_resposta.get('erro')

        if erro == "true":
            # print(dados_resposta)
            lista_localidade.append("N/A") 
            lista_status.append(resposta.status_code)
            lista_mensagem.append("Sem retorno na API")

        else:
            # print(dados_resposta)
            str_localidade = str(dados_resposta['localidade'])
            lista_localidade.append(str_localidade)

            lista_status.append(resposta.status_code)
            lista_mensagem.append(resposta.reason)

    else:
        # CEP no formato inválido
        # print('Status Code', resposta.status_code)
        # print('Reason', resposta.reason)
        #print(resposta.json())
        lista_localidade.append("N/A") 
        lista_status.append(resposta.status_code)
        lista_mensagem.append("CEP no formato inválido")



data = {'CEP': dados.iloc[:,0],
        'Localidade': lista_localidade,
        'Status': lista_status,
        'Mensagem': lista_mensagem
        }

df2 = pd.DataFrame(data)

df2.to_excel(r"C:\Users\elton.duarte\Downloads\python-rpa\teste.xlsx", index=False)