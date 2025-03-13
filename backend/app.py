from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import glob
import base64
# import tensorflow as tf  # Removing TensorFlow import
from models.recommendation_model import RecipeRecommender
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../Food Images')
# Enable full CORS support for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize the recommender
dataset_path = '../Food Ingredients and Recipe Dataset with Image Name Mapping.csv'
recommender = RecipeRecommender(dataset_path)

# Set the path to the images directory - corrected to match actual directory structure
images_dir = '../Food Images/Food Images'  # This matches the actual nested directory structure

# Print the absolute path for debugging
print(f"Images directory absolute path: {os.path.abspath(images_dir)}")
print(f"Directory exists: {os.path.exists(images_dir)}")
if os.path.exists(images_dir):
    print(f"Directory contents sample: {os.listdir(images_dir)[:5]}")  # Show first 5 files

# Default image as fallback for missing images
DEFAULT_IMAGE_SVG = '''
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="#f5f5f5"/>
  <text x="100" y="100" font-family="Arial" font-size="16" text-anchor="middle" fill="#888">
    Recipe Image Not Available
  </text>
  <path d="M60,80 C60,70 70,60 80,60 L120,60 C130,60 140,70 140,80 L140,120 C140,130 130,140 120,140 L80,140 C70,140 60,130 60,120 Z" 
        fill="none" stroke="#888" stroke-width="2"/>
  <circle cx="80" cy="80" r="6" fill="#888"/>
  <path d="M70,120 L90,100 L100,110 L120,90 L130,100 L130,120 Z" fill="#888"/>
</svg>
'''

# Serve default image when image is not found
@app.route('/api/images/default-recipe-image')
def default_image():
    svg_data = DEFAULT_IMAGE_SVG.encode('utf-8')
    return Response(svg_data, mimetype='image/svg+xml')

