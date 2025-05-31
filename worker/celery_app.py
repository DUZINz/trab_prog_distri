from celery import Celery
import os

# Tenta pegar a URL do Redis das variáveis de ambiente (para Docker/Nuvem)
# Ou usa um padrão para desenvolvimento local se não estiverem definidas.
redis_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend_url = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Cria a instância do Celery
# O primeiro argumento é o nome do módulo atual.
# O broker é onde as mensagens de tarefa são enviadas.
# O backend é onde os resultados das tarefas são armazenados.
app = Celery(
    'tasks', # Nome do módulo onde as tarefas serão definidas (tasks.py)
    broker=redis_url,
    backend=result_backend_url,
    include=['tasks'] # Lista de módulos de tarefas a serem importados quando o worker iniciar
)

# Configurações opcionais do Celery (pode adicionar mais conforme necessário)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Apenas aceita conteúdo json
    result_serializer='json',
    timezone='America/Sao_Paulo', # Ajuste para seu fuso horário
    enable_utc=True,
    broker_connection_retry_on_startup=True # Tenta reconectar ao broker na inicialização
)

if __name__ == '__main__':
    app.start()