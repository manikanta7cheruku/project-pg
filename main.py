from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import feedparser
from transformers import pipeline
from huggingface_hub import login
from diffusers import StableDiffusionPipeline
import torch

# ----------------- Configuration -----------------

HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN"

app = Flask(__name__, static_folder='static')
CORS(app)

# Login to Hugging Face
login(HF_TOKEN)

# Load AI models
generator = pipeline("text-generation", model="gpt2")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to("cpu")  # Use 'cuda' if you have GPU

# Optional RSS feeds (not used in web version, but expandable)
rss_feeds = {
    "technology": "http://feeds.arstechnica.com/arstechnica/technology-lab",
    "space": "http://feeds.nasa.gov/nasa_technology.rss",
    "science": "http://feeds.nature.com/nature/rss/current",
}

# ----------------- AI Functions -----------------

def generate_caption(prompt):
    outputs = generator(prompt, max_new_tokens=60, num_return_sequences=1, truncation=True)
    return outputs[0]['generated_text'].strip()

def generate_realistic_image(prompt, filename="static/realistic_post.jpg"):
    image = pipe(prompt).images[0]
    image.save(filename)
    return filename

# ----------------- Routes -----------------

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/generate_post", methods=["POST"])
def generate_post():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Missing topic"}), 400

    caption = generate_caption(f"Instagram caption for: {topic}")
    image_path = generate_realistic_image(topic)

    return jsonify({
        "caption": caption,
        "image_url": f"/{image_path}"
    })

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

# ----------------- Run App -----------------

if __name__ == "__main__":
    app.run(debug=True)
