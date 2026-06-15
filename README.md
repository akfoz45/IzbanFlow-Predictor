# 🚆 IzbanFlow Predictor: AI-Powered Station Density Prediction System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20.svg?style=for-the-badge&logo=django)](https://www.djangoproject.com)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)

IzbanFlow Predictor is an end-to-end machine learning and web backend project that predicts the density status of stations on the İZBAN line—one of İzmir's most critical public transportation arteries—based on time, location, and weather parameters.

The project features a modular software architecture covering all stages from synthetic data generation and Exploratory Data Analysis (EDA) to training a model with resolved class imbalances and deploying a Django REST backend with an asynchronous Fetch API frontend.

---

## 📸 Screenshot & UI

User interface featuring a revamped glassmorphic design, dynamic state icons, and asynchronous loading animations:

![İZBAN Density Prediction System Interface](izban_preview.png)

---

## 🛠️ System Architecture & Workflow

The project consists of 3 main decoupled layers, from the creation of the data to the moment it reaches the user:

1. **Data Generation & ETL Layer (`generate_data.py`):** Generates a 1-year hourly synthetic dataset (`izban_data.csv`) using time-series rules, transfer center weights, and log-normal weather simulations.
2. **AI & Modeling Layer (`model_final.ipynb`):** A decision mechanism trained using the Gradient Boosting algorithm with managed class imbalances, serialized (`izban_model.pkl`) along with its architectural schema (`model_columns`).
3. **Web Server & API Layer (Django & Vanilla JS):** A REST endpoint that vectorizes incoming raw JSON data according to the model schema at runtime, and a modern frontend that consumes it asynchronously.

---

## 📊 Dataset Logical Rules

To ensure the model learns the correct patterns, real-world İzmir public transportation dynamics were simulated during dataset creation:
- **Time Rules:** The density score is algorithmically increased during peak hours (07:00-09:00 and 17:00-19:00) on weekdays, representing work and school commute times.
- **Location Effect:** 8 critical stations on the line are simulated; extra density weights are assigned to major transfer centers like **Halkapınar** and busy stations like Alsancak and Çiğli.
- **Weather Correlation:** In scenarios where rainfall (`rains_mm`) increases, the tendency towards public transportation is simulated by shifting the density class upwards.

---

## 📈 Model Performance

The natural imbalance between the "Sakin" (Quiet) and "Çok Yoğun" (Very Crowded) classes in the dataset was addressed using the `compute_sample_weight(class_weight='balanced')` method during training. This resulted in high success rates in predicting the minority class, "Çok Yoğun".

**Classification Report (Gradient Boosting Classifier):**

| Target Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Normal** | 0.79 | 0.73 | 0.76 | 458 |
| **Sakin** | 0.94 | 0.94 | 0.94 | 1177 |
| **Çok Yoğun** | 0.64 | 0.79 | 0.71 | 117 |
| **Accuracy** | | | **0.88** | 1752 |
| **Macro Avg** | | | **0.80** | 1752 |

---

## 🚀 Installation & Setup

To run the project on your local machine, you can follow the steps below:

### 1. Clone the Repository and Navigate to the Directory
```bash
git clone https://github.com/akfoz45/IzbanFlow-Predictor.git
cd izbanflow-predictor/izban_project
```

### 2. Install Required Libraries
```bash
pip install django pandas scikit-learn requests
```

### 3. Prepare the Database and Start the Server
```bash
python manage.py migrate
python manage.py runserver
```
Once the server is up and running, you can access the interface by navigating to http://127.0.0.1:8000/ in your browser.

## 🔌 REST API Usage
The system hosts a pure JSON REST API endpoint that can be consumed by external services (mobile apps, different microservices, etc.).

* Endpoint: POST /api/predict/
* Content-Type: application/json

### Example Request (Payload):

```json
{
    "time_of_day": 8,
    "day_of_week": 0,
    "weekend": 0,
    "heat": 14.5,
    "rains_mm": 4.2,
    "station": "Halkapınar"
}
```

### Example Success Response:

```json
{
    "status": "success",
    "inputs": {
        "time_of_day": 8,
        "day_of_week": 0,
        "weekend": 0,
        "heat": 14.5,
        "rains_mm": 4.2,
        "station": "Halkapınar"
    },
    "prediction": "Çok Yoğun"
}
```