from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['IMAGE_FOLDER'] = './static/images'
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

# API keys
STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")

# Stability AI API Endpoints
GENERATE_IMAGE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
REMOVE_BACKGROUND_URL = "https://api.stability.ai/v2beta/stable-image/edit/remove-background"
SEARCH_AND_RECOLOR_URL = "https://api.stability.ai/v2beta/stable-image/edit/search-and-recolor"

# Global variable to store the last generated image path
last_generated_image = os.path.join(app.config['IMAGE_FOLDER'], "generated_image.png")


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
        modified_image_path = os.path.join(app.config['IMAGE_FOLDER'], "background_removed.png")
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
        "output_format": "png",
    }
    response = requests.post(SEARCH_AND_RECOLOR_URL, headers=headers, files=files, data=data)

    if response.status_code == 200:
        modified_image_path = os.path.join(app.config['IMAGE_FOLDER'], "recolored_image.png")
        with open(modified_image_path, 'wb') as file:
            file.write(response.content)
        return modified_image_path
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
        generated_image_path = generate_image(prompt)
        return jsonify({'image_path': generated_image_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/modify-image', methods=['POST'])
def modify_image():
    """Modify the generated image based on the selected task."""
    global last_generated_image
    data = request.json
    task = data.get('task')
    prompt = data.get('prompt', '')

    try:
        if task == "remove_background":
            modified_image = remove_background(last_generated_image)
        elif task == "recolor":
            modified_image = search_and_recolor(last_generated_image, prompt)
        else:
            return jsonify({'error': f"Unknown task: {task}"}), 400
        return jsonify({'image_path': modified_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)