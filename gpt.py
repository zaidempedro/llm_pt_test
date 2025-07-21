import os
import time
import openai
import subprocess
import json

def traduzir_ptpt_para_ptbr(texto):
    MAX_TENTATIVAS = 3
    tentativas = 0
    while tentativas < MAX_TENTATIVAS:
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-4",  # Alterado para usar o modelo gpt-4
                messages=[
                    {"role": "system", "content": "modifique o seguinte texto para português do Brasil"},
                    {"role": "user", "content": texto}
                ],
                temperature=0.3,  # Mantendo consistência
                max_tokens=1000  # Limitando para evitar excesso de tokens
            )
            return resposta["choices"][0]["message"]["content"].strip()
        except openai.error.OpenAIError as e:
            print(f"Erro na API: {e}")
            tentativas += 1
            if tentativas < MAX_TENTATIVAS:
                print(f"Tentando novamente ({tentativas}/{MAX_TENTATIVAS})...")
                time.sleep(10)
            else:
                print("Número máximo de tentativas atingido.")
                return None

def dividir_texto_em_partes(texto, limite_tokens=1000):
    # Função para dividir o texto em partes menores com base no limite de tokens.
    palavras = texto.split()
    partes = []
    parte_atual = []
    tamanho_parte = 0

    for palavra in palavras:
        tamanho_parte += len(palavra.split())
        if tamanho_parte > limite_tokens:
            partes.append(" ".join(parte_atual))
            parte_atual = [palavra]
            tamanho_parte = len(palavra.split())
        else:
            parte_atual.append(palavra)

    if parte_atual:
        partes.append(" ".join(parte_atual))

    return partes

def processar_arquivos(pasta_entrada="textos_originais", pasta_saida="textos_traduzidos"):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    arquivos = os.listdir(pasta_entrada)
    print(f"Iniciando o processamento de {len(arquivos)} arquivos.")
    
    for i, nome_arquivo in enumerate(arquivos):
        caminho_entrada = os.path.join(pasta_entrada, nome_arquivo)
        nome_base, _ = os.path.splitext(nome_arquivo)
        caminho_saida_pt = os.path.join(pasta_saida, f"{nome_base}_pt.txt")
        caminho_saida_br = os.path.join(pasta_saida, f"{nome_base}_br.txt")
        
        with open(caminho_entrada, "r", encoding="utf-8") as f:
            texto_original = f.read()
        
        print(f"Traduzindo {nome_arquivo} ({i+1}/{len(arquivos)})...")

        # Dividindo o texto em partes menores, se necessário
        partes_texto = dividir_texto_em_partes(texto_original)
        texto_traduzido = ""
        
        for j, parte in enumerate(partes_texto):
            parte_traduzida = traduzir_ptpt_para_ptbr(parte)
            if parte_traduzida:
                texto_traduzido += parte_traduzida + " "
                print(f"Parte {j+1}/{len(partes_texto)} traduzida com sucesso.")
            else:
                print(f"Falha na tradução da parte {j+1} de {nome_arquivo}. Tentando novamente em 10 segundos...")
                time.sleep(10)  # Espera antes de tentar de novo

        if texto_traduzido:
            with open(caminho_saida_pt, "w", encoding="utf-8") as f:
                f.write(texto_original)
            with open(caminho_saida_br, "w", encoding="utf-8") as f:
                f.write(texto_traduzido.strip())
            print(f"Tradução concluída: {nome_arquivo}")
        else:
            print(f"Falha na tradução de {nome_arquivo}. Nenhum texto traduzido foi gerado.")

if __name__ == "__main__":
    processar_arquivos()

