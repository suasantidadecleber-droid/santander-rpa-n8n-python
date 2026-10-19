# Santander — RPA com n8n e Python

Projeto demonstrativo de automação de triagem de solicitações de compra. O n8n recebe a solicitação por webhook e orquestra o fluxo; um serviço Python valida os dados, calcula subtotais e total e classifica pedidos até R$ 5.000,00 para encaminhamento conforme política interna. Valores superiores ficam marcados para revisão humana.

> **Escopo e segurança:** este MVP não realiza compras, pagamentos ou aprovações financeiras efetivas. A classificação automática é demonstrativa e o limite deve ser ajustado à política da organização. Não envie dados pessoais ou financeiros reais.

## Componentes

- `workflow.json`: workflow n8n (Webhook → serviço Python → resposta JSON).
- `app/main.py`: API Python com validação e regras de negócio.
- `docker-compose.yml` e `Dockerfile`: execução local de n8n e Python.
- `examples/solicitacao.json`: payload de teste.
- `tests/test_main.py`: testes das regras básicas.

## Requisitos

Docker Desktop ou Docker Engine com Docker Compose. Não é necessário instalar n8n separadamente. Os serviços n8n e Python comunicam-se pela rede interna do Compose.

## Como executar

1. Clone/baixe o repositório e abra um terminal na pasta do projeto.
2. Inicie os serviços: `docker compose up --build -d`.
3. Acesse `http://localhost:5678` e crie o usuário local no n8n.
4. Importe `workflow.json`, salve e ative o fluxo.
5. No modo de teste, use a URL de teste exibida no nó Webhook. Com o fluxo ativo, a URL local é `http://localhost:5678/webhook/rpa-solicitacao`.
6. Envie a solicitação de exemplo:

```bash
curl -X POST http://localhost:5678/webhook/rpa-solicitacao \
  -H 'Content-Type: application/json' \
  --data @examples/solicitacao.json
```

Resposta esperada: total `1278.8` e decisão `aprovacao_automatica`. Para parar: `docker compose down`. O volume `n8n_data` preserva dados; `docker compose down -v` também o remove.

## Testes locais (opcional)

Com Python 3.11+, execute `pip install -r requirements.txt` e `python -m unittest discover -s tests -v`.

## Publicação no GitHub

Crie um repositório público, envie o conteúdo deste projeto e cole o link na página de entrega do curso. Confira os critérios oficiais do desafio na plataforma, pois podem solicitar algo diferente deste exemplo. Não publique senhas, tokens, credenciais ou arquivos `.env`.
