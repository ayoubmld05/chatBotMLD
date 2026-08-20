import streamlit as st
import re
from DatabaseManager import getUtente, registraNuovoUtente, getListaChat, creaNuovaChat, getMessaggiChat, salvaMessaggio, salvaTitolo, eliminaChat
from LLMManager import gestioneRichiesta, richiediTitolo

# 1. IMPOSTAZIONI PAGINA WEB
st.set_page_config(page_title="MLD Chat", page_icon="🤖")

# 2. MEMORIA DELLA PAGINA (SESSION STATE)
# Se l'utente entra per la prima volta, creiamo le scatole vuote per ricordarci chi è
if "utente_email" not in st.session_state:
    st.session_state.utente_email = None
if "utente_nome" not in st.session_state:
    st.session_state.utente_nome = None
if "chat_attuale" not in st.session_state:
    st.session_state.chat_attuale = None

# ==========================================
# 3. BARRA LATERALE (Il Menu a Sinistra)
# ==========================================
with st.sidebar:
    st.title("👤 Profilo MLD")
    pattern_email= r'^[\w\.-]+@[\w\.-]+\.\w+$'
    pattern_password = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    # SE L'UTENTE NON E' ANCORA LOGGATO:
    if st.session_state.utente_email is None:
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        
        with tab1: # Modulo di Login
            login_email = st.text_input("La tua email")
            login_password=st.text_input("La tua password", type="password")
            if st.button("Accedi"):
                if re.match(pattern_email,login_email):
                    utente = getUtente(str(login_email), str(login_password))
                    if utente is not None:
                        st.session_state.utente_email = str(login_email)
                        st.session_state.utente_nome = utente[0]
                        st.rerun() # Ricarica la pagina per far sparire il login
                    else:
                        st.error("Utente non trovato, email o password errati...non preoccuparti riprova")
                else:
                    st.error("Inserisci un email valida")
                    
        with tab2: # Modulo di Registrazione
            nuova_email=st.text_input("Email:")
            st.text("scegli una password con almeno 8 caratteri,1 maiuscola, 1 minuscola, 1 numero ed 1 carattere speciale,")
            nuova_password=st.text_input("Password:", type="password")
            nuovo_nome = st.text_input("Nome:")
            nuovo_cognome = st.text_input("Cognome:")
            if st.button("Registrati"):
                if not re.match(pattern_email,nuova_email):
                    st.error("Errore: Il formato dell'email non è valido.")
                elif not re.match(pattern_password,nuova_password):
                    st.error("Errore: La password è troppo debole. Leggi i requisiti sopra!")
                elif not nuovo_nome or not nuovo_cognome :
                    st.error("Errore: Devi inserire sia il Nome che il Cognome.")
                else:
                    esisto=registraNuovoUtente(nuova_email,nuova_password,nuovo_nome, nuovo_cognome)
                    if esisto is not False:
                        st.success(f"Registrato! fantastico {nuovo_nome}, ti do il mio benvenuto!")
                        st.session_state.utente_email = nuova_email
                        st.session_state.utente_nome = nuovo_nome
                        st.rerun()
                    else:
                        st.error("Email già presente...usante un'altra")

    # SE L'UTENTE E' LOGGATO:
    else:
        st.success(f"Bentornato, {st.session_state.utente_nome}!")
        
        # Bottone Nuova Chat
        if st.button("➕ Crea Nuova Chat", use_container_width=True):
            nuova_id = creaNuovaChat(st.session_state.utente_email)
            st.session_state.chat_attuale = nuova_id
            st.rerun()
            
        st.divider()
        st.subheader("Le tue Chat:")
        
        # Peschiamo e mostriamo le vecchie chat come bottoni
        lista_chat = getListaChat(st.session_state.utente_email)
        for idChat, titolo in lista_chat:
            # Se clicco su questo bottone, cambia la chat attuale!
            
                col1,col2=st.columns([4,1])
                with col1:
                    if st.button(f"💬 {titolo}", key=f"btn_{idChat}", use_container_width=True):
                        st.session_state.chat_attuale = idChat
                        st.rerun()
                with col2:
                    with st.popover("⋮", help="Opzioni"):
                        rinominaTitolo=st.text_input("Rinomina il titolo", key=f"input_titolo_{idChat}")
                        if st.button("Salva", key=f"salva_{idChat}"):
                            if nuovo_titolo:
                                salvaTitolo(idChat, nuovo_titolo)
                                st.rerun()
                        st.divider()
                        if st.button("Elimina", key=f"elimina_{idChat}"):
                            eliminaChat(idChat)
                        # Se ho eliminato la chat in cui mi trovavo, mi butto fuori
                        if st.session_state.chat_attuale == idChat:
                            st.session_state.chat_attuale = None
                            st.rerun()
                
        st.divider()
        if st.button("Esci (Logout)"):
            st.session_state.utente_email = None
            st.session_state.chat_attuale = None
            st.rerun()

# ==========================================
# 4. AREA PRINCIPALE (La Chat Centrale)
# ==========================================
st.title("Assistente MLD 🚀")

if st.session_state.utente_email is None:
    st.info("👈 Fai il login o registrati dal menu a sinistra per iniziare.")
    
elif st.session_state.chat_attuale is None:
    st.info("👈 Seleziona una chat dalla barra laterale o creane una nuova!")
    
else:
    # A. Mostriamo tutta la cronologia passata
    cronologia = getMessaggiChat(st.session_state.chat_attuale)
    for ruolo, testo, dataMessaggio in cronologia:
        with st.chat_message(ruolo):
            st.markdown(testo) # st.markdown supporta testo, tabelle e grassetti perfetti!

    # B. La barra di testo dove l'utente scrive
    richiesta = st.chat_input("Chiedi pure...")
    
    if richiesta:
        # 1. Mostriamo subito a schermo il messaggio appena digitato
        with st.chat_message("user"):
            st.markdown(richiesta)
            
        # 2. Salviamo il messaggio nel DB
        salvaMessaggio(st.session_state.chat_attuale, 'user', richiesta)
        
        # 3. Peschiamo gli ultimi 6 messaggi per la memoria (Sliding Window)
        lista_completa = getMessaggiChat(st.session_state.chat_attuale)
        lista_al_minimo = lista_completa[-6:]
        
        # 4. MAGIA: Generazione del titolo automatico se è il primo messaggio
        if len(lista_al_minimo) == 1:
            titoloNuovo = richiediTitolo(richiesta)
            salvaTitolo(st.session_state.chat_attuale, titoloNuovo)
            
        # 5. Chiamata all'Intelligenza Artificiale (con animazione di caricamento)
        with st.chat_message("assistant"):
            with st.spinner("Elaboro un secondo..."):
                risposta = gestioneRichiesta(lista_al_minimo)
                st.markdown(risposta)
                
        # 6. Salviamo la risposta dell'AI nel DB
        salvaMessaggio(st.session_state.chat_attuale, 'assistant', risposta)
        

        
        # 7. Ricarichiamo la pagina per aggiornare eventuali titoli cambiati nel menu
        st.rerun()