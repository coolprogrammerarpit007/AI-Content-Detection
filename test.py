import requests

url = "https://api.gowinston.ai/v2/ai-content-detection"
text_content = "Hello My name Is Arpit, I am from, Jaipur Rajasthan I specialize in backend development and enjoy building scalable, efficient, and reliable systems that solve real-world problems. Over the years, I have gained hands-on expertise in designing APIs, optimizing database structures, integrating third-party services, and developing AI-driven solutions tailored for different business use cases.I am deeply passionate about clean architecture, performance optimization, and writing maintainable code. Whether it’s creating robust backend services, working with cloud platforms, or integrating intelligent automation, I focus on delivering solutions that are not only technically strong but also meaningful for the end users. I enjoy exploring emerging technologies, especially in the field of AI and automation, and I constantly look for opportunities to improve my skills and stay updated with the latest trends.Being from Jaipur—a city known for its heritage, creativity, and innovation—I draw a lot of inspiration from my surroundings. I strongly believe in continuous learning and collaboration, and I enjoy working on projects that challenge me to think differently and push boundaries."

payload = {
    "text": text_content,
    "version": 4.11,
    "sentences": True,
    "language": "en"
}
headers = {
    "Authorization": "Bearer YlDb2EYnx3QceU16rvPPEPHnetYcndSHj9oeE90H8522dd96",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())