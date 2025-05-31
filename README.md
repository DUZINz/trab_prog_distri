# Sistema Distribuído em Python

Este projeto é uma implementação de um sistema distribuído utilizando Flask para a API e Celery para o processamento assíncrono de tarefas. O sistema é orquestrado usando Docker e Docker Compose.

## Estrutura do Projeto

```
sistema_distribuido_python/
├── api/                      # Contém a API Flask
│   ├── app.py                # Ponto de entrada da API
│   ├── Dockerfile            # Dockerfile para a API
│   └── requirements.txt      # Dependências da API
├── worker/                   # Contém os workers do Celery
│   ├── tasks.py              # Definição das tarefas do Celery
│   ├── celery_app.py         # Configuração do Celery
│   ├── Dockerfile            # Dockerfile para o worker
│   └── requirements.txt      # Dependências do worker
├── .gitignore                # Arquivo para ignorar arquivos no Git
├── docker-compose.yml        # Orquestração dos containers
└── README.md                 # Documentação do projeto
```

## Uso

- Acesse a API Flask em `http://localhost:5000`.
- As tarefas do Celery podem ser enviadas para processamento assíncrono através da API.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.