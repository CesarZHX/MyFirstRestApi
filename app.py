import requests
from flask import Flask, request, jsonify
          
app = Flask(__name__)

# Definir la API key (solo para fines prácticos)
api_key = "1234567890"

# Función para autenticar la API key
def authenticate_api_key():
    provided_api_key = request.args.get("apikey")
    if provided_api_key != api_key:
        return jsonify({"error": "API key no válida"}), 401
    return None

@app.route("/")
def home():      
    return "Home"

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com",
    }
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    return jsonify(user_data), 200

@app.route('/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify(data), 201

'''
{
  "username": "Tim"
}
'''

@app.route('/transcribe-audio/url', methods=['POST'])
def transcribe_audio_url():
    error_response = authenticate_api_key()
    if error_response:
        return error_response

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Se requiere una URL"}), 400

    try:
        # Realizar una solicitud GET a la URL proporcionada
        response = requests.get(url)

        if response.status_code == 200:
            # Si la solicitud es exitosa, obtener el contenido HTML
            html_content = response.text
            return jsonify({"html": html_content}), 200
        else:
            return jsonify({"error": "No se pudo obtener el HTML de la URL"}), 500
    except requests.RequestException as e:
        # Manejar errores de solicitud (p. ej. timeout, URL incorrecta)
        return jsonify({"error": str(e)}), 500
    
''' http://127.0.0.1:5000/transcribe-audio/url?apikey=1234567890
{
  "url": "https://static.wikia.nocookie.net/valorant/images/2/22/JettPick.mp3/revision/latest"
}
'''