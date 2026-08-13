from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent.processor import process_transcript

app=FastAPI(title='Meeting2Action')
class Request(BaseModel): transcript:str

@app.get('/api/health')
def health(): return {'ok':True,'service':'meeting2action'}

@app.post('/api/process')
def process(req:Request):
    return process_transcript(req.transcript).model_dump(mode='json')

@app.get('/',response_class=HTMLResponse)
def home():
    return '''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Meeting2Action</title><style>body{font-family:system-ui;max-width:900px;margin:auto;padding:24px;background:#f6f7fb}.card{background:white;padding:20px;border-radius:16px;margin:16px 0}textarea{width:100%;min-height:240px;box-sizing:border-box}button{padding:12px 18px;border:0;border-radius:10px;background:#111827;color:white}</style></head><body><h1>Meeting2Action</h1><p>Turn meeting transcripts into summaries, decisions and action items.</p><div class="card"><textarea id="t" placeholder="Paste your meeting transcript..."></textarea><br><button onclick="go()">Process meeting</button><pre id="out"></pre></div><script>async function go(){const out=document.getElementById('out');out.textContent='Processing...';const r=await fetch('/api/process',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({transcript:document.getElementById('t').value})});out.textContent=JSON.stringify(await r.json(),null,2)}</script></body></html>'''
