import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Header from './components/Header';
import ChatBox from './components/ChatBox';
import RecipeList from './components/RecipeList';
import Footer from './components/Footer';

function App() {
  const [ingredients, setIngredients] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { 
      id: 1, 
      text: "Hello! I'm your recipe assistant. Tell me what ingredients you have, and I'll suggest some delicious recipes!", 
      sender: 'bot' 
    }
  ]);

  const addMessage = (text, sender) => {
    const newMessage = {
      id: messages.length + 1,
      text,
      sender
    };
    setMessages([...messages, newMessage]);
  };

  // Function to extract ingredients from user input
  const extractIngredients = (userInput) => {
    // Remove common phrases that might precede ingredient lists
    const cleanedInput = userInput
      .toLowerCase()
      .replace(/i have|i've got|i've|i got|i am using|using|with|got|have/g, '')
      .trim();
    
    // Split by common separators
    const extractedIngredients = cleanedInput
      .split(/,|\s+and\s+|\s+&\s+|\n|;/)
      .map(item => item.trim())
      .filter(item => item.length > 2); // Filter out very short items
    
    return extractedIngredients;
  };

  const handleSendIngredients = async (userInput) => {
    setLoading(true);
    addMessage(userInput, 'user');
    
    // Extract ingredients from user input
    const extractedIngredients = extractIngredients(userInput);
    
    if (extractedIngredients.length === 0) {
      addMessage("I couldn't identify any ingredients in your message. Please list the ingredients you have, separated by commas.", 'bot');
      setLoading(false);
      return;
    }
    
    setIngredients(extractedIngredients);
    
    // Add a message showing the extracted ingredients
    addMessage(`I identified these ingredients: ${extractedIngredients.join(', ')}. Let me find some recipes for you...`, 'bot');
    
    try {
      const response = await fetch('http://localhost:5000/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ingredients: extractedIngredients }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch recipes');
      }
      
      const data = await response.json();
      
      // Process recipes to add matched_ingredients
      const processedRecipes = data.recipes.map(recipe => {
        const recipeIngredients = recipe.ingredients;
        const matchedIngredients = extractedIngredients.filter(ing => 
          recipeIngredients.some(recipeIng => recipeIng.toLowerCase().includes(ing.toLowerCase()))
        );
        
        return {
          ...recipe,
          matched_ingredients: matchedIngredients
        };
      });
      
      setRecipes(processedRecipes);
      
      // Add bot response
      if (processedRecipes.length > 0) {
        addMessage(`I found ${processedRecipes.length} recipes you can make with those ingredients! Check them out below.`, 'bot');
      } else {
        addMessage("I couldn't find any recipes with those exact ingredients. Try adding more ingredients or being more general.", 'bot');
      }
      
    } catch (error) {
      console.error('Error:', error);
      addMessage('Sorry, I had trouble finding recipes. Please try again.', 'bot');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Header />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-1 lg:grid-cols-2 gap-8"
        >
          <ChatBox 
            messages={messages} 
            onSendMessage={handleSendIngredients} 
            loading={loading}
          />
          
          <RecipeList recipes={recipes} />
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App; 