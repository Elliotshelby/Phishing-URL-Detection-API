from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn
import socket
import requests


# =======================
# Load trained model
# =======================
# For demo: use a dummy model
# Replace with your trained model (joblib.load("website_model.pkl"))
class DummyModel:
    def predict(self, X):
        # Just a mock: classify URLs with "https" as safe, else unsafe
        return [1 if "https" in x[0] else 0 for x in X]


model = DummyModel()


# =======================
# Feature extraction
# =======================
def extract_features(url: str):
    # Example features, expand as per your dataset
    return [
        len(url),  # length of URL
        1 if "https" in url else 0,  # HTTPS present
        url.count(".")  # number of dots
    ]


# =======================
# Domain/IP/Location Info
# =======================
def get_domain_info(url: str):
    try:
        domain = url.split("//")[-1].split("/")[0]
        ip_address = socket.gethostbyname(domain)

        # IP info via ipinfo.io (no API key needed for basic)
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()

        location = data.get("city", "Unknown") + ", " + data.get("country", "Unknown")
        org = data.get("org", "Unknown")

        return {
            "domain": domain,
            "ip": ip_address,
            "location": location,
            "organization": org
        }
    except Exception:
        return {"domain": None, "ip": None, "location": None, "organization": None}


# =======================
# FastAPI App
# =======================
app = FastAPI()


class WebsiteRequest(BaseModel):
    url: str


@app.post("/predict")
def predict_website(data: WebsiteRequest):
    url = data.url

    # Extract ML features
    features = extract_features(url)
    prediction = model.predict([features])[0]

    # Get domain/IP/location
    domain_info = get_domain_info(url)

    return {
        "url": url,
        "safe": bool(prediction),
        "domain": domain_info["domain"],
        "ip": domain_info["ip"],
        "location": domain_info["location"],
        "organization": domain_info["organization"]
    }


# =======================
# Run locally
# =======================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)