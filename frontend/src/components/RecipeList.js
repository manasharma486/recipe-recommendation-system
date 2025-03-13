import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { getImageUrl, handleImageError } from '../utils';
import config from '../config';

const RecipeCard = ({ recipe, index }) => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });
  
  const [showInstructions, setShowInstructions] = useState(false);

  // Helper function to handle ingredients in either string or array format
  const getIngredientsList = (ingredients) => {
    if (!ingredients) return [];
    if (Array.isArray(ingredients)) return ingredients;
    if (typeof ingredients === 'string') return ingredients.split(',').map(i => i.trim());
    return [];
  };
  
  // Calculate match percentage if available
  const matchPercentage = recipe.similarity_score 
    ? Math.round(recipe.similarity_score * 100)
    : null;

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, x: 0 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-xl shadow-md overflow-hidden recipe-card w-full max-w-2xl mx-auto"
    >
      <div className="w-full h-64 bg-gray-200 overflow-hidden">
        {recipe.image_name ? (
          <img 
            src={getImageUrl(recipe.image_name)} 
            alt={recipe.title} 
            className="w-full h-full object-cover"
            onError={handleImageError}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-500">
            No image available
          </div>
        )}
      </div>
      
      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-2xl font-semibold text-gray-800">{recipe.title}</h3>
          {matchPercentage && (
            <span className="bg-green-100 text-green-800 text-sm px-3 py-1 rounded-full">
              {matchPercentage}% match
            </span>
          )}
        </div>
        
        <div className="mb-6">
          {recipe.rating && (
            <p className="text-lg text-gray-600 mb-3">
              <i className="fas fa-star mr-2 text-yellow-500"></i>
              Rating: {recipe.rating.toFixed(1)}/5
            </p>
          )}
          
          <div className="mt-4">
            <h4 className="text-lg font-medium text-gray-700 mb-2">Ingredients:</h4>
            <div className="flex flex-wrap gap-2 mt-2">
              {getIngredientsList(recipe.ingredients).map((ingredient, i) => (
                <span 
                  key={i} 
                  className={`text-sm px-3 py-1 rounded-full ${
                    recipe.matched_ingredients?.includes(ingredient)
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {ingredient}
                </span>
              ))}
            </div>
          </div>
        </div>
        
        <div className="flex flex-col space-y-3">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setShowInstructions(!showInstructions)}
            className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg transition-colors text-lg font-medium"
          >
            {showInstructions ? 'Hide Recipe' : 'View Recipe'}
          </motion.button>
        </div>
        
        {showInstructions && recipe.instructions && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.3 }}
            className="mt-6 p-4 bg-gray-50 rounded-lg"
          >
            <h4 className="text-lg font-medium text-gray-800 mb-3">Instructions:</h4>
            <p className="text-base text-gray-700 whitespace-pre-line leading-relaxed">{recipe.instructions}</p>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

const RecipeList = ({ ingredients }) => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      console.log("API URL being used:", `${config.API_URL}/api/recommend`);
      console.log("Ingredients being sent:", ingredients);

      const response = await fetch(`${config.API_URL}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients }),
      });
      
      console.log("Response status:", response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response:", errorText);
        throw new Error(`Failed to fetch recipes: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      setRecipes(data.recipes || []);
      console.log("Recipes received:", data);
    } catch (error) {
      setError(error.message);
      console.error('Error fetching recipes:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (ingredients && ingredients.length > 0) {
      fetchRecipes();
    }
  }, [ingredients]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!recipes || recipes.length === 0) return <div>No recipes found</div>;

  const goToNextRecipe = () => {
    setCurrentIndex((prev) => (prev + 1) % recipes.length);
  };

  const goToPreviousRecipe = () => {
    setCurrentIndex((prev) => (prev - 1 + recipes.length) % recipes.length);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-800 flex items-center">
          <i className="fas fa-utensils mr-2 text-green-600"></i>
          Recipe {currentIndex + 1} of {recipes.length}
        </h2>
        <div className="flex gap-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={goToPreviousRecipe}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
            disabled={recipes.length <= 1}
          >
            <i className="fas fa-chevron-left mr-1"></i> Previous
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={goToNextRecipe}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
            disabled={recipes.length <= 1}
          >
            Next <i className="fas fa-chevron-right ml-1"></i>
          </motion.button>
        </div>
      </div>
      
      <AnimatePresence mode="wait">
        <RecipeCard 
          key={currentIndex} 
          recipe={recipes[currentIndex]} 
          index={currentIndex} 
        />
      </AnimatePresence>
    </div>
  );
};

export default RecipeList; 