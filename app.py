import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import requests
import util
import json
import sys
import seaborn as sns

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

    # Apresentar correlação dos dados
    st.subheader("Correlação de dados")
    fig, ax = plt.subplots()
    sns.heatmap(dados_ajustados.corr(), ax=ax)
    st.write(fig)

    # Calculando o número de valores únicos em cada coluna
    st.subheader("Qtd. valores únicos em cada coluna")
    unique_values = dados_ajustados.nunique()

    # Criando um DataFrame para armazenar essas informações
    unique_dataset = pd.DataFrame({
        'Features': unique_values.index,
        'Uniques': unique_values.values
    })

    # Configurando o tamanho do gráfico
    plt.figure(figsize=(15, 8))

    # Criando o gráfico de barras usando seaborn
    splot = sns.barplot(x=unique_dataset['Features'], y=unique_dataset['Uniques'], alpha=0.8, color='red')

    # Adicionando rótulos aos topos das barras
    for p in splot.patches:
        splot.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                    va='center', xytext=(0, 9), textcoords='offset points')

    # Adicionando título e rótulos dos eixos
    # plt.title('Qtd. valores únicos em cada coluna', weight='bold', size=15)
    plt.ylabel('Valores únicos', size=18, weight='bold')
    plt.xlabel('Features', size=18, weight='bold')
    plt.xticks(rotation=90)

    # Exibindo o gráfico
    st.pyplot(plt)

    # Criando a visualização dos dados de aluguel de bicicletas por mês
    st.subheader("Bicicletas alugadas X Mês")
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(data=dados_ajustados, x='Month', y='Rented Bike Count', color='lightblue', errorbar=None)
    ax.set_xlabel('Mês', fontsize=18, weight='bold')
    ax.set_ylabel('Qtd. bicicletas alugadas', fontsize=18, weight='bold')

    for bar in ax.patches:
        ax.annotate(format(bar.get_height(), '.2f'), (bar.get_x() + bar.get_width() / 2, bar.get_height()), ha='center',
                    va='center', size=10, xytext=(0, 8), textcoords='offset points')

    # Exibindo o gráfico
    st.pyplot(fig)

    # Apresentando o gráfico de comparação da quantidade de bicicletas alugadas com o dia da semana
    st.subheader("Média de bicicletas alugadas X Dia da semana")

    # Criando o gráfico de barras para a média do número de bicicletas alugadas por dia
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(data=dados_ajustados, x='Day', y='Rented Bike Count', errorbar=None, color='lightgreen', ax=ax)
    ax.set_xlabel('Dia da semana', fontsize=18, weight='bold')
    ax.set_ylabel('Média de bicicletas alugadas', fontsize=18, weight='bold')

    # Adicionando rótulos nas barras
    for bar in ax.patches:
        ax.annotate(format(bar.get_height(), '.2f'), (bar.get_x() + bar.get_width() / 2, bar.get_height()), ha='center',
                    va='center', size=10, xytext=(0, 8), textcoords='offset points')

    # Exibindo o gráfico
    st.pyplot(fig)


    # Criando o gráfico de caixa para o número de bicicletas alugadas em relação à hora do dia
    st.subheader("Bicicletas alugadas X hora")
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.boxplot(data=dados_ajustados, x='Hour', y='Rented Bike Count', color='blue', ax=ax)
    ax.set_xlabel('Hora', fontsize=22, weight='bold')
    ax.set_ylabel('Bicicletas alugadas', fontsize=22, weight='bold')

    fig,ax=plt.subplots(figsize=(20,6))
    sns.barplot(data=dados_ajustados,x='Hour',y='Rented Bike Count', ax=ax, errorbar=None, color ='violet')
    for bar in ax.patches:
        ax.annotate(format(bar.get_height(), '.2f'),
                    (bar.get_x() + bar.get_width() / 2,
                        bar.get_height()), ha='center', va='center',
                    size=10, xytext=(0, 8),
                    textcoords='offset points')
    ax.set_xlabel('Horas',fontsize=22, weight='bold')
    ax.set_ylabel('Média bicicletas alugadas',fontsize=22, weight='bold')

    # Exibindo o gráfico
    st.pyplot(fig)


    # Criado a verificação da quantidade de bicicletas alugadas em dia de funcionamento e dias que não são
    st.subheader("Bicicletas alugadas X Dia de funcionamento")
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(data=dados_ajustados, x='Functioning Day', y='Rented Bike Count', errorbar=None, color='lightpink', ax=ax)
    ax.set_xlabel('Dia de funcionamento', fontsize=18, weight='bold')
    ax.set_ylabel('Bicicletas alugadas', fontsize=18, weight='bold')

    # Exibindo o gráfico
    st.pyplot(fig)


    # Criado a verificação da quantidade de bicicletas alugadas em cada estação do ano
    st.subheader("Bicicletas alugadas X Estação")
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.barplot(data=dados_ajustados, x='Seasons', y='Rented Bike Count', errorbar=None, color='peachpuff', ax=ax)
    ax.set_xlabel('Estação do ano\n Spring: 1, Summer: 2, Autumn: 3, Winter: 4', fontsize=18, weight='bold')
    ax.set_ylabel('Bicicletas alugadas', fontsize=18, weight='bold')

    # Exibindo o gráfico
    st.pyplot(fig)


    # Calculando a média do número de bicicletas alugadas em relação à temperatura
    st.subheader("Bicicletas alugadas X Temperatura °C")

    df_temperature = pd.DataFrame(dados_ajustados.groupby('Temperature(°C)')['Rented Bike Count'].mean().sort_values(ascending=False))

    # Criando o gráfico de dispersão para a média do número de bicicletas alugadas em relação à temperatura
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.scatterplot(data=df_temperature, x='Temperature(°C)', y='Rented Bike Count', color='black', ax=ax)
    ax.set_xlabel('Temperatura(°C)', fontsize=18, weight='bold')
    ax.set_ylabel('Qnt. bicicletas alugadas', fontsize=18, weight='bold')

    # Exibindo o gráfico
    st.pyplot(fig)


    # Calculando a média do número de bicicletas alugadas em relação à chuva
    st.subheader("Bicicletas alugadas X Chuva (mm)")

    df_rain = pd.DataFrame(dados_ajustados.groupby('Rainfall(mm)')['Rented Bike Count'].mean().sort_values(ascending=False))

    # Criando o gráfico de dispersão para a média do número de bicicletas alugadas em relação à chuva
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.scatterplot(data=df_rain, x='Rainfall(mm)', y='Rented Bike Count', color='black', ax=ax)
    ax.set_xlabel('Chuva(mm)', fontsize=18, weight='bold')
    ax.set_ylabel('Qnt. bicicletas alugadas', fontsize=18, weight='bold')

    # Exibindo o gráfico
    st.pyplot(fig)


    # Calculando a média do número de bicicletas alugadas em relação à neve
    st.subheader("Bicicletas alugadas X Neve (cm)")

    df_rain = pd.DataFrame(dados_ajustados.groupby('Snowfall (cm)')['Rented Bike Count'].mean().sort_values(ascending=False))

    # Criando o gráfico de dispersão para a média do número de bicicletas alugadas em relação à neve
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.scatterplot(data=df_rain, x='Snowfall (cm)', y='Rented Bike Count', color='black', ax=ax)
    ax.set_xlabel('Neve(cm)', fontsize=18, weight='bold')
    ax.set_ylabel('Qnt. bicicletas alugadas', fontsize=18, weight='bold')

    # Exibindo o gráfico
    st.pyplot(fig)

    # Apresentar como ficou o dataset
    st.subheader("Dataset com o tratamento dos dados")
    st.dataframe(dados_ajustados)
    
    # Apresentar as comparações de modelos treinados
    st.title("Comparação de modelos")
    st.write("Aqui vamos apresentar o comparativo que fizemos dos modelos que foram treinados no Colab com o dataset preparado.")
    # Regressão linear
    st.subheader("Regressão linear")
    st.image("./media/regressao_linear.png", caption="Resultados do modelo de regressão linear")
    # Random forest
    st.subheader("Random forest")
    st.image("./media/random_forest.png", caption="Resultados do modelo random forest")
    # Random forest utilizando GridSearchCV
    st.subheader("Random forest utilizando GridSearchCV")
    st.image("./media/random_forest_gridsearchcv.png", caption="Resultados do modelo random forest utilizando GridSearchCV")
    # XGBoost utilizando GridSearchCV
    st.subheader("XGBoost utilizando GridSearchCV")
    st.image("./media/xgboost_gridsearchcv.png", caption="Resultados do modelo XGBoost utilizando GridSearchCV")
    # LightGBM utilizando GridSearchCV
    st.subheader("LightGBM utilizando GridSearchCV")
    st.image("./media/lightgbm_gridsearchcv.png", caption="Resultados do modelo LightGBM utilizando GridSearchCV")
    # Gráfico comparativo
    st.subheader("Gráfico comparativo")
    st.image("./media/r2_score.png", caption="Resultados de TESTE de cada modelo treinado em forma de gráfico")
    # Gráfico comparativo
    st.subheader("Tabela comparativa")
    st.image("./media/r2_score_table.png", caption="Tabela apresentando o resultado de TREINO e TESTE de cada modelo treinado")
    


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

        # Caso o usuário der um feedback da precisão, vamos agradecer e armazenar a predição no arquivo local JSON
        if correct_prediction or wrong_prediction:
            message = "Muito obrigado pelo seu feedback. "

            if wrong_prediction:
                message += "Iremos utilizar esses dados para melhorar nosso modelo."

            # Armazenar a informação se a predição foi correta ou não, para futuro uso de apresentação de dados.
            if correct_prediction:
                info['CorrectPrediction'] = True
            elif wrong_prediction:
                info['CorrectPrediction'] = False

            # Armazenar a predição no objeto
            info['target'] = st.session_state['target']
            
            # Apresentar a mensagem para o usuário
            st.write(message)

            # Salvar predição no arquivo JSON via requisição POST para nossa API
            response = requests.post(f"{API_URL}/save-prediction", json=json.dumps(info))

            # Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
            if response.status_code != 200:
                msg = f"Falha ao salvar a predição: {response.status_code}"
                print(msg)
                raise Exception(msg)

    # Caso foi feita uma predição, apresentamos um botão para iniciar uma nova análise
    col1, col2, col3 = st.columns(3)

    with col2:
        new_test = st.button("Iniciar nova análise")

        # Se pressionou o botão de nova análise e tem dados em cache de predição, vai limpar
        if new_test and 'target' in st.session_state:
            # Limpar dados da sessão
            del st.session_state['target']
            st.rerun()

