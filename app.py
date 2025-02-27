from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# AES Configuration
key = get_random_bytes(16)  # Generates a random 16-byte key for AES

# Padding for AES encryption
def pad(data):
    return data + b' ' * (16 - len(data) % 16)

# AES Encryption
def encrypt_image(data):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data))
    return base64.b64encode(encrypted).decode('utf-8')

# AES Decryption
def decrypt_image(data):
    cipher = AES.new(key, AES.MODE_ECB)
    decoded = base64.b64decode(data)
    decrypted = cipher.decrypt(decoded).rstrip()
    return decrypted

# Test Route to Check if Server is Running
@app.route('/', methods=['GET'])
def home():
    return "API is running!"

# Encryption Endpoint
@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    data = file.read()
    encrypted_data = encrypt_image(data)
    return jsonify({"encrypted_data": encrypted_data})

# Decryption Endpoint
@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_data = request.json.get('encrypted_data')
    if not encrypted_data:
        return jsonify({"error": "No encrypted data provided"}), 400

    decrypted_data = decrypt_image(encrypted_data)
    decrypted_filename = "decrypted_image.png"

    # Save decrypted image
    with open(decrypted_filename, "wb") as f:
        f.write(decrypted_data)

    # Send the decrypted image back to the user
    return send_file(decrypted_filename, mimetype='image/png')

# Debug Route to Check Registered Endpoints
@app.route('/routes', methods=['GET'])
def routes():
    return str(app.url_map)

# Run the Flask App
if __name__ == '__main__':
    print("Server is starting...")
    print(app.url_map)  # Logs all available routes
    app.run(port=5000, debug=True)
