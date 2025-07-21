
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
# Teste com o BOTO
# Use a pipeline as a high-level helper

device="cuda"
model_name = "Qwen/Qwen2.5-7B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto",
            offload_buffers=True
        )

tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Fui ao supermercado de ônibus."
messages = [
            {"role": "system", "content": "modifique o seguinte texto para português do Brasil"},
            {"role": "user", "content": prompt}
           ]
text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
            **model_inputs,
             max_new_tokens=512
           )
generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids) ]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)

