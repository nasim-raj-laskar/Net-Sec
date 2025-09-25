# NetworkSecurity - Phishing Detection System

AI-powered phishing detection system with integrated web interface for file upload, model training, and results visualization.

## Features

- **Phishing Detection**: Upload CSV files for bulk phishing website analysis
- **Model Training**: Train ML models with real-time progress tracking
- **Results Visualization**: View predictions with enhanced table formatting
- **Single Page Interface**: All features accessible from one unified page

## Quick Start

### Windows
```bash
start_server.bat
```

### Linux/Mac
```bash
chmod +x start_server.sh
./start_server.sh
```

### Manual Start
```bash
python app.py
```

Open browser: http://localhost:8000

## Requirements

- Python 3.8+
- MongoDB connection
- Required packages in requirements.txt

## Usage

1. **Upload CSV**: Select file and click "Analyze File"
2. **Train Model**: Click "Start Training" to update the model
3. **Download Results**: Export predictions as CSV file

## API Endpoints

- `GET /` - Main application interface
- `POST /predict` - File upload and prediction
- `GET /train` - Model training endpoint