import streamlit as st
from difflib import SequenceMatcher
import re

# Configuração da página
st.set_page_config(page_title="Tuga2BR", page_icon="🌍", layout="wide")

# Título e subtítulo
st.title("Tuga2BR:")
st.subheader("Traduzindo Variantes do Português")

st.markdown(
    "Insira o texto em português (Portugal) na caixa da esquerda e clique em 'Converter' para ver a variante do português (Brasil) com as diferenças destacadas na caixa da direita."
)

# Função para contar palavras
def count_words(text: str) -> int:
    return len(text.strip().split())

# Função de tradução simplificada PT-PT → PT-BR
def translate_pt_to_br(text: str) -> str:
    replacements = {
        r"\bautocarro\b": "ônibus",
        r"\bcomboio\b": "trem",
    }
    result = text
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result

# Função para gerar diffs com destaque
def diff_sentence_composite(text_pt: str, text_br: str, threshold=0.3) -> str:
    tokens_pt = text_pt.split()
    tokens_br = text_br.split()
    matcher = SequenceMatcher(None, tokens_pt, tokens_br)
    ratio = matcher.ratio()

    if ratio < threshold:
        return (
            f'<del style="background:#ffe6e6;text-decoration:line-through;">{text_pt}</del> '
            f'<ins style="background:#e6ffe6;text-decoration:underline;">{text_br}</ins>'
        )

    result_tokens = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            result_tokens.append(" ".join(tokens_pt[i1:i2]))
        elif tag == "replace":
            deleted = " ".join(tokens_pt[i1:i2])
            inserted = " ".join(tokens_br[j1:j2])
            result_tokens.append(
                f'<del style="background:#ffe6e6;text-decoration:line-through;">{deleted}</del>'
            )
            result_tokens.append(
                f'<ins style="background:#e6ffe6;text-decoration:underline;">{inserted}</ins>'
            )
        elif tag == "delete":
            deleted = " ".join(tokens_pt[i1:i2])
            result_tokens.append(
                f'<del style="background:#ffe6e6;text-decoration:line-through;">{deleted}</del>'
            )
        elif tag == "insert":
            inserted = " ".join(tokens_br[j1:j2])
            result_tokens.append(
                f'<ins style="background:#e6ffe6;text-decoration:underline;">{inserted}</ins>'
            )
    return " ".join(result_tokens)

# Dropdown para escolha de modelo (opcional)
llm_options = ["mistral", "qwen", "phi4"]
selected_llm = st.selectbox("Escolha o modelo de linguagem (LLM):", llm_options)

# Layout em duas colunas
col_input, col_output = st.columns(2)

# Formulário com botão
with st.form("translation_form"):
    with col_input:
        pt_text = st.text_area("Texto em Português (Portugal):", height=300)

    submitted = st.form_submit_button("Converter")

    with col_output:
        if submitted:
            if pt_text:
                num_words = count_words(pt_text)
                if num_words > 1024:
                    st.warning("O texto excede o limite de 1024 palavras.")
                else:
                    pt_br_text = translate_pt_to_br(pt_text)
                    diff_html = diff_sentence_composite(pt_text, pt_br_text)
                    st.markdown("### Variante em Português (Brasil):")
                    st.markdown(diff_html, unsafe_allow_html=True)
            else:
                st.markdown("### Variante em Português (Brasil):")
                st.markdown(
                    "<span style='color: gray;'>Insira um texto à esquerda e clique em 'Converter'.</span>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("### Variante em Português (Brasil):")
            st.markdown(
                "<span style='color: gray;'>A tradução aparecerá aqui após clicar em 'Converter'.</span>",
                unsafe_allow_html=True,
            )

# Estilo customizado
st.markdown(
    """
    <style>
        .stTextArea textarea {
            border-radius: 10px;
        }
        .stButton > button {
            background-color: #4285F4;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background-color: #357ae8;
        }
    </style>
    """,
    unsafe_allow_html=True
)
