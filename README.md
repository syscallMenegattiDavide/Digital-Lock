# Digital-Lock
ProjectWork ITS 
Sistema di Firma Digitale

Membri e Ruoli:
- Davide Menegatti: Programmatore sezione Database | server web | comunicazione delle pagine | gestore crittografia e hashing
- Aldo Ferhati: Programmatore sezione Admin
- Lorenzo Petrillo: Controllo burocratico secondo il GDPR | policy della privacy
- Angelo Scardovi: Programmatore sezione estetica (css e impaginazione)
- Tommaso Arlati: Leader | coordinatore | programmatore sezione containerizzazione 

Descrizione del Progetto

Il progetto mira a creare un sistema basilare per la firma e la verifica dei documenti utilizzando firme digitali, sviluppato in Python e supportato da una base di dati per memorizzare le informazioni essenziali.
- Creazione di Firme Digitali: Implementare un sistema che permetta agli utenti di caricare documenti e firmarli digitalmente usando la libreria cryptography di Python.
- Verifica delle Firme: Consentire agli utenti di verificare l'autenticità delle firme digitali sui documenti caricati nel sistema.
 -Gestione dei Documenti: Implementare una funzione di base per caricare e scaricare documenti firmati.
- Base di Dati: Utilizzare un database per memorizzare informazioni sui documenti e le firme associate.

Obiettivi del Progetto
- Creare un sistema per la gestione delle firme digitali utilizzando Python e una base di dati.
- Implementare un'interfaccia utente intuitiva che consenta agli utenti di firmare e verificare i documenti.
- Utilizzare una base di dati per memorizzare in modo persistente le informazioni sui documenti e le firme associate.


Implementazione di un Sistema di Autenticazione Sicuro
- Accesso sicuro: 
  - Sviluppare un sistema di autenticazione robusto per studenti e personale.
- Tutela dei dati sensibili: 
  - Implementare tecnologie avanzate di crittografia per proteggere i dati.


Programmazione (44 ore):
1. Pagina login
- Nome utente, password (hashata e salt), email:
  - Nome utente: Campo per l'inserimento del nome utente.
  - Password: La password inserita dall'utente deve essere hashata e saltata per motivi di sicurezza. Utilizzare una libreria come bcrypt per hashare e salare le password.
  - Email: Campo per l'inserimento dell'email dell'utente, utile per eventuali recuperi di password.
2. Pagina database
- Database: Configurazione di un database relazionale (es. MySQL, PostgreSQL) per memorizzare le informazioni degli utenti, i documenti caricati e le firme digitali.
- Tabella Utenti: Con colonne per ID utente, nome utente, password hashata e salata, email, ruolo (utente/admin).
- Tabella Documenti: Con colonne per ID documento, ID utente proprietario, nome file, percorso file criptato, chiave simmetrica criptata, timestamp.
3. 3 account, di cui 1 admin
- Account predefiniti: Creare tre account iniziali, includendo un amministratore, per testare il sistema. Gli account devono essere inseriti nel database all'avvio del sistema.
4. File caricabili
- Visibilità solo per l'utente proprietario: Gli utenti devono poter caricare file che saranno visibili solo a loro. I file devono essere associati al loro ID nel database.
- Criptazione con chiave simmetrica: Utilizzare una libreria come cryptography per criptare i file con una chiave simmetrica prima di salvarli.
- Scaricabili ed eliminabili: Gli utenti devono poter scaricare e eliminare i loro file caricati. Quando un file viene eliminato, deve essere rimosso anche dal database e dal sistema di file.
5. Verifica firma
- Confronto file: Implementare una funzione che permette agli utenti di caricare un file dal loro computer per confrontarlo con uno già caricato nel sistema, verificando così l'integrità e l'autenticità del file.
6. Pagina "About Us"
- Informazioni sul progetto: Una pagina che fornisce informazioni sul progetto, il team di sviluppo e gli obiettivi del sistema.
7. Logout
- Chiusura sessione: Implementare la funzionalità di logout per permettere agli utenti di uscire dalla loro sessione in modo sicuro.
8. Funzioni specifiche per admin (da implementare)
- Pannello di amministrazione: Creare una sezione del sito riservata agli amministratori, con funzionalità avanzate come la gestione degli utenti (creazione, modifica, eliminazione) e la visualizzazione di log delle attività.
9. Cambio libreria
- Valutazione e aggiornamento delle librerie: Assicurarsi che tutte le librerie utilizzate siano aggiornate e, se necessario, sostituirle con alternative più sicure o efficienti.
10. Containerizzazione del programma
- Docker: Utilizzare Docker per containerizzare l'applicazione, facilitando la distribuzione e l'esecuzione su diversi ambienti. Creare un file Dockerfile per definire l'ambiente di esecuzione e utilizzare Docker Compose per gestire i diversi servizi (es. database, applicazione web).
11. Modifica admin
- Gestione utenti e documenti: Implementare le funzionalità specifiche per l'admin che permettano di gestire gli utenti e i documenti presenti nel sistema. L'admin deve poter visualizzare, modificare ed eliminare gli account utente e avere accesso ai file caricati dagli utenti per monitorare le attività.
12.Aggiornamenti al Sistema di Firme Digitali
- Completamente rinnovato il sistema di creazione delle firme digitali. Le modifiche includono:
- Database: Modificato per memorizzare le firme digitali.
- Chiavi di Verifica: Creati due nuovi file (private_key.pem e public_key.pem) per consentire la verifica delle firme.
- Criptazione: Le firme sono criptate utilizzando SHA-256.
- Chiave Privata: Implementata una chiave RSA da 2048 bit.
- Upload dei File: Modificato il processo di caricamento dei file per criptarli con una chiave specifica. I file possono essere successivamente scaricati e viene applicata la firma digitale utilizzando il metodo descritto sopra.
Questi aggiornamenti migliorano la sicurezza e l'integrità dei documenti gestiti dal sistema.

Front-End (15 ore):
- CSS (Parte Estetica)
  - Stilizzazione delle pagine web:
    - Login: Creare uno stile accattivante e intuitivo per la pagina di login, utilizzando colori che rendano il testo facilmente leggibile e un layout che guidi l'utente nell'inserimento delle credenziali.
    - Dashboard: Assicurarsi che la dashboard sia ben organizzata, con un layout pulito che permetta agli utenti di visualizzare e gestire facilmente i propri documenti.
    - About Us: Creare uno stile informativo e accattivante per la pagina "About Us".
    - Logout: Assicurarsi che il pulsante di logout sia visibile e facilmente accessibile in tutte le pagine.

GDPR (General Data Protection Regulation) (5 ore):
1. Conformità GDPR
- Informativa sulla Privacy:
  - Redazione di una Privacy Policy: Creare una dettagliata informativa sulla privacy che descriva come i dati degli utenti vengono raccolti, utilizzati, memorizzati e protetti. La privacy policy deve essere facilmente accessibile e comprensibile.
2. Sicurezza dei Dati
- Protezione dei Dati:
  - Crittografia dei Dati: Assicurarsi che tutti i dati sensibili (come le password) siano crittografati sia in transito che a riposo. Utilizzare protocolli di sicurezza come HTTPS per proteggere i dati in transito.
3. Diritto all'Oblio
- Cancellazione dei Dati:
  - Richiesta di cancellazione: Fornire un metodo semplice e chiaro per gli utenti che desiderano esercitare il loro diritto all'oblio, cioè richiedere la cancellazione di tutti i loro dati personali dal sistema.

Documentazione (10 ore)
