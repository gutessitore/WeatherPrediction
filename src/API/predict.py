"""
curl -X POST -H "Content-Type: application/json" -d '{"feature1": 1, "feature2": 2, "feature3": 3, "feature4": 4}' http://127.0.0.1:5000/predict/clima
"""
import os
import json
import joblib
import pandas as pd
from keras.models import load_model
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

# Carrega a configuração das features
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


def _load_model(model_name, load_func=joblib.load, file_extension='pkl'):
    model_path = os.path.join('..', '..', 'models', f'{model_name}.{file_extension}')
    if not os.path.isfile(model_path):
        return None
    return load_func(model_path)


@app.route('/predict/clima', methods=['POST'])
def predict_clima():
    return predict('modelo_clima')


@app.route('/predict/temperatura', methods=['POST'])
def predict_temperatura():
    return predict('modelo_temperatura')


@app.route('/predict/transito', methods=['POST'])
def predict_transito():
    return predict('modelo_transito')


@app.route('/predict/irradiacao', methods=['POST'])
def predict_irradiacao():
    return predict('modelo_irradiacao')


def predict(model_name):
    data = request.get_json()[0]
    features = config[model_name]['features']

    missing_features = [k for k in features if k not in data]
    if missing_features:
        return jsonify(
            {"error": "Dados insuficientes para realizar a previsão.", "missing_features": missing_features}), 400

    # Carrega o modelo
    load_function = eval(config[model_name].get('load_function', "joblib.load"))
    file_extension = config[model_name].get('file_extension', 'pkl')
    model = _load_model(model_name, load_function, file_extension)
    if model is None:
        return jsonify({"error": f"Modelo '{model_name}' não encontrado."}), 404

    # Extrai os dados das features
    feature_data = eval(config[model_name]['input_data_structure'].format("data"))

    # Realiza a previsão
    prediction = model.predict(feature_data)[0]

    # Retorna o resultado
    return jsonify({f"{model_name}_prediction": float(prediction)}), 200


if __name__ == '__main__':
    app.run(debug=True)
