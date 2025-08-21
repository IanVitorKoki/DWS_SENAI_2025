# Semana 4 — Práticas (Parte 1 e Parte 2) — PRONTO ✅

Este diretório já contém as duas práticas pedidas pelo professor, **copiadas** do material e **exercícios resolvidos**.

## Onde está cada prática

- **Parte 1** → `Semana_4/meu_app/`
  - Executável: `python app.py`
  - Rotas:
    - `/` — menu
    - `/formulario` — formulário em branco (exemplo do material)
    - `/formulario/preenchido-args` — exemplo com argumentos
    - `/formulario/preenchido-obj` — exemplo com objeto
    - **`/registro` — EXERCÍCIO RESOLVIDO** (Formulário de Registro Avançado)
- **Parte 2** → `Semana_4/meu_app_2/`
  - Executável: `python app.py`
  - Rotas:
    - `/` — menu
    - `/vazio` — formulário de **Cadastro de Evento** (exercício) em branco
    - `/via-argumentos` — preenchido via argumentos
    - `/via-objeto` — preenchido via objeto
    - **Após enviar**: exibe `sucesso.html` (passando o nome do organizador)

## Como instalar dependências

> Use um ambiente virtual, se quiser (recomendado).

```bash
pip install -r requirements.txt
```

Isto instalará `Flask`, `Flask-WTF` e `WTForms`.

## Como rodar cada prática

### Parte 1
```bash
cd Semana_4/meu_app
python app.py
# abrir http://127.0.0.1:5000/
```

### Parte 2
```bash
cd Semana_4/meu_app_2
python app.py
# abrir http://127.0.0.1:5000/
```

## O que foi resolvido de acordo com o material

- **Parte 1 (Registro de Usuário)**  
  Implementado o formulário `FormularioRegistro` com:
  - `nome` (obrigatório)
  - `email` (obrigatório + formato)
  - `senha` (mín. 8)
  - `confirmar_senha` (igual à senha)
  - `biografia` (opcional)
  - `aceitar_termos` (obrigatório)
  - Rota: `/registro` e template `templates/registro.html`.

- **Parte 2 (Cadastro de Evento)**  
  Adaptado o formulário de contato para **`EventoForm`**, com:
  - `nome_evento` (obrigatório)
  - `data_evento` (obrigatória, **não pode ser no passado**)
  - `organizador` (obrigatório)
  - `tipo_evento` (`Palestra`, `Workshop`, `Meetup`, `Outro`)
  - `mensagem` (opcional, **mas obrigatório se `tipo_evento == "Outro"`**)
  - Roteamento com os 3 modos de preenchimento e exibição de sucesso.

## Observações

- As páginas já possuem `CSRF` habilitado (via `SECRET_KEY`).
- Se a data estiver no passado, o envio será bloqueado com mensagem de erro.
- Caso o tipo selecionado seja **Outro**, a descrição passa a ser obrigatória.
- O arquivo `requirements.txt` foi atualizado para garantir as dependências.

Bom estudo! ✨