from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
import os
import subprocess

# Load environment variables
load_dotenv()

app = Flask(__name__)

# API keys
STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
import openai
openai.api_key = OPENAI_API_KEY

# Stability AI API Endpoints
GENERATE_IMAGE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
SEARCH_AND_RECOLOR_URL = "https://api.stability.ai/v2beta/stable-image/edit/search-and-recolor"
REMOVE_BACKGROUND_URL = "https://api.stability.ai/v2beta/stable-image/edit/remove-background"
REPLACE_BACKGROUND_URL = "https://api.stability.ai/v2beta/stable-image/edit/replace-background-and-relight"

# Global variable to store the last generated image path
last_generated_image = "./static/generated_image.png"

def convert_webm_to_wav(input_file, output_file):
    """Convert webm audio file to wav using FFmpeg."""
    command = [
        "ffmpeg",
        "-i", input_file,
        "-ar", "16000",  # Whisper API compatible sample rate
        "-ac", "1",      # Mono channel
        output_file
    ]
    subprocess.run(command, check=True)

def generate_image(prompt):
    """Generate an image using Stability AI."""
    headers = {
        "authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
        "accept": "image/*"
    }
    data = {
        "prompt": prompt,
        "output_format": "png",
    }
    response = requests.post(GENERATE_IMAGE_URL, headers=headers, files={"none": ''}, data=data)

    if response.status_code == 200:
        with open(last_generated_image, 'wb') as file:
            file.write(response.content)
        return last_generated_image
    else:
        raise Exception(f"Error: {response.json()}")

def parse_and_execute_task(audio_instruction):
    # Define recognized tasks
    recognized_tasks = {
        "create image": handle_image_creation,
        "modify image": handle_image_modification,
        # Add more tasks as needed
    }
    
    # Try to find a matching task in the instruction
    for task, handler in recognized_tasks.items():
        if task in audio_instruction.lower():
            return handler(audio_instruction)
    
    # If no task matches, raise a detailed error
    raise ValueError(f"Task not recognized in audio instruction: '{audio_instruction}'. "
                     "Please provide a valid instruction such as 'create image' or 'modify image'.")

# Example handlers
def handle_image_creation(instruction):
    print("Handling image creation...")
    # Implement creation logic
    return "path_to_created_image.png"

def handle_image_modification(instruction):
    print("Handling image modification...")
    # Implement modification logic
    return "path_to_modified_image.png"


def search_and_recolor(input_image_path, prompt, select_prompt):
    """Edit image colors."""
    headers = {
        "authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
        "accept": "image/*"
    }
    files = {
        "image": open(input_image_path, "rb")
    }
    data = {
        "prompt": prompt,
        "select_prompt": select_prompt,
        "output_format": "png",
    }
    response = requests.post(SEARCH_AND_RECOLOR_URL, headers=headers, files=files, data=data)

    if response.status_code == 200:
        modified_image_path = "./static/recolored_image.png"
        with open(modified_image_path, 'wb') as file:
            file.write(response.content)
        return modified_image_path
    else:
        raise Exception(f"Error: {response.json()}")

def remove_background(input_image_path):
    """Remove the background of the image."""
    headers = {
        "authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
        "accept": "image/*"
    }
    files = {
        "image": open(input_image_path, "rb")
    }
    data = {
        "output_format": "png"
    }
    response = requests.post(REMOVE_BACKGROUND_URL, headers=headers, files=files, data=data)

    if response.status_code == 200:
        modified_image_path = "./static/background_removed.png"
        with open(modified_image_path, 'wb') as file:
            file.write(response.content)
        return modified_image_path
    else:
        raise Exception(f"Error: {response.json()}")

def replace_background_and_relight(subject_image_path, background_prompt):
    """Replace the background of the image and apply relighting."""
    headers = {
        "authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
        "accept": "image/*"
    }
    files = {
        "subject_image": open(subject_image_path, "rb")
    }
    data = {
        "background_prompt": background_prompt,
        "output_format": "png",
    }
    response = requests.post(REPLACE_BACKGROUND_URL, headers=headers, files=files, data=data)

    if response.status_code == 200:
        modified_image_path = "./static/background_replaced.png"
        with open(modified_image_path, 'wb') as file:
            file.write(response.content)
        return modified_image_path
    else:
        raise Exception(f"Error: {response.json()}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    """Process audio input and execute the task."""
    global last_generated_image
    audio_file = request.files['audio']

    # Save the audio file
    input_path = "/tmp/input_audio.webm"
    output_path = "/tmp/output_audio.wav"
    audio_file.save(input_path)

    # Convert to wav format
    convert_webm_to_wav(input_path, output_path)

    # Convert audio to text
    with open(output_path, "rb") as f:
        response = openai.Audio.transcribe("whisper-1", f)
    audio_instruction = response.get('text', '')

    # Parse and execute the task
    modified_image_path = parse_and_execute_task(audio_instruction)

    return jsonify({'audio_instruction': audio_instruction, 'image_path': modified_image_path})


if __name__ == '__main__':
    app.run(debug=True)