from flask import Flask, request, jsonify
from celery import Celery
from celery.result import AsyncResult
import os

flask_app = Flask(__name__)

# Configuração do Celery Client (para enviar tarefas e verificar resultados)
# Deve usar as mesmas URLs de broker e backend que os workers
redis_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend_url = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery_client = Celery(
    'api_client', # Nome diferente do app Celery do worker para clareza
    broker=redis_url,
    backend=result_backend_url
)
# Importante: O cliente Celery na API não precisa do 'include'
# Ele apenas envia tarefas para as definições que os workers conhecem.

@flask_app.route('/enviar_tarefa_longa', methods=['POST'])
def enviar_tarefa_longa_endpoint():
    dados = request.json.get('dados')
    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido"}), 400

    # Envia a tarefa para a fila.
    # 'tasks.processar_dados_longos' é o nome completo da tarefa
    # (nome_do_modulo_onde_celery_foi_instanciado.nome_da_tarefa)
    # No nosso caso, o app Celery no worker foi chamado 'tasks' e a função é 'processar_dados_longos'
    # Se você definiu app = Celery('meu_worker_app', ...) em celery_app.py,
    # e a tarefa está em tasks.py, seria 'tasks.processar_dados_longos'
    # ou se a tarefa estivesse em um módulo 'modulo_de_tarefas.py' e o app se chamasse 'celery_app',
    # seria 'modulo_de_tarefas.processar_dados_longos'
    # A forma mais segura é usar o nome que o worker Celery registra.
    # A instância Celery no worker foi: app = Celery('tasks', ..., include=['tasks'])
    # E a tarefa está em tasks.py. Então o nome é 'tasks.processar_dados_longos'
    try:
        # Para que funcione com a estrutura atual, o Celery client precisa saber onde encontrar
        # a definição da tarefa. A forma mais simples para o cliente é apenas enviar o nome.
        # Os workers já sabem como lidar com 'tasks.processar_dados_longos'.
        tarefa_async = celery_client.send_task('tasks.processar_dados_longos', args=[dados], queue='default')
        # O 'return' DEVE estar em uma nova linha, devidamente indentado:
        return jsonify({"mensagem": "Tarefa longa enviada!", "id_tarefa": tarefa_async.id}), 202
    except Exception as e:
        return jsonify({"erro": f"Erro ao enviar tarefa: {str(e)}"}), 500


@flask_app.route('/enviar_tarefa_simples', methods=['POST'])
def enviar_tarefa_simples_endpoint():
    try:
        x = request.json.get('x')
        y = request.json.get('y')
        if x is None or y is None:
            return jsonify({"erro": "Valores 'x' e 'y' são obrigatórios"}), 400

        # Envia a tarefa para a fila
        tarefa_async = celery_client.send_task('tasks.tarefa_simples', args=[int(x), int(y)], queue='default')
        return jsonify({"mensagem": "Tarefa simples enviada!", "id_tarefa": tarefa_async.id}), 202
    except Exception as e:
        return jsonify({"erro": f"Erro ao enviar tarefa: {str(e)}"}), 500

@flask_app.route('/status_tarefa/<task_id>', methods=['GET'])
def status_tarefa_endpoint(task_id):
    # Cria um objeto AsyncResult para obter o status/resultado da tarefa
    resultado_async = AsyncResult(task_id, app=celery_client)

    if resultado_async.ready(): # Tarefa concluída (com sucesso ou falha)
        if resultado_async.successful():
            return jsonify({
                "id_tarefa": task_id,
                "status": resultado_async.status,
                "resultado": resultado_async.result
            }), 200
        else: # Tarefa falhou
            return jsonify({
                "id_tarefa": task_id,
                "status": resultado_async.status,
                "erro": str(resultado_async.info) # Informações da exceção
            }), 500 # Ou 200 com status de falha, dependendo da sua API
    else: # Tarefa ainda pendente ou em processamento
        return jsonify({
            "id_tarefa": task_id,
            "status": resultado_async.status
        }), 202 # Accepted, mas ainda não concluído

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=True)