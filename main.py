import os
import psycopg2
import uuid        # <--- AGGIUNGI QUESTO (per generà i token univoci)
import smtplib     # <--- AGGIUNGI QUESTO (per spedì le mail)
from email.message import EmailMessage # <--- AGGIUNGI QUESTO
from psycopg2 import errors
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles # 1. Importa questo per le immagini

app = FastAPI()

# 2. Monta la cartella 'static' per poter usare immagini e file CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Definiamo la connessione una sola volta
def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

# --- INIZIALIZZAZIONE ---
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Creazione tabelle con PostgreSQL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS domande (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            testo TEXT NOT NULL
        )
    """)

    # AGGIUNGI QUESTO PEZZO QUI SOTTO:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reset_tokens (
            id SERIAL PRIMARY KEY,
            email TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            scadenza TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '1 hour')
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

# Eseguiamo l'inizializzazione all'avvio
init_db()
# Sotto init_db()
ADMIN_PASSWORD = "29102003"
EMAIL_ADDRESS = "sandruvadiko@gmail.com"  # <--- Metti la tua mail
EMAIL_PASSWORD = "VadimS2003!" # <--- Metti la password per le app di Google

# Sostituisci "TuaPasswordSegreta" con quella che preferisci
ADMIN_PASSWORD = "29102003"

@app.get("/admin")
async def admin_page():
    return HTMLResponse("""
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #121212; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); opacity: 0; animation: fadeIn 0.8s forwards; }
            @keyframes fadeIn { to { opacity: 1; } }
            input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 5px; border: none; }
            button { width: 100%; padding: 12px; background: #6200ea; color: white; border: none; border-radius: 5px; cursor: pointer; transition: 0.3s; }
            button:hover { background: #3700b3; transform: scale(1.02); }
        </style>
        <div class="card">
            <h2>🔐 Accesso Admin</h2>
            <form method="post" action="/admin-login">
                <input type="password" name="password" placeholder="Password Segreta" required>
                <button type="submit">Entra nel Sistema</button>
            </form>
        </div>
    """)

@app.post("/admin-login")
async def admin_login(password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, testo FROM domande")
        domande = cursor.fetchall()
        cursor.close()
        conn.close()

        # Iniziamo la costruzione dell'HTML con lo stile CSS incluso
        html_content = """
        <style>
            body { font-family: sans-serif; background: #121212; color: #fff; padding: 40px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e1e1e; border-radius: 10px; overflow: hidden; }
            th { background: #6200ea; padding: 15px; text-align: left; }
            td { padding: 15px; border-bottom: 1px solid #333; }
            tr:hover { background: #2a2a2a; }
            .btn-del { color: #ff5252; text-decoration: none; font-weight: bold; }
            .btn-del:hover { text-decoration: underline; }
            .back-link { display: inline-block; margin-top: 20px; color: #6200ea; text-decoration: none; }
        </style>
        <h2>Controllo Operativo</h2>
        <table>
            <tr><th>ID</th><th>Utente</th><th>Domanda</th><th>Azione</th></tr>
        """
        for d in domande:
            html_content += f"<tr><td>{d[0]}</td><td>{d[1]}</td><td>{d[2]}</td><td><a href='/delete/{d[0]}' class='btn-del'>Elimina</a></td></tr>"
        html_content += "</table><a href='/admin' class='back-link'>← Logout / Torna al login</a>"
        
        return HTMLResponse(html_content)
    # ... fine della tua funzione admin_login ...
    else:
        return HTMLResponse("<body style='background:#121212; color:white; text-align:center; padding:50px;'>Password errata! <br><a href='/admin'>Riprova</a></body>")

# --- DA QUI INCOLLA LE ROTTE NUOVE ---

# --- LOGICA RECUPERO PASSWORD (FINE FILE) ---

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page():
    return """
    <html>
    <head><title>Recupero Password</title></head>
    <body style="background: #0f1218; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
        <div style="background: #141820; padding: 30px; border-radius: 12px; width: 350px; text-align: center; border: 1px solid #1e2530;">
            <h2 style="color: #bb86fc;">🔑 Recupero</h2>
            <p style="color: #888; font-size: 14px;">Inserisci la mail per ricevere il link di reset.</p>
            <form action="/forgot-password" method="post">
                <input type="email" name="email" placeholder="Tua Email" required 
                       style="width: 100%; padding: 12px; margin: 15px 0; background: #1e2530; border: 1px solid #333; color: white; border-radius: 6px;">
                <button type="submit" style="width: 100%; padding: 12px; background: #6200ea; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">Invia Link</button>
            </form>
            <a href="/" style="color: #03dac6; text-decoration: none; font-size: 13px;">⬅️ Torna al Login</a>
        </div>
    </body>
    </html>
    """

@app.post("/forgot-password")
async def process_forgot_password(email: str = Form(...)):
    token = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vediamo se l'email esiste davvero
    cursor.execute("SELECT username FROM utenti WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    if user:
        # Salviamo il token nel DB
        cursor.execute("INSERT INTO reset_tokens (email, token) VALUES (%s, %s)", (email, token))
        conn.commit()
        
        # Link per il reset (cambia l'URL se sei su Render)
        link = f"https://tuo-sito.onrender.com/reset-password/{token}" 
        
        msg = EmailMessage()
        msg['Subject'] = 'Reset Password - Minecraft Hub'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg.set_content(f"Ciao! Usa questo link per cambiare la tua password: {link}\nIl link scadrà tra un'ora.")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            res_msg = "Link inviato! Controlla la posta."
        except Exception as e:
            print(f"Errore mail: {e}")
            res_msg = "Errore invio mail. Riprova più tardi."
    else:
        res_msg = "Email non trovata nel sistema."

    conn.close()
    return RedirectResponse(url=f"/?msg={res_msg}", status_code=303)

@app.get("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_page(token: str):
    return f"""
    <html>
    <head><title>Nuova Password</title></head>
    <body style="background: #0f1218; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div style="background: #141820; padding: 30px; border-radius: 12px; width: 350px; text-align: center;">
            <h2 style="color: #03dac6;">🆕 Nuova Password</h2>
            <form action="/reset-password-final" method="post">
                <input type="hidden" name="token" value="{token}">
                <input type="password" name="new_password" placeholder="Nuova password" required 
                       style="width: 100%; padding: 12px; margin: 15px 0; background: #1e2530; border: 1px solid #333; color: white; border-radius: 6px;">
                <button type="submit" style="width: 100%; padding: 12px; background: #03dac6; color: black; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">Aggiorna Password</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/reset-password-final")
async def update_password(token: str = Form(...), new_password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Controlliamo il token
    cursor.execute("SELECT email FROM reset_tokens WHERE token = %s", (token,))
    res = cursor.fetchone()
    
    if res:
        email = res[0]
        # Aggiorniamo la password
        cursor.execute("UPDATE utenti SET password = %s WHERE email = %s", (new_password, email))
        # Pulizia: cancelliamo il token usato
        cursor.execute("DELETE FROM reset_tokens WHERE token = %s", (token,))
        conn.commit()
        conn.close()
        return RedirectResponse(url="/?msg=Password aggiornata! Ora puoi loggare.", status_code=303)
    
    conn.close()
    return RedirectResponse(url="/?msg=Token non valido o scaduto!", status_code=303)
@app.get("/delete/{domanda_id}")
async def delete_domanda(domanda_id: int):
    # Eseguiamo la cancellazione
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM domande WHERE id = %s", (domanda_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    # Invece di ritornare HTML, facciamo un REDIRECT immediato
    return RedirectResponse(url="/admin")

# --- PAGINA 1: HOME PAGE (Hub Principale) ---
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, msg: str = None):
    session_user = request.cookies.get("session_user")
    # Controllo dello stato di login tramite i cookie di sessione
    session_user = request.cookies.get("session_user")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Recupera gli ultimi 5 utenti registrati
    cursor.execute("SELECT username FROM utenti ORDER BY id DESC LIMIT 5")
    utenti_html = "".join([f"<li>{row[0]}</li>" for row in cursor.fetchall()]) or "<li>Nessun player registrato</li>"
    
    # 2. Recupera tutte le domande salvate nel database
    cursor.execute("SELECT username, testo FROM domande ORDER BY id DESC")
    domande_salvate = cursor.fetchall()
    conn.close()
    
    # Genera l'HTML per l'elenco delle domande inviate
    domande_html = "".join([f"<div style='background: #11141a; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #81c784; text-align: left;'><b>{d[0]}:</b> {d[1]}</div>" for d in domande_salvate]) or "<p style='color: #b0bec5;'>Nessuna domanda presente. Fai la prima!</p>"
    
    alert_box = f'<div style="background:#238636; padding:10px; border-radius:6px; margin-bottom:20px; text-align:center; font-weight:bold;">{msg}</div>' if msg else ""

    # Logica dinamica e centrata per il Banner Q&A
    if session_user:
        qa_banner = f"""
        <div class="card" style="background: linear-gradient(135deg, #1b5e20, #004d40); border: 2px solid #81c784; text-align: center; max-width: 600px; margin: 20px auto 20px auto;">
            <h2 style="color: #a5d6a7; margin-bottom: 10px;">🔓 TAVERNA DEI VETERANI (Q&A ATTIVO)</h2>
            <p>Salute a te, <b>{session_user}</b>! Puoi inviare una domanda o lasciare un consiglio per la community:</p>
            
            <form action="/invia-domanda" method="post" style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px; margin-bottom: 20px;">
                <textarea name="testo_domanda" rows="3" placeholder="Scrivi qui la tua domanda o trucco di sopravvivenza..." style="width: 100%; padding: 10px; background: #11141a; border: 1px solid #2d3545; color: white; border-radius: 6px; resize: none; font-family: sans-serif;" required></textarea>
                <button type="submit" class="btn btn-green" style="font-size: 15px; padding: 10px; width: auto; align-self: center; min-width: 150px;">Invia Domanda</button>
            </form>
            
            <h3 style="border-bottom: 1px solid #2d3545; padding-bottom: 5px; color: #a5d6a7; font-size: 16px; text-align: left; margin-top: 20px;">Domande Recenti:</h3>
            <div style="max-height: 250px; overflow-y: auto; margin-top: 10px;">
                {domande_html}
            </div>
            
            <a href="/logout" style="display: block; margin-top: 15px; color: #ff5252; text-decoration: underline; font-size: 14px;">Scollega Account / Logout</a>
        </div>
        """
        auth_section = "" 
    else:
        qa_banner = """
        <div class="card" style="border: 2px dashed #ff5252; text-align: center; background-color: #1a1515; opacity: 0.9; max-width: 600px; margin: 20px auto 20px auto;">
            <h2 style="color: #ff5252; margin-bottom: 10px;">🔒 TAVERNA DEI VETERANI (Q&A PROIBITO)</h2>
            <p style="color: #b0bec5; margin: 0;">L'accesso alle frequenze radio di Domande & Risposte è riservato. Registrati o effettua il login per sbloccare questo modulo.</p>
        </div>
        """
        auth_section = """
        <div class="auth-container">
            <div class="card auth-card">
                <h2>🎮 Registra Nuovo Profilo</h2>
                <form action="/register" method="post">
                    <div class="form-group">
                        <input type="text" name="username" required placeholder="Username In-Game">
                    </div>
                    <div class="form-group">
                        <input type="email" name="email" required placeholder="Tua Email">
                    </div>
                    <div class="form-group">
                        <input type="password" name="password" required placeholder="Crea Password">
                    </div>
                    <button type="submit" class="btn">Registrati nel Database</button>
                </form>
            </div>

            <div class="card auth-card" style="background: #141820;">
    <h2>🔑 Accedi all'Hub</h2>
    <form action="/login" method="post">
        <div class="form-group">
            <input type="text" name="username" required placeholder="Username In-Game">
        </div>
        <div class="form-group">
            <input type="password" name="password" required placeholder="La tua Password">
        </div>
        <button type="submit" class="btn btn-blue">Effettua il Login</button>
    </form>
    
    <div style="text-align: center; margin-top: 15px;">
        <a href="/forgot-password" style="color: #b0bec5; font-size: 0.85em; text-decoration: none; transition: 0.3s;" onmouseover="this.style.color='#6200ea'" onmouseout="this.style.color='#b0bec5'">
            Password dimenticata? Clicca qui
        </a>
    </div>
</div>
"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Minecraft Hardcore Survival Hub</title>
        <style>
            /* Reset generale e sfondo di Minecraft a schermo intero fisso */
            body {{ 
                font-family: 'Segoe UI', sans-serif; 
                
                /* Immagine di sfondo con un leggero filtro scuro per leggere bene i testi bianchi */
                background-image: linear-gradient(rgba(17, 20, 26, 0.75), rgba(17, 20, 26, 0.75)), url('https://wallpapers.com/images/featured-full/sfondo-di-minecraft-cfljc4haleghnajo.jpg'); 
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
                background-repeat: no-repeat;
                
                color: #e3e6eb; 
                padding: 10px; 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                margin: 0; 
                min-height: 100vh;
                box-sizing: border-box;
            }}

            /* Contenitore principale: non deve mai superare il 100% della larghezza */
            .container {{ 
                width: 100%; 
                max-width: 650px; 
                display: flex;
                flex-direction: column;
                box-sizing: border-box;
            }}

            /* Header centrato */
            .header {{ 
                text-align: center; 
                padding: 20px; 
                background: linear-gradient(135deg, #b71c1c, #7f0000); 
                border-radius: 12px; 
                margin-bottom: 20px; 
                box-sizing: border-box;
            }}
            .header h1 {{ margin-top: 0; font-size: 24px; }}
            .header p {{ margin-bottom: 0; font-size: 14px; }}

            /* Le Card: box-sizing e margini automatici per il centramento */
            .card {{ 
                background-color: #1c212b; 
                border: 1px solid #2d3545; 
                border-radius: 12px; 
                padding: 20px; /* Ridotto per mobile */
                margin: 0 auto 20px auto; /* Centramento orizzontale forzato */
                width: 100%; /* Occupa tutto lo spazio disponibile nel container */
                box-sizing: border-box; /* Cruciale per non far uscire padding/border */
            }}
            h2 {{ color: #e53935; margin-top: 0; font-size: 20px; text-align: center; }}
            
            /* Box per l'alert verde (messaggi di successo) */
            .alert {{
                background-color: #238636; 
                padding: 10px; 
                border-radius: 6px; 
                margin: 0 auto 20px auto;
                width: 100%;
                text-align: center;
                box-sizing: border-box;
                font-weight: bold;
            }}

            /* Correzione specifica per il Banner Q&A (verde/rosso) per centrarlo */
            .card-qa {{
                max-width: 600px; /* Manteniamo il limite visivo */
                width: 100%; /* Ma deve poter rimpicciolire */
                margin-left: auto; /* Forziamo il centramento */
                margin-right: auto;
                box-sizing: border-box;
            }}

            /* Form, input e textarea: non devono mai uscire dai bordi */
            .auth-container {{ 
                display: flex; 
                gap: 15px; 
                flex-wrap: wrap; /* Fa andare a capo su mobile */
                width: 100%; 
                margin-bottom: 20px; 
                justify-content: center;
                box-sizing: border-box;
            }}
            .auth-card {{ flex: 1; min-width: 280px; margin: 0; }} /* Centrate dal flex-wrap */
            
            .form-group {{ margin-bottom: 15px; width: 100%; box-sizing: border-box; }}
            
            /* Input e Textarea forzati a stare dentro con box-sizing */
            input, textarea {{ 
                width: 100%; 
                padding: 12px; 
                background: #11141a; 
                border: 1px solid #2d3545; 
                border-radius: 6px; 
                color: #fff; 
                box-sizing: border-box; /* Impedisce che il padding le faccia uscire */
                font-size: 16px; /* Evita zoom automatico su iOS */
            }}
            
            /* Pulsanti centrati e reattivi */
            .btn {{ 
                background-color: #e53935; 
                color: white; 
                border: none; 
                padding: 12px 20px; 
                font-weight: bold; 
                border-radius: 6px; 
                cursor: pointer; 
                width: 100%; 
                max-width: 300px; /* Per non farli giganti su PC */
                text-decoration: none; 
                display: block; 
                text-align: center; 
                box-sizing: border-box; 
                font-size: 15px; 
                margin: 0 auto; /* Centramento automatico del pulsante stesso */
            }}
            .btn-nav {{ 
                margin-top: 12px; 
                font-size: 14px; 
                padding: 14px 10px; 
                max-width: 100%; /* Sulle nav rioccupano tutto */
            }}
            
            /* Varianti colore pulsanti (già presenti) */
            .btn-purple {{ background-color: #4a148c; }}
            .btn-orange {{ background-color: #e65100; }}
            .btn-green {{ background-color: #1b5e20; }}
            .btn-blue {{ background-color: #0d47a1; }}
            .btn-dark {{ background-color: #37474f; }}
            .btn-magenta {{ background-color: #880e4f; }}
            
            /* Storico domande: formattazione pulita */
            .domanda-box {{
                background: #11141a; 
                padding: 10px; 
                border-radius: 6px; 
                margin-bottom: 8px; 
                border-left: 4px solid #81c784; 
                text-align: left;
                width: 100%;
                box-sizing: border-box;
            }}

            /* --- REGOLE SPECIFICHE PER MOBILE --- */
            @media (max-width: 600px) {{
                body {{ padding: 5px; }} /* Margine ancora più ridotto */
                .container {{ padding: 0 5px; }}
                .header {{ padding: 15px; border-radius: 8px; }}
                .header h1 {{ font-size: 19px; }}
                .card {{ padding: 15px; border-radius: 8px; }}
                h2 {{ font-size: 17px; }}
                
                /* I pulsanti di navigazione occupano tutta la larghezza per facilità di tocco */
                .btn-nav {{ font-size: 13px; padding: 12px 5px; max-width: 100%; }}
                
                /* La textarea Q&A deve stare dentro */
                textarea {{ font-size: 14px; padding: 8px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💀 MINECRAFT HARDCORE HUB 💀</h1>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Benvenuto Recluta. Scegli il tuo modulo di addestramento.</p>
            </div>
            
            {alert_box}
            {qa_banner}
            {auth_section}

            <div class="card">
                <h2>🗂️ MANUALI DI SOPRAVVIVENZA DISPONIBILI</h2>
                <p style="font-size: 14px; color: #b0bec5;">Clicca sulle guide per studiare le minacce e l'ambiente dell'Overworld:</p>
                
                <a href="/guida-avanzata" class="btn btn-nav btn-purple">📖 ACCEDI AL PROTOCOLLO GIORNO 1 (MINUTO PER MINUTO)</a>
                <a href="/mob-guide" class="btn btn-nav btn-orange">🧟 BESTIARIO: GUIDA AI MOB E MINACCE</a>
                <a href="/biomi-guide" class="btn btn-nav btn-green">🌲 CARTOGRAFIA: TUTTI I BIOMI DELL'OVERWORLD</a>
                <a href="/craft-guide" class="btn btn-nav btn-blue">🛠️ OFFICINA: COSTRUZIONI E CRAFTING SALVAVITA</a>
                <a href="/farms-guide" class="btn btn-nav btn-dark">⚙️ AUTOMAZIONE: FARM SEMPLICI E VITALI</a>
                <a href="/enchants-guide" class="btn btn-nav btn-magenta">🔮 ARCANO: INCANTESIMI PERFETTI (GOD ROLL)</a>
            </div>

            <div class="card" style="background: #141820;">
                <h3 style="margin-top: 0; font-size: 16px; color: #90a4ae;">Ultimi Survivalist Registrati:</h3>
                <ul style="padding-left: 20px; color: #b0bec5; margin-bottom: 0;">{utenti_html}</ul>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- ENDPOINT REGISTRAZIONE ---
@app.post("/register")
async def register_user(response: Response, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO utenti (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        msg = f"Grande {username}, registrato con successo!"
        redirect = RedirectResponse(url=f"/?msg={msg}", status_code=303)
        redirect.set_cookie(key="session_user", value=username, max_age=3600)
        return redirect
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return RedirectResponse(url="/?msg=Errore:+Username+gia+esistente!", status_code=303)
    finally:
        conn.close()

# --- ENDPOINT LOGIN ---
@app.post("/login")
async def login_user(response: Response, username: str = Form(...), password: str = Form(...)):
    # Tutto il codice qui sotto deve essere indentato di 4 spazi!
    conn = get_db_connection()
    cursor = conn.cursor()
    # ATTENZIONE: Usa %s invece di ? per PostgreSQL
    cursor.execute("SELECT username FROM utenti WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        msg = f"Accesso eseguito. Bentornato {user[0]}!"
        redirect = RedirectResponse(url=f"/?msg={msg}", status_code=303)
        redirect.set_cookie(key="session_user", value=user[0], max_age=3600)
        return redirect
    else:
        return RedirectResponse(url="/?msg=Credenziali+errate!+Riprova.", status_code=303)

# --- ENDPOINT LOGOUT ---
@app.get("/logout")
async def logout_user():
    redirect = RedirectResponse(url="/?msg=Sessione+chiusa+correttamente.", status_code=303)
    redirect.delete_cookie("session_user")
    return redirect

# --- ENDPOINT PER SALVARE LA DOMANDA ---
@app.post("/invia-domanda")
async def invia_domanda(request: Request, testo_domanda: str = Form(...)):
    session_user = request.cookies.get("session_user")
    if not session_user:
        return RedirectResponse(url="/?msg=Errore:+Devi+effettuare+il+login!", status_code=303)
        
    conn = get_db_connection()
    cursor = conn.cursor()  # <-- Allineato perfettamente a sinistra con conn = ...
    cursor.execute("INSERT INTO domande (username, testo) VALUES (%s, %s)", (session_user, testo_domanda))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/?msg=Domanda+pubblicata+nella+Taverna!", status_code=303)

# --- PAGINA 2: GUIDA AVANZATA MINUTO PER MINUTO ---
@app.get("/guida-avanzata", response_class=HTMLResponse)
async def guida_avanzata():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Manuale Avanzato Giorno 1</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0b0d12; color: #e3e6eb; padding: 15px; display: flex; flex-direction: column; align-items: center; margin: 0; box-sizing: border-box; }
            .container { max-width: 700px; width: 100%; box-sizing: border-box; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #4a148c, #880e4f); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #151922; border: 1px solid #252d3d; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-sizing: border-box; }
            h2 { color: #ba68c8; margin-top: 0; }
            .timeline-step { border-left: 3px dashed #ba68c8; padding-left: 15px; margin-bottom: 25px; }
            .time-title { color: #e1bee7; font-weight: bold; margin: 0 0 5px 0; }
            .desc { color: #b0bec5; line-height: 1.6; margin: 0; font-size: 15px; }
            .btn { background-color: #37474f; color: white; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; text-align: center; }
            @media (max-width: 600px) { .header h1 { font-size: 18px; } .card { padding: 15px; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📖 PROTOCOLLO DI SOPRAVVIVENZA DETTAGLIATO</h1>
                <p style="margin:5px 0 0 0;">La timeline ufficiale dei primi 20 minutes di gioco</p>
            </div>

            <div class="card">
                <h2>⏱️ Cronologia Minuto per Minuto</h2>
                <div class="timeline-step"><p class="time-title">Minuto 0:00 - Lo Spawn</p><p class="desc">Prendi le coordinate (F3) e corri subito a cercare alberi. Non perdere tempo.</p></div>
                <div class="timeline-step"><p class="time-title">Minuto 1:30 - Primi Strumenti</p><p class="desc">Rompi 4 alberi, fatti un piccone di legno e scava sotto terra per trovare la pietra.</p></div>
                <div class="timeline-step"><p class="time-title">Minuto 3:00 - Età della Pietra & Caccia</p><p class="desc">Fatti gli attrezzi in pietra. Trova 3 pecore dello stesso colore per il letto. La lana è fondamentale per skippare la notte.</p></div>
                <div class="timeline-step"><p class="time-title">Minuto 6:00 - Fornace e Cibo</p><p class="desc">Crea carbonella se non trovi carbone. Cuoci la carne, non mangiarla cruda o perderai saturazione velocemente.</p></div>
                <div class="timeline-step"><p class="time-title">Minuto 9:00 - Il Tramonto</p><p class="desc">Se hai il letto dormi. Se non ce l'hai, scavati un buco 1x1 profondo tre blocchi sotto i piedi e tappati dentro.</p></div>
                <div class="timeline-step"><p class="time-title">Minuto 10:00 - Scavo Notturno</p><p class="desc">Mentre sei chiuso al buio, scava a scaletta verso il basso per cercare ferro. Illumina sempre per evitare spawn interni.</p></div>
                <div class="timeline-step"><p class="time-title">Minuto 20:00 - L'Alba del Giorno 2</p><p class="desc">I mostri bruciano fuori. Esci con cautela (occhio ai creeper) e inizia a costruire la tua base!</p></div>

                <a href="/" class="btn">⬅️ Torna all'Hub Principale</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- PAGINA 3: GUIDA AI MOB ---
@app.get("/mob-guide", response_class=HTMLResponse)
async def mob_guide():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bestiario Overworld - Hardcore Tactical</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0c0f14; color: #e3e6eb; padding: 15px; display: flex; flex-direction: column; align-items: center; margin: 0; box-sizing: border-box; }
            .container { max-width: 750px; width: 100%; box-sizing: border-box; }
            .header { text-align: center; padding: 20px; background: linear-gradient(135deg, #e65100, #bf360c); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #171c26; border: 1px solid #2d374a; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-sizing: border-box; }
            h2 { color: #ffb74d; margin-top: 0; border-bottom: 1px solid #2d374a; padding-bottom: 8px; margin-bottom: 20px; font-size: 18px; }
            .mob-entry { margin-bottom: 30px; padding-left: 15px; border-left: 4px solid #ff9800; }
            .mob-name { font-weight: bold; color: #ffa726; font-size: 18px; display: block; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
            .danger-high { border-left-color: #d32f2f; }
            .danger-high .mob-name { color: #f44336; }
            .field-row { display: flex; margin: 8px 0; font-size: 15px; line-height: 1.5; align-items: flex-start; }
            .field-label { font-weight: bold; color: #cfd8dc; width: 140px; flex-shrink: 0; }
            .field-val { color: #b0bec5; flex-grow: 1; }
            .highlight-red { color: #ff5252; font-weight: bold; }
            .btn { background-color: #37474f; color: white; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            
            @media (max-width: 600px) {
                .field-row { flex-direction: column; }
                .field-label { width: 100%; margin-bottom: 2px; }
                .header h1 { font-size: 18px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧟 SCHEDE TATTICHE DEI MOB (DIFFICOLTÀ HARDCORE)</h1>
                <p style="margin:5px 0 0 0; font-size:14px;">Analisi balistica dei rompicoglioni e delle risorse utili. Niente contorni inutili.</p>
            </div>

            <div class="card">
                <h2>🚨 FONDAMENTALI DEL SOPRAMONDO (CHI TI VUOLE MORTO)</h2>
                <div class="mob-entry danger-high">
                    <span class="mob-name">🟢 Creeper</span>
                    <div class="field-row"><span class="field-label">Minaccia:</span><span class="field-val highlight-red">Esplosione ravvicinata fatale al 100% senza scudo (64 punti danno).</span></div>
                    <div class="field-row"><span class="field-label">Strategia:</span><span class="field-val">Se senti "ssss", scudo alzato istantaneamente (azzera il danno) o colpiscilo correndo all'indietro pe' resettare il timer.</span></div>
                    
                    <img src="/static/creeper.png" alt="Creeper" style="width: 150px; margin-top: 10px; display: block;">
                </div>
                <div class="mob-entry danger-high">
                    <span class="mob-name">🔮 Enderman</span>
                    <div class="field-row"><span class="field-label">Minaccia:</span><span class="field-val highlight-red">Danni pesanti da mischia e teletrasporto imprevedibile.</span></div>
                    <div class="field-row"><span class="field-label">Strategia:</span><span class="field-val">Non lo guardà negli occhi. Se succede, buttati in acqua o piazzati sotto una tettoia alta esattamente 2 blocchi: tu lo meni e lui resta a guardà.</span></div>
                </div>
                <div class="mob-entry">
                    <span class="mob-name">🦇 Phantom</span>
                    <div class="field-row"><span class="field-label">Minaccia:</span><span class="field-val">Attacchi aerei a sciame se non dormi da più di 3 giorni di fila.</span></div>
                    <div class="field-row"><span class="field-label">Strategia:</span><span class="field-val">Basta cliccare su un letto la notte per resettare il timer dello spawn. Se arrivano, tiragli giù con l'arco mentre picchiano.</span></div>
                </div>
            </div>

            <div class="card">
                <h2>🔥 INFERNO E FINE (NETHER & END)</h2>
                <div class="mob-entry danger-high">
                    <span class="mob-name">🔥 Blaze</span>
                    <div class="field-row"><span class="field-label">Utilità:</span><span class="field-val">Rilasciano le Verghe (Blaze Rod), essenziali per le pozioni e per finire il gioco.</span></div>
                    <div class="field-row"><span class="field-label">Strategia:</span><span class="field-val">Sparano raffiche di 3 palle di fuoco. Usa lo scudo o bersagliali da lontano con le palle di neve, che subiscono danni massicci da freddo.</span></div>
                </div>
                <div class="mob-entry danger-high">
                    <span class="mob-name">🐷 Piglin Brute</span>
                    <div class="field-row"><span class="field-label">Minaccia:</span><span class="field-val highlight-red">Ti attaccano pure se hai l'armatura d'oro. Hanno un'ascia che spacca gli scudi.</span></div>
                    <div class="field-row"><span class="field-label">Strategia:</span><span class="field-val">Non affrontarli mai corpo a corpo. Murati vivo e crea una fessura per colpirgli i piedi o buttali giù nei burroni con l'arco.</span></div>
                </div>
            </div>

            <div class="card">
                <h2>👑 I PEZZI GROSSI (BOSS FIGHTS & BESTIE)</h2>
                <div class="mob-entry danger-high">
                    <span class="mob-name">🐉 Ender Dragon & Wither</span>
                    <div class="field-row"><span class="field-label">Strategia Drago:</span><span class="field-val">Rompi prima tutti i cristalli sulle torri d'ossidiana (usa le frecce). Quando scende al centro, colpiscilo sotto la pancia o usa i letti che esplodono.</span></div>
                    <div class="field-row"><span class="field-label">Strategia Wither:</span><span class="field-val">Evocalo sotto terra, a livello della Bedrock drento a una galleria stretta 1x2. Così non può volare e lo scassi a colpi di spada in totale sicurezza.</span></div>
                </div>
                <div class="mob-entry danger-high">
                    <span class="mob-name">🔊 Il Warden</span>
                    <div class="field-row"><span class="field-label">Minaccia:</span><span class="field-val highlight-red">Ti shotta pure se hai l'armatura di Netherite. Spara un raggio sonoro che passa attraverso i muri.</span></div>
                    <div class="field-row"><span class="field-label">Strategia:</span><span class="field-val">NON CI DEVI COMBATTERE. Cammina sempre accucciato (Shift) nei Deep Dark. Tira palle di neve lontano da te per distrarre i sensori e scappa via.</span></div>
                </div>
            </div>

            <div class="card">
                <h2>💼 I MOB UTILI (ECONOMIA E STRATEGIA)</h2>
                <div class="mob-entry" style="border-left-color: #4caf50;">
                    <span class="mob-name">🌾 Villager & Zombie Villager</span>
                    <div class="field-row"><span class="field-label">Utilità:</span><span class="field-val">I bibliotecari vendono i libri perfetti (Mending, Protezione IV) senza passare per la casualità del tavolo.</span></div>
                    <div class="field-row"><span class="field-label">Il Trucco:</span><span class="field-val">Falli infettare da uno zombie a difficoltà Hard (si convertono sempre) e curali con pozione di debolezza + mela d'oro: sconti fissi a 1 solo smeraldo.</span></div>
                </div>
            </div>

            <a href="/" class="btn">⬅️ Torna all'Hub Principale</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- PAGINA 4: GUIDA AI BIOMI ---
@app.get("/biomi-guide", response_class=HTMLResponse)
async def biomi_guide():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartografia Overworld - Hardcore Full Guide</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0c0f14; color: #e3e6eb; padding: 15px; display: flex; flex-direction: column; align-items: center; margin: 0; box-sizing: border-box; }
            .container { max-width: 800px; width: 100%; box-sizing: border-box; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #1b5e20, #004d40); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #171c26; border: 1px solid #2d374a; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-sizing: border-box; }
            h2 { color: #81c784; margin-top: 0; border-bottom: 1px solid #2d374a; padding-bottom: 8px; margin-bottom: 25px; font-size: 18px; }
            .biome-entry { margin-bottom: 30px; padding-left: 15px; border-left: 4px solid #4caf50; }
            .biome-name { font-weight: bold; color: #a5d6a7; font-size: 18px; display: block; margin-bottom: 10px; text-transform: uppercase; }
            .biome-neutral { border-left-color: #ffb74d; }
            .biome-neutral .biome-name { color: #ffe082; }
            .biome-danger { border-left-color: #e53935; }
            .biome-danger .biome-name { color: #ef5350; }
            .b-row { display: flex; margin: 5px 0; font-size: 15px; }
            .b-label { font-weight: bold; color: #cfd8dc; width: 130px; flex-shrink: 0; }
            .b-val { color: #b0bec5; flex-grow: 1; }
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            
            @media (max-width: 600px) {
                .b-row { flex-direction: column; }
                .b-label { width: 100%; margin-bottom: 2px; }
                .header h1 { font-size: 18px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌲 ENCICLOPEDIA DEI BIOMI OVERWORLD</h1>
                <p style="margin:5px 0 0 0; font-size:14px;">Analisi sistematica di ogni ambiente, risorse disponibili, strutture e fattori di rischio.</p>
            </div>

            <div class="card">
                <h2>🟢 BIOMI FAVOREVOLI (Ideali per Spawn e Basi)</h2>
                <div class="biome-entry">
                    <span class="biome-name">Pianura (Plains / Sunflower Plains)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Mucche, pecore, maiali, cavalli, api, fiumi.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Villaggi (altissima probabilità), avamposto dei predoni.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Molto basso. Visibilità totale di notte.</span></div>
                </div>
                <div class="biome-entry">
                    <span class="biome-name">Foresta Standard (Forest / Flower Forest)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Legno di quercia e betulla, lupi, fiori.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Rari portali rovinati, stagniche di lava superficiali.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Basso. Ottimo per fare scorta di legname.</span></div>
                </div>
                <div class="biome-entry">
                    <span class="biome-name">Prateria (Meadow)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Pecore, asini, distese enormi di fiori, alberi solitari con alveari.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Villaggi montani, rari avamposti.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Molto basso. Ottima altitudine e visibilità.</span></div>
                </div>
            </div>

            <div class="card">
                <h2>🟡 BIOMI INTERMEDI (Risorse utili ma occhio ai pericoli)</h2>
                <div class="biome-entry biome-neutral">
                    <span class="biome-name">Taiga (Taiga / Old Growth Pine / Snowy Taiga)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Legno di abete (Spruce), bacche dolci, lupi, volpi.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Villaggi della taiga, capanni delle streghe.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Medio. Le bacche spinose possono rallentarti mentre scappi.</span></div>
                </div>
                <div class="biome-entry biome-neutral">
                    <span class="biome-name">Giungla (Jungle / Sparse Jungle / Bamboo Jungle)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Legno di giungla, bamboo infinito, cacao, meloni, pappagalli.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Templi della giungla (pieni di trappole).</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Medio-Alto. La vegetazione fittissima azzera la visibilità diurna.</span></div>
                </div>
                <div class="biome-entry biome-neutral">
                    <span class="biome-name">Savana (Savanna / Windswept Savanna)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Legno di acacia, lama, cavalli. Pioggia assente.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Villaggi della savana, avamposti dei predoni.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Medio. Terreno sconnesso con burroni improvvisi nell'erba.</span></div>
                </div>
                <div class="biome-entry biome-neutral">
                    <span class="biome-name">Oceano (Ocean / Cold, Frozen Ocean)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Pesci, alghe, coralli, delfini, blocchi di ghiaccio.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Monumenti oceanici, relitti di navi, rovine marine.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Medio. Rischio annegamento e attacchi de 'Annegati' con tridente.</span></div>
                </div>
                <div class="biome-entry biome-neutral">
                    <span class="biome-name">Palude (Swamp / Mangrove Swamp)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Legno di mangrovia, rane, slime superficiali, ninfee.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Capanne delle streghe (Witch Huts).</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Medio-Alto. Fango e acqua rallentano; le streghe lanciano veleni.</span></div>
                </div>
            </div>

            <div class="card">
                <h2>🔴 BIOMI AD ALTO RISCHIO (Massima Attenzione o Fuga)</h2>
                <div class="biome-entry biome-danger">
                    <span class="biome-name">Deserto (Desert)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Sabbia, cactus, conigli. Manca il legno e cibo superficiale.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Templi del deserto (trappole esplosive), villaggi.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Alto. Pieno zeppo di Husk che non bruciano e infliggono Fame.</span></div>
                </div>
                <div class="biome-entry biome-danger">
                    <span class="biome-name">Foresta Oscura (Dark Forest)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Legno di quercia scura, funghi giganti.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Magione della Foresta (Woodland Mansion).</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Alto. Fronde fitte creano buio pesto: mostri presenti anche a mezzogiorno.</span></div>
                </div>
                <div class="biome-entry biome-danger">
                    <span class="biome-name">Calanchi (Badlands / Mesa)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Terracotta, sabbia rossa, miniere d'oro superficiali massicce.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Miniere abbandonate all'aperto.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Alto. Mancanza di cibo e legno; ragni delle caverne in superficie.</span></div>
                </div>
                <div class="biome-entry biome-danger">
                    <span class="biome-name">Vette Montuose (Jagged Peaks / Frozen Peaks)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Neve, blocchi di smeraldo grezzi, capre montane.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Avamposti dei predoni d'alta quota.</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Estremo. Il danno da caduta e la neve farinosa sono letali.</span></div>
                </div>
                <div class="biome-entry biome-danger">
                    <span class="biome-name">Deep Dark (Sottosuolo Profondo)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Blocchi di catalizzatori e sensori di Sculk, zero mob classici.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Antica Città (Ancient City).</span></div>
                    <div class="b-row"><span class="b-label">Fattore Rischio:</span><span class="b-val">Totale. Attivando gli urlatori evochi il Warden che ti shotta.</span></div>
                </div>
            </div>

            <a href="/" class="btn">⬅️ Torna all'Hub Principale</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- PAGINA 5: GUIDA AI CRAFTING SALVAVITA ---
@app.get("/craft-guide", response_class=HTMLResponse)
async def craft_guide():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Officina Hardcore - Crafting Consigliati</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #090c10; color: #e3e6eb; padding: 15px; display: flex; flex-direction: column; align-items: center; margin: 0; box-sizing: border-box; }
            .container { max-width: 750px; width: 100%; box-sizing: border-box; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #0d47a1, #002171); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #171c26; border: 1px solid #2d374a; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-sizing: border-box; }
            h2 { color: #64b5f6; margin-top: 0; border-bottom: 1px solid #2d374a; padding-bottom: 8px; margin-bottom: 25px; font-size: 18px; }
            
            .craft-entry { margin-bottom: 35px; border-bottom: 1px dashed #2d374a; padding-bottom: 25px; }
            .craft-entry:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
            .craft-name { font-weight: bold; color: #90caf9; font-size: 19px; display: block; margin-bottom: 8px; text-transform: uppercase; }
            .craft-desc { color: #b0bec5; font-size: 15px; margin-bottom: 15px; line-height: 1.4; }
            
            .craft-box { display: flex; gap: 20px; align-items: center; background: #0f131a; padding: 15px; border-radius: 8px; border: 1px solid #21262d; flex-wrap: wrap; }
            .materials-list { font-size: 14px; color: #cfd8dc; line-height: 1.6; }
            
            .grid-3x3 { display: grid; grid-template-columns: repeat(3, 55px); grid-template-rows: repeat(3, 55px); gap: 4px; background: #444; padding: 6px; border-radius: 4px; flex-shrink: 0; width: 173px; }
            .grid-cell { background: #8b8b8b; border: 2px solid #3c3c3c; border-top-color: #b5b5b5; border-left-color: #b5b5b5; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: #111; text-align: center; font-family: monospace; word-wrap: break-word; overflow: hidden; padding: 2px; text-shadow: 1px 1px 0px #aaa; }
            .grid-cell:empty { background: #8b8b8b; }
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            
            @media (max-width: 600px) {
                .header h1 { font-size: 18px; }
                .craft-box { justify-content: center; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛠️ OFFICINA HARDCORE: ARTIGIANATO SALVAVITA</h1>
                <p style="margin:5px 0 0 0; font-size:14px;">La disposition esatta dei blocchi nella tavola da crafting per gli oggetti indispensabili.</p>
            </div>

            <div class="card">
                <h2>📐 SCHEMI DI MONTAGGIO CRUCIALI</h2>

                <div class="craft-entry">
                    <span class="craft-name">🛡️ Lo Scudo (Giorno 1 Priority)</span>
                    <p class="craft-desc">L'oggetto più importante del gioco. Azzera completamente il danno da esplosione ravvicinata dei creeper e blocca le frecce degli scheletri.</p>
                    <div class="craft-box">
                        <div class="grid-3x3">
                            <div class="grid-cell">ASSI</div><div class="grid-cell">FERRO</div><div class="grid-cell">ASSI</div>
                            <div class="grid-cell">ASSI</div><div class="grid-cell">ASSI</div><div class="grid-cell">ASSI</div>
                            <div class="grid-cell"></div><div class="grid-cell">ASSI</div><div class="grid-cell"></div>
                        </div>
                        <div class="materials-list">
                            <b>Materiali Richiesti:</b><br>
                            • 6x Assi di legno (qualsiasi tipo)<br>
                            • 1x Lingotto di Ferro
                        </div>
                    </div>
                </div>

                <div class="craft-entry">
                    <span class="craft-name">🪣 Secchio d'Acqua (Anti-Caduta / MLG)</span>
                    <p class="craft-desc">Indispensabile per scalare pareti verticali, spegnere la lava nei sotterranei e piazzare l'acqua sotto i piedi un millisecondo prima di toccare terra per azzerare il danno da caduta.</p>
                    <div class="craft-box">
                        <div class="grid-3x3">
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                            <div class="grid-cell">FERRO</div><div class="grid-cell"></div><div class="grid-cell">FERRO</div>
                            <div class="grid-cell"></div><div class="grid-cell">FERRO</div><div class="grid-cell"></div>
                        </div>
                        <div class="materials-list">
                            <b>Materiali Richiesti:</b><br>
                            • 3x Lingotti di Ferro<br>
                            <i>(Riempilo subito in una sorgente d'acqua!)</i>
                        </div>
                    </div>
                </div>

                <div class="craft-entry">
                    <span class="craft-name">🔥 Acciarino (Flint and Steel)</span>
                    <p class="craft-desc">Usato per accendere istantaneamente il Portale del Nether. Tattica d'emergenza: bruciare il terreno alle tue spalle per cuocere i mob inseguitori o far esplodere forzatamente un creeper da lontano.</p>
                    <div class="craft-box">
                        <div class="grid-3x3">
                            <div class="grid-cell">FERRO</div><div class="grid-cell"></div><div class="grid-cell"></div>
                            <div class="grid-cell"></div><div class="grid-cell">SELCE</div><div class="grid-cell"></div>
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                        </div>
                        <div class="materials-list">
                            <b>Materiali Richiesti:</b><br>
                            • 1x Lingotto di Ferro<br>
                            • 1x Selce (Flint - si trova scavando la ghiaia)
                        </div>
                    </div>
                </div>

                <div class="craft-entry">
                    <span class="craft-name">👁️ Occhio di Ender (Portali ed Endgame)</span>
                    <p class="craft-desc">Essenziale per localizzare la Fortezza (Stronghold) lanciandolo in aria e indispensabile per attivare il portale che conduce all'End per battere il Drago.</p>
                    <div class="craft-box">
                        <div class="grid-3x3">
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                            <div class="grid-cell">ENDER<br>PEARL</div><div class="grid-cell">POLV.<br>BLAZE</div><div class="grid-cell"></div>
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                        </div>
                        <div class="materials-list">
                            <b>Materiali Richiesti:</b><br>
                            • 1x Perla di Ender (Uccidendo Enderman)<br>
                            • 1x Polvere de Blaze (Craftando le verghe dei Blaze nel Nether)
                        </div>
                    </div>
                </div>

            </div>

            <a href="/" class="btn">⬅️ Torna all'Hub Principale</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- PAGINA 6: GUIDA ALLE FARM SALVAVITA ---
@app.get("/farms-guide", response_class=HTMLResponse)
async def farms_guide():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Automazione Hardcore - Farm Semplici</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0e1117; color: #e3e6eb; padding: 15px; display: flex; flex-direction: column; align-items: center; margin: 0; box-sizing: border-box; }
            .container { max-width: 750px; width: 100%; box-sizing: border-box; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #37474f, #21272a); border-radius: 12px; margin-bottom: 20px; border: 1px solid #455a64; }
            .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-sizing: border-box; }
            h2 { color: #cfd8dc; margin-top: 0; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 25px; font-size: 18px; }
            
            .farm-entry { margin-bottom: 35px; border-left: 4px solid #81c784; padding-left: 15px; }
            .farm-name { font-weight: bold; color: #a5d6a7; font-size: 19px; display: block; margin-bottom: 6px; text-transform: uppercase; }
            .farm-meta { font-size: 14px; color: #ffb74d; margin-bottom: 12px; font-weight: 500; }
            .farm-text { color: #b0bec5; font-size: 15px; line-height: 1.5; margin-bottom: 10px; }
            
            .steps-box { background: #0d1117; padding: 15px; border-radius: 8px; border: 1px solid #21262d; margin-top: 10px; box-sizing: border-box; }
            .steps-box ul { margin: 0; padding-left: 15px; color: #e3e6eb; font-size: 14px; line-height: 1.6; }
            .steps-box li { margin-bottom: 6px; }
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            @media (max-width: 600px) { .header h1 { font-size: 18px; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚙️ PROTOCOLLO DI AUTOMAZIONE: FARM VITALI</h1>
                <p style="margin:5px 0 0 0; font-size:14px;">3 strutture banali da tirare su in 5 minuti per assicurarti risorse infinite senza rischiare la vita.</p>
            </div>

            <div class="card">
                <h2>🌱 LE STRUTTURE ANTICRISI DI EARLY-GAME</h2>

                <div class="farm-entry" style="border-left-color: #ffb74d;">
                    <span class="farm-name">🍗 Micro-Farm di Pollo Cotto Automatica</span>
                    <div class="farm-meta">Fattore Utilità: Cibo Infinito + Piume (per le Frecce) | Difficoltà: Ridicola</div>
                    <p class="farm-text">Ti permette di avere cibo cotto sfornato H24 senza sprecare carbone o inseguire animali di notte. Sfrutta l'entità dei blocchi e la lava per cuocere solo i polli adulti.</p>
                    <div class="steps-box">
                        <b>Materiali:</b> 1x Cassa, 2x Tramogge (Hopper), 1x Distributore (Dispenser), 1x Lastra (Slab), 1x Secchio di Lava, Blocchi di vetro, 1x Comparatore di redstone.<br><br>
                        <b>Come montarla:</b>
                        <ul>
                            <li>Piazza la cassa a terra e collegaci dietro una tramoggia. Dietro la tramoggia metti il distributore rivolto verso la cassa.</li>
                            <li>Sopra la tramoggia metti una mezza lastra di pietra. Sopra il distributore metti un'altra tramoggia (lì andranno i polli genitori).</li>
                            <li>Chiudi tutto il perimetro con blocchi di vetro alti due blocchi. Sopra lo spazio vuoto della prima tramoggia, metti un secchio di lava (al secondo blocco d'altezza).</li>
                            <li>Fai un piccolo circuito dietro che attiva il distributore ogni volta che riceve un uovo dalla tramoggia dei genitori.</li>
                            <li>I polli piccoli nascono sulla lastra sotto la lava. Quando crescono, toccano la lava, bruciano e il pollo cotto cade dritto nella cassa!</li>
                        </ul>
                    </div>
                </div>

                <div class="farm-entry" style="border-left-color: #64b5f6;">
                    <span class="farm-name">📜 Farm di Canna da Zucchero (Carta per Smeraldi)</span>
                    <div class="farm-meta">Fattore Utilità: Libri per Incantesimi + Smeraldi Infiniti coi Villager | Difficoltà: Bassa</div>
                    <p class="farm-text">La canna da zucchero serve per fare la carta. La carta la vendi ai villager bibliotecari per fare smeraldi puliti o ci fai i libri per la tavola degli incantesimi a Livello 30.</p>
                    <div class="steps-box">
                        <b>Materiali:</b> Canne da zucchero, 1x Secchio d'acqua, Blocchi di terra, Pistoni normali, Osservatori (Observer), Polvere di Redstone, Tramoggia e Cassa.<br><br>
                        <b>Come montarla:</b>
                        <ul>
                            <li>Scava un solco lungo 8 blocchi, riempilo d'acqua e piazza una fila di terra accanto. In fondo al flusso d'acqua metti una tramoggia legata a una cassa.</li>
                            <li>Pianta la canna da zucchero sulla terra lungo l'acqua. Dietro la canna da zucchero, alza un muro di blocchi solidi.</li>
                            <li>Sopra questo muro, piazza una fila di pistoni normali rivolti verso la canna da zucchero (all'altezza del secondo blocco della pianta).</li>
                            <li>Sopra i pistoni, piazza gli osservatori rivolti con la "faccia" verso la pianta (altezza terzo blocco). Dietro i pistoni metti una striscia di polvere di redstone.</li>
                            <li>Appena la canna cresce al terzo blocco, l'osservatore la vede, attiva la redstone e i pistoni tagliano la pianta al secondo blocco facendola cadere nell'acqua verso la cassa.</li>
                        </ul>
                    </div>
                </div>

                <div class="farm-entry" style="border-left-color: #ef5350;">
                    <span class="farm-name">🪨 Generatore Sicuro di Cobblestone (Anti-Scavo)</span>
                    <div class="farm-meta">Fattore Utilità: Blocchi da costruzione senza scendere in miniera | Difficoltà: Elementare</div>
                    <p class="farm-text">Scendere in miniera per prendere pietra da costruzione è un rischio inutile in Hardcore. Con questo generatore ti barrichi dentro casa e mini all'infinito in totale sicurezza.</p>
                    <div class="steps-box">
                        <b>Materiali:</b> 1x Secchio d'Acqua, 1x Secchio di Lava, Blocchi ininfiammabili (Pietra o Mattoni).<br><br>
                        <b>Come montarla:</b>
                        <ul>
                            <li>Scava un linea retta di 4 blocchi nel terreno.</li>
                            <li>Nel secondo foro da sinistra, scava un blocco in più verso il basso (diventa profondo 2 blocchi). Questo serve per far defluire l'acqua.</li>
                            <li>Metti l'acqua nell'estrema sinistra (blocco 1). L'acqua scorrerà e cadrà nel buco profondo senza avanzare oltre.</li>
                            <li>Metti la lava nell'estrema destra (blocco 4).</li>
                            <li>La lava andrà a toccare l'acqua che scorre dal buco e, nel punto di contatto (blocco 3), si creerà istantaneamente un blocco di Cobblestone infinito da minare!</li>
                        </ul>
                    </div>
                </div>

            </div>

            <a href="/" class="btn">⬅️ Torna all'Hub Principale</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- PAGINA 7: GUIDA AGLI INCANTESIMI ---
@app.get("/enchants-guide", response_class=HTMLResponse)
async def enchants_guide():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grimorio degli Incantesimi Perfetti - Hardcore Edition</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d0914; color: #e3e6eb; padding: 15px; display: flex; flex-direction: column; align-items: center; margin: 0; box-sizing: border-box; }
            .container { max-width: 780px; width: 100%; box-sizing: border-box; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #4a148c, #6a1b9a); border-radius: 12px; margin-bottom: 20px; border: 1px solid #7b1fa2; }
            .card { background-color: #161224; border: 1px solid #3c245c; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-sizing: border-box; }
            h2 { color: #e1bee7; margin-top: 0; border-bottom: 1px solid #3c245c; padding-bottom: 8px; margin-bottom: 25px; text-transform: uppercase; font-size: 18px; }
            
            .gear-box { background: #211a36; border: 1px solid #4a3475; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
            .gear-title { font-weight: bold; color: #f3e5f5; font-size: 16px; display: block; margin-bottom: 10px; border-left: 3px solid #ba68c8; padding-left: 10px; }
            
            .enchant-badge { display: inline-block; background: #4a148c; color: #f3e5f5; font-size: 12px; font-weight: bold; padding: 4px 8px; border-radius: 4px; margin: 4px 4px 4px 0; font-family: monospace; border: 1px solid #7b1fa2; }
            .enchant-badge.meta { background: #880e4f; border-color: #c2185b; }
            
            .strat-list { padding-left: 15px; font-size: 15px; color: #b0bec5; line-height: 1.6; }
            .strat-list li { margin-bottom: 10px; }
            .highlight-purple { color: #ce93d8; font-weight: bold; }
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            @media (max-width: 600px) { .header h1 { font-size: 18px; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔮 IL GRIMORIO DEGLI INCANTESIMI PERFETTI (GOD ROLLS)</h1>
                <p style="margin:5px 0 0 0; font-size:14px;">La lista definitiva delle combinazioni massime e la strategia infallibile dei Villager per ottenerle al 100%.</p>
            </div>

            <div class="card">
                <h2>🛡️ I SET COMPLETI AL LIVELLO MASSIMO</h2>
                <p style="color:#b0bec5; margin-top:0; font-size:14px;">Ecco gli incantesimi precisi da schiaffare su ogni pezzo per azzerare i rischi di morte:</p>

                <div class="gear-box">
                    <span class="gear-title">🪖 Elmo (Helmet)</span>
                    <span class="enchant-badge">Protezione IV</span>
                    <span class="enchant-badge">Affinità all'Acquatico I</span>
                    <span class="enchant-badge">Respirazione III</span>
                    <span class="enchant-badge">Indistruttibilità III</span>
                    <span class="enchant-badge meta">Ripristino (Mending)</span>
                </div>

                <div class="gear-box">
                    <span class="gear-title">👕 Pettorale (Chestplate) - Salvavita Antiesplosione</span>
                    <span class="enchant-badge">Protezione IV</span>
                    <span class="enchant-badge">Spine III (Opzionale)</span>
                    <span class="enchant-badge">Indistruttibilità III</span>
                    <span class="enchant-badge meta">Ripristino (Mending)</span>
                </div>

                <div class="gear-box">
                    <span class="gear-title">👖 Gambali (Leggings)</span>
                    <span class="enchant-badge">Protezione IV</span>
                    <span class="enchant-badge">Passo Rapido Furtivo III (Antica Città)</span>
                    <span class="enchant-badge">Indistruttibilità III</span>
                    <span class="enchant-badge meta">Ripristino (Mending)</span>
                </div>

                <div class="gear-box">
                    <span class="gear-title">🥾 Stivali (Boots) - Anti Danno da Caduta</span>
                    <span class="enchant-badge">Protezione IV</span>
                    <span class="enchant-badge">Atterraggio Morbido IV (Feather Falling)</span>
                    <span class="enchant-badge">Passo Anfibio III</span>
                    <span class="enchant-badge">Agilità d'Anima III (Nether)</span>
                    <span class="enchant-badge">Indistruttibilità III</span>
                    <span class="enchant-badge meta">Ripristino (Mending)</span>
                </div>

                <div class="gear-box">
                    <span class="gear-title">⚔️ Spada (Sword)</span>
                    <span class="enchant-badge">Affilatezza V (Sharpness)</span>
                    <span class="enchant-badge">Contraccolpo II (Knockback - tiene lontani i Creeper!)</span>
                    <span class="enchant-badge">Aspetto di Fuoco II</span>
                    <span class="enchant-badge">Saccheggio III (Looting)</span>
                    <span class="enchant-badge">Indistruttibilità III</span>
                    <span class="enchant-badge meta">Ripristino (Mending)</span>
                </div>
            </div>

            <div class="card">
                <h2>📈 STRATEGIA: RECLUTAMENTO DEI BIBLIOTECARI (NO RANDOM)</h2>
                <p style="color:#b0bec5; margin-top:0; font-size:14px;">Affidarsi alla Tavola degli Incantesimi è un suicidio di risorse. La vera tattica Hardcore prevede l'abuso dei <span class="highlight-purple">Villager Bibliotecari</span>:</p>
                
                <ul class="strat-list">
                    <li><span class="highlight-purple">Il Ciclo del Leggìo (Lectern):</span> Intrappola un villager disoccupato in uno spazio 1x2. Piazza un Leggìo davanti a lui per farlo diventare Bibliotecario. Controlla il suo primo libro in vendita. Se NON è quello che vuoi (es. cerchi Mending o Protezione IV), rompi il leggìo con l'ascia e ripiazzalo subito. Il villager cambierà istantaneamente inventario. Ripeti finché non esce il libro perfetto.</li>
                    <li><span class="highlight-purple">Bloccare il Prezzo:</span> Appena esce il libro che desideri, fai **un singolo scambio** con lui (compra un libro o vendigli della carta). Questo bloccherà la sua professione e i suoi scambi per sempre, impedendogli di resettarsi.</li>
                    <li><span class="highlight-purple">Sconti da Zombie (Opzione Avanzata):</span> Fai trasformare il villager bloccato da uno zombie a difficoltà Difficile (in Hardcore si converte al 100%, non muore). Poi curalo con una <span class="highlight-purple">Pozione da Lancio di Debolezza</span> e una <span class="highlight-purple">Mela d'Oro</span>. Ti abbasserà il costo dei libri massimi a 1 solo Smeraldo!</li>
                </ul>

                <a href="/" class="btn">⬅️ Torna all'Hub Principale</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
