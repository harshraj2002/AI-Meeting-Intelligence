# AI Meeting Intelligence Platform

A web application that extracts actionable insights from meeting recordings. Users can upload audio/video files and receive structured information about action items, decisions, and participant interactions.

***

## Features

- File upload for audio/video (MP3, WAV, MP4, AVI, MOV, M4A, FLAC, up to 100MB)
- Automated speech-to-text (Whisper or faster-whisper/OpenAI Whisper)
- Information extraction using an LLM (Ollama)
- Persistent storage (SQLite)
- Semantic vector search (ChromaDB)
- Frontend dashboard for upload and insights, built with React + Tailwind CSS

***

## Project Structure

```
AI Meeting Intelligence/
├── frontend/
│   ├── public/
│   └── src/
│       ├── pages/
│       │   ├── UploadPage.jsx
│       │   └── MeetingsPage.jsx
│       ├── services/
│       │   └── api.js
│       ├── App.js
│       ├── index.css
│       └── ... (other React files)
│   └── ... (React config files)
├── models/
│   ├── __init__.py
│   └── database.py
├── services/
│   ├── __init__.py
│   ├── insight_extraction.py
│   ├── transcription.py
│   └── vector_store.py
├── uploads/
├── processed/
├── chroma_db/
│   └── chroma.sqlite3
├── config.py
├── main.py
├── meetings.db
└── README.md
```

***

## Requirements

- Python 3.10+
- Node.js 18+ (includes npm and npx)
- [ffmpeg](https://ffmpeg.org/) available in system PATH (for audio extraction)
- Disk space for models and DBs

### Python Packages

- fastapi
- uvicorn
- sqlalchemy
- chromadb
- python-multipart
- requests
- openai-whisper (or faster-whisper)
- (Optional) dotenv for environment variable management

### Node Packages (handled by `npm install`)

- react
- react-router-dom
- react-dropzone
- tailwindcss
- postcss
- autoprefixer

***

## Backend Setup

1. **Clone the repository**  
   Download or clone this directory.

2. **Create a virtual environment**
   ```sh
   python -m venv venv
   ```

3. **Activate the environment**
   - Windows:
     ```sh
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```sh
     source venv/bin/activate
     ```

4. **Install Python dependencies**
   ```sh
   pip install fastapi uvicorn sqlalchemy chromadb python-multipart requests openai-whisper
   ```

   - If you wish to use `faster-whisper` (recommended for local speed on CPU/GPU):
     ```sh
     pip install faster-whisper
     ```

5. **Install and run Ollama (for LLM inference)**
   - See: https://ollama.com/
   - Download and run Ollama; ensure the default LLM (e.g., llama3.2) is available.

6. **Ensure ffmpeg is installed and in your PATH**
   - Download from: https://ffmpeg.org/download.html

7. **Create upload, processed, and chroma_db directories if they do not exist**
   ```sh
   mkdir uploads processed chroma_db
   ```

8. **Run the backend server**
   ```sh
   python main.py
   ```

   The API will be available at `http://localhost:8000`

9. **API Documentation**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs (Swagger).

***

## Frontend Setup

1. **Navigate to the frontend directory**
   ```sh
   cd frontend
   ```

2. **Install Node dependencies**
   ```sh
   npm install
   ```

3. **If not already initialized, run these for Tailwind CSS**
   ```sh
   npm install -D tailwindcss@^3.4.0 postcss autoprefixer
   npx tailwindcss init -p
   ```

4. **Run the frontend**
   ```sh
   npm start
   ```

   The React frontend will be available at `http://localhost:3000`

***

## Configuration

- Edit `config.py` to update backend settings (e.g., database paths, ChromaDB directory, LLM endpoints).
- The default configuration assumes Ollama is running on `http://localhost:11434` and the model is `llama3.2`.
- Adjust `ALLOWED_EXTENSIONS`, upload size, and directory paths as needed in `config.py`.

***

## Usage

1. Open `http://localhost:3000` in your browser.
2. Drag and drop or select an audio/video file on the Upload page.
3. Wait for processing to complete (check backend logs for status).
4. Go to the Meetings page to view processed meetings and their insights.

***

## Troubleshooting

- **`npx` or `npm` not found:** Ensure Node.js (with npm/npx) is installed and in your PATH.
- **Transcription fails:** Make sure ffmpeg is in your PATH and the correct Whisper model is installed.
- **Database errors:** Ensure you have permission to write to files in the project directory.
- **Ollama errors:** Make sure the Ollama server is running, the model is loaded, and accessible at the configured endpoint.

***

## License

This project is for demonstration purposes. For production use, review licenses of all dependencies, models, and services (e.g., Whisper, Ollama).