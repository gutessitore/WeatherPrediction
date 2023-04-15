# WeatherPrediction

## Architeture Diagram

```mermaid
graph TD
    subgraph "Data Collection"
        A[API] --> B((ETL))
        B --> C{Database}
    end

    subgraph "Data Processing"
        C --> D((Data Lake))
        D --> E[Spark]
        D --> F[Dashboard]
    end

    subgraph "Machine Learning"
        E --> G{Model}
        G --> H((Trainning))
        H --> G
        E --> I((Prediction))
        I --> J[Prediction API]
    end

    subgraph "API"
        C --> K[Query API]
        J --> L[Predicted Data API]
        K --> L
    end
```
## Repository Structure

```
weather_prediction/
    ├── api/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── ...
    ├── notebooks/
    │   ├── data_exploration.ipynb
    │   ├── data_preprocessing.ipynb
    │   ├── model_training.ipynb
    │   └── ...
    ├── src/
    │   ├── data/
    │   │   ├── data.py
    │   │   └── ...
    │   ├── models/
    │   │   ├── lstm.py
    │   │   └── ...
    │   └── ...
    ├── streamlit/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── ...
    ├── tests/
    │   ├── test_data.py
    │   ├── test_models.py
    │   └── ...
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    └── ...
```
