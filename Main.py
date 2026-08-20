from DatabaseManager import getUtente, registraNuovoUtente, getListaChat,creaNuovaChat,getMessaggiChat,salvaMessaggio,salvaTitolo
from LLMManager import gestioneRichiesta,richiediTitolo
def avviaChat():
    primoId = input("Benvenuto, sono l'assistente MLD. Mi servirebbe il tuo ID (premi Invio se sei nuovo): ")
    
    if primoId == "":
        print("Sei nuovo, benvenuto, registrati pure")
        nome = input("Come ti chiami? ")
        cognome = input("Il tuo cognome? ")
        int_id = registraNuovoUtente(nome, cognome) 
        print(f"Fantastico {nome}, ecco il tuo id: {int_id}")
        lista = []
        
    elif primoId.isdigit() is False:
        print("Hai inserito un ID non valido, riprova.")
        print("Ti ricordo che deve contenere solo cifre.")
        return 
        
    else:
        int_id = int(primoId)
        utente = getUtente(int_id)
        
        if utente is None:
            print("Utente non valido... riprova")
            return
            
        nome = utente[0]
        print(f"Bentornato {nome}")
        lista = getListaChat(int_id) 
        
    
    
    if len(lista) > 0:
        print(f"{nome} le tue chat:")
        for chat in lista:
            nomeChat = chat[0]
            argomentoChat = chat[1]
            print(f"Chat {nomeChat}, con argomento {argomentoChat}")
    else:
        print("Come utente nuovo, non hai naturalmente vecchie chat. Iniziamone adesso una nuova!")
    
    print("\nCosa vuoi fare?")
    print("[0] Crea una Nuova Chat")
    
    scelta = int(input("Digita il numero della chat (o 0): "))
    
    if scelta == 0:
        print("Creiamo una nuova chat!")
        chat_attuale =creaNuovaChat(int_id)
        lista=[]
    else:
        print(f"Riprendiamo la chat numero {scelta}...")
        chat_attuale=scelta
        lista=getMessaggiChat(scelta)

        for ruolo, testo, dataMessaggio in lista:
            if(ruolo=="user"):
                print(f"Inviato da te {nome}")
                print(f"Data {dataMessaggio}")
                print(f"{testo}")
            else:
                print(f"Inviato da MLD ")
                print(f"Data {dataMessaggio}")
                print(f"{testo}")

    richiesta=input("Chiedi pure...")
    while richiesta!='esci':

        salvaMessaggio(chat_attuale,'user',richiesta)
        lista=getMessaggiChat(chat_attuale)#così ho proprio la lista con in aggiunta l'ultima richiesta
        lista_al_minimo=lista[-6:]
        if(len(lista_al_minimo)==1):#primo mess
            titoloNuovo=richiediTitolo(richiesta)
            salvaTitolo(chat_attuale,titoloNuovo)
        print("Elaboro un secondo...")
        risposta=gestioneRichiesta(lista_al_minimo)
        print("\nInviato da MLD")
        print(f"{risposta}")
        salvaMessaggio(chat_attuale,'assistant',risposta)
        richiesta=input("\nChiedi pure...")


if __name__ == "__main__":
    avviaChat(),