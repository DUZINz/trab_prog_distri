# Imagem base Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Comando para executar o worker Celery
# O nome 'tasks' deve corresponder ao nome dado ao app Celery e ao módulo de tarefas.
CMD ["celery", "-A", "celery_app", "worker", "-l", "info", "-Q", "default", "-c", "2"]
# -A tasks: Aponta para a instância Celery no módulo tasks (que importa de celery_app)
# worker: Inicia um worker
# -l info: Nível de log
# -Q default: Escuta a fila 'default' (pode ter múltiplas filas)
# -c 2: Número de processos concorrentes do worker (ajuste conforme CPU/necessidade)