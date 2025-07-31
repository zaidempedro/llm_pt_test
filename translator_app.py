import streamlit as st
from difflib import SequenceMatcher
import re

# Page configuration
st.set_page_config(page_title="Tuga2BR", page_icon="🌍", layout="wide")

# Title and subtitle
st.title("Tuga2BR:")
st.subheader("Translating Variants of Portuguese")

st.markdown(
    "Enter the text in Portuguese (Portugal) on the left and click 'Convert' to see the Brazilian Portuguese variant highlighted on the right."
)

# Word counting function
def count_words(text: str) -> int:
    return len(text.strip().split())

# Simplified PT-PT → PT-BR translation
def translate_pt_to_br(text: str) -> str:
    replacements = {
        r"\bautocarro\b": "ônibus",
        r"\bcomboio\b": "trem",
    }
    result = text
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result

# Diff highlighting
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
                f'<del>{deleted}</del>'
            )
            result_tokens.append(
                f'<ins>{inserted}</ins>'
            )
        elif tag == "delete":
            deleted = " ".join(tokens_pt[i1:i2])
            result_tokens.append(
                f'<del>{deleted}</del>'
            )
        elif tag == "insert":
            inserted = " ".join(tokens_br[j1:j2])
            result_tokens.append(
                f'<ins>{inserted}</ins>'
            )
    return " ".join(result_tokens)

# LLM dropdown
llm_options = ["Mistral-7B", "Qwen 2.5", "GPT-4"]
col_llm, _ = st.columns([1, 6])
with col_llm:
    selected_llm = st.selectbox("LLM:", llm_options)

# Criação do formulário
with st.form("translation_form"):
    col_input, col_output = st.columns([1, 1])

    with col_input:
        st.markdown("#### Portuguese (Portugal) Text")
        pt_text = st.text_area(" ", height=300, label_visibility="collapsed")

    with col_output:
        st.markdown("#### Brazilian Portuguese")
        output_placeholder = st.empty()

    submitted = st.form_submit_button("Convert")

# Resultado após submissão
if submitted:
    if pt_text:
        num_words = count_words(pt_text)
        if num_words > 1024:
            st.warning("The text exceeds the 1024 words limit.")
        else:
            pt_br_text = translate_pt_to_br(pt_text)
            diff_html = diff_sentence_composite(pt_text, pt_br_text)

            # Output com destaque
            with col_output:
                output_placeholder.markdown(
                    f"<div class='output-box'>{diff_html}</div>",
                    unsafe_allow_html=True
                )
    else:
        with col_output:
            output_placeholder.markdown(
                "<div class='output-box' style='color:gray;'>Enter text on the left and click 'Convert'.</div>",
                unsafe_allow_html=True
            )
else:
    with col_output:
        output_placeholder.markdown(
            "<div class='output-box' style='color:gray;'>The translation will appear here after clicking 'Convert'.</div>",
            unsafe_allow_html=True
        )

# Estilo CSS
st.markdown(
    """
    <style>
        .stTextArea textarea {
            border-radius: 10px;
            height: 300px !important;
        }
        .output-box {
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 12px;
            height: 300px;
            overflow-y: auto;
            font-family: monospace;
            white-space: pre-wrap;
        }
        del {
            background-color: #ffe6e6;
            text-decoration: line-through;
            padding: 2px;
            border-radius: 4px;
        }
        ins {
            background-color: #e6ffe6;
            text-decoration: underline;
            padding: 2px;
            border-radius: 4px;
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
