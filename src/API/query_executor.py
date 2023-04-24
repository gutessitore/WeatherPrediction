"""
curl -X POST -H "Content-Type: application/json" -d '{"query": "SELECT * FROM `your_project.your_dataset.your_table` LIMIT 10;"}' http://127.0.0.1:5000/query
"""
from flask import Flask, jsonify, request
from google.cloud import bigquery
import os

app = Flask(__name__)

# Configuração da autenticação
# Substitua 'path/to/keyfile.json' pelo caminho do arquivo de chave JSON da sua conta de serviço do Google Cloud

api_key_json_path = r"C:\Users\gugat\Documents\puc-sp-ab9bc14a5151.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key_json_path
bigquery_client = bigquery.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])


@app.route('/query', methods=['POST'])
def run_query():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"error": "A chave 'query' é obrigatória no JSON."}), 400

    try:
        query_job = bigquery_client.query(query)
        results = query_job.result()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    rows = [dict(row) for row in results]
    return jsonify({"data": rows}), 200


if __name__ == '__main__':
    app.run(debug=True)
