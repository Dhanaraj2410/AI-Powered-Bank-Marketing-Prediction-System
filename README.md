# BankPredict AI - AI-Powered Bank Marketing Prediction System

> **"The system not only predicts whether a customer will subscribe to a term deposit, but also provides prediction probability, model performance metrics, prediction history, dashboard analytics, and explainable insights."**

BankPredict AI is a production-grade machine learning web application built with **Python, Django, MySQL 8, Scikit-learn Pipeline (`ColumnTransformer`), Bootstrap 5, Chart.js, and Django REST Framework**.

---

## 🗄️ Database Architecture & MySQL Integration

The system uses **MySQL 8** (via `pymysql` driver) with fallback support to SQLite.

### MySQL `.env` Configuration
```env
DB_ENGINE=mysql
DB_NAME=bankpredict_db
DB_USER=root
DB_PASSWORD=Dhanaraj2410
DB_HOST=localhost
DB_PORT=3306
```

### Core Relational Schema

```text
       ┌──────────┐
       │   USER   │ (auth_user)
       └────┬─────┘
            │ 1:1
       ┌────┴─────┐
       │ PROFILE  │ (accounts_userprofile)
       └──────────┘
            │ 1:N
       ┌────┴─────┐ 1:N ┌──────────┐
       │PREDICTION│─────│ CUSTOMER │ (customers_customer)
       └──────────┘     └──────────┘
```

---


## 🌟 Key Features

1. **Unified ML Pipeline (`ColumnTransformer`)**
   - Single serialized Scikit-learn pipeline (`bankpredict_pipeline.pkl`) handling numerical scaling and categorical one-hot encoding without train/inference mismatch.

2. **Explainable AI (XAI)**
   - **"Why did the model make this prediction?"**: Displays coefficient feature contribution breakdown highlighting top positive drivers and resisting factors per customer.

3. **Prediction Probability & Confidence**
   - Calculates exact conversion probability (e.g. 78.5%), confidence level, risk tier, and actionable AI recommendations.

4. **Model Comparison Engine**
   - Benchmarks Logistic Regression against Decision Trees and Random Forests, displaying Accuracy, Precision, Recall, F1 Score, and ROC-AUC metrics dynamically.

5. **Visual Metrics & Visualizers**
   - Interactive Confusion Matrix heatmap (TP, TN, FP, FN) and ROC Curve plot powered by Chart.js.

6. **Batch CSV Prediction & Download**
   - Upload customer CSV files, run bulk predictions, view summary table, and download results as CSV.

7. **Analytics Dashboard**
   - 5 KPI cards (Total Predictions, Yes Predictions, No Predictions, Average Probability, Active Model Accuracy) + 5 Chart.js charts.

8. **User Feedback System**
   - Interactive 👍 Yes / 👎 No feedback rating buttons recorded into MySQL for model tracking.

9. **Django REST Framework API**
   - Fully documented REST endpoints under `/api/`.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| **Backend** | Python 3.11+, Django 4.2+, Django REST Framework, Django ORM |
| **Database** | MySQL 8 (via `pymysql`) with SQLite fallback |
| **Machine Learning** | Scikit-learn, Pandas, NumPy, Joblib |
| **ML Models** | Logistic Regression, Decision Tree, Random Forest |
| **Preprocessing** | `ColumnTransformer` + `Pipeline` |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5, Chart.js, Font Awesome |
| **Testing** | Pytest, Django `TestCase` & `APITestCase` |
| **Deployment** | Gunicorn, Docker, Docker Compose |

---

## 🚀 Getting Started Locally

### 1. Prerequisites
- Python 3.11+
- Git

### 2. Installation
```bash
git clone https://github.com/Dhanaraj2410/Bank-Marketing-Prediction-ML.git
cd "Bank Customer Prediction"

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Model Training & Database Setup
```bash
# Train Scikit-learn Pipeline models
python ml_model/train_model.py

# Run Database Migrations
python manage.py makemigrations accounts customers predictions dataset_manager
python manage.py migrate

# Seed Model & Dataset Information into Database
python ml_model/seed_db.py

# Create Superuser (Admin)
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

---

## 📡 Django REST API Endpoints

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/predict/` - Submit single customer JSON prediction
- `GET  /api/predictions/` - List prediction history
- `GET  /api/predictions/<id>/` - Detailed prediction object
- `POST /api/predictions/<id>/feedback/` - Record 👍/👎 feedback
- `GET  /api/dashboard/` - Dashboard KPI stats & chart datasets
- `GET  /api/model-performance/` - Active model & benchmark comparison metrics

---

## 🧪 Running Automated Tests

```bash
python manage.py test tests
```

---

## 🐳 Docker Deployment

```bash
docker compose up --build
```
This launches both Django web app (Gunicorn) and MySQL 8 database container.
