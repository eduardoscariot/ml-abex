from fastapi import Body, FastAPI
import data_handler 
import json
from typing import Any

# Para rodar a API usar:  uvicorn main:api --reload
api = FastAPI()

# Método base do projeto, pode ser utilizada, por exemplo, para verificar se a API está online
@api.get("/")
def read_root():
    return {"Hello": "World"}

# Método para recuperar o dataset do projeto e retornar um JSON
@api.get("/get-dataset")
def get_dataset():
    # Chama o procedimento para carregar o dataset
    dados = data_handler.load_data()
    # Cada registro, vai trazer o nome da coluna e atributo para todos eles
    json = dados.to_json(orient='records')
    return json

# Método para salvar a predição no arquivo local JSON. O método recebe um JSON do paciente
@api.post("/save-prediction")
def save_prediction(paciente: Any = Body(None)):
    # Transforma o JSON em objeto python
    paciente_obj = json.loads(paciente)
    # Chama procedimento para salvar a predição
    result = data_handler.save_prediction(paciente_obj)
    return result

# Método para recuperar todas as predições salvar no arquivo JSON local
@api.get("/get-all-predictions")
def get_all_predictions():
    # Chama procedimento para recuperar as predições
    predictions = data_handler.get_all_predictions()
    return predictions

# Método para realizar a predição. O método recebe um JSON do paciente e retorna o valor da predição
@api.post("/predict")
def predict(paciente: Any = Body(None)):
    # Chama procedimento para realizar a predição, passando o JSON do paciente
    result = data_handler.diagnosis_predict(json.loads(paciente))
    return result

