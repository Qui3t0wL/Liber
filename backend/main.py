from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from typing import Optional
import uvicorn
import os

from database import Database
from importer import ExcelImporter

app = FastAPI(title="Registos Paroquiais API")

# CORS para o frontend público
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

db = Database()

# ── Middleware: proteger /admin por IP local ──────────────────────────────────
LOCAL_NETWORKS = ("127.", "192.168.", "10.", "172.")

def verificar_ip_local(request: Request):
    client_ip = request.client.host
    # Suporte a proxy reverso (nginx, etc.)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    if not any(client_ip.startswith(prefix) for prefix in LOCAL_NETWORKS):
        raise HTTPException(status_code=403, detail="Acesso restrito à rede local.")
    return client_ip

# ── Rotas públicas: pesquisa ──────────────────────────────────────────────────

@app.get("/api/pesquisar")
def pesquisar(
    q: Optional[str] = Query(None, description="Termo de pesquisa (nome, notas...)"),
    tipo: Optional[str] = Query(None, description="batismo | casamento | obito"),
    ano_min: Optional[int] = None,
    ano_max: Optional[int] = None,
    fonte: Optional[str] = None,
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(25, ge=1, le=100),
):
    resultados, total = db.pesquisar(
        q=q, tipo=tipo, ano_min=ano_min, ano_max=ano_max,
        fonte=fonte, pagina=pagina, por_pagina=por_pagina
    )
    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "paginas": (total + por_pagina - 1) // por_pagina,
        "resultados": resultados,
    }

@app.get("/api/registo/{tipo}/{id}")
def detalhe_registo(tipo: str, id: int):
    if tipo not in ("batismo", "casamento", "obito"):
        raise HTTPException(status_code=400, detail="Tipo inválido.")
    registo = db.obter_registo(tipo, id)
    if not registo:
        raise HTTPException(status_code=404, detail="Registo não encontrado.")
    return registo

@app.get("/api/estatisticas")
def estatisticas():
    return db.estatisticas()

@app.get("/api/fontes")
def listar_fontes():
    return db.listar_fontes()

# ── Rotas de administração (apenas rede local) ────────────────────────────────

@app.get("/admin/api/uploads")
def listar_uploads(request: Request, _=Depends(verificar_ip_local)):
    return db.listar_uploads()

@app.post("/admin/api/upload")
async def fazer_upload(
    request: Request,
    ficheiro: UploadFile = File(...),
    tipo: str = Query(..., description="batismo | casamento | obito"),
    _=Depends(verificar_ip_local),
):
    if tipo not in ("batismo", "casamento", "obito"):
        raise HTTPException(status_code=400, detail="Tipo inválido.")
    if not ficheiro.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Apenas ficheiros Excel (.xlsx, .xls).")

    conteudo = await ficheiro.read()
    importer = ExcelImporter(db)
    resultado = importer.validar_e_importar(conteudo, tipo, ficheiro.filename, dry_run=True)
    return resultado

@app.post("/admin/api/confirmar-upload")
async def confirmar_upload(
    request: Request,
    ficheiro: UploadFile = File(...),
    tipo: str = Query(..., description="batismo | casamento | obito"),
    _=Depends(verificar_ip_local),
):
    if tipo not in ("batismo", "casamento", "obito"):
        raise HTTPException(status_code=400, detail="Tipo inválido.")

    conteudo = await ficheiro.read()
    importer = ExcelImporter(db)
    resultado = importer.validar_e_importar(conteudo, tipo, ficheiro.filename, dry_run=False)
    return resultado

# ── Servir frontends estáticos ────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="../frontend/public"), name="public")

@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse("../frontend/public/index.html")

@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, _=Depends(verificar_ip_local)):
    return FileResponse("../frontend/admin/index.html")

app.mount("/admin/static", StaticFiles(directory="../frontend/admin"), name="admin")

if __name__ == "__main__":
    db.criar_tabelas()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
