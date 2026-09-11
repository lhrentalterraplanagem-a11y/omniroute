from sqlalchemy import create_engine, text
from models import Base

# Conectar ao banco
engine = create_engine("sqlite:///./maintenance.db")

# Adicionar a coluna manualmente se ela não existir
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE manutencoes ADD COLUMN custo_total FLOAT DEFAULT 0"))
        conn.commit()
        print("Coluna 'custo_total' adicionada com sucesso!")
    except Exception as e:
        print(f"Erro (provavelmente a coluna já existe ou banco bloqueado): {e}")
