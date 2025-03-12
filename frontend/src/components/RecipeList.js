import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

const RecipeCard = ({ recipe, index }) => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });
  
  const [showInstructions, setShowInstructions] = useState(false);
  
  // Determine which ingredients the user has and which are missing
  const userIngredients = recipe.matched_ingredients || [];
  const allIngredients = recipe.ingredients || [];
  
  // Calculate match percentage
  const matchPercentage = userIngredients.length > 0 
    ? Math.round((userIngredients.length / allIngredients.length) * 100) 
    : 0;

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className="bg-white rounded-xl shadow-md overflow-hidden recipe-card"
    >
      {(recipe.image_url || recipe.image_name) && (
        <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
          <img 
            src={recipe.image_url || `http://localhost:5000/api/images/${recipe.image_name}`} 
            alt={recipe.title} 
            className="w-full h-48 object-cover"
            loading="lazy"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = 'https://via.placeholder.com/400x300?text=No+Image+Available';
            }}
          />
        </div>
      )}
      
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-semibold text-gray-800">{recipe.title}</h3>
          {recipe.similarity_score && (
            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
              {Math.round(recipe.similarity_score * 100)}% match
            </span>
          )}
        </div>
        
        <div className="mb-3">
          {recipe.rating && (
            <p className="text-sm text-gray-600 mb-1">
              <i className="fas fa-star mr-1 text-yellow-500"></i>
              Rating: {recipe.rating.toFixed(1)}/5
            </p>
          )}
          
          <div className="mt-3">
            <h4 className="text-sm font-medium text-gray-700 mb-1">Ingredients:</h4>
            <div className="flex flex-wrap gap-1 mt-1">
              {allIngredients.map((ingredient, i) => (
                <span 
                  key={i} 
                  className={`text-xs px-2 py-1 rounded-full ${
                    userIngredients.includes(ingredient)
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
        
        <div className="flex flex-col space-y-2">
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={() => setShowInstructions(!showInstructions)}
            className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg transition-colors"
          >
            {showInstructions ? 'Hide Recipe' : 'View Recipe'}
          </motion.button>
        </div>
        
        {showInstructions && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.3 }}
            className="mt-4 p-3 bg-gray-50 rounded-lg"
          >
            <h4 className="font-medium text-gray-800 mb-2">Instructions:</h4>
            <p className="text-sm text-gray-700 whitespace-pre-line">{recipe.instructions}</p>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

const RecipeList = ({ recipes }) => {
  if (!recipes || recipes.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 h-full flex flex-col justify-center items-center text-center">
        <div className="text-6xl mb-4">🍽️</div>
        <h2 className="text-xl font-semibold text-gray-800 mb-2">No Recipes Yet</h2>
        <p className="text-gray-600">
          Tell me what ingredients you have, and I'll find matching recipes for you!
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
        <i className="fas fa-utensils mr-2 text-green-600"></i>
        Recommended Recipes ({recipes.length})
      </h2>
      
      <div className="grid grid-cols-1 gap-6">
        {recipes.map((recipe, index) => (
          <RecipeCard key={recipe.id || index} recipe={recipe} index={index} />
        ))}
      </div>
    </div>
  );
};

export default RecipeList; 