import requests
import os
from dotenv import load_dotenv
load_dotenv() 
API_KEY = os.getenv("API_KEY_SEGRETA")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def gestioneRichiesta(lista:list)->str: 
    memoria_formatta=[]
    for ruolo, testo,data in lista:
        ruoloFormato=ruolo.strip()
        memoria_formatta.append({"role": ruoloFormato, "content": testo})
    header = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": memoria_formatta
    }
    risposta=requests.post(url=API_URL, headers=header, json=payload)
    if risposta.status_code==200:
        dati=risposta.json()
        testo_ai = dati.get("choices", [{}])[0].get("message", {}).get("content", "") #questo mi permette di prendere solo il succo del messaggio
        return testo_ai
    else:
        return f"Errore {risposta.status_code} da Groq: {risposta.text}"
    
def richiediTitolo(richiesta:str)->str:
    richiestaTitolo=richiesta + "\n \n Riassumi questo testo in poche parole, per formare un fantastico titolo che riesca a descrivere tutto"
    header = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "user", "content": richiestaTitolo} 
        ]
    }
    risposta=requests.post(url=API_URL, headers=header, json=payload)
    if risposta.status_code==200:
        dati=risposta.json()
        testo_ai = dati.get("choices", [{}])[0].get("message", {}).get("content", "") #questo mi permette di prendere solo il succo del messaggio
        return testo_ai
    else:
        return "Nuova chat" 