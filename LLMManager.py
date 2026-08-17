import requests
API_URL = "https://api.esempio-ai.com/v1/chat"
API_KEY = "CHIAVE_SEGRETA"

def gestioneRichiesta(lista:list)->str: 
    memoria_formatta=[]
    for ruolo, testo,data in lista:
        memoria_formatta.append({"role": ruolo, "content": testo})
    header = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "modello": "gpt-4",
        "messaggi": memoria_formatta
    }
    risposta=requests.post(url=API_URL, headers=header, json=payload)
    if risposta.status_code==200:
        dati=risposta.json()
        testo_ai = dati.get("choices", [{}])[0].get("message", {}).get("content", "") #questo mi permette di prendere solo il succo del messaggio
        return testo_ai
    else:
        return f"Errore di connessione con MLD. Codice: {risposta.status_code}"
    
def richiediTitolo(richiesta:str)->str:
    richiestaTitolo=richiesta + "\n \n Riassumi questo testo in poche parole, per formare un fantastico titolo che riesca a descrivere tutto"
    header = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "modello": "gpt-4",
        "messaggi": [
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