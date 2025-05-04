from flask import Flask, request, jsonify, render_template_string
from encriptador import encriptar, desencriptar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

EMAIL_ORIGEN = "ecemilianocorona05@gmail.com"
CLAVE_APP = "ppkp eenm mrzz qxwh"  # Tu contraseña de aplicación de Gmail

@app.route('/enviar', methods=['POST'])
def enviar():
    data = request.json
    correo = data.get("correo")
    mensaje = data.get("mensaje")

    if not correo or not mensaje:
        return jsonify({"error": "Correo y mensaje requeridos"}), 400

    try:
        mensaje_cifrado = encriptar(mensaje)

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>🔐 Mensaje cifrado</h2>
                <p>{mensaje_cifrado}</p>
                <a href="https://correo-encriptado.onrender.com/desencriptar?token=...">Desencriptar"
                   style="background-color: #3498db; color: white; padding: 10px 20px;
                          text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px;">
                   🔓 Desencriptar mensaje
                </a>
            </body>
        </html>
        """

        email = MIMEMultipart("alternative")
        email["Subject"] = "Mensaje encriptado"
        email["From"] = EMAIL_ORIGEN
        email["To"] = correo
        email.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ORIGEN, CLAVE_APP)
            server.send_message(email)

        return jsonify({"status": "Mensaje enviado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/desencriptar')
def ver_desencriptado():
    token = request.args.get("token")
    if not token:
        return "Token no proporcionado", 400

    try:
        texto_original = desencriptar(token)
        return render_template_string(f"""
        <html>
            <head>
                <title>Mensaje desencriptado</title>
            </head>
            <body style="font-family: Arial, sans-serif; padding: 2rem;">
                <h2>🔓 Mensaje desencriptado</h2>
                <p style="font-size: 1.2em; color: #2c3e50;">{texto_original}</p>
            </body>
        </html>
        """)
    except Exception as e:
        return f"Error al desencriptar: {str(e)}", 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5005))  # Render asigna el puerto aquí
    app.run(host='0.0.0.0', port=port)
