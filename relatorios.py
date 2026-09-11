from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

def gerar_pdf_manutencao(manutencao, output_filename="relatorio_manutencao.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []

    # Estilo do Título
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, spaceAfter=20)
    story.append(Paragraph("LH RENTAL MANUTENÇÃO", title_style))

    # Tabela de Dados Principais
    data = [
        ["INFORMAÇÕES DA ORDEM DE SERVIÇO"],
        ["Ordem:", f"#{manutencao.id}"],
        ["Data:", manutencao.data.strftime('%d/%m/%Y')],
        ["Máquina:", f"{manutencao.maquina.nome} ({manutencao.maquina.placa_serie})"],
        ["Mecânico:", manutencao.mecanico.nome],
        ["Horímetro:", f"{manutencao.horimetro_atual} h"],
    ]

    t = Table(data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # Descrição do Serviço
    story.append(Paragraph("DESCRIÇÃO DO SERVIÇO:", styles['Heading2']))
    story.append(Paragraph(manutencao.descricao.replace('\n', '<br/>'), styles['BodyText']))
    story.append(Spacer(1, 20))

    # Valor Total
    val_data = [["VALOR TOTAL DO SERVIÇO", f"R$ {manutencao.custo_total:.2f}"]]
    vt = Table(val_data, colWidths=[300, 150])
    vt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(vt)

    doc.build(story)
    return output_filename

def gerar_pdf_relatorio_mensal(maquina, manutencoes, mes, ano, output_filename="relatorio_mensal.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("LH RENTAL MANUTENÇÃO", styles['Title']))
    story.append(Paragraph(f"Relatório Mensal: {maquina.nome} - {mes}/{ano}", styles['Heading2']))
    story.append(Spacer(1, 20))

    data = [["DATA", "TIPO", "DESCRIÇÃO", "VALOR"]]
    total = 0
    for m in manutencoes:
        data.append([m.data.strftime('%d/%m'), m.tipo_servico, m.descricao[:30], f"R$ {m.custo_total:.2f}"])
        total += m.custo_total

    data.append(["TOTAL", "", "", f"R$ {total:.2f}"])

    t = Table(data, colWidths=[50, 80, 200, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(t)

    doc.build(story)
    return output_filename
