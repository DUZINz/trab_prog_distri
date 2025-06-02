from celery_app import app # Importa a instância Celery de celery_app.py
import time

@app.task(bind=True) # bind=True dá acesso à instância da tarefa (self)
def processar_dados_longos(self, data):
    """
    Uma tarefa de exemplo que simula um processamento demorado.
    """
    try:
        print(f"Worker {self.request.hostname} processando tarefa ID: {self.request.id} com dados: {data}")
        # Simula um trabalho demorado
        time.sleep(10)
        resultado = f"Dados '{data}' processados com sucesso pelo worker {self.request.hostname}!"
        print(f"Tarefa ID: {self.request.id} finalizada com resultado: {resultado}")
        return resultado
    except Exception as e:
        print(f"Erro ao processar tarefa ID: {self.request.id}: {e}")
        # Você pode querer lançar a exceção novamente ou retornar um estado de falha
        raise

@app.task
def tarefa_simples(x, y):
    time.sleep(2)
    return x + y