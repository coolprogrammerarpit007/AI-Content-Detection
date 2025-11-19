import requests
import json

url = "https://api.zerogpt.com/api/detect/detectText"

payload = json.dumps({
  "input_text": "Hello, My name is Arpit and I am from Jaipur India, Our latest software update includes Project Chimera, a hyper-learning AI module. Chimera can analyze unstructured data sets $10$ times faster than previous models, enabling real-time predictive analytics and truly personalized user experiences. This proprietary model is designed to optimize everything from battery life to application rendering speed."
})
headers = {
  'ApiKey': '9c22a8df-6e31-422f-82de-00ca5d8b275d',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
