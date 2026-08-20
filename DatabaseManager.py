import psycopg
import os
from dotenv import load_dotenv
load_dotenv()
DB_CONFIG = os.getenv("DB_PASSWORD")
def getUtente(email:str, password:str):
    with psycopg.connect(DB_CONFIG) as connessione:
        with connessione.cursor() as cursore:
            query="SELECT nome, cognome from utente where email=%s AND passw=%s"
            cursore.execute(query,(email,password))
            return cursore.fetchone()   
def registraNuovoUtente(email:str,password:str,nome:str, cognome:str):
               try:
                with psycopg.connect(DB_CONFIG) as connessione:
                    with connessione.cursor() as cursore:
                        queryNewUtente="INSERT INTO utente (email,passw, nome, cognome) VALUES (%s, %s,%s, %s)"
                        cursore.execute(queryNewUtente,(email,password,nome,cognome))
                        connessione.commit()
                        return True
               except UniqueViolation:
                    return False
                        
def getListaChat(email:str)->list:
    with psycopg.connect(DB_CONFIG) as connessione:
        with connessione.cursor() as cursore:
            queryChat="SELECT idChat, titolo from chat where emailUtente=%s"
            cursore.execute(queryChat,(email,))
            return cursore.fetchall()
        
def creaNuovaChat(email:str)->int:
     with psycopg.connect(DB_CONFIG) as connessione:
          with connessione.cursor() as cursore:
               query="INSERT INTO CHAT (emailUtente) VALUES (%s) RETURNING idChat"
               cursore.execute(query,(email,))
               idChat=cursore.fetchone()[0]
               connessione.commit()
               return idChat
def getMessaggiChat(idChat:int)->list:
     with psycopg.connect(DB_CONFIG) as connessione:
          with connessione.cursor() as cursore:
               query="SELECT ruolo, testo, dataMessaggio from messaggio where idChat=%s ORDER BY dataMessaggio ASC"
               cursore.execute(query,(idChat,))
               return cursore.fetchall()
def salvaMessaggio(idChat:int, ruolo:str, testo:str):
     with psycopg.connect(DB_CONFIG) as connessione:
          with connessione.cursor() as cursore:
               query="INSERT INTO messaggio(idChat,ruolo, testo) VALUES(%s,%s,%s) "
               cursore.execute(query,(idChat,ruolo,testo))
               connessione.commit()
def salvaTitolo( idChat:int,titolo:str):
     with psycopg.connect(DB_CONFIG) as connessione:
          with connessione.cursor() as cursore:
               query="UPDATE chat SET titolo=%s where idChat=%s "
               cursore.execute(query,(titolo,idChat))
               connessione.commit()

def eliminaChat(idChat:int):
     with psycopg.connect(DB_CONFIG) as connessione:
          with connessione.cursor() as cursore:
               query="DELETE FROM chat where idChat=%s"
               query2="DELETE FROM messaggio where idChat=%s"
               cursore.execute(query,(idChat,))
               cursore.execute(query2,(idChat,))
               connessione.commit()
     