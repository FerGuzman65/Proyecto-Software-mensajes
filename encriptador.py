from cryptography.fernet import Fernet

CLAVE = b'_O_aoczOvsOQUOx_m_u30CO0P01nZXZ59d3YEiDVCZ4='
fernet = Fernet(CLAVE)

def encriptar(texto):
    """Encripta texto plano (str) y devuelve texto encriptado (str)."""
    token = fernet.encrypt(texto.encode())  # Esto da bytes
    return token.decode()  # Convertir bytes a str

def desencriptar(token):
    """Desencripta un mensaje (str) y devuelve texto plano (str)."""
    texto = fernet.decrypt(token.encode())  # Convertir str a bytes
    return texto.decode()  # Devolver str
