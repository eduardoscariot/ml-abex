import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import requests
import util
import json
import sys

# URL da API local
API_URL = "http://127.0.0.1:8000"

# Verificar senha de acesso
if not util.check_password():
    st.stop()  # Se tiver incorreta, não permite prosseguir na aplicação.

# Recuperar os dados ORIGINAIS via API - Bike Sharing
response = requests.get(f"{API_URL}/get-dataset?original=1")

# Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
if response.status_code != 200:
    msg = f"Falha ao recuperar os dados: {response.status_code}"
    print(msg)
    raise Exception(msg)

# Fazer a conversão do JSON de retorno para dataframe
dados_json = json.loads(response.json())
dados = pd.DataFrame(dados_json)

# Recuperar os dados AJUSTADOS via API - Bike Sharing
response = requests.get(f"{API_URL}/get-dataset?original=0")

# Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
if response.status_code != 200:
    msg = f"Falha ao recuperar os dados: {response.status_code}"
    print(msg)
    raise Exception(msg)

# Fazer a conversão do JSON de retorno para dataframe
dados_json = json.loads(response.json())
dados_ajustados = pd.DataFrame(dados_json)

# Montar layout
st.title('Bike Sharing - Seoul')
data_analyses_on = st.toggle('Exibir análise dos dados')

# Se foi selecionado para apresentar os dados, apresenta o dataframe, um histograma de idades e a quantidade de registros com e sem doença.
if data_analyses_on:

    # Apresenta o dataframe
    st.subheader("Dataset Original - Sem tratamento de dados")
    st.dataframe(dados)

    st.subheader("Dataset com o tratamento dos dados")
    st.dataframe(dados_ajustados)
    # Apresentar um histograma de idades
    # st.header("Histograma - Idade")
    # fig = plt.figure()
    # plt.hist(dados['age'], bins=30)
    # plt.xlabel("Idade")
    # plt.ylabel("Quantidade")
    # st.pyplot(fig)

    # # Gerar gráfico com a quantidade de registros de diagnósticos sem doença(1) e com doença(2).
    # st.header("Diagnóstico de doença cardíaca (diagnóstico angiográfico)")
    # st.bar_chart(dados.target.value_counts())

# Vai montar as linhas de campos de entrada de dados
st.header('Preditor de compartilhamento de bicicleta')

#Rented Bike Count - Nosso Y
#Day,Month,weekend - Dados que serão transformados

# Row 1 - #Date, Hour,Temperature(°C)
col1, col2, col3 = st.columns(3)
with col1:
    date = st.date_input("Date")

with col2:
    hour = st.time_input("Hour")

with col3:
    temperature = st.number_input("Temperature (°C)", step=0.1)

# Row 2 - #Humidity(%), Wind speed (m/s),Visibility (10m)
col1, col2, col3 = st.columns(3)
with col1:
    humidity = st.number_input("Humidity (%)", step=1, min_value=0)

with col2:
    wind_speed = st.number_input("Wind speed (m/s)", step=0.1, min_value=0.0)

with col3:
    visibility = st.number_input("Visibility (10m)", step=0.3, min_value=0.000)

# Row 3 - #Dew point temperature(°C), Solar Radiation (MJ/m2),Rainfall(mm)
col1, col2, col3 = st.columns(3)
with col1:
    dew_point = st.number_input("Dew point temperature (°C)", step=0.1)

with col2:
    solar_radiation = st.number_input("Solar Radiation (MJ/m2)", step=0.2, min_value=0.00)

with col3:
    rainfall = st.number_input("Rainfall (mm)", step=0.1, min_value=0.0)

# Row 4 - Snowfall (cm), Seasons, Holiday
col1, col2, col3 = st.columns(3)
with col1:
    snowfall = st.number_input("Snowfall (cm)", step=0.1, min_value=0.0)

with col2:
    classes = ["Spring", "Summer", "Autumn", "Winter"]
    season = st.selectbox('Seasons', classes)

with col3:
    classes = ["True", "False"]
    holiday = st.selectbox('Holiday', classes)

# Row 5 - #Functioning Day
col1, col2, col3 = st.columns(3)
with col1:
    classes = ["True", "False"]
    functioning_day = st.selectbox('Functioning Day', classes)

with col2:
    # Botão para realizar a predição
    submit = st.button("Verificar")

# Dicionário para armazenar dados da predição
info = {}

