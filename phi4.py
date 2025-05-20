import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"


model_name = "microsoft/phi-4-mini-instruct"


torch.cuda.empty_cache()


model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Usar precisão mista para economizar memória
    device_map="auto",  # Ajuste automático para dispositivos
    offload_buffers=True,  # Permitir offload de buffers para a CPU
    trust_remote_code=True
)


model = model.to(device)


torch.cuda.empty_cache()


tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)

# Texto original e instrução
prompt = "Fui ao supermercado de ônibus."
instruction = f"Reescreve o seguinte texto em português de Portugal:\n\n{prompt}"

# Tokenização
inputs = tokenizer(instruction, return_tensors="pt").to(device)

# Limpar a memória CUDA antes de gerar a saída
torch.cuda.empty_cache()

# Geração da resposta com número de tokens reduzido para economizar memória
generated_ids = model.generate(
    **inputs,
    max_new_tokens=32,  
    do_sample=True,
    temperature=0.7
)


response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)


print(response)
