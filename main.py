from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3

app = FastAPI()

# --- LOGICA DEL DATABASE ---
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- PAGINA 1: HOME PAGE (Hub Principale) ---
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, msg: str = None):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM utenti ORDER BY id DESC LIMIT 5")
    ultimi_utenti = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    utenti_html = "".join([f"<li>{u}</li>" for u in ultimi_utenti]) or "<li>Nessun player registrato</li>"
    alert_box = f'<div style="background:#238636; padding:10px; border-radius:6px; margin-bottom:20px;">{msg}</div>' if msg else ""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Minecraft Hardcore Survival Hub</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #11141a; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }}
            .container {{ max-width: 650px; width: 100%; }}
            .header {{ text-align: center; padding: 20px; background: linear-gradient(135deg, #b71c1c, #7f0000); border-radius: 12px; margin-bottom: 20px; }}
            .card {{ background-color: #1c212b; border: 1px solid #2d3545; border-radius: 12px; padding: 25px; margin-bottom: 20px; }}
            h2 {{ color: #e53935; margin-top: 0; }}
            .step {{ border-left: 4px solid #e53935; padding-left: 15px; margin-bottom: 20px; }}
            .form-group {{ margin-bottom: 15px; }}
            input {{ width: 100%; padding: 10px; background: #11141a; border: 1px solid #2d3545; border-radius: 6px; color: #fff; box-sizing: border-box; }}
            .btn {{ background-color: #e53935; color: white; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; text-decoration: none; display: block; text-align: center; box-sizing: border-box; }}
            .btn-nav {{ margin-top: 12px; font-size: 15px; }}
            .btn-purple {{ background-color: #4a148c; }}
            .btn-purple:hover {{ background-color: #6a1b9a; }}
            .btn-orange {{ background-color: #e65100; }}
            .btn-orange:hover {{ background-color: #f57c00; }}
            .btn-green {{ background-color: #1b5e20; }}
            .btn-green:hover {{ background-color: #2e7d32; }}
            .btn-blue {{ background-color: #0d47a1; }}
            .btn-blue:hover {{ background-color: #1565c0; }}
            .btn-dark {{ background-color: #37474f; }}
            .btn-dark:hover {{ background-color: #455a64; }}
            .btn-magenta {{ background-color: #880e4f; }}
            .btn-magenta:hover {{ background-color: #ad1457; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💀 MINECRAFT HARDCORE HUB 💀</h1>
                <p>Benvenuto Recluta. Scegli il tuo modulo di addestramento.</p>
            </div>
            
            {alert_box}

            <div class="card">
                <h2>🗂️ MANUALI DI SOPRAVVIVENZA DISPONIBILI</h2>
                <p>Clicca sulle guide per studiare le minacce e l'ambiente dell'Overworld:</p>
                
                <a href="/guida-avanzata" class="btn btn-nav btn-purple">📖 ACCEDI AL PROTOCOLLO GIORNO 1 (MINUTO PER MINUTO)</a>
                <a href="/mob-guide" class="btn btn-nav btn-orange">🧟 BESTIARIO: GUIDA AI MOB E MINACCE</a>
                <a href="/biomi-guide" class="btn btn-nav btn-green">🌲 CARTOGRAFIA: TUTTI I BIOMI DELL'OVERWORLD</a>
                <a href="/craft-guide" class="btn btn-nav btn-blue">🛠️ OFFICINA: COSTRUZIONI E CRAFTING SALVAVITA</a>
                <a href="/farms-guide" class="btn btn-nav btn-dark">⚙️ AUTOMAZIONE: FARM SEMPLICI E VITALI</a>
                <a href="/enchants-guide" class="btn btn-nav btn-magenta">🔮 ARCANO: INCANTESIMI PERFETTI (GOD ROLL)</a>
            </div>

            <div class="card">
                <h2>🎮 Unisciti alla Community dei Sopravvissuti</h2>
                <form action="/register" method="post">
                    <div class="form-group">
                        <input type="text" name="username" required placeholder="Username In-Game">
                    </div>
                    <div class="form-group">
                        <input type="email" name="email" required placeholder="Tua Email">
                    </div>
                    <button type="submit" class="btn">Registrati nel Database</button>
                </form>
            </div>

            <div class="card" style="background: #141820;">
                <h3>Ultimi Survivalist Registrati:</h3>
                <ul>{utenti_html}</ul>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- PAGINA 2: GUIDA AVANZATA MINUTO PER MINUTO ---
@app.get("/guida-avanzata", response_class=HTMLResponse)
async def guida_avanzata():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Manuale Avanzato Giorno 1</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0b0d12; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .container { max-width: 700px; width: 100%; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #4a148c, #880e4f); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #151922; border: 1px solid #252d3d; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
            h2 { color: #ba68c8; margin-top: 0; }
            .timeline-step { border-left: 3px dashed #ba68c8; padding-left: 15px; margin-bottom: 25px; }
            .time-title { color: #e1bee7; font-weight: bold; margin: 0 0 5px 0; }
            .desc { color: #b0bec5; line-height: 1.6; margin: 0; }
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background-color: #455a64; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📖 PROTOCOLLO DI SOPRAVVIVENZA DETTAGLIATO</h1>
                <p>La timeline ufficiale dei primi 20 minutes di gioco</p>
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

# --- PAGINA 3: GUIDA AI MOB (Aggiornata e Scremata) ---
@app.get("/mob-guide", response_class=HTMLResponse)
async def mob_guide():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Bestiario Overworld - Hardcore Tactical</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0c0f14; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .container { max-width: 750px; width: 100%; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #e65100, #bf360c); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #171c26; border: 1px solid #2d374a; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
            h2 { color: #ffb74d; margin-top: 0; border-bottom: 1px solid #2d374a; padding-bottom: 8px; margin-bottom: 20px; }
            .mob-entry { margin-bottom: 30px; padding-left: 15px; border-left: 4px solid #ff9800; }
            .mob-name { font-weight: bold; color: #ffa726; font-size: 20px; display: block; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
            .danger-high { border-left-color: #d32f2f; }
            .danger-high .mob-name { color: #f44336; }
            .field-row { display: flex; margin: 8px 0; font-size: 15px; line-height: 1.5; align-items: flex-start; }
            .field-label { font-weight: bold; color: #cfd8dc; width: 160px; flex-shrink: 0; }
            .field-val { color: #b0bec5; flex-grow: 1; }
            .highlight-red { color: #ff5252; font-weight: bold; }
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background-color: #455a64; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧟 SCHEDE TATTICHE DEI MOB (DIFFICOLTÀ HARDCORE)</h1>
                <p>Analisi balistica dei rompicoglioni e delle risorse utili. Niente contorni inutile.</p>
            </div>

            <!-- FONDAMENTALI DEL SOPRAMONDO -->
            <div class="card">
                <h2>🚨 FONDAMENTALI DEL SOPRAMONDO (CHI TI VUOLE MORTO)</h2>
                <div class="mob-entry danger-high">
                    <span class="mob-name">🟢 Creeper</span>
                    <div class="field-row"><span class="field-label">Minaccia:</span><span class="field-val highlight-red">Esplosione ravvicinata fatale al 100% senza scudo (64 punti danno).</span></div>
                    <div class="field-row"><span class="field-label">Strategia:</span><span class="field-val">Se senti "ssss", scudo alzato istantaneamente (azzera il danno) o colpiscilo correndo all'indietro pe' resettare il timer.</span></div>
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

            <!-- PERICOLI DEL NETHER & END -->
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

            <!-- I PEZZI GROSSI -->
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

            <!-- ECONOMIA E LOGISTICA -->
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
        <title>Cartografia Overworld - Hardcore Full Guide</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0c0f14; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .container { max-width: 800px; width: 100%; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #1b5e20, #004d40); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #171c26; border: 1px solid #2d374a; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
            h2 { color: #81c784; margin-top: 0; border-bottom: 1px solid #2d374a; padding-bottom: 8px; margin-bottom: 25px; }
            .biome-entry { margin-bottom: 30px; padding-left: 15px; border-left: 4px solid #4caf50; }
            .biome-name { font-weight: bold; color: #a5d6a7; font-size: 19px; display: block; margin-bottom: 10px; text-transform: uppercase; }
            .biome-neutral { border-left-color: #ffb74d; }
            .biome-neutral .biome-name { color: #ffe082; }
            .biome-danger { border-left-color: #e53935; }
            .biome-danger .biome-name { color: #ef5350; }
            .b-row { display: flex; margin: 5px 0; font-size: 15px; }
            .b-label { font-weight: bold; color: #cfd8dc; width: 150px; flex-shrink: 0; }
            .b-val { color: #b0bec5; flex-grow: 1; }
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background-color: #455a64; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌲 ENCICLOPEDIA DEI BIOMI OVERWORLD</h1>
                <p>Analisi sistematica di ogni ambiente, risorse disponibili, strutture e fattori di rischio.</p>
            </div>

            <div class="card">
                <h2>🟢 BIOMI FAVOREVOLI (Ideali per Spawn e Basi)</h2>
                <div class="biome-entry">
                    <span class="biome-name">Pianura (Plains / Sunflower Plains)</span>
                    <div class="b-row"><span class="b-label">Cosa trovi:</span><span class="b-val">Mucche, pecore, maiali, cavalli, api, fiumi.</span></div>
                    <div class="b-row"><span class="b-label">Strutture:</span><span class="b-val">Villaggi (altissima probabilità), avamposti dei predoni.</span></div>
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
        <title>Officina Hardcore - Crafting Consigliati</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #090c10; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .container { max-width: 750px; width: 100%; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #0d47a1, #002171); border-radius: 12px; margin-bottom: 20px; }
            .card { background-color: #171c26; border: 1px solid #2d374a; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
            h2 { color: #64b5f6; margin-top: 0; border-bottom: 1px solid #2d374a; padding-bottom: 8px; margin-bottom: 25px; }
            
            .craft-entry { margin-bottom: 35px; border-bottom: 1px dashed #2d374a; padding-bottom: 25px; }
            .craft-entry:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
            .craft-name { font-weight: bold; color: #90caf9; font-size: 20px; display: block; margin-bottom: 8px; text-transform: uppercase; }
            .craft-desc { color: #b0bec5; font-size: 15px; margin-bottom: 15px; line-height: 1.4; }
            
            .craft-box { display: flex; gap: 20px; align-items: center; background: #0f131a; padding: 15px; border-radius: 8px; border: 1px solid #21262d; }
            .materials-list { font-size: 14px; color: #cfd8dc; line-height: 1.6; }
            
            .grid-3x3 { display: grid; grid-template-columns: repeat(3, 60px); grid-template-rows: repeat(3, 60px); gap: 4px; background: #444; padding: 6px; border-radius: 4px; flex-shrink: 0; width: 188px; }
            .grid-cell { background: #8b8b8b; border: 2px solid #3c3c3c; border-top-color: #b5b5b5; border-left-color: #b5b5b5; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; color: #111; text-align: center; font-family: monospace; word-wrap: break-word; overflow: hidden; padding: 2px; text-shadow: 1px 1px 0px #aaa; }
            .grid-cell:empty { background: #8b8b8b; }
            
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background-color: #455a64; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛠️ OFFICINA HARDCORE: ARTIGIANATO SALVAVITA</h1>
                <p>La disposition esatta dei blocchi nella tavola da crafting per gli oggetti indispensabili.</p>
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
        <title>Automazione Hardcore - Farm Semplici</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0e1117; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .container { max-width: 750px; width: 100%; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #37474f, #21272a); border-radius: 12px; margin-bottom: 20px; border: 1px solid #455a64; }
            .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
            h2 { color: #cfd8dc; margin-top: 0; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 25px; }
            
            .farm-entry { margin-bottom: 35px; border-left: 4px solid #81c784; padding-left: 20px; }
            .farm-name { font-weight: bold; color: #a5d6a7; font-size: 20px; display: block; margin-bottom: 6px; text-transform: uppercase; }
            .farm-meta { font-size: 14px; color: #ffb74d; margin-bottom: 12px; font-weight: 500; }
            .farm-text { color: #b0bec5; font-size: 15px; line-height: 1.5; margin-bottom: 10px; }
            
            .steps-box { background: #0d1117; padding: 15px; border-radius: 8px; border: 1px solid #21262d; margin-top: 10px; }
            .steps-box ul { margin: 0; padding-left: 20px; color: #e3e6eb; font-size: 14px; line-height: 1.6; }
            .steps-box li { margin-bottom: 6px; }
            .steps-box li:last-child { margin-bottom: 0; }
            
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background-color: #455a64; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚙️ PROTOCOLLI DI AUTOMAZIONE: FARM VITALI</h1>
                <p>3 strutture banali da tirare su in 5 minuti per assicurarti risorse infinite senza rischiare la vita.</p>
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

# --- PAGINA 7: GUIDA AGLI INCANTESIMI AL MASSIMO ---
@app.get("/enchants-guide", response_class=HTMLResponse)
async def enchants_guide():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Grimorio degli Incantesimi Perfetti - Hardcore Edition</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0d0914; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .container { max-width: 780px; width: 100%; }
            .header { text-align: center; padding: 25px; background: linear-gradient(135deg, #4a148c, #6a1b9a); border-radius: 12px; margin-bottom: 20px; border: 1px solid #7b1fa2; }
            .card { background-color: #161224; border: 1px solid #3c245c; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
            h2 { color: #e1bee7; margin-top: 0; border-bottom: 1px solid #3c245c; padding-bottom: 8px; margin-bottom: 25px; text-transform: uppercase; font-size: 20px; }
            
            .gear-box { background: #211a36; border: 1px solid #4a3475; padding: 18px; border-radius: 8px; margin-bottom: 20px; }
            .gear-title { font-weight: bold; color: #f3e5f5; font-size: 17px; display: block; margin-bottom: 10px; border-left: 3px solid #ba68c8; padding-left: 10px; }
            
            .enchant-badge { display: inline-block; background: #4a148c; color: #f3e5f5; font-size: 13px; font-weight: bold; padding: 4px 8px; border-radius: 4px; margin: 4px 4px 4px 0; font-family: monospace; border: 1px solid #7b1fa2; }
            .enchant-badge.meta { background: #880e4f; border-color: #c2185b; }
            
            .strat-list { padding-left: 20px; font-size: 15px; color: #b0bec5; line-height: 1.6; }
            .strat-list li { margin-bottom: 10px; }
            .highlight-purple { color: #ce93d8; font-weight: bold; }
            
            .btn { background-color: #37474f; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background-color: #455a64; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔮 IL GRIMORIO DEGLI INCANTESIMI PERFETTI (GOD ROLLS)</h1>
                <p>La lista definitiva delle combinazioni massime e la strategia infallibile dei Villager per ottenerle al 100%.</p>
            </div>

            <!-- SEZIONE 1: I PEZZI PERFETTI -->
            <div class="card">
                <h2>🛡️ I SET COMPLETI AL LIVELLO MASSIMO</h2>
                <p style="color:#b0bec5; margin-top:0;">Ecco gli incantesimi precisi da schiaffare su ogni pezzo per azzerare i rischi di morte:</p>

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

            <!-- SEZIONE 2: LA STRATEGIA INFALLIBILE -->
            <div class="card">
                <h2>📈 STRATEGIA: RECLUTAMENTO DEI BIBLIOTECARI (NO RANDOM)</h2>
                <p style="color:#b0bec5; margin-top:0;">Affidarsi alla Tavola degli Incantesimi è un suicidio di risorse. La vera tattica Hardcore prevede l'abuso dei <span class="highlight-purple">Villager Bibliotecari</span>:</p>
                
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

# --- ENDPOINT REGISTRAZIONE ---
@app.post("/register")
async def register_user(username: str = Form(...), email: str = Form(...)):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO utenti (username, email) VALUES (?, ?)", (username, email))
    conn.commit()
    conn.close()
    return RedirectResponse(url=f"/?msg=Grande+{username},+registrato+con+successo!", status_code=303)