# Verificar se o botão de fazer a predição foi pressionado ou se o campo 'target' está em cache
if submit or 'target' in st.session_state:
    # Tratar o dia da semana
    weekday = datetime.date(date.year, date.month, date.day).weekday()
    weekend = 0
    if weekday >= 5: # 5 Sat, 6 Sun
        weekend = 1
    
    # Alimentar o objeto com os dados que precisamos
    info = {
        'date': str(date),
        'day': date.day, #Pegar somente dia da semana
        'month': date.month, #Pegar somente mês
        'weekend': weekend,
        'hour': hour.hour, #Pegar somente a hora
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'visibility':visibility,
        'dew_point':dew_point,
        'solar_radiation': solar_radiation,
        'rainfall': rainfall,
        'snowfall': snowfall,
        'season': season,
        'holiday': holiday,
        'functioning_day': functioning_day,
    }

    print(f"Dados: {repr(info)}")

    # Realiza uma requisição POST para a nossa API, com o intuito de realizar a predição
    # Para a predição é enviado o objeto dados como um JSON.
    response = requests.post(f"{API_URL}/predict", json=json.dumps(info))
    result = None

    # Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
    if response.status_code != 200:
        msg = f"Falha ao efetuar a predição: {response.status_code}"
        print(msg)
        raise Exception(msg)

    # Recuperar o retorno da API
    result = response.json()

    if result is not None:
        st.subheader(f"Valor retornado pela predição: {result}")
        # disease = result

        # # Resultado: 1 = no disease | 2 = disease
        # if disease == 1:
        #     # Caso o paciente não apresentar ter problemas cardíacos, apresenta uma mensagem positiva!
        #     st.subheader("Paciente não tem problemas cardíacos! 👏🎉🎆")
        #     if 'target' not in st.session_state:
        #         st.balloons()
        # else:
        #     # Caso o paciente apresente ter problemas cardíacos, apresenta uma mensagem triste!
        #     st.subheader("Infelizmente foi detectado problema cardíaco, seria adequado buscar orientação médica. 😢😟🥺")
        #     if 'target' not in st.session_state:
        #         st.snow()

        # Armazenar o resultado da predição na sessão
        st.session_state['target'] = result

    # Validação para solicitar feedback quando for feita uma nova predição
    if info and 'target' in st.session_state:
        st.write("A predição está correta?")

        col1, col2, col3 = st.columns([1,1,5])
        with col1:
            # Botão para feedback de predição correta
            correct_prediction = st.button("👍")
        with col2:
            # Botão para feedback de predição incorreta
            wrong_prediction = st.button("👎")

#         # Caso o usuário der um feedback da precisão, vamos agradecer e armazenar a predição no arquivo local JSON
#         if correct_prediction or wrong_prediction:
#             message = "Muito obrigado pelo seu feedback. "

#             if wrong_prediction:
#                 message += "Iremos utilizar esses dados para melhorar nosso modelo."

#             # Armazenar a informação se a predição foi correta ou não, para futuro uso de apresentação de dados.
#             if correct_prediction:
#                 paciente['CorrectPrediction'] = True
#             elif wrong_prediction:
#                 paciente['CorrectPrediction'] = False

#             # Armazenar a predição no objeto do paciente
#             paciente['target'] = st.session_state['target']
            
#             # Apresentar a mensagem para o usuário
#             st.write(message)

#             # Salvar predição no arquivo JSON via requisição POST para nossa API
#             response = requests.post(f"{API_URL}/save-prediction", json=json.dumps(paciente))

#             # Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
#             if response.status_code != 200:
#                 msg = f"Falha ao salvar a predição: {response.status_code}"
#                 print(msg)
#                 raise Exception(msg)

#     # Caso foi feita uma predição, apresentamos um botão para iniciar uma nova análise
#     col1, col2, col3 = st.columns(3)

#     with col2:
#         new_test = st.button("Iniciar nova análise")

#         # Se pressionou o botão de nova análise e tem dados em cache de predição, vai limpar
#         if new_test and 'target' in st.session_state:
#             # Limpar dados da sessão
#             del st.session_state['target']
#             st.rerun()

# # Botão apresentar os dados de acurácia
# accuracy_prediction_on = st.toggle("Exibir acurácia")

# if accuracy_prediction_on:
#     # Recuperar as predições salvas em nosso arquivo JSON via requisição GET para a API
#     response = requests.get(f"{API_URL}/get-all-predictions")
    
#     # Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
#     if response.status_code != 200:
#         msg = f"Falha ao recuperar as predições: {response.status_code}"
#         print(msg)
#         raise Exception(msg)

#     predictions = response.json()

#     # Inicializar as variáveis para calcular a acurácia
#     num_total_predictions = len(predictions)
#     correct_predictions = 0
#     total = 0
#     accuracy_hist = []

#     # Para cada predição vamos fazer o cálculo para gerar um histórico de acurácia e salvando o número de predições corretas
#     for index, paciente in enumerate(predictions):
        
#         total = total + 1
#         if paciente['CorrectPrediction'] == True:
#             correct_predictions += 1

#         temp_accuracy = correct_predictions / total if total else 0

#         # Adiciona a acurácia calculada para o array de histórico
#         accuracy_hist.append(round(temp_accuracy, 2))

#     # Calcular a acurácia geral das predições
#     accuracy = correct_predictions / num_total_predictions if num_total_predictions else 0

#     # Apresentar mética no layout
#     st.metric("Acurácia", round(accuracy, 2))

#     # Apresentar o gráfico de histórico de acurácia
#     st.subheader("Histórico de acurácia")
#     st.line_chart(accuracy_hist)


