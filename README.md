# Interactive AI Art Show Project

## Overview
This project is a web-based interactive AI art show application. It leverages Stability AI's API for generating and editing images based on text or audio inputs. The app features an intuitive user interface for creating and modifying artwork, allowing users to experiment with various image editing tasks like background removal, recoloring, and outpainting.

---

## Features
- **Real-Time Audio Input**: Generate image prompts using voice commands.
- **Image Generation**: Create images based on descriptive text prompts.
- **Image Modification**:
  - Remove background from images.
  - Recolor images based on a given prompt.
  - Search and replace objects in images.
  - Outpaint images by expanding boundaries in specific directions.
- **Dynamic User Interface**: View and modify images directly within the web application.

---

## Technologies Used
- **Backend**:
  - Flask (Python) for handling API requests.
  - Stability AI API for image generation and editing.
  - `dotenv` for environment variable management.
  - `requests` for handling HTTP requests.
- **Frontend**:
  - HTML, CSS, and JavaScript for the user interface.
  - Web Speech API for real-time audio input and processing.
- **Environment**:
  - Python 3.9+
  - Stability AI API Key for accessing the Stable Diffusion API.

---

## Setup Instructions

### Prerequisites
1. Python 3.9 or higher.
2. Stability AI API key (obtain from [Stability AI](https://platform.stability.ai)).
3. Install required Python packages:
   ```bash
   pip install flask python-dotenv requests