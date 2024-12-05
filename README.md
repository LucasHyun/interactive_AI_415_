# 🎨 Interactive AI Art Show

Welcome to the **Interactive AI Art Show**, an innovative web application that allows users to generate and modify AI-created artwork interactively. This application utilizes **Stability AI's API** to generate images based on text or audio prompts and offers a variety of modification tools such as recoloring, background removal, search-and-replace editing, and outpainting.

---

## 🌟 Features

### Image Generation
- **Audio or Text-Based Prompts**: Generate unique images by entering a text prompt or speaking into the microphone.
- **Real-Time Speech Recognition**: Supports real-time audio-to-prompt conversion for effortless interaction.

### Image Modification
- **Recolor**: Change the hues of your artwork based on a prompt (e.g., "blue shades").
- **Remove Background**: Effortlessly remove the background from any generated image.
- **Search and Replace**: Replace specific elements in the image based on a search prompt (e.g., "dog") and replacement prompt (e.g., "cat").
- **Outpainting**: Expand your artwork by adding additional content to the left, right, or bottom of the image.

### User-Friendly Interface
- Easy-to-use web-based interface built with HTML, CSS, and JavaScript.
- Displays generated and modified images in real time.

---

## 🚀 Getting Started

### Prerequisites

To run this application, ensure the following:

1. **Python**: Version 3.8 or higher installed on your machine.
2. **API Key**: Obtain a **Stability AI API Key** by registering on their platform.
3. **Browser**: A modern browser that supports the Web Speech API (e.g., Google Chrome).

---

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/interactive-ai-art-show.git
   cd interactive-ai-art-show
2. **Install Dependencies: Install all necessary Python libraries by running**:
   ```bash
   pip install -r requirements.txt
3. **Set Up Environment Variables: Create a .env file in the root directory and add your Stability AI API Key**:
   STABLE_DIFFUSION_API_KEY=your_stable_diffusion_api_key
4. **Run the Application**:
   ```bash
   python app.py
5. **Access the Application: Open your browser and navigate to**:
   ```bash
   http://127.0.0.1:5000/
   
