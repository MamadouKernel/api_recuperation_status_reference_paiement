# app.py
import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
import os
from dotenv import load_dotenv

app = FastAPI(title="RECUPERATION DES PAIEMENTS,STATUS D'UN PAIEMENT, REFERENCES DES PAIEMENTS")
security = HTTPBearer()

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Récupère la clé secrète à partir des variables d'environnement
jwt_secret = os.getenv("JWT_SECRET", "default_secret_key")

# Données fictives des paiements
payments = [
    {"reference": "REF001", "status": "PAID"},
    {"reference": "REF002", "status": "PENDING"},
    {"reference": "REF003", "status": "FAILED"},
    # Ajoute d'autres paiements fictifs ici
]

# Fonction pour générer le token JWT
def generate_jwt_token():
    payload = {
        # Tu peux inclure ici des informations supplémentaires sur l'utilisateur si nécessaire
        "user_id": 123,
        "username": "john_doe",
        "role": "admin",
        # Ajoute d'autres données si nécessaire
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire dans 1 heure
    }
    token = jwt.encode(payload, jwt_secret, algorithm='HS256')
    return token
# my_token = generate_jwt_token()
# print(my_token)

# Endpoint pour afficher le token valide
@app.get('/afficher_token/')
def afficher_token():
    token = generate_jwt_token()
    return {"token de connection": token}

# Fonction pour vérifier un JWT
def verify_jwt(token: str = Depends(security)):
    try:
        decoded_payload = jwt.decode(token.credentials, jwt_secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")
    return decoded_payload

# Endpoint pour récupérer toutes les références de paiement
@app.get('/paiements/references')
def get_payment_references(payload: dict = Depends(verify_jwt)):
    references = [payment['reference'] for payment in payments]
    return references

# Endpoint pour récupérer tous les statuts de paiement
@app.get('/paiements/statuts')
def get_payment_statuses(payload: dict = Depends(verify_jwt)):
    statuses = [payment['status'] for payment in payments]
    return statuses

# Endpoint pour récupérer un paielement par reference

@app.get('/paiements/{reference}')
def get_payment_by_reference(reference: str, payload: dict = Depends(verify_jwt)):
    for payment in payments:
        if payment['reference'] == reference:
            return payment


# Endpoint pour récupérer tous les paiements
@app.get('/paiements/')
def get_payment(payload: dict = Depends(verify_jwt)):
    return payments
