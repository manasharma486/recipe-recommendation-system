/**
 * Utility functions for the Recipe Recommendation System
 */

// Base URL for the API - adjust according to your backend deployment
const API_BASE_URL = 'http://localhost:5000';

/**
 * Creates a proper image URL for the given image name
 * 
 * @param {string} imageName - The name of the image (with or without extension)
 * @returns {string} The full URL to the image
 */
export const getImageUrl = (imageName) => {
  if (!imageName) {
    return null;
  }
  
  // Remove any file extension if present
  const nameWithoutExt = imageName.includes('.') 
    ? imageName.substring(0, imageName.lastIndexOf('.')) 
    : imageName;
  
  // Return absolute URL
  return `${API_BASE_URL}/api/images/${nameWithoutExt}`;
};

/**
 * Handles image loading errors by providing a fallback
 * 
 * @param {Event} event - The error event
 */
export const handleImageError = (event) => {
  console.error('Image failed to load:', event.target.src);
  event.target.src = `${API_BASE_URL}/api/images/default-recipe-image`;
  event.target.alt = 'Recipe image unavailable';
  
  // Add a class to style the error state if needed
  event.target.classList.add('image-error');
};

/**
 * Format API request URL
 * 
 * @param {string} endpoint - API endpoint path (without leading slash)
 * @returns {string} The complete API URL
 */
export const apiUrl = (endpoint) => {
  // Ensure endpoint starts without a slash and add it
  const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
  return `${API_BASE_URL}/${path}`;
}; 