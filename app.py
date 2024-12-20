from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
import os
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['IMAGE_FOLDER'] = './static/images'
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

# API Keys
STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")

# Stability AI API Endpoints
GENERATE_IMAGE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
REMOVE_BACKGROUND_URL = "https://api.stability.ai/v2beta/stable-image/edit/remove-background"
SEARCH_AND_RECOLOR_URL = "https://api.stability.ai/v2beta/stable-image/edit/search-and-recolor"
SEARCH_AND_REPLACE_URL = "https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"
OUTPAINT_URL = "https://api.stability.ai/v2beta/stable-image/edit/outpaint"

# Global variable to store the last generated image path
last_generated_image = None


def generate_unique_file_path(task_name, extension="png"):
    """Generate a unique file path for a task."""
    return os.path.join(app.config['IMAGE_FOLDER'], f"{task_name}_{uuid.uuid4().hex}.{extension}")


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
        generated_image_path = generate_unique_file_path("generated")
        with open(generated_image_path, 'wb') as file:
            file.write(response.content)
        return generated_image_path
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
    response = requests.post(REMOVE_BACKGROUND_URL, headers=headers, files=files)

    if response.status_code == 200:
        modified_image_path = generate_unique_file_path("background_removed")
        with open(modified_image_path, 'wb') as file:
            file.write(response.content)
        return modified_image_path
    else:
        raise Exception(f"Error: {response.json()}")


def search_and_recolor(input_image_path, prompt):
    """Recolor the image based on the prompt."""
    headers = {
        "authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
        "accept": "image/*"
    }
    files = {
        "image": open(input_image_path, "rb")
    }
    data = {
        "prompt": prompt,
        "select_prompt": prompt,
        "output_format": "png",
    }
    response = requests.post(SEARCH_AND_RECOLOR_URL, headers=headers, files=files, data=data)

    if response.status_code == 200:
        modified_image_path = generate_unique_file_path("recolored")
        with open(modified_image_path, 'wb') as file:
            file.write(response.content)
        return modified_image_path
    else:
        raise Exception(f"Error: {response.json()}")


def search_and_replace(input_image_path, search_prompt, new_prompt):
    """Replace part of the image based on search and replace prompts."""
    headers = {
        "authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
        "accept": "image/*"
    }
    files = {
        "image": open(input_image_path, "rb")
    }
    data = {
        "prompt": new_prompt,
        "search_prompt": search_prompt,
        "output_format": "png",
    }
    response = requests.post(SEARCH_AND_REPLACE_URL, headers=headers, files=files, data=data)

    if response.status_code == 200:
        modified_image_path = generate_unique_file_path("search_replaced")
        with open(modified_image_path, 'wb') as file:
            file.write(response.content)
        return modified_image_path
    else:
        raise Exception(f"Error: {response.json()}")


def outpaint_image(input_image_path, left, down):
    """Perform outpainting on the image."""
    headers = {
        "authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
        "accept": "image/*"
    }
    files = {
        "image": open(input_image_path, "rb")
    }
    data = {
        "left": left,
        "down": down,
        "output_format": "webp",
    }
    response = requests.post(OUTPAINT_URL, headers=headers, files=files, data=data)

    if response.status_code == 200:
        outpainted_image_path = generate_unique_file_path("outpainted", "webp")
        with open(outpainted_image_path, 'wb') as file:
            file.write(response.content)
        return outpainted_image_path
    else:
        raise Exception(f"Error: {response.json()}")


@app.route('/')
def index():
    """Render the main application interface."""
    return render_template('index.html')


@app.route('/generate-image', methods=['POST'])
def generate_image_from_text():
    """Generate an image based on text input."""
    global last_generated_image
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': "Prompt is required."}), 400

    try:
        last_generated_image = generate_image(prompt)
        return jsonify({'image_path': last_generated_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/modify-image', methods=['POST'])
def modify_image():
    """Modify the generated image based on the selected task."""
    global last_generated_image
    data = request.json
    task = data.get('task')
    prompt = data.get('prompt', '')
    search_prompt = data.get('search_prompt', '')
    new_prompt = data.get('new_prompt', '')
    left = data.get('left', 0)
    down = data.get('down', 0)

    if not last_generated_image:
        return jsonify({'error': "No image generated yet."}), 400

    try:
        if task == "remove_background":
            last_generated_image = remove_background(last_generated_image)
        elif task == "recolor":
            last_generated_image = search_and_recolor(last_generated_image, prompt)
        elif task == "search_and_replace":
            last_generated_image = search_and_replace(last_generated_image, search_prompt, new_prompt)
        elif task == "outpaint":
            last_generated_image = outpaint_image(last_generated_image, left, down)
        else:
            return jsonify({'error': f"Unknown task: {task}"}), 400
        return jsonify({'image_path': last_generated_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)