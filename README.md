🛡️ Phishing URL Detection API
📌 Overview

This project is a Machine Learning + FastAPI based system to detect whether a given URL is Safe or Phishing.

Takes single or multiple URLs as input (JSON).

Returns predictions through a REST API.

Lightweight, fast, and easy to deploy.

Useful for cybersecurity research, awareness, and practical phishing detection tools.

🚀 Features

✅ Accepts single or multiple URLs
✅ Predicts phishing vs safe websites
✅ REST API built using FastAPI
✅ Can be extended with new models or datasets

⚙️ Installation
1.Clone the repo:
git clone https://github.com/YOUR_USERNAME/Phishing-URL-Detection-API.git
cd Phishing-URL-Detection-API
2.Install dependencies:
3.pip install -r requirements.txt
Run the server:
uvicorn app:app --reload


🧠 How It Works

Dataset – Model is trained on phishing & legitimate URL datasets.

Feature Extraction – Extracts characteristics like length, special symbols, HTTPS usage, etc.

Model – A ML classifier (e.g., RandomForest, Logistic Regression) predicts Safe/Phishing.

API – FastAPI serves the model so anyone can test URLs via HTTP requests.

📌 Future Improvements

🔹 Add deep learning models for higher accuracy
🔹 Integrate live web scraping (content analysis)
🔹 Create a Chrome/Firefox extension for real-time detection
🔹 Build a dashboard for monitoring phishing attacks

📚 References

Phishing Website Detection using Machine Learning

FastAPI Documentation

UCI Repository Phishing Dataset
