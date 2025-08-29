from fastapi import FastAPI
from pydantic import BaseModel
import socket, requests

# =======================
# Dummy ML Model
# =======================
class DummyModel:
    def predict(self, X):
        # Safe if https_flag == 1
        return [1 if features[1] == 1 else 0 for features in X]

model = DummyModel()

# =======================
# Feature Extraction
# =======================
def extract_features(url: str):
    return [
        len(url),                     # length of URL
        1 if "https" in url else 0,   # HTTPS check
        url.count(".")                # number of dots
    ]

# =======================
# Domain / IP / Location Info
# =======================
def get_domain_info(url: str):
    try:
        # Extract domain part
        domain = url.split("//")[-1].split("/")[0]

        # Resolve IP safely
        try:
            ip_address = socket.gethostbyname(domain)
        except Exception:
            ip_address = None

        # Try location lookup only if IP available
        location, org = "Unknown", "Unknown"
        if ip_address:
            try:
                response = requests.get(f"https://ipinfo.io/{ip_address}/json", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    location = data.get("city", "Unknown") + ", " + data.get("country", "Unknown")
                    org = data.get("org", "Unknown")
            except Exception:
                pass

        return {
            "domain": domain,
            "ip": ip_address,
            "location": location,
            "organization": org
        }

    except Exception as e:
        return {
            "domain": None,
            "ip": None,
            "location": None,
            "organization": None,
            "error": str(e)
        }

# =======================
# FastAPI App
# =======================
app = FastAPI()

class WebsiteRequest(BaseModel):
    url: str

@app.post("/predict")
def predict_website(data: WebsiteRequest):
    try:
        url = data.url
        features = extract_features(url)
        prediction = model.predict([features])[0]
        domain_info = get_domain_info(url)
        return {
            "url": url,
            "safe": bool(prediction),
            **domain_info
        }
    except Exception as e:
        return {"error": str(e)}
