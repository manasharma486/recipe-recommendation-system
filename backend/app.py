from flask import Flask, request, jsonify, send_from_directory, Response, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import glob
import base64
import sys
# import tensorflow as tf  # Removing TensorFlow import
from models.recommendation_model import RecipeRecommender
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../Food Images')
# Enable full CORS support for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Get the absolute path of the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)  # Go up one directory to project root

# Use absolute paths for datasets and images
dataset_path = os.path.join(base_dir, 'Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
images_dir = os.path.join(base_dir, 'Food Images', 'Food Images')

# Print the paths for debugging
print(f"Current directory: {current_dir}")
print(f"Base directory: {base_dir}")
print(f"Dataset path: {dataset_path}")
print(f"Images directory: {images_dir}")
print(f"Dataset exists: {os.path.exists(dataset_path)}")
print(f"Images directory exists: {os.path.exists(images_dir)}")

# Initialize the recommender
recommender = RecipeRecommender(dataset_path)

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
    """Return a default image SVG when no recipe image is available"""
    print("Serving default image")
    svg_data = DEFAULT_IMAGE_SVG.encode('utf-8')
    response = Response(svg_data, mimetype='image/svg+xml')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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

# Serve images from the Food Images folder
@app.route('/api/images/<image_name>')
def serve_image(image_name):
    # Clean up the image name to prevent directory traversal
    image_name = os.path.basename(image_name)
    
    # First, try to find an exact match with extension
    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
        image_path = os.path.join(images_dir, f"{image_name}{ext}")
        if os.path.exists(image_path):
            response = send_file(image_path, mimetype=f'image/{ext[1:]}')
            # Add CORS headers
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'GET')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Cache-Control', 'max-age=86400')  # Cache for 24 hours
            return response
    
    # If we got here, we couldn't find the image with any extension
    print(f"Image not found: {image_name}", file=sys.stderr)
    
    # Return a 404 instead of redirecting to a default image
    # This will let the frontend handle the fallback with an embedded image
    return jsonify({"error": "Image not found"}), 404

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
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_ingredients = [ingredient.lower() for ingredient in data.get('ingredients', [])]
        
        print(f"Received ingredients: {user_ingredients}")
        
        if not user_ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400
        
        # Make sure data is loaded
        if recommender.df is None:
            # Try to load data
            try:
                print("Loading dataset...")
                success = recommender.load_data()
                if not success:
                    return jsonify({'error': 'Failed to load dataset'}), 500
                    
                recommender.build_tfidf_model()
                print("Dataset loaded successfully!")
            except Exception as e:
                print(f"Error loading dataset: {str(e)}", file=sys.stderr)
                return jsonify({'error': f'Failed to load dataset: {str(e)}'}), 500
        
        # Get recommendations
        try:
            recommended_recipes = recommender.recommend_recipes_tfidf(user_ingredients, top_n=10)
            print(f"Found {len(recommended_recipes)} recipes")
        except Exception as e:
            print(f"Error getting recommendations: {str(e)}", file=sys.stderr)
            return jsonify({'error': f'Error getting recommendations: {str(e)}'}), 500
        
        # Add image URLs to the recipes
        backend_url = request.host_url.rstrip('/')  # Get the base URL of the backend
        for recipe in recommended_recipes:
            if recipe.get('image_name'):
                # Check if file exists
                image_name = os.path.splitext(recipe['image_name'])[0]
                
                # Don't set image_url if we don't have the image file
                # This will make frontend use the embedded fallback
                found_image = False
                for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    full_name = f"{image_name}{ext}"
                    full_path = os.path.join(images_dir, full_name)
                    if os.path.exists(full_path):
                        found_image = True
                        break
                
                if found_image:
                    recipe['image_url'] = f"{backend_url}/api/images/{image_name}"
                    print(f"Set image URL to: {recipe['image_url']}")
                else:
                    # Instead of serving a "default" image that might get blocked,
                    # just don't set an image URL, forcing frontend to use embedded image
                    recipe['image_name'] = None  # Let frontend use embedded fallback
                    print(f"Image not found for: {image_name}, using frontend fallback")
        
        # Add CORS headers to the response
        response = jsonify({'recipes': recommended_recipes})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    
    except Exception as e:
        print(f"Unexpected error in recommend_recipes: {str(e)}", file=sys.stderr)
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

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test route to check if the dataset is loaded properly"""
    try:
        # Check dataset status
        dataset_loaded = recommender.df is not None
        
        # If not loaded, try to load it
        if not dataset_loaded:
            try:
                print("Attempting to load dataset...")
                success = recommender.load_data()
                if success:
                    recommender.build_tfidf_model()
                    dataset_loaded = True
                    print("Dataset loaded successfully on test!")
                else:
                    print("Failed to load dataset during test")
            except Exception as e:
                print(f"Error loading dataset during test: {e}", file=sys.stderr)
        
        # Create a test recipe if dataset is loaded
        test_recipe = None
        if dataset_loaded and recommender.df is not None and len(recommender.df) > 0:
            try:
                # Get the first recipe as a test
                test_idx = 0
                test_recipe = {
                    'id': int(test_idx),
                    'title': recommender.df.iloc[test_idx]['Title'],
                    'columns_available': recommender.df.columns.tolist()
                }
            except Exception as e:
                print(f"Error creating test recipe: {e}", file=sys.stderr)
        
        return jsonify({
            'status': 'API is working',
            'dataset_loaded': dataset_loaded,
            'dataset_path': dataset_path,
            'dataset_exists': os.path.exists(dataset_path),
            'dataset_size': os.path.getsize(dataset_path) if os.path.exists(dataset_path) else 0,
            'test_recipe': test_recipe
        })
        
    except Exception as e:
        print(f"Error in test API: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

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