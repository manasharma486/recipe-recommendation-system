# Recipe Recommendation System

A web application that recommends recipes based on available ingredients, featuring an interactive interface and image support.

## Features

- Ingredient-based recipe search
- Interactive chat interface
- Detailed recipe information with images
- Recipe ratings and instructions
- Responsive design
- Ingredient matching highlighting

## Tech Stack

### Backend
- Flask (Python web framework)
- Pandas (Data processing)
- NumPy (Numerical computations)
- scikit-learn (TF-IDF model)
- Flask-CORS (Cross-Origin Resource Sharing)
- Gunicorn (WSGI HTTP Server)

### Frontend
- React
- Tailwind CSS
- Framer Motion (Animations)
- React Intersection Observer

## Prerequisites

- Python 3.9+
- Node.js and npm
- Git

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd recipe-recommendation-system
```

2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

## Running Locally

1. Start the backend server:
```bash
cd backend
python app.py
```
The backend will run on http://localhost:5000

2. Start the frontend development server:
```bash
cd frontend
npm start
```
The frontend will run on http://localhost:3000

## Deployment

This project is configured for deployment on Render.com.

### Deployment Configuration

The project includes a `render.yaml` file that defines the deployment configuration:

1. Backend Web Service:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && gunicorn app:app`
   - Environment Variables:
     - PYTHON_VERSION: 3.9.0
     - PORT: 10000

2. Frontend Static Site:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`
   - Environment Variables:
     - REACT_APP_API_URL: (automatically set to backend URL)

### Deploying to Render

1. Create a Render account at https://render.com
2. Connect your GitHub repository
3. Click "New +" and select "Web Service"
4. Choose your repository
5. Render will automatically detect the configuration from `render.yaml`
6. Click "Create Web Service"

## Project Structure

```
recipe-recommendation-system/
├── backend/
│   ├── app.py                 # Flask application
│   ├── models/               # ML models
│   └── Food Images/          # Recipe images
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── utils/           # Utility functions
│   │   └── config.js        # Configuration
│   └── public/              # Static assets
├── requirements.txt         # Python dependencies
└── render.yaml             # Render deployment config
```

## Usage

1. Enter ingredients in the search bar
2. Get personalized recipe recommendations
3. View detailed recipe information including:
   - Ingredients list with matching highlights
   - Step-by-step instructions
   - Recipe images
   - Ratings

## Troubleshooting

### Common Issues

1. Backend not starting:
   - Check if all Python dependencies are installed
   - Verify Python version (3.9+)
   - Check if port 5000 is available

2. Frontend not connecting:
   - Verify backend URL in `config.js`
   - Check CORS settings
   - Ensure backend is running

3. Images not loading:
   - Verify image paths
   - Check image directory structure
   - Ensure image format is supported (jpg, jpeg, png)

## License

[Your License Here]

## Acknowledgments

- Recipe dataset source
- Image contributors
- Open source libraries used in the project 