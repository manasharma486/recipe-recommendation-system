import numpy as np
import pandas as pd

class RecipeRecommender:
    def __init__(self, dataset_path):
        """
        Initialize the recipe recommender with a dataset
        
        Args:
            dataset_path (str): Path to the recipe dataset CSV
        """
        self.dataset_path = dataset_path
        self.df = None
        
    def load_data(self):
        """Load and preprocess the recipe dataset"""
        try:
            self.df = pd.read_csv(self.dataset_path)
            # Clean and preprocess ingredients
            self.df['ingredients_list'] = self.df['Cleaned_Ingredients'].apply(lambda x: x.lower().split(', '))
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def build_tfidf_model(self):
        """Placeholder for compatibility"""
        return True
    
    def recommend_recipes_tfidf(self, user_ingredients, top_n=10):
        """
        Recommend recipes based on user ingredients using a simple matching algorithm
        
        Args:
            user_ingredients (list): List of ingredients the user has
            top_n (int): Number of recipes to recommend
            
        Returns:
            list: List of recommended recipe dictionaries
        """
        if self.df is None:
            raise ValueError("Dataset not loaded. Call load_data() first.")
        
        # Convert user ingredients to lowercase
        user_ingredients = [ing.lower() for ing in user_ingredients]
        
        # Calculate a simple match score for each recipe
        recipe_scores = []
        
        for idx, row in self.df.iterrows():
            recipe_ingredients = row['ingredients_list']
            
            # Count how many user ingredients are in the recipe
            matches = sum(1 for ing in user_ingredients if any(ing in recipe_ing for recipe_ing in recipe_ingredients))
            
            # Calculate a simple score based on the number of matches and total ingredients
            if matches > 0:
                # Higher score for recipes with more matches and fewer total ingredients
                score = matches / len(recipe_ingredients)
                recipe_scores.append((idx, score))
        
        # Sort recipes by score (descending)
        recipe_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N recipes
        top_recipes = recipe_scores[:top_n]
        
        # Create recipe dictionaries
        recommended_recipes = []
        for idx, score in top_recipes:
            recipe = {
                'id': int(idx),
                'title': self.df.iloc[idx]['Title'],
                'ingredients': self.df.iloc[idx]['Cleaned_Ingredients'].split(', '),
                'instructions': self.df.iloc[idx]['Instructions'],
                'rating': float(self.df.iloc[idx]['Rating']) if 'Rating' in self.df.columns else None,
                'image_name': self.df.iloc[idx]['Image_Name'] if 'Image_Name' in self.df.columns else None,
                'similarity_score': float(score)
            }
            recommended_recipes.append(recipe)
        
        return recommended_recipes 