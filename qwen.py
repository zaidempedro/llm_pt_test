import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Configuração do modelo Qwen
device = "cuda"
model_name = "Qwen/Qwen2.5-7B-Instruct"

# Carregar modelo e tokenizer
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
    offload_buffers=True
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def traduzir_ptpt_para_ptbr(texto):
    messages = [
        {"role": "system", "content": "modifique o seguinte texto para português do Brasil"},
        {"role": "user", "content": texto}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([prompt], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        do_sample=False,
        temperature=0.3
    )

    # Remover o prompt da resposta
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response.strip()

def dividir_texto_em_partes(texto, limite_tokens=700):
    palavras = texto.split()
    partes = []
    parte_atual = []
    tamanho_parte = 0

    for palavra in palavras:
        tamanho_parte += 1
        parte_atual.append(palavra)
        if tamanho_parte >= limite_tokens:
            partes.append(" ".join(parte_atual))
            parte_atual = []
            tamanho_parte = 0

    if parte_atual:
        partes.append(" ".join(parte_atual))

    return partes

def processar_arquivos(pasta_entrada="textos_originais", pasta_saida="textos_traduzidos_qwen"):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    arquivos = [f for f in os.listdir(pasta_entrada) if not f.startswith('.')]
    print(f"Iniciando o processamento de {len(arquivos)} arquivos.\n")

    for i, nome_arquivo in enumerate(arquivos):
        nome_base, _ = os.path.splitext(nome_arquivo)
        caminho_saida_br = os.path.join(pasta_saida, f"{nome_base}_br.txt")

        # Pula se já existe tradução pronta
        if os.path.exists(caminho_saida_br):
            print(f"Pulo {nome_arquivo} porque já existe tradução.")
            continue

        caminho_entrada = os.path.join(pasta_entrada, nome_arquivo)
        caminho_saida_pt = os.path.join(pasta_saida, f"{nome_base}_pt.txt")

        try:
            with open(caminho_entrada, "r", encoding="utf-8") as f:
                texto_original = f.read()
        except UnicodeDecodeError:
            print(f"✗ Erro ao ler {nome_arquivo}: codificação inválida.")
            continue

        print(f"Traduzindo {nome_arquivo} ({i+1}/{len(arquivos)})...")

        partes = dividir_texto_em_partes(texto_original)
        traducao_completa = ""

        for j, parte in enumerate(partes):
            try:
                traducao = traduzir_ptpt_para_ptbr(parte)
                traducao_completa += traducao + " "
                print(f" → Parte {j+1}/{len(partes)} traduzida.")
            except Exception as e:
                print(f"Erro ao traduzir parte {j+1} de {nome_arquivo}: {e}")
                continue

        with open(caminho_saida_pt, "w", encoding="utf-8") as f:
            f.write(texto_original)

        with open(caminho_saida_br, "w", encoding="utf-8") as f:
            f.write(traducao_completa.strip())

        print(f"✓ Tradução concluída: {nome_arquivo}\n")

if __name__ == "__main__":
    processar_arquivos()
