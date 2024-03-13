import pandas as pd
import json
import pickle

# Definição global map das variáveis para valores numéricos
HOLIDAY_MAP = {
    'False': 0, # No holiday
    'True': 1, # Holiday
}
FUNCTIONING_DAY_MAP = {
    'False': 0, # No
    'True': 1, # Yes
}
DAY_MAP = {
    'Sunday': 1,
    'Monday': 2,
    'Tuesday': 3,
    'Wednesday': 4,
    'Thursday': 5,
    'Friday': 6,
    'Saturday': 7,
}
SEASON_MAP = {
    'Spring': 1,
    'Summer': 2,
    'Autumn': 3,
    'Winter': 4,
}

# Procedimento para carregar o nosso dataset
def load_data(original=1):    
    dados = None
    if original == 1:
        dados = pd.read_csv('./data/SeoulBikeData.csv', encoding='cp1252')
    else:
        dados = pd.read_csv('./data/dataset_ajustado.csv', encoding='cp1252')
    return dados

# Procedimento para retornar todas as predições existentes no arquivo JSON local 
def get_all_predictions():
    data = None
    with open('predictions.json', 'r') as f:
        data = json.load(f)
        
    return data

# Salvar a predição efetuada em nosso arquivo local de resultados de predição
def save_prediction(paciente):
    # Mapear os valores para numérico
    # paciente['sex'] = SEX_MAP[paciente['sex']]
    # paciente['cp'] = CHEST_PAIN_MAP[paciente['cp']]
    # paciente['fbs'] = FBS_MAP[paciente['fbs']]
    # paciente['restecg'] = RESTECG_MAP[paciente['restecg']]
    # paciente['exang'] = EXANG_MAP[paciente['exang']]
    # paciente['slope'] = SLOPE_MAP[paciente['slope']]
    # paciente['thal'] = THAL_MAP[paciente['thal']]

    # Recuperar todas as predições existentes
    data = get_all_predictions()

    # Adicionar a nova predição
    data.append(paciente)

    # Escrever no arquivo local
    with open('predictions.json', 'w') as f:
        json.dump(data, f)

# Retornar o diagnóstico da predição
def predict(info):
    # Mapear os valores para numérico
    info['season'] = SEASON_MAP[info['season']]
    info['holiday'] = HOLIDAY_MAP[info['holiday']]
    info['functioning_day'] = FUNCTIONING_DAY_MAP[info['functioning_day']]

    # Objeto apenas com os dados de entrada do modelo
    predict_obj = {
        'Hour': info['hour'],
        'Temperature(°C)': info['temperature'],
        'Humidity(%)': info['humidity'],
        'Wind speed (m/s)': info['wind_speed'],
        'Visibility (10m)': info['visibility'],
        'Dew point temperature(°C)': info['dew_point'],
        'Solar Radiation (MJ/m2)': info['solar_radiation'],
        'Rainfall(mm)': info['rainfall'],
        'Snowfall (cm)': info['snowfall'],
        'Seasons': info['season'],
        'Holiday': info['holiday'],
        'Functioning Day': info['functioning_day'],
        'Day': info['day'],
        'Month': info['month'],
        'weekend': info['weekend'],
    }

    # Transforma o objeto em dataframe
    values = pd.DataFrame([predict_obj])
    
    # Recuperar o modelo
    # model = pickle.load(open('./models/bike_gridsearch.pkl', 'rb'))
    model = None
    model = pd.read_pickle('./models/bike_gridsearch.pkl')  
    
    # Efetuar a predição
    results = model.predict(values)
    result = None

    # Caso teve retorno, armazena o valor na variável de retorno
    if len(results) == 1:
        result = int(results[0])

    return result

