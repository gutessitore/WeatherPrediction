"""
curl -X POST -H "Content-Type: application/json" -d '{"feature1": 1, "feature2": 2, "feature3": 3, "feature4": 4}' http://127.0.0.1:5000/predict/clima
"""
import os
import json
import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Carrega a configuração das features
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


def load_model(model_name):
    model_path = os.path.join('..', '..', 'models', f'{model_name}.pkl')
    if not os.path.isfile(model_path):
        return None
    return joblib.load(model_path)


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
    model = load_model(model_name)
    if model is None:
        return jsonify({"error": f"Modelo '{model_name}' não encontrado."}), 404

    # Extrai os dados das features
    feature_data = pd.DataFrame(data, index=[0])

    # Realiza a previsão
    prediction = model.predict(feature_data)[0]

    # Retorna o resultado
    return jsonify({f"{model_name}_prediction": float(prediction)}), 200


if __name__ == '__main__':
    app.run(debug=True)
