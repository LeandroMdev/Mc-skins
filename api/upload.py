from flask import Flask, request, jsonify
import requests  # Importante: para hablar con la API de GitHub
import base64    # GitHub pide las imágenes en formato base64
import os

app = Flask(__name__)

# Configuración de tu Repo (Cámbialo por lo tuyo)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "LeandroMdev"
REPO_NAME = "Mc-skins"
BRANCH = "main"

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if 'skin' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400
    
    file = request.files['skin']
    if file.filename == '':
        return jsonify({"error": "Sin nombre de archivo"}), 400

    # 1. Convertir la imagen a Base64 para GitHub
    image_content = base64.b64encode(file.read()).decode('utf-8')
    
    # Ruta donde el Mod buscará la imagen (ejemplo: skins/nombre.png)
    file_path = f"skins/{file.filename}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"

    # 2. Preparar el envío a GitHub
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Nueva skin subida: {file.filename}",
        "content": image_content,
        "branch": BRANCH
    }

    # 3. Hacer el "Push" automático
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
    # Este es el link "Raw" que descarga la imagen directamente
        download_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{file_path}"
        return jsonify({
        "message": "¡Skin subida!",
        "url": download_url
        }), 200
