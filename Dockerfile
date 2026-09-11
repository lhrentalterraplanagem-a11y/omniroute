# Usa uma versão oficial do Python
FROM python:3.10-slim

# Define a pasta de trabalho
WORKDIR /app

# Copia os arquivos
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Render vai usar (o Render exige a 10000)
EXPOSE 10000

# Comando para rodar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