# Test endpoint to list available images
@app.route('/api/test_images', methods=['GET'])
def test_images():
    try:
        if not os.path.exists(images_dir):
            return jsonify({'error': 'Images directory not found'}), 404
        
        # Get a sample of image files
        image_files = os.listdir(images_dir)[:20]  # Get first 20 images
        
        # Create test URLs for these images
        test_images = []
        for img in image_files:
            name, ext = os.path.splitext(img)
            test_images.append({
                'name': name,
                'full_name': img,
                'test_url': f"/api/images/{name}"
            })
        
        return jsonify({
            'message': 'Images found',
            'count': len(image_files),
            'sample_images': test_images
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve images from the Food Images directory - simplified approach
@app.route('/api/images/<path:filename>')
def serve_image(filename):
    print(f"Image request received for: {filename}")
    
    # If the filename is "default-recipe-image", return the default SVG
    if filename == 'default-recipe-image':
        return default_image()
    
    # Define a function to check if a file exists with any of the common extensions
    def find_with_extension(base_name):
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            full_name = f"{base_name}{ext}"
            full_path = os.path.join(images_dir, full_name)
            if os.path.exists(full_path):
                return full_name
        return None
    
    # First try with the exact filename
    file_with_ext = find_with_extension(filename)
    if file_with_ext:
        print(f"Found exact match: {file_with_ext}")
        try:
            response = send_from_directory(images_dir, file_with_ext)
            # Add CORS headers explicitly
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as e:
            print(f"Error serving image {file_with_ext}: {str(e)}")
            return default_image()
    
    # If no exact match, try to find pattern matches
    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
        pattern = os.path.join(images_dir, f"{filename}*{ext}")
        matching_files = glob.glob(pattern)
        if matching_files:
            match_file = os.path.basename(matching_files[0])
            print(f"Found pattern match: {match_file}")
            try:
                response = send_from_directory(images_dir, match_file)
                # Add CORS headers explicitly
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            except Exception as e:
                print(f"Error serving image {match_file}: {str(e)}")
                return default_image()
    
    # If no matching file is found
    print(f"Image not found: {filename}")
    return default_image()

# Load the dataset
@app.route('/api/load_data', methods=['GET'])
def load_data():
    try:
        # Check if the file exists
        if not os.path.exists(dataset_path):
            return jsonify({'error': 'Dataset file not found'}), 404
        
        # Load the dataset
        success = recommender.load_data()
        
        if success:
            # Build the TF-IDF model
            recommender.build_tfidf_model()
            return jsonify({'message': 'Dataset loaded successfully', 'rows': len(recommender.df)}), 200
        else:
            return jsonify({'error': 'Failed to load dataset'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Recommend recipes based on ingredients
@app.route('/api/recommend', methods=['POST'])
def recommend_recipes():
    try:
        # Get ingredients from request
        data = request.get_json()
        user_ingredients = [ingredient.lower() for ingredient in data.get('ingredients', [])]
        
        if not user_ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400
        
        # Make sure data is loaded
        if recommender.df is None:
            # Load data directly instead of calling the route function
            try:
                recommender.load_data()
                recommender.build_tfidf_model()
            except Exception as e:
                return jsonify({'error': f'Failed to load dataset: {str(e)}'}), 500
        
        # Get recommendations
        recommended_recipes = recommender.recommend_recipes_tfidf(user_ingredients, top_n=10)
        
        # Add image URLs to the recipes
        backend_url = request.host_url.rstrip('/')  # Get the base URL of the backend
        for recipe in recommended_recipes:
            if recipe['image_name']:
                # Print debug info for each image
                print(f"Recipe image name: {recipe['image_name']}")
                # Remove file extension if present
                image_name = os.path.splitext(recipe['image_name'])[0]
                # Use absolute URL with the backend host
                recipe['image_url'] = f"{backend_url}/api/images/{image_name}"
                print(f"Set image URL to: {recipe['image_url']}")
        
        return jsonify({'recipes': recommended_recipes}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a simple test HTML page to test image rendering
@app.route('/test-images-page')
def test_images_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Test</title>
        <style>
            .image-container { display: flex; flex-wrap: wrap; }
            .image-item { margin: 10px; text-align: center; }
            img { max-width: 200px; max-height: 200px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>Image Test Page</h1>
        <div class="image-container" id="images">Loading...</div>
        
        <script>
            fetch('/api/test_images')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('images');
                    container.innerHTML = '';
                    
                    data.sample_images.forEach(img => {
                        const div = document.createElement('div');
                        div.className = 'image-item';
                        
                        const image = document.createElement('img');
                        image.src = img.test_url;
                        image.alt = img.name;
                        image.onerror = () => {
                            image.src = 'data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect width="100%" height="100%" fill="#ddd"/><text x="50%" y="50%" font-family="Arial" font-size="14" text-anchor="middle" dominant-baseline="middle">Image Error</text></svg>';
                        };
                        
                        const p = document.createElement('p');
                        p.textContent = img.name;
                        
                        div.appendChild(image);
                        div.appendChild(p);
                        container.appendChild(div);
                    });
                })
                .catch(error => {
                    document.getElementById('images').innerHTML = 'Error loading images: ' + error;
                });
        </script>
    </body>
    </html>
    """
    return html

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# Add root route to handle requests to the root URL
@app.route('/')
def root():
    return jsonify({
        "status": "online",
        "message": "Recipe Recommendation API is running",
        "endpoints": {
            "/": "Root endpoint with API information",
            "/api/health": "Health check endpoint",
            "/api/recommend": "Get recipe recommendations based on ingredients (POST)",
            "/api/images/<filename>": "Get recipe images",
            "/api/test_images": "Test endpoint to list available images"
        }
    })

if __name__ == '__main__':
    # Load data on startup (directly, not through the route)
    try:
        print("Loading dataset...")
        recommender.load_data()
        recommender.build_tfidf_model()
        print("Dataset loaded successfully!")
    except Exception as e:
        print(f"Error loading dataset: {e}")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 