import os
import zipfile
import csv
from repositories.database import db, cursor
from services.gatekeeper import executar_gatekeeper
from repositories.nota_fiscal_repo import _salvar_nota

# Ajuste o caminho se a sua pasta de arquivos brutos estiver em outro lugar
PASTA_BRUTA = "dados_brutos" 

def processar_lote_notas():
    print("[BACKGROUND] Iniciando processamento do ZIP em lote...")

    arquivos = [f for f in os.listdir(PASTA_BRUTA) if f.endswith('.zip')]
    if not arquivos:
        print(f"[BACKGROUND] Nenhum arquivo ZIP encontrado na pasta '{PASTA_BRUTA}'.")
        return

    caminho_zip = os.path.join(PASTA_BRUTA, arquivos[0])
    
    # O nosso famoso Filtro de Ouro!
    chaves_aprovadas = set()

    contador = 0

    with zipfile.ZipFile(caminho_zip, 'r') as z:
        arquivos_zip = z.namelist()

        # Encontra os arquivos dinamicamente dentro do ZIP
        arq_notas = next((f for f in arquivos_zip if "NotaFiscal.csv" in f), None)
        arq_itens = next((f for f in arquivos_zip if "NotaFiscalItem.csv" in f), None)

        if not arq_notas or not arq_itens:
            print("[BACKGROUND] Arquivos CSV ausentes dentro do ZIP.")
            return

        # ==========================================================
        # PASSO 1: PROCESSAR CABEÇALHOS (NOTAS FISCAIS)
        # ==========================================================
        print(f"[BACKGROUND] Analisando Cabeçalhos: {arq_notas}")
        with z.open(arq_notas, 'r') as f:
            linhas = (linha.decode('iso-8859-1') for linha in f)
            leitor = csv.DictReader(linhas, delimiter=';')

            for linha in leitor:

                contador+=1
                # O Gatekeeper novo espera a data em DD/MM/YYYY
                # O CSV original traz "DD/MM/YYYY HH:MM:SS", então cortamos os primeiros 10 chars
                data_limpa = linha.get("DATA EMISSÃO", "")[:10]

                # Montamos um Dicionário que simula a resposta da API do Governo
                # Assim, o repositório dos seus colegas funciona perfeitamente!
                nota_dto = {
                    "chaveNotaFiscal": linha.get("CHAVE DE ACESSO", "").strip(),
                    "dataEmissao": data_limpa,
                    "cnpjFornecedor": linha.get("CPF/CNPJ Emitente", "").strip(),
                    "nomeFornecedor": linha.get("RAZÃO SOCIAL EMITENTE", "").strip(),
                    "codigoOrgaoDestinatario": linha.get("CÓDIGO ÓRGÃO DESTINATÁRIO", ""),
                    "orgaoDestinatario": linha.get("ÓRGÃO DESTINATÁRIO", ""),
                    "valorNotaFiscal": linha.get("VALOR NOTA FISCAL", "0")
                }

                # Executa a nova lógica do Gatekeeper (Valida, Suspeita, Invalida)
                status = executar_gatekeeper(nota_dto)

                # Se a nota for válida ou suspeita, nós a salvamos no banco
                if status in ["valida", "suspeita"]:
                    try:
                        _salvar_nota(nota_dto, status)
                        chaves_aprovadas.add(nota_dto["chaveNotaFiscal"])
                    except Exception as e:
                        print(f"Erro ao salvar a nota {nota_dto['chaveNotaFiscal']}: {e}")

                if contador >=30: #CONTADOR PARA LIMITAR POR ENQUANTO A BUSCA
                    break;

            db.commit()
            print(f"Cabeçalhos finalizados. {len(chaves_aprovadas)} notas prontas para receber itens.")

        # ==========================================================
        # PASSO 2: PROCESSAR ITENS COM FILTRO DE CHAVES
        # ==========================================================
        print(f"[BACKGROUND] Processando Itens de forma otimizada: {arq_itens}")
        with z.open(arq_itens, 'r') as f:
            linhas = (linha.decode('iso-8859-1') for linha in f)
            leitor = csv.DictReader(linhas, delimiter=';')

            buffer_itens = []
            BATCH_SIZE = 1000  # Salva de 1000 em 1000 para velocidade máxima no MySQL

            query_insercao = """
                INSERT IGNORE INTO itens_notas_fiscais (
                    chave_nota, numero_produto, descricao, codigo_ncm,
                    ncm, cfop, quantidade, unidade, valor_unitario, valor
                ) VALUES (
                    %(chave_nota)s, %(numero_produto)s, %(descricao)s, %(codigo_ncm)s,
                    %(ncm)s, %(cfop)s, %(quantidade)s, %(unidade)s, %(valor_unitario)s, %(valor)s
                )
            """

            for linha in leitor:
                chave = linha.get("CHAVE DE ACESSO", "").strip()

                # Só processa o item se a nota dele passou pelo Gatekeeper!
                if chave in chaves_aprovadas:
                    try:
                        qtd = float(linha.get("QUANTIDADE", "0").replace(".", "").replace(",", "."))
                        v_unit = float(linha.get("VALOR UNITÁRIO", "0").replace(".", "").replace(",", "."))
                        v_tot = float(linha.get("VALOR TOTAL", "0").replace(".", "").replace(",", "."))
                    except ValueError:
                        qtd, v_unit, v_tot = 0.0, 0.0, 0.0

                    item = {
                        "chave_nota": chave,
                        "numero_produto": linha.get("NÚMERO PRODUTO", ""),
                        "descricao": linha.get("DESCRIÇÃO DO PRODUTO/SERVIÇO", "").strip(),
                        "codigo_ncm": linha.get("CÓDIGO NCM/SH", ""),
                        "ncm": linha.get("NCM/SH (TIPO DE PRODUTO)", ""),
                        "cfop": linha.get("CFOP", ""),
                        "quantidade": qtd,
                        "unidade": linha.get("UNIDADE", "").strip(),
                        "valor_unitario": v_unit,
                        "valor": v_tot
                    }
                    buffer_itens.append(item)

                    # Quando o buffer enche, dispara o comando SQL de uma vez (Super Rápido)
                    if len(buffer_itens) >= BATCH_SIZE:
                        cursor.executemany(query_insercao, buffer_itens)
                        buffer_itens.clear()

            # Salva o resto dos itens que ficaram no buffer
            if buffer_itens:
                cursor.executemany(query_insercao, buffer_itens)

            db.commit()

    print("[BACKGROUND] Processamento completo! Notas e Itens salvos com sucesso no MySQL.")