import pandas as pd
import json
import pickle

# Definição global map das variáveis para valores numéricos
SEX_MAP = {
    'Female': 0,
    'Male': 1,
}
CHEST_PAIN_MAP = {
    'Typical Angina': 1, 
    'Atypical Angina': 2, 
    'Non-anginal Pain': 3, 
    'Asymptomatic': 4,
}
FBS_MAP = {
    'False': 0, 
    'True': 1,
}
RESTECG_MAP = {
    'Normal': 0, 
    'ST-T abnormalities': 1,
    'Probable or definite left ventricular hypertrophy': 2,
}
EXANG_MAP = {
    'No': 0, 
    'Yes': 1,
}
SLOPE_MAP = {
    'Upsloping': 1, 
    'Flat': 1,
    'Downsloping': 3,
}
THAL_MAP = {
    'Normal': 3, 
    'Fixed defect': 6,
    'Reversible defect': 7,
}

# Procedimento para carregar o nosso dataset
def load_data():
    dados = pd.read_csv('./data/heart-disease-uci.csv')
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
    paciente['sex'] = SEX_MAP[paciente['sex']]
    paciente['cp'] = CHEST_PAIN_MAP[paciente['cp']]
    paciente['fbs'] = FBS_MAP[paciente['fbs']]
    paciente['restecg'] = RESTECG_MAP[paciente['restecg']]
    paciente['exang'] = EXANG_MAP[paciente['exang']]
    paciente['slope'] = SLOPE_MAP[paciente['slope']]
    paciente['thal'] = THAL_MAP[paciente['thal']]

    # Recuperar todas as predições existentes
    data = get_all_predictions()

    # Adicionar a nova predição
    data.append(paciente)

    # Escrever no arquivo local
    with open('predictions.json', 'w') as f:
        json.dump(data, f)

# Retornar o diagnóstico da predição
def diagnosis_predict(paciente):
    # Mapear os valores para numérico
    paciente['sex'] = SEX_MAP[paciente['sex']]
    paciente['cp'] = CHEST_PAIN_MAP[paciente['cp']]
    paciente['fbs'] = FBS_MAP[paciente['fbs']]
    paciente['restecg'] = RESTECG_MAP[paciente['restecg']]
    paciente['exang'] = EXANG_MAP[paciente['exang']]
    paciente['slope'] = SLOPE_MAP[paciente['slope']]
    paciente['thal'] = THAL_MAP[paciente['thal']]

    # Transforma o objeto em dataframe
    values = pd.DataFrame([paciente])
    
    # Recuperar o modelo
    model = pickle.load(open('./models/heart_disease_model.pkl', 'rb'))

    # Efetuar a predição
    results = model.predict(values)
    result = None

    # Caso teve retorno, armazena o valor na variável de retorno
    if len(results) == 1:
        result = int(results[0])

    return result

