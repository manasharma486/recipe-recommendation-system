import React from 'react';
import { motion } from 'framer-motion';

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-green-600 to-teal-500 text-white shadow-md">
      <div className="container mx-auto px-4 py-6">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex flex-col md:flex-row justify-between items-center"
        >
          <div className="flex items-center mb-4 md:mb-0">
            <motion.div
              whileHover={{ rotate: 10 }}
              className="mr-3 text-3xl"
            >
              🍳
            </motion.div>
            <h1 className="text-2xl md:text-3xl font-bold">Recipe Finder</h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <p className="hidden md:block text-sm md:text-base">
              Find delicious recipes with ingredients you already have!
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-white text-green-600 px-4 py-2 rounded-lg font-medium shadow-sm hover:shadow-md transition-all"
            >
              <i className="fas fa-info-circle mr-2"></i>
              How It Works
            </motion.button>
          </div>
        </motion.div>
      </div>
    </header>
  );
};

export default Header; 