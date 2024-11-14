# polyglottal-backend

This is the backend for a Real-Time Chat Application using WebSockets, built with FastAPI and Python. 

---

## Technologies Used

- **Python**
- **FastAPI**: for API endpoints and WebSocket connections
- **Poetry**: for dependency management
- **MongoDB with PyMongo**: for database management
- **Uvicorn**: for ASGI server
- **Pydantic**: for data validation
- **python-dotenv**: for environment variable management

## Features

- Real-time chat with WebSockets
- MongoDB database for storing chat messages
- Support for handling user connections and disconnections
- CORS enabled for frontend integration

## Getting Started

### Prerequisites

- **Python** 3.12 or higher
- **Poetry** for managing dependencies. 
- **MongoDB** server (local or remote)

### Installation

1. **Clone the repository**

2. **Install dependencies using Poetry**
   
```bash
poetry install
```

3. **Set up MongoDB**: Ensure MongoDB is running locally or specify a remote connection URL in the environment variables.

## Environment Variables

Create a .env file in the root directory of the project and add the following variables:

```env
FRONTEND_URL=http://localhost:5173 # API endpoint for backend
MONGODB_CONN_STRING="mongodb://localhost:27017" # MongoDB connection URL
```

## Running the Application

1. **Start the FastAPI Server**

```bash
poetry run uvicorn main:app --reload
```

2. **Access the API**: The API will be available at http://localhost:8000.

- You can check out the interactive documentation at http://localhost:8000/docs.

3. **WebSocket Testing**: Use the WebSocket URL (ws://localhost:8000).
