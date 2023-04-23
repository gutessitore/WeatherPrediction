import os
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from google.api_core.exceptions import NotFound


def read_data_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_type = file_extension.lower()[1:]

    if file_type == "parquet":
        return pd.read_parquet(file_path)
    elif file_type == "csv":
        return pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def create_dataset_if_not_exists(client, dataset_full_name):
    try:
        client.get_dataset(dataset_full_name)
    except NotFound:
        dataset = bigquery.Dataset(dataset_full_name)
        client.create_dataset(dataset)


def table_exists(client, table_full_name):
    try:
        client.get_table(table_full_name)
        return True
    except NotFound:
        return False


def load_data_to_bigquery(df, table_full_name, project_id):
    pandas_gbq.to_gbq(df, table_full_name, project_id=project_id, if_exists="replace")
    print(f"Carregados {len(df)} linhas na tabela {table_full_name}.")


def main(config):
    client = bigquery.Client()

    dataset_full_name = f"{config['project_id']}.{config['dataset_id']}"
    table_full_name = f"{dataset_full_name}.{config['table_id']}"

    df = read_data_file(config['file_path'])

    create_dataset_if_not_exists(client, dataset_full_name)

    if not table_exists(client, table_full_name):
        load_data_to_bigquery(df, table_full_name, config['project_id'])
    else:
        print(f"A tabela {table_full_name} já existe.")


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\gugat\Documents\puc-sp-ab9bc14a5151.json"

    config = {
        "project_id": "puc-sp",
        "dataset_id": "weather_prediction",
        "table_id": "irradiation_by_month",
        "file_path": "../data/irradiation_by_month.parquet",
    }

    main(config)
