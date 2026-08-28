\# 💿 Vinili - Catalogo E-commerce



Un'applicazione web e-commerce completa per la gestione e la visualizzazione di un catalogo di vinili, sviluppata in Python con il framework Django, HTML e CSS. Il progetto include un pannello di controllo Amministratore per la gestione dei prodotti.



\## 🛠️ Requisiti di Sistema

Prima di avviare il progetto, assicurati di avere installato:

\* \*\*Python:\*\* 3.12.x

\* \*\*Django:\*\* 5.x



\## 🚀 Installazione e Avvio Rapido



Segui questi passaggi per clonare il progetto e avviarlo in locale sul tuo computer.



\### 1. Clonare il repository

```bash

git clone git@github.com:KALAByte/Vinili.git

cd Vinili

```



\### 2. Configurare l'ambiente virtuale

Attiva il tuo ambiente virtuale esistente per isolare le librerie:

```bash

\# Esempio su Windows per attivarlo

.venv\\Scripts\\activate

```



\### 3. Installare le dipendenze

Installa tutte le librerie necessarie salvate nel file requirements:

```bash

pip install -r requirements.txt

```



\### 4. Configurare le variabili d'ambiente

Crea un file chiamato `.env` nella cartella principale del progetto e inserisci la tua chiave segreta:

```text

SECRET\_KEY=la\_tua\_secret\_key\_di\_django

DEBUG=True

```



\### 5. Applicare le migrazioni del database

Prepara il database locale SQLite:

```bash

python manage.py migrate

```



\### 6. Avviare il server di sviluppo

```bash

python manage.py runserver

```

Il sito sarà accessibile all'indirizzo locale: `http://127.0.0`



\## 👤 Accesso Amministratore

Per accedere al pannello di gestione dei vinili, naviga su `http://127.0.0admin`. 

\*(Nota: Per accedere è necessario creare un account amministratore locale sul proprio PC tramite il comando `python manage.py createsuperuser`)\*.



