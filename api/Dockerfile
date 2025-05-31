# Imagem base Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de requirements primeiro
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o Flask usará
EXPOSE 5000

# Comando para executar a aplicação Flask
# Usamos gunicorn em produção, mas para simplicidade aqui, o dev server do Flask
# Para produção, seria algo como: CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:flask_app"]
CMD ["flask", "run", "--host=0.0.0.0"]