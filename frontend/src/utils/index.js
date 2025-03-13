import config from '../config';

/**
 * Get the URL for a recipe image based on its filename
 * @param {string} imageName - The filename of the image
 * @returns {string} The complete URL to the image
 */
export const getImageUrl = (imageName) => {
  if (!imageName) {
    return `${config.API_URL}/api/images/default-recipe-image`;
  }
  
  // Remove file extension if present
  const baseName = imageName.split('.')[0];
  
  return `${config.API_URL}/api/images/${baseName}`;
};

/**
 * Handle image loading errors by substituting with a default image
 * @param {Event} event - The error event from the image
 */
export const handleImageError = (event) => {
  console.log('Image failed to load:', event.target.src);
  event.target.src = `${config.API_URL}/api/images/default-recipe-image`;
}; 