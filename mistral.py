import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Defina o dispositivo
device = "cuda"

# Nome do modelo Mistral
model_name = "mistralai/Mistral-7B-Instruct-v0.3"

# Carregar o modelo e o tokenizador
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
   #não tem necessidade - device_map="auto",
    offload_buffers=True
)
model.to(device)
print(model.device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Defina o prompt para a geração
prompt = "Fui ao supermercado de ônibus."
messages = [
    {"role": "system", "content": "modifique o seguinte texto para português de portugal"},
    {"role": "user", "content": prompt}
]

# Formatação do prompt usando o modelo de chat
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# Preparar os inputs para o modelo
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# Gerar a resposta
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)

# Separar os IDs gerados
generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]

# Decodificar os tokens gerados
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

# Exibir a resposta gerada
print(response)
