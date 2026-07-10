


# Ágoradit - maratonaSBSC
Sistema de controle e centralização de gastos governamentais. O Ágoradit consome dados diretamente do **Portal da Transparência** através de um pipeline de importação automatizado, organizando notas fiscais, contratos, empenhos, liquidações e pagamentos em um único banco de dados.

O objetivo é oferecer uma base centralizada e consultável para fiscalização e análise de gastos públicos.


# Pré-requisitos

Antes de rodar o projeto, garanta que as seguintes ferramentas estejam instaladas:

- Python 3.10+
- Pip


# Instalação

## 1. Clonar o repositório

```bash
git clone <repository-url>
cd maratonaSBSC
```


## 2. Configurar ambiente virtual Python
- ## Linux
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

- ## Windows CMD
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate.bat
    ```

- ## Windows PowerShell
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

## 3. Instalar dependências Python
```bash
pip install -r requirements.txt
```

# Endpoints

- ### GET /notas/
    ---
    Listar Notas
    Insere um cnpj e recebe suas notas e itens de cada emissão,
    além disso as informações serão organizadas e colocadas no database
    SE a emissão da nota for antes de 3 meses desde a criação da empresa, ela será considerada suspeita, essa informação também será colocada no DB

- ### GET /contratos/
    ---
    Listar Contratos
    Insere duas datas (inicial e final)
    E recebe os contratos que foram postados nesse período

- ### POST /despesas/importar
    ---
    Importar Despesas
    Insere duas datas (inicial e final) e importa os empenhos,
    liquidações e pagamentos do Portal da Transparência para o banco de dados.
    O processo inteiro pode levar alguns minutos dependendo da quantidade.


# Inicializando Projeto

Para inicializar o servidor rode:

```cmd
uvicorn main:app --reload
```

Para facilitar o processo de consumo dos endpoints, utilizem a documentação interativa
> http://localhost:8000/docs#
