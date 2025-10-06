
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# "Banco de dados" em memória — inicie com 3 produtos de exemplo
produtos = [
    {"id": 1, "nome": "Mouse Gamer", "preco": 99.90, "estoque": 12},
    {"id": 2, "nome": "Teclado Mecânico", "preco": 249.00, "estoque": 7},
    {"id": 3, "nome": "Headset USB", "preco": 179.50, "estoque": 0},
]

# Utilitário simples para encontrar produto por id
def achar_produto(pid: int):
    return next((p for p in produtos if p["id"] == pid), None)

# ----------------------------
# GET /produtos  (listar todos)
# ----------------------------
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos), 200

# ------------------------------------------
# GET /produtos/<id>  (obter um específico)
# ------------------------------------------
@app.route("/produtos/<int:produto_id>", methods=["GET"])
def obter_produto(produto_id):
    produto = achar_produto(produto_id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto), 200

# ----------------------------------------------------
# POST /produtos  (criar novo: nome, preco, estoque)
# ----------------------------------------------------
@app.route("/produtos", methods=["POST"])
def criar_produto():
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser application/json"}), 415

    data = request.get_json() or {}
    nome = data.get("nome")
    preco = data.get("preco")
    estoque = data.get("estoque")

    # validações simples
    if nome is None or preco is None or estoque is None:
        return jsonify({"erro": "Campos obrigatórios: nome, preco, estoque"}), 400
    if not isinstance(nome, str) or not isinstance(preco, (int, float)) or not isinstance(estoque, int):
        return jsonify({"erro": "Tipos inválidos: nome(str), preco(float), estoque(int)"}), 422
    if preco < 0 or estoque < 0:
        return jsonify({"erro": "preco e estoque devem ser não-negativos"}), 422

    novo_id = (produtos[-1]["id"] + 1) if produtos else 1
    novo_produto = {"id": novo_id, "nome": nome, "preco": float(preco), "estoque": int(estoque)}
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

# ------------------------------------------------------------
# PUT /produtos/<id>  (atualizar: nome, preco, estoque — parciais)
# ------------------------------------------------------------
@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    produto = achar_produto(produto_id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser application/json"}), 415

    data = request.get_json() or {}

    # atualizações parciais com .get(valor_padrao)
    if "nome" in data:
        if not isinstance(data["nome"], str):
            return jsonify({"erro": "nome deve ser string"}), 422
        produto["nome"] = data["nome"]

    if "preco" in data:
        preco = data["preco"]
        if not isinstance(preco, (int, float)) or preco < 0:
            return jsonify({"erro": "preco deve ser número >= 0"}), 422
        produto["preco"] = float(preco)

    if "estoque" in data:
        estoque = data["estoque"]
        if not isinstance(estoque, int) or estoque < 0:
            return jsonify({"erro": "estoque deve ser inteiro >= 0"}), 422
        produto["estoque"] = int(estoque)

    return jsonify(produto), 200

# ---------------------------------------
# DELETE /produtos/<id>  (remover item)
# ---------------------------------------
@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    produto = achar_produto(produto_id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    produtos.remove(produto)
    # você pode retornar 204 No Content; aqui retorno 200 com mensagem
    return jsonify({"resultado": "Produto deletado com sucesso"}), 200

# ---------------------------------------------------
# DESAFIO EXTRA: POST /produtos/<id>/comprar (–1)
# ---------------------------------------------------
@app.route("/produtos/<int:produto_id>/comprar", methods=["POST"])
def comprar_produto(produto_id):
    produto = achar_produto(produto_id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    if produto["estoque"] <= 0:
        return jsonify({"erro": "Produto fora de estoque"}), 400
    produto["estoque"] -= 1
    return jsonify(produto), 200

if __name__ == "__main__":
    app.run(debug=True)
