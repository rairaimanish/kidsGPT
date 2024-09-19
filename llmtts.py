from mlx_lm import load, generate
import ChatTTS
import torch
import torchaudio
import whisper

sttmodel = whisper.load_model("base")


#Load LLM
model, tokenizer = load('Qwen/Qwen2-7B-Instruct-MLX', tokenizer_config={"eos_token": "<|im_end|>"})

#Load TTS
chat = ChatTTS.Chat()
chat.load(compile=True) # Set to True for better performance

result = sttmodel.transcribe("prompt.wav")
print(result["text"])

# prompt = input("Enter a prompt:")
messages = [
    {"role": "system", "content": "You are a children expert. You need to respond appropriately to children questions and remarks. Keep it simple and short."},
    {"role": "user", "content": result["text"]}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

response = generate(model, tokenizer, prompt=text, verbose=True, top_p=0.8, temp=0.7, repetition_penalty=1.05, max_tokens=512)


texts = [response]

wavs = chat.infer(texts)

for i in range(len(wavs)):
    """
    In some versions of torchaudio, the first line works but in other versions, so does the second line.
    """
    try:
        torchaudio.save(f"basic_output{i}.wav", torch.from_numpy(wavs[i]).unsqueeze(0), 24000)
    except:
        torchaudio.save(f"basic_output{i}.wav", torch.from_numpy(wavs[i]), 24000)