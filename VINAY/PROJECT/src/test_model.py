from model_loader import load_model
import torch

tokenizer, model = load_model()

prompt = "Give one healthy breakfast idea for fitness beginners."

inputs = tokenizer.encode(prompt, return_tensors="pt")
outputs = model.generate(inputs, max_length=40, temperature=0.7)

print(tokenizer.decode(outputs[0]))
