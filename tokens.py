
import os


# Caminho para o diretório com os textos
caminho = "/Users/pedrozaidem/Documents/llm_pt_test/textos_originais"

# Lista de arquivos .txt
arquivos = [f for f in os.listdir(caminho) if f.endswith(".txt")]

# Contar tokens com base em split simples
contagens = []
for nome_arquivo in arquivos:
    with open(os.path.join(caminho, nome_arquivo), 'r', encoding='utf-8') as f:
        texto = f.read()
        tokens = texto.split()
        contagens.append(len(tokens))

# Média
media_tokens_simples = sum(contagens) / len(contagens)
print(f"Média de tokens por notícia (aproximada): {media_tokens_simples:.2f}")

