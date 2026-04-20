# Geospatial Emergency Response System

A modern, full-stack emergency dispatch system that intelligently routes GPS-based emergency requests to the most optimal hospitals using geospatial algorithms and multi-criteria scoring.

## Project Overview

The Geospatial Emergency Response System is designed to save lives by rapidly dispatching emergency calls to the most suitable hospitals. When an emergency request is submitted with GPS coordinates, the system:

1. **Identifies nearby hospitals** using KD-Tree vectorial spatial indexing (k-dimensional tree) for deterministic, optimal performance
2. **Calculates distances** using the Haversine formula to determine great-circle distances
3. **Scores hospitals** using a sophisticated multi-weighted algorithm that considers:
   - Travel time (40% weight) - Critical for emergency response
   - Bed availability (25% weight) - Hospital capacity constraints
   - Specialty matching (20% weight) - Cardiac, trauma, burn, stroke, etc.
   - Hospital rating (15% weight) - Quality of care

The system features a responsive React-based frontend with interactive map visualization and a high-performance FastAPI backend optimized for real-time dispatch decisions. Advanced geospatial indexing using KD-Trees enables sub-millisecond hospital lookups for time-critical emergency scenarios.

## Workflow

### Step 1: Emergency Request Submission
- User triggers an emergency request from the React frontend
- GPS coordinates are captured (latitude, longitude)
- Emergency type is specified (cardiac, trauma, burn, stroke, general)

### Step 2: Backend Processing
- FastAPI backend receives the request via `/api/emergency` endpoint
- **Distance Calculation**: Haversine formula computes accurate distances between incident location and each hospital
- **Hospital Filtering**: Filters hospitals by specialty requirements
- **Scoring System**: Applies weighted scoring:
  - **Travel Time Score**: Distance converted to time with penalty of ~5 points per km
  - **Bed Occupancy Score**: Calculates free bed ratio for capacity constraints
  - **Specialty Match Score**: 100 for exact match, 40 for general hospitals, 0 if specialty unavailable
  - **Quality Rating Score**: Hospital reputation/rating factor
  
### Step 3: Results & Dispatch
- Hospitals ranked by composite score (weighted sum of all factors)
- Results returned to frontend sorted by optimization score
- User can view ranked hospitals with distances, scores, and details on interactive map

## Installation Guide

### Prerequisites
- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/)
- **Git** (optional, for cloning repository)

### Backend Setup (FastAPI)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment:**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `fastapi` - Web framework for building APIs
   - `uvicorn` - ASGI server for running FastAPI
   - `pydantic` - Data validation using Python type hints

### Frontend Setup (React + Vite)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**
   ```bash
   npm install
   ```

   This installs:
   - `react` & `react-dom` - UI framework
   - `vite` - Lightning-fast build tool
   - `leaflet` & `react-leaflet` - Interactive mapping
   - `axios` - HTTP client for API calls
   - `tailwindcss` - Utility-first CSS framework

## How to Run

### Option 1: Running Both Services Simultaneously (Recommended)

#### On Windows (PowerShell or CMD):
```bash
# Terminal 1: Start the backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Start the frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

#### On macOS/Linux:
```bash
# Terminal 1: Start the backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2: Start the frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

### What Each Service Does:
- **Backend** (FastAPI): Runs on `http://localhost:8000`
  - API endpoints: `http://localhost:8000/api/emergency`
  - Interactive docs: `http://localhost:8000/docs`
- **Frontend** (React/Vite): Runs on `http://localhost:5173`
  - User interface for submitting emergency requests

### Accessing the Application:
Open your browser and navigate to:
```
http://localhost:5173
```

The frontend will automatically connect to the backend API for emergency dispatch processing.

## CORS Configuration

### What is CORS?
CORS (Cross-Origin Resource Sharing) is a security feature that controls which domains can access your API. Without proper CORS setup, your React frontend (running on a different port) cannot communicate with your FastAPI backend.

### Current Configuration
The backend includes CORS middleware configured to allow requests from all origins (suitable for development):

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Currently allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Production Deployment
⚠️ **Security Note**: The current configuration (`allow_origins=["*"]`) is suitable for development but NOT recommended for production.

For production, replace with specific allowed origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Troubleshooting Connection Issues
If the frontend cannot connect to the backend:
1. Verify both services are running on their respective ports
2. Check browser console for CORS error messages
3. Ensure the frontend is configured with the correct backend URL
4. Review the FastAPI logs for errors

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── hospitals.py            # Hospital database
│   ├── scoring_system.py       # Multi-criteria scoring algorithm
│   ├── a_star_routing.py       # Advanced routing (optional)
│   ├── kdtree.py              # KD-Tree spatial indexing
│   ├── requirements.txt        # Python dependencies
│   ├── performance_test.py     # Performance benchmarking
│   ├── test_kdtree.py         # Unit tests
│   └── test_scoring.py        # Scoring system tests
│
├── frontend/
│   ├── index.html             # HTML entry point
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── src/
│   │   ├── main.jsx           # React entry point
│   │   ├── App.jsx            # Main App component
│   │   ├── App.css            # Application styles
│   │   └── modules/           # Feature modules
│   └── public/                # Static assets
│
└── README.md                  # This file
```

## Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Python 3.8+** - Core language

### Frontend
- **React 19** - UI library
- **Vite** - Build tool
- **Leaflet/React-Leaflet** - Interactive mapping
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Node.js** - Runtime

## API Endpoints

### Emergency Dispatch Endpoint
**POST** `/api/emergency`

Request body:
```json
{
  "lat": 40.7128,
  "lng": -74.0060,
  "type": "cardiac"
}
```

Response:
```json
[
  {
    "name": "Hospital A",
    "distance_km": 2.5,
    "travel_time_minutes": 8,
    "score": 87.5,
    "specialties": ["cardiology", "emergency"],
    "available_beds": 12,
    "rating": 4.8
  },
  ...
]
```

## Performance Optimization

The system uses several optimization techniques:

### Spatial Indexing Strategy: KD-Tree (Vectorial Approach)
The system employs a **KD-Tree (k-dimensional tree)** spatial indexing structure - a deterministic vectorial indexing method, not probabilistic. This approach:

- **Vectorial Partitioning**: Recursively divides 2D space (latitude, longitude coordinates) into rectangular regions
- **Binary Tree Structure**: Creates a balanced tree where each node represents a hospital and splitting planes alternate between dimensions
- **Efficient K-NN Search**: Uses recursive depth-first search with branch pruning to find K-nearest hospitals in O(log N) average time
- **Deterministic Results**: Guarantees exact nearest neighbors, not approximations (unlike probabilistic methods)
- **Suitable for Geospatial**: Ideal for 2D coordinate-based queries with real-world distance metrics (Haversine)

**Why KD-Tree over probabilistic methods?**
- Emergency dispatch requires exact, deterministic results (no approximations)
- Real-time performance: O(log N) lookups vs O(1) probabilistic methods with lower accuracy guarantees
- Low memory overhead compared to learned index structures

### Additional Optimizations
- **Haversine Formula**: Accurate great-circle distance calculations between GPS coordinates
- **Multi-threaded Processing**: Concurrent request handling
- **Caching**: Hospital data pre-loaded in memory

## Testing

Run unit tests for critical components:
```bash
# Backend tests
cd backend
pytest test_kdtree.py
pytest test_scoring.py
python performance_test.py
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Specify your license here]

## Support

For issues or questions, please open an issue on the repository or contact the development team.

---

**Last Updated**: April 2026
