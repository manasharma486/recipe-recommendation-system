import os
import shutil
import pandas as pd

def setup_data():
    """
    Copy the dataset to the backend data directory and create a smaller version for testing
    """
    print("Setting up data for the recipe recommendation system...")
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created data directory")
    
    # Path to the original dataset
    original_dataset = '../Food Ingredients and Recipe Dataset with Image Name Mapping.csv'
    
    # Check if the original dataset exists
    if not os.path.exists(original_dataset):
        print(f"Error: Original dataset not found at {original_dataset}")
        return False
    
    # Copy the dataset to the data directory
    target_path = 'data/recipes_full.csv'
    shutil.copy(original_dataset, target_path)
    print(f"Copied dataset to {target_path}")
    
    # Create a smaller version for testing
    try:
        df = pd.read_csv(target_path)
        # Take a sample of 1000 recipes
        sample_df = df.sample(n=min(1000, len(df)), random_state=42)
        sample_df.to_csv('data/recipes_sample.csv', index=False)
        print(f"Created sample dataset with {len(sample_df)} recipes")
        
        # Print dataset info
        print(f"Full dataset has {len(df)} recipes")
        print(f"Columns: {', '.join(df.columns)}")
        
        return True
    except Exception as e:
        print(f"Error creating sample dataset: {e}")
        return False

if __name__ == "__main__":
    setup_data() 