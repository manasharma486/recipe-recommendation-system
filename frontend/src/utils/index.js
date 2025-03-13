import config from '../config';

// Base64 encoded fallback image (a simple food plate icon)
const FALLBACK_IMAGE = `data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <rect width="200" height="200" fill="%23f5f5f5"/>
  <text x="100" y="100" font-family="Arial" font-size="16" text-anchor="middle" fill="%23888">
    Recipe Image Not Available
  </text>
  <path d="M60,80 C60,70 70,60 80,60 L120,60 C130,60 140,70 140,80 L140,120 C140,130 130,140 120,140 L80,140 C70,140 60,130 60,120 Z" 
        fill="none" stroke="%23888" stroke-width="2"/>
  <circle cx="80" cy="80" r="6" fill="%23888"/>
  <path d="M70,120 L90,100 L100,110 L120,90 L130,100 L130,120 Z" fill="%23888"/>
</svg>`;

/**
 * Get the URL for a recipe image based on its filename
 * @param {string} imageName - The filename of the image
 * @returns {string} The complete URL to the image
 */
export const getImageUrl = (imageName) => {
  if (!imageName) {
    console.log('No image name provided, using fallback');
    return FALLBACK_IMAGE;
  }
  
  try {
    // Remove file extension if present
    const baseName = imageName.split('.')[0];
    
    // Build API URL
    const imageUrl = `${config.API_URL}/api/images/${baseName}`;
    console.log('Generated image URL:', imageUrl);
    return imageUrl;
  } catch (error) {
    console.error('Error creating image URL:', error);
    return FALLBACK_IMAGE;
  }
};

/**
 * Handle image loading errors by substituting with a fallback image
 * @param {Event} event - The error event from the image
 */
export const handleImageError = (event) => {
  console.log('Image failed to load:', event.target.src);
  event.target.src = FALLBACK_IMAGE;
  // Prevent further error events
  event.target.onerror = null;
}; 