// Base URL for API
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Fallback image as a data URL - an embedded SVG for recipe images
const FALLBACK_IMAGE = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZpbGw9IiM4ODgiPlJlY2lwZTwvdGV4dD48dGV4dCB4PSI1MCUiIHk9IjYyJSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjI0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSIgZmlsbD0iIzg4OCI+SW1hZ2U8L3RleHQ+PHRleHQgeD0iNTAlIiB5PSI3NCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIzMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZpbGw9IiM4ODgiPu+MhDwvdGV4dD48L3N2Zz4=';

/**
 * Get the image URL for a recipe
 * @param {string} imageName - The name of the image
 * @returns {string} - The URL of the image
 */
export const getImageUrl = (imageName) => {
  console.log(`Getting image URL for: ${imageName}`);
  
  // If no image name or the default image is requested, return the fallback image
  if (!imageName || imageName === 'default-recipe-image') {
    console.log('Using embedded fallback image');
    return FALLBACK_IMAGE;
  }

  // Remove file extension if present
  const imagePath = imageName.includes('.') 
    ? imageName.substring(0, imageName.lastIndexOf('.')) 
    : imageName;
  
  // Return the proper URL for the image
  return `${API_URL}/api/images/${imagePath}`;
};

/**
 * Handle image loading errors by setting the src to the fallback image
 * @param {Event} event - The error event
 */
export const handleImageError = (event) => {
  console.log('Image failed to load, using fallback');
  event.target.src = FALLBACK_IMAGE;
  // Remove onerror to prevent loops
  event.target.onerror = null; 
}; 