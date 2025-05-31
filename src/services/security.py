from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json
import os


# Middleware de Descifrado (para las solicitudes entrantes)
class DecryptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, key: bytes):
        super().__init__(app)
        self.key = key  # Clave AES-256 para descifrar

    async def dispatch(self, request: Request, call_next):
        # Excluir rutas como /docs y /openapi.json (documentación de FastAPI)
        if request.url.path in ["/docs", "/openapi.json"]:
            return await call_next(request)

        # No descifrar solicitudes GET, HEAD o OPTIONS
        if request.method in ["GET", "HEAD", "OPTIONS", "DELETE"]:
            return await call_next(request)

        # Leer el cuerpo de la solicitud
        body = await request.body()
        if not body:
            return await call_next(request)  # Si no hay cuerpo, pasar directamente

        try:
            body_json = json.loads(body.decode())
            encrypted_body = body_json.get("pl")
            if not encrypted_body:
                raise Exception("Falta el cuerpo de la solicitud")
            # Separar IV y texto cifrado (formato: "IV:cuerpo_cifrado" en base64)
            iv_b64, encrypted_b64 = encrypted_body.decode().split(":")
            iv = base64.b64decode(iv_b64)
            encrypted = base64.b64decode(encrypted_b64)

            # Descifrar con AES-256-CBC
            cipher = Cipher(
                algorithms.AES(self.key), modes.CBC(iv), backend=default_backend()
            )
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted) + decryptor.finalize()

            # Eliminar el padding PKCS7
            pad_len = padded_data[-1]
            decrypted_data = padded_data[:-pad_len]

            # Reemplazar el cuerpo de la solicitud con los datos descifrados
            json_data = json.loads(decrypted_data.decode())
            request._body = json.dumps(json_data).encode()
        except Exception as e:
            return Response(content=f"Error al descifrar: {str(e)}", status_code=400)

        # Continuar con la solicitud procesada
        return await call_next(request)


# Middleware de Cifrado (para las respuestas salientes)
class EncryptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, key: bytes):
        super().__init__(app)
        self.key = key

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Excluir el cifrado para /docs y /openapi.json
        if request.url.path in ["/docs", "/openapi.json"]:
            return response

        try:
            # Leer el cuerpo de la respuesta
            response_body = [chunk async for chunk in response.body_iterator]
            response_body = b"".join(response_body)
            json_response = json.loads(response_body.decode())

            # Convertir a string JSON
            json_str = json.dumps(json_response)

            # Generar un IV aleatorio
            iv = os.urandom(16)

            # Cifrar con AES-256-CBC
            cipher = Cipher(
                algorithms.AES(self.key), modes.CBC(iv), backend=default_backend()
            )
            encryptor = cipher.encryptor()

            # Agregar padding PKCS7
            pad_len = 16 - (len(json_str) % 16)
            padded_data = json_str.encode() + bytes([pad_len] * pad_len)
            encrypted = encryptor.update(padded_data) + encryptor.finalize()

            # Codificar IV y texto cifrado en base64
            iv_b64 = base64.b64encode(iv).decode()
            encrypted_b64 = base64.b64encode(encrypted).decode()
            encrypted_response = f"{iv_b64}:{encrypted_b64}"

            # Crear un JSON con la clave 'pl' y el valor cifrado
            final_response = {"pl": encrypted_response}

            # Devolver el JSON como respuesta
            return Response(
                content=json.dumps(final_response),
                status_code=response.status_code,
                headers={"Content-Type": "application/json"},
            )
        except Exception as e:
            return Response(content=f"Error al cifrar: {str(e)}", status_code=500)
