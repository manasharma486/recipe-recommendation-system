# Recipe Recommendation System

A web application that recommends recipes based on the ingredients you have available. Simply enter the ingredients you have in your kitchen, and the system will suggest recipes you can make.

## Features

- **Ingredient-Based Recipe Search**: Enter ingredients you have, and get matching recipes
- **Interactive Chat Interface**: Easy-to-use chat interface for entering ingredients
- **Recipe Details**: View detailed recipe information including ingredients, instructions, and ratings
- **Image Support**: Visual representation of recipes with food images
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- **Flask**: Python web framework for the API
- **Pandas**: For data processing and manipulation
- **NumPy**: For numerical operations
- **CORS**: For cross-origin resource sharing

### Frontend
- **React**: JavaScript library for building the user interface
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Framer Motion**: For smooth animations and transitions
- **React Intersection Observer**: For lazy loading components

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+**: For running the backend server
- **Node.js and npm**: For running the frontend application

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd recipe-recommendation-system
```

### 2. Set Up the Backend

Navigate to the backend directory and install the required Python packages:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Set Up the Frontend

Navigate to the frontend directory and install the required npm packages:

```bash
cd ../frontend
npm install
```

## Running the Application

### 1. Start the Backend Server

From the project root directory:

```bash
cd backend
python app.py
```

The Flask server will start running at `http://localhost:5000`.

### 2. Start the Frontend Development Server

Open a new terminal window, navigate to the project root directory, and run:

```bash
cd frontend
npm start
```

The React development server will start running at `http://localhost:3000`.

### 3. Access the Application

Open your web browser and go to `http://localhost:3000` to use the application.

## How to Use

1. **Enter Ingredients**: Type the ingredients you have in the chat box (e.g., "chicken, rice, tomatoes")
2. **Get Recommendations**: The system will analyze your ingredients and suggest recipes
3. **View Recipe Details**: Click "View Recipe" to see the full instructions
4. **Try Different Combinations**: Experiment with different ingredient combinations to discover new recipes

## Troubleshooting

### Backend Issues

- **Missing Dataset**: Ensure the dataset file is in the correct location
- **Port Already in Use**: If port 5000 is already in use, modify the port in `app.py`
- **Module Not Found**: Make sure all required packages are installed with `pip install -r requirements.txt`

### Frontend Issues

- **Node Modules Missing**: Run `npm install` in the frontend directory
- **Connection to Backend Failed**: Ensure the backend server is running
- **Image Loading Issues**: Check that the image paths in the backend are correct

## Project Structure

```
recipe-recommendation-system/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models/                # ML models and recommendation logic
│   │   └── recommendation_model.py
│   ├── data/                  # Data storage
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/                # Static files
│   ├── src/                   # React source code
│   │   ├── components/        # React components
│   │   ├── App.js             # Main application component
│   │   └── index.js           # Entry point
│   └── package.json           # npm dependencies
├── Food Images/               # Recipe images
└── README.md                  # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Recipe data sourced from Epicurious (https://www.epicurious.com/)
- Food images included in the dataset 