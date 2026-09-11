from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
import database, models, relatorios
from database import engine, get_db
from datetime import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

# --- ROTAS ---

@app.get("/relatorios", response_class=HTMLResponse)
async def pagina_relatorios(request: Request, db: Session = Depends(get_db)):
    maquinas = db.query(models.Maquina).all()
    return templates.TemplateResponse(request, "relatorios.html", {"maquinas": maquinas})

@app.post("/relatorios/gerar")
async def gerar_relatorio(
    maquina_id: int = Form(...),
    mes: int = Form(...),
    ano: int = Form(...),
    db: Session = Depends(get_db)
):
    maquina = db.query(models.Maquina).filter(models.Maquina.id == maquina_id).first()
    manutencoes = db.query(models.Manutencao).filter(
        models.Manutencao.maquina_id == maquina_id,
        extract('month', models.Manutencao.data) == mes,
        extract('year', models.Manutencao.data) == ano
    ).all()

    arquivo_pdf = relatorios.gerar_pdf_relatorio_mensal(maquina, manutencoes, mes, ano)
    return FileResponse(arquivo_pdf, media_type='application/pdf', filename=f"Relatorio_{maquina.nome}_{mes}_{ano}.pdf")

@app.get("/imprimir_manutencao/{manutencao_id}")
async def imprimir_manutencao(manutencao_id: int, db: Session = Depends(get_db)):
    manutencao = db.query(models.Manutencao).filter(models.Manutencao.id == manutencao_id).first()
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")

    arquivo_pdf = relatorios.gerar_pdf_manutencao(manutencao)
    return FileResponse(arquivo_pdf, media_type='application/pdf', filename=f"Manutencao_{manutencao_id}.pdf")

@app.get("/manutencao/excluir/{manutencao_id}")
async def excluir_manutencao(manutencao_id: int, db: Session = Depends(get_db)):
    manutencao = db.query(models.Manutencao).filter(models.Manutencao.id == manutencao_id).first()
    if manutencao:
        maquina_id = manutencao.maquina_id
        db.delete(manutencao)
        db.commit()
        return RedirectResponse(url=f"/manutencoes/{maquina_id}", status_code=303)
    raise HTTPException(status_code=404, detail="Manutenção não encontrada")

@app.get("/manutencao/enviar_whatsapp/{manutencao_id}")
async def enviar_whatsapp(manutencao_id: int, db: Session = Depends(get_db)):
    manutencao = db.query(models.Manutencao).filter(models.Manutencao.id == manutencao_id).first()
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")

    texto = f"""*ORDEM DE MANUTENÇÃO #{manutencao.id}*
━━━━━━━━━━━━━━━━━━━
🚧 Máquina: {manutencao.maquina.nome}
🔧 Tipo: {manutencao.maquina.tipo}
🪪 Identificação: {manutencao.maquina.placa_serie}
👷 Mecânico: {manutencao.mecanico.nome}
📅 Data: {manutencao.data.strftime('%d/%m/%Y')}
⏱️ Horímetro: {manutencao.horimetro_atual} horas
━━━━━━━━━━━━━━━━━━━
SERVIÇOS REALIZADOS:
{manutencao.descricao}
━━━━━━━━━━━━━━━━━━━
"""
    import whatsapp
    return RedirectResponse(url=whatsapp.preparar_link_whatsapp(texto), status_code=303)

@app.get("/maquinas", response_class=HTMLResponse)
async def listar_maquinas(request: Request, db: Session = Depends(get_db)):
    maquinas = db.query(models.Maquina).all()
    return templates.TemplateResponse(request, "maquinas.html", {"maquinas": maquinas})

@app.post("/maquinas/criar")
async def criar_maquina(
    nome: str = Form(...),
    tipo: str = Form(...),
    placa_serie: str = Form(...),
    db: Session = Depends(get_db)
):
    nova_maquina = models.Maquina(nome=nome, tipo=tipo, placa_serie=placa_serie)
    db.add(nova_maquina)
    db.commit()
    return RedirectResponse(url="/maquinas", status_code=303)

@app.get("/mecanicos", response_class=HTMLResponse)
async def listar_mecanicos(request: Request, db: Session = Depends(get_db)):
    mecanicos = db.query(models.Mecanico).all()
    return templates.TemplateResponse(request, "mecanicos.html", {"mecanicos": mecanicos})

@app.post("/mecanicos/criar")
async def criar_mecanico(
    nome: str = Form(...),
    telefone: str = Form(...),
    db: Session = Depends(get_db)
):
    novo_mecanico = models.Mecanico(nome=nome, telefone=telefone)
    db.add(novo_mecanico)
    db.commit()
    return RedirectResponse(url="/mecanicos", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    maquinas = db.query(models.Maquina).all()
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    gastos = db.query(
        models.Maquina.nome,
        func.sum(models.Manutencao.custo_total).label("total")
    ).join(models.Manutencao).filter(
        extract('month', models.Manutencao.data) == mes_atual,
        extract('year', models.Manutencao.data) == ano_atual
    ).group_by(models.Maquina.nome).all()

    return templates.TemplateResponse(request, "dashboard.html", {
        "maquinas": maquinas,
        "gastos": gastos,
        "datetime": datetime # Passando datetime pro template
    })

@app.get("/manutencoes/{maquina_id}", response_class=HTMLResponse)
async def read_manutencoes(maquina_id: int, request: Request, db: Session = Depends(get_db)):
    maquina = db.query(models.Maquina).filter(models.Maquina.id == maquina_id).first()
    manutencoes = db.query(models.Manutencao).filter(models.Manutencao.maquina_id == maquina_id).order_by(models.Manutencao.data.desc()).all()
    mecanicos = db.query(models.Mecanico).all()
    return templates.TemplateResponse(request, "manutencao.html", {"maquina": maquina, "manutencoes": manutencoes, "mecanicos": mecanicos})

@app.post("/manutencao/criar")
async def criar_manutencao(
    maquina_id: int = Form(...),
    mecanico_id: int = Form(...),
    tipo_servico: str = Form(...),
    descricao: str = Form(...),
    horimetro: float = Form(...),
    data: str = Form(...),
    custo: float = Form(...),
    db: Session = Depends(get_db)
):
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    nova_manutencao = models.Manutencao(
        maquina_id=maquina_id,
        mecanico_id=mecanico_id,
        tipo_servico=tipo_servico,
        descricao=descricao,
        horimetro_atual=horimetro,
        data=data_formatada,
        custo_total=custo
    )
    db.add(nova_manutencao)
    db.commit()
    return RedirectResponse(url=f"/manutencoes/{maquina_id}", status_code=303)
