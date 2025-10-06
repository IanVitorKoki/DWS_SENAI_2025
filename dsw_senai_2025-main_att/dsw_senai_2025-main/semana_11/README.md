
# API de Gerenciamento de Produtos (Flask)

Projeto pronto para executar a atividade "Exercício Prático: API de Gerenciamento de Produtos".

## Requisitos
- Python 3.10+
- Pip

## Como executar
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

pip install -r requirements.txt
python app.py
```
Servidor: `http://127.0.0.1:5000/`

## Rotas

### GET /produtos
Lista todos os produtos.

### GET /produtos/<id>
Retorna um produto específico.

### POST /produtos
Cria um novo produto.
Body (JSON):
```json
{ "nome": "Webcam Full HD", "preco": 139.90, "estoque": 5 }
```

### PUT /produtos/<id>
Atualiza um produto (parcial ou completo).
Body (JSON):
```json
{ "preco": 229.00, "estoque": 10 }
```

### DELETE /produtos/<id>
Remove um produto.

### POST /produtos/<id>/comprar
Decrementa 1 unidade do estoque (desafio extra).

## Testando no Hoppscotch
1. Abra https://hoppscotch.io/
2. Use as URLs acima (http://127.0.0.1:5000/...) e os corpos JSON sugeridos.
3. Garanta que o servidor Flask esteja rodando no seu terminal.

## Observações
- Este projeto usa um "banco" em memória (lista Python). Ao reiniciar, os dados voltam ao estado inicial.
- Em produção, prefira um banco com autoincremento/UUID e validações mais robustas.
