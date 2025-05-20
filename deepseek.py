import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Defina o dispositivo como 'cuda' se uma GPU estiver disponível, caso contrário, use 'cpu'
device = "cuda" if torch.cuda.is_available() else "cpu"

# Nome do modelo
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

# Carregar o modelo com configurações específicas
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Usar precisão mista para economizar memória
    device_map="auto",  # Distribuir automaticamente o modelo entre os dispositivos disponíveis
    offload_buffers=True,  # Permitir que buffers sejam descarregados para a CPU
    trust_remote_code=True  # Confiar no código remoto para configurações específicas do modelo
)

# Mover o modelo para o dispositivo selecionado
model = model.to(device)

# Carregar o tokenizer com configurações específicas
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True  # Confiar no código remoto para configurações específicas do tokenizer
)

# Texto de entrada
prompt = "Fui ao supermercado de ônibus."
instruction = f"Reescreva o seguinte texto em português de Portugal:\n\n{prompt}"

# Tokenização
inputs = tokenizer(instruction, return_tensors="pt").to(device)

# Geração de texto
generated_ids = model.generate(
    **inputs,
    max_new_tokens=512,  # Número máximo de tokens a serem gerados
    do_sample=True,
    temperature=0.7
)

# Decodificação
response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

print(response)
