import psycopg
DB_CONFIG = "dbname=chatbot user=postgres password=segreto host=localhost port=5432"
def getUtente(idUtente:int):
    with psycopg.connect(DB_CONFIG) as connessione:
        with connessione.cursor() as cursore:
            query="SELECT nome, cognome from utente where idUtente=%s"
            cursore.execute(query,(idUtente,))
            return cursore.fetchone()   
def registraNuovoUtente(nome:str, cognome:str)->int:
                with psycopg.connect(DB_CONFIG) as connessione:
                    with connessione.cursor() as cursore:
                        queryNewUtente="INSERT INTO utente (nome, cognome) VALUES (%s, %s) RETURNING idUtente"
                        cursore.execute(queryNewUtente,(nome,cognome))
                        idUtente=cursore.fetchone()[0]
                        connessione.commit()     
                        return idUtente
def getListaChat(idUtente:int)->list:
    with psycopg.connect(DB_CONFIG) as connessione:
        with connessione.cursor() as cursore:
            queryChat="SELECT nomeChat, titolo from chat where idUtente=%s"
            cursore.execute(queryChat,(idUtente,))
            return cursore.fetchall()
        
def creaNuovaChat(idUtente:int)->int:
     with psycopg.connect(DB_CONFIG) as connessione:
          with connessione.cursor() as cursore:
               query="INSERT INTO CHAT (idUtente) VALUES (%s) RETURNING idChat"
               cursore.execute(query,(idUtente,))
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
