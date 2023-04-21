"""
curl -X POST -H "Content-Type: application/json" -d '{"feature1": 1, "feature2": 2, "feature3": 3, "feature4": 4}' http://127.0.0.1:5000/predict/clima
"""
import os
import json
import joblib
from flask import Flask, jsonify, request

app = Flask(__name__)

# Carrega a configuração das features
with open('config.json', 'r') as f:
    config = json.load(f)

features = config['features']


def load_model(model_name):
    model_path = os.path.join('models', f'{model_name}.pkl')
    if not os.path.isfile(model_path):
        return None
    return joblib.load(model_path)


@app.route('/predict/clima', methods=['POST'])
def predict_clima():
    return predict('model_clima')


@app.route('/predict/temperatura', methods=['POST'])
def predict_temperatura():
    return predict('model_temperatura')


def predict(model_name):
    data = request.get_json()

    # Verifica se os dados necessários estão presentes
    if not all(k in data for k in features):
        return jsonify({"error": "Dados insuficientes para realizar a previsão."}), 400

    # Carrega o modelo
    model = load_model(model_name)
    if model is None:
        return jsonify({"error": f"Modelo '{model_name}' não encontrado."}), 404

    # Extrai os dados das features
    feature_data = [data[feature] for feature in features]

    # Realiza a previsão
    prediction = model.predict([feature_data])[0]

    # Retorna o resultado
    return jsonify({f"{model_name}_prediction": prediction}), 200


if __name__ == '__main__':
    app.run(debug=True)
