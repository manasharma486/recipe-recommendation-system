import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <div className="flex items-center">
              <span className="text-2xl mr-2">🍳</span>
              <h2 className="text-xl font-bold">Recipe Finder</h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Find delicious recipes with ingredients you already have
            </p>
          </div>
          
          <div className="flex flex-col md:flex-row md:space-x-8">
            <div className="mb-4 md:mb-0">
              <h3 className="text-lg font-semibold mb-2">Features</h3>
              <ul className="text-gray-400 text-sm space-y-1">
                <li>Ingredient-based search</li>
                <li>AI-powered recommendations</li>
                <li>Easy-to-follow recipes</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">Connect</h3>
              <div className="flex space-x-4 text-xl">
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <i className="fab fa-github"></i>
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <i className="fab fa-twitter"></i>
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <i className="fab fa-linkedin"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-6 pt-6 text-center text-gray-400 text-sm">
          <p>&copy; {new Date().getFullYear()} Recipe Finder. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 