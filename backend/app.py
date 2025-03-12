from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import glob
# import tensorflow as tf  # Removing TensorFlow import
from models.recommendation_model import RecipeRecommender

app = Flask(__name__)
CORS(app)

# Initialize the recommender
dataset_path = '../Food Ingredients and Recipe Dataset with Image Name Mapping.csv'
recommender = RecipeRecommender(dataset_path)

# Set the path to the images directory
images_dir = '../Food Images/Food Images'

# Serve images from the Food Images directory
@app.route('/api/images/<path:filename>')
def serve_image(filename):
    # Check if the file exists with various extensions
    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
        # First try exact match
        full_path = os.path.join(images_dir, filename + ext)
        if os.path.exists(full_path):
            print(f"Serving image: {full_path}")
            return send_from_directory(images_dir, filename + ext)
        
        # If not found, try to find a file that starts with the filename
        pattern = os.path.join(images_dir, filename + '*' + ext)
        matching_files = glob.glob(pattern)
        if matching_files:
            # Use the first matching file
            matching_file = os.path.basename(matching_files[0])
            print(f"Serving image: {matching_file}")
            return send_from_directory(images_dir, matching_file)
    
    # If no matching file is found, return a 404 error
    print(f"Image not found: {filename}")
    return jsonify({'error': 'Image not found'}), 404

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
        for recipe in recommended_recipes:
            if recipe['image_name']:
                recipe['image_url'] = f"/api/images/{recipe['image_name']}"
        
        return jsonify({'recipes': recommended_recipes}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Load data on startup (directly, not through the route)
    try:
        print("Loading dataset...")
        recommender.load_data()
        recommender.build_tfidf_model()
        print("Dataset loaded successfully!")
    except Exception as e:
        print(f"Error loading dataset: {e}")
    
    # Run the Flask app
    app.run(debug=True) 