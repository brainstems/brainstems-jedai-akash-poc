import os
from flask import Flask, request, jsonify
from transformers import AutoTokenizer
from ctransformers import AutoModelForCausalLM
from optimum.onnxruntime import ORTModelForSeq2SeqLM
import torch

# Create a Flask object
app = Flask("Dolphin-2.6.mistral-7b server")
model = None
tokenizer = None

# Get the model path from environment variable or use default
model_path = "TheBloke/dolphin-2.6-mistral-7B-dpo-laser-GGUF" #change for env variable
tokenizer_path ="gpt2"
# Template for the prompt
template = "system\n{system_context}\nuser\n{user_prompt}\nassistant\n{assistant_context}"

@app.route('/dolphin', methods=['POST'])
def generate_response():
    global model
    global tokenizer
    
    try:
        data = request.get_json()

        # Check if the required fields are present in the JSON data
        if 'system_context' in data and 'user_prompt' in data and 'max_tokens' in data and 'assistant_context' in data:
            system_context = data['system_context']
            user_prompt = data['user_prompt']
            max_tokens = int(data['max_tokens'])
            assistant_context = data['assistant_context']

            # Create the prompt using the template
            prompt = template.format(system_context=system_context, user_prompt=user_prompt, assistant_context=assistant_context)
            
            # Load the model and tokenizer if not previously loaded
            if model is None:
                # Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
                model = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-Chat-GGUF", model_file="llama-2-7b-chat.Q4_K_M.gguf", model_type="llama", gpu_layers=50)
              #  tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
              #  model = ORTModelForSeq2SeqLM.from_pretrained(model_path, from_transformers=True)
              #  model.to("cuda")
             
            # Generate response using the model
            # inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
            # outputs = model.generate(inputs.input_ids, max_new_tokens=max_tokens)
            # generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return jsonify({"response": model(prompt)})

        else:
            return jsonify({"error": "Missing required parameters"}), 400

    except Exception as e:
        return jsonify({"Error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)