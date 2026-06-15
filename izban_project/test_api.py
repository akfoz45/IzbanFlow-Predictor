import requests

url = "http://127.0.0.1:8000/api/predict/"
payload = {
    "time_of_day": 8,       
    "day_of_week": 0,       
    "weekend": 0,           
    "heat": 14.5,           
    "rains_mm": 4.2,        
    "station": "Halkapınar" 
}

response = requests.post(url, json=payload)
print("Durum Kodu:", response.status_code)
print("Dönen Yanıt (Ham):")
print(response.text)