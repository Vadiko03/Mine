from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def guida():
    html_content = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Minecraft Hardcore - Protocollo Giorno 1</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #0b0d12; color: #e3e6eb; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .container { max-width: 750px; width: 100%; }
            .header { text-align: center; padding: 30px; background: linear-gradient(135deg, #880e4f, #4a148c); border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }
            h1 { margin: 0; color: #fff; font-size: 26px; text-shadow: 2px 2px #000; }
            .card { background-color: #151922; border: 1px solid #252d3d; border-radius: 12px; padding: 30px; margin-bottom: 20px; }
            h2 { color: #ba68c8; margin-top: 0; border-bottom: 1px solid #252d3d; padding-bottom: 10px; }
            .timeline-step { border-left: 3px dashed #ba68c8; padding-left: 20px; margin-bottom: 30px; position: relative; }
            .timeline-step::before { content: '⏱️'; position: absolute; left: -12px; top: 0; background: #0b0d12; padding: 2px; }
            .time-title { color: #e1bee7; font-weight: bold; font-size: 18px; margin: 0 0 8px 0; }
            .desc { color: #b0bec5; line-height: 1.7; margin: 0; }
            .alert-text { background-color: #261418; border-left: 4px solid #ff1744; padding: 12px; border-radius: 4px; margin-top: 10px; color: #ff8a80; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📖 MANUALE DI SOPRAVVIVENZA AVANZATO 📖</h1>
                <p>Microservizio Guida - Giorno 1 Minuto per Minuto</p>
            </div>

            <div class="card">
                <h2>⏱️ CRONACHE DEL GIORNO 1 (20 Minuti Reali)</h2>
                
                <div class="timeline-step">
                    <p class="time-title">Minuto 0:00 - Lo Spawn (Il Risveglio)</p>
                    <p class="desc">Appena sblocchi gli occhi, guardati intorno. Memorizza le coordinate premendo F3. Cerca subito alberi nelle vicinanze. Se spawni in un deserto o su un'isola sperduta, comincia a correre verso un bioma con piante. Non c'è tempo da perdere, il sole si muove veloce.</p>
                </div>

                <div class="timeline-step">
                    <p class="time-title">Minuto 1:30 - Il Primo Sangue (Arboreo)</p>
                    <p class="desc">Tira giù almeno 3-4 alberi a mani nude. Trasforma i tronchi in assi di legno, pianta una Crafting Table e fai subito un piccone di legno. Cerca la pietra prima possibile scendendo a scaletta nel terreno o cercando una parete di roccia aperta.</p>
                </div>

                <div class="timeline-step">
                    <p class="time-title">Minuto 3:00 - L'Età della Pietra & Caccia</p>
                    <p class="desc">Scava 3 blocchi di pietra e crafta IMMEDIATAMENTE il piccone di pietra. Butta via quello di legno. Tira giù altra pietra per fare: ascia, spada e una fornace. Se vedi pecore lungo la strada, uccidile: ti servono 3 blocchi di lana dello stesso colore per fare il letto. La lana è VITA.</p>
                </div>

                <div class="timeline-step">
                    <p class="time-title">Minuto 6:00 - Il Carburante e il Cibo</p>
                    <p class="desc">Il sole comincia a scendere verso l'orizzonte. Se hai trovato il carbone bene, sennò usa l'ascia per fare altro legno e brucia i tronchi nella fornace usando le assi come combustibile per generare la carbonella. Ammazza mucche o maiali e cuoci la carne. Non mangiare robba cruda in Hardcore, la saturazione bassa ti uccide.</p>
                    <p class="alert-text">⚠️ ATTENZIONE: Se arrivi a questo punto senza cibo o senza lana, comincia a pianificare il bunker sotterraneo.</p>
                </div>

                <div class="timeline-step">
                    <p class="time-title">Minuto 9:00 - Coprifuoco (Il Tramonto)</p>
                    <p class="desc">Il cielo diventa arancione scuro. Se hai il letto, piazzalo e cliccaci a ripetizione per dormire istantaneamente e skippare la notte bastarda. Se NON hai la lana, non fare l'eroe all'aperto. Scava un buco 1x1 profondo tre blocchi sotto i tuoi piedi, tappati la testa con un blocco di terra e aspetta.</p>
                </div>

                <div class="timeline-step">
                    <p class="time-title">Minuto 10:00 - La Lunga Notte Sotterranea</p>
                    <p class="desc">Se sei chiuso nel buco di terra, non stare fermo a tremare. Alza il volume delle cuffie per sentire da dove vengono i versi dei mob. Sfrutta il tempo per scavare una piccola miniera a scaletta verso il basso per cercare ferro. Ricordati di illuminare ogni singolo blocco che scavi, o i mob ti spawneranno alle spalle dentro la tua stessa galleria!</p>
                </div>

                <div class="timeline-step">
                    <p class="time-title">Minuto 20:00 - L'Alba del Secondo Giorno</p>
                    <p class="desc">Sentirai i rumori dei mob che prendono fuoco all'esterno (zombie e scheletri). Scava verso l'alto con estrema cautela (occhio ai Creeper che non bruciano al sole!). Guarda il cielo: se il sole è alto, esci, raccogli i drop dei mob morti e comincia a pianificare la tua base permanente. Sei sopravvissuto alla prima notte!</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
