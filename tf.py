import time
import torch
import psutil
from transformers import AutoModelForCausalLM, AutoTokenizer

# Measure the start time and memory usage
start_time = time.time()
process = psutil.Process()
initial_memory = process.memory_info().rss / (1024 * 1024)  # Memory in MB

model_name = "Qwen/Qwen2.5-7B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Measure time after loading the model
model_load_time = time.time() - start_time
memory_after_loading = process.memory_info().rss / (1024 * 1024)  # Memory in MB
print(f"Model loaded in {model_load_time:.2f} seconds.")
print(f"Memory used after loading model: {memory_after_loading - initial_memory:.2f} MB")

prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt},
]

# Measure time for tokenization
tokenization_start = time.time()
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
tokenization_time = time.time() - tokenization_start
print(f"Tokenization time: {tokenization_time:.2f} seconds.")

# Measure time for model generation
generation_start = time.time()
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512,
)
generation_time = time.time() - generation_start
print(f"Generation time: {generation_time:.2f} seconds.")

# Measure time for decoding
decoding_start = time.time()
# Extract the generated tokens, skipping the input tokens
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
decoding_time = time.time() - decoding_start
print(f"Decoding time: {decoding_time:.2f} seconds.")

# Measure total time and memory used
total_time = time.time() - start_time
final_memory = process.memory_info().rss / (1024 * 1024)  # Memory in MB
memory_used = final_memory - initial_memory

print(f"Total time: {total_time:.2f} seconds.")
print(f"Total memory used: {memory_used:.2f} MB.")
print(f"Generated response: {response}")
