# Part 1: Setting Up the Environment

# Change directory to /content
%cd /content

# Clone the required repository
!git clone -b dev https://github.com/camenduru/seamless-m4t-v2-large-hf

# Install dependencies
!pip install -q fairseq2 gradio
!pip install -q https://huggingface.co/spaces/facebook/seamless-m4t-v2-large/resolve/main/whl/seamless_communication-1.0.0-py3-none-any.whl

# Download sample audio files
!wget https://huggingface.co/spaces/facebook/seamless-m4t-v2-large/resolve/main/assets/sample_input.mp3 -O /content/seamless-m4t-v2-large-hf/assets/sample_input.mp3
!wget https://huggingface.co/spaces/facebook/seamless-m4t-v2-large/resolve/main/assets/sample_input_2.mp3 -O /content/seamless-m4t-v2-large-hf/assets/sample_input_2.mp3

# Install aria2 for downloading models
!apt -y install -qq aria2

# Download model files
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/facebook/seamless-m4t-v2-large/resolve/main/seamlessM4T_v2_large.pt -d /content/models -o seamlessM4T_v2_large.pt
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/facebook/seamless-m4t-v2-large/resolve/main/spm_char_lang38_tc.model -d /content/models -o spm_char_lang38_tc.model
!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/facebook/seamless-m4t-v2-large/resolve/main/vocoder_v2.pt -d /content/models -o vocoder_v2.pt

# Change directory to the cloned repository
%cd /content/seamless-m4t-v2-large-hf

# Ensure the model files are available in the correct path
!mkdir -p /content/seamless-m4t-v2-large-hf/assets
!cp /content/models/seamlessM4T_v2_large.pt /content/seamless-m4t-v2-large-hf/assets/
!cp /content/models/spm_char_lang38_tc.model /content/seamless-m4t-v2-large-hf/assets/
!cp /content/models/vocoder_v2.pt /content/seamless-m4t-v2-large-hf/assets/

# Part 2: Writing the Testing Script

import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import matplotlib.pyplot as plt
from seamless_communication import SeamlessModel

# Load the Seamless model
model_path = "./assets/seamlessM4T_v2_large.pt"
spm_model_path = "./assets/spm_char_lang38_tc.model"

seamless_model = SeamlessModel(model_path, spm_model_path)

# Dummy Data: Replace this with actual test data
data = [
    {"source_text": "hello", "target_text": "bonjour", "src_lang": "en", "tgt_lang": "fr"},
    {"source_text": "world", "target_text": "monde", "src_lang": "en", "tgt_lang": "fr"},
    # Add more data entries
]

# Lists to keep track of accuracy per epoch
epochs = 10
accuracy_per_epoch = []

def translate(text, src_lang, tgt_lang):
    return seamless_model.translate(text, src_lang, tgt_lang)

def calculate_accuracy(ground_truths, predictions):
    matches = sum(1 for gt, pred in zip(ground_truths, predictions) if gt == pred)
    return matches / len(ground_truths)

for epoch in range(epochs):
    ground_truths = []
    predictions = []

    print(f"Epoch {epoch+1}/{epochs}")

    for item in tqdm(data):
        source_text = item['source_text']
        target_text = item['target_text']
        src_lang = item['src_lang']
        tgt_lang = item['tgt_lang']

        # Perform translation using the model
        predicted_text = translate(source_text, src_lang, tgt_lang)

        # Collecting results
        ground_truths.append(target_text)
        predictions.append(predicted_text)

    # Calculating accuracy for the current epoch
    accuracy = calculate_accuracy(ground_truths, predictions)
    accuracy_per_epoch.append(accuracy)
    print(f"Accuracy: {accuracy:.2f}")

# Plotting the accuracy per epoch
plt.plot(range(1, epochs + 1), accuracy_per_epoch, marker='o')
plt.title('Accuracy Per Epoch')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.show()