# Botão apresentar os dados de acurácia
accuracy_prediction_on = st.toggle("Exibir acurácia")

if accuracy_prediction_on:
    # Recuperar as predições salvas em nosso arquivo JSON via requisição GET para a API
    response = requests.get(f"{API_URL}/get-all-predictions")
    
    # Se o código da resposta da API for diferente de 200, apresenta mensagem de erro e da exceção 
    if response.status_code != 200:
        msg = f"Falha ao recuperar as predições: {response.status_code}"
        print(msg)
        raise Exception(msg)

    predictions = response.json()

    # Inicializar as variáveis para calcular a acurácia
    num_total_predictions = len(predictions)
    correct_predictions = 0
    total = 0
    accuracy_hist = []

    # Para cada predição vamos fazer o cálculo para gerar um histórico de acurácia e salvando o número de predições corretas
    for index, info in enumerate(predictions):
        
        total = total + 1
        if info['CorrectPrediction'] == True:
            correct_predictions += 1

        temp_accuracy = correct_predictions / total if total else 0

        # Adiciona a acurácia calculada para o array de histórico
        accuracy_hist.append(round(temp_accuracy, 2))

    # Calcular a acurácia geral das predições
    accuracy = correct_predictions / num_total_predictions if num_total_predictions else 0

    # Apresentar mética no layout
    st.metric("Acurácia", round(accuracy, 2))

    # Apresentar o gráfico de histórico de acurácia
    st.subheader("Histórico de acurácia")
    st.line_chart(accuracy_hist)


