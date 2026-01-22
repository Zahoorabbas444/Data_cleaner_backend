# Data Cleaner & Visual Insight Tool

A web application for uploading, cleaning, validating, and visualizing Excel/CSV data. Built with FastAPI (Python) backend and React frontend.

---

## Features

- **File Upload**: Drag-and-drop CSV/XLSX files (max 10MB)
- **Automated Cleaning**: Remove empty rows/columns, trim whitespace, normalize dates
- **Data Validation**: Detect missing values, duplicates, mixed types, invalid formats
- **Readiness Scoring**: Status badges (Ready/Warning/Not Ready) based on data quality
- **Visualizations**: Auto-generated charts (bar, line, histogram, box plot, heatmap)
- **Reports**: Download cleaned data and validation reports as Excel files
- **Free Tier**: Process up to 100 rows free (watermarked exports)

---

## Project Structure

```
Data-cleaner/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt        # Python dependencies
│   ├── routers/
│   │   ├── upload.py           # File upload & processing endpoints
│   │   └── payment.py          # Stripe payment endpoints
│   ├── services/
│   │   ├── parser.py           # File parsing & normalization
│   │   ├── cleaner.py          # Data cleaning logic
│   │   ├── validator.py        # Validation & scoring
│   │   ├── visualizer.py       # Chart generation
│   │   ├── reporter.py         # Excel report generation
│   │   └── tier_manager.py     # Free/paid tier management
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   └── utils/
│       ├── file_manager.py     # Temp file handling
│       ├── rate_limiter.py     # API rate limiting
│       └── serialization.py    # JSON serialization helpers
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main application
│   │   ├── components/         # React components
│   │   └── services/api.js     # API client
│   ├── package.json
│   └── vite.config.js
├── test_data.csv               # Sample test file
└── PLAN.md                     # Implementation plan
```

---

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

---

## Running the Application

### Development Mode

**Terminal 1 - Start Backend:**

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Start Frontend:**

```bash
cd frontend
npm run dev
```

**Access:**

- Frontend: http://localhost:5173 (or http://localhost:3000 if port 5173 is busy)
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker Mode

```bash
# From project root
docker-compose up --build
```

Access at http://localhost (frontend) and http://localhost:8000 (API)

---

## How It Works

### Workflow Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Upload    │────▶│   Parse &   │────▶│   Clean &   │────▶│  Generate   │
│    File     │     │  Normalize  │     │  Validate   │     │   Charts    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Download   │◀────│   Display   │◀────│   Create    │◀────│   Return    │
│   Reports   │     │   Results   │     │   Reports   │     │   Results   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Step-by-Step Process

#### 1. File Upload

- User uploads CSV or XLSX file via drag-and-drop or file picker
- Backend validates file type and size (max 10MB)
- File is saved to temporary storage with a unique job ID
- Processing starts in background

#### 2. Parsing & Normalization

- File is read into a pandas DataFrame
- Column headers are normalized:
  - Converted to lowercase
  - Whitespace trimmed
  - Spaces replaced with underscores
  - Special characters removed

#### 3. Data Cleaning

The cleaner automatically:

- Removes completely empty rows
- Removes completely empty columns
- Trims whitespace from all string cells
- Normalizes text to lowercase
- Converts date columns to YYYY-MM-DD format
- Coerces invalid numeric values to NaN

#### 4. Validation & Scoring

The validator checks for:

- **Missing Values**: Counts null/empty cells per column
- **Duplicates**: Identifies duplicate rows
- **Mixed Types**: Detects columns with inconsistent data types
- **Invalid Formats**: Flags unparseable dates or numbers

**Status Logic:**
| Status | Criteria |
|--------|----------|
| Ready | 0 critical issues, <5% missing values |
| Warning | Some issues but <20% missing, no blocking errors |
| Not Ready | >20% missing OR >50% duplicates OR critical type errors |

#### 5. Visualization

Auto-generates charts based on column types:

| Column Type              | Chart Generated               |
| ------------------------ | ----------------------------- |
| Categorical (<20 unique) | Bar chart (top 10 values)     |
| Temporal (dates)         | Line chart (trends over time) |
| Numerical                | Histogram + Box plot          |
| All columns              | Missingness heatmap           |

Charts are created in two formats:

- **Static (matplotlib)**: Embedded in Excel reports
- **Interactive (Plotly)**: Displayed in web UI

#### 6. Report Generation

Two downloadable files are created:

**Cleaned Dataset (`_cleaned.xlsx`):**

- Original data with all cleaning operations applied

**Validation Report (`_report.xlsx`):**

- Summary sheet: Overview statistics
- Issues sheet: Detailed problem log
- Column Details: Per-column statistics
- Charts: Embedded visualizations

---

## API Endpoints

| Method | Endpoint                         | Description                         |
| ------ | -------------------------------- | ----------------------------------- |
| POST   | `/api/upload`                    | Upload file, returns job_id         |
| GET    | `/api/status/{job_id}`           | Get processing status (0-100%)      |
| GET    | `/api/results/{job_id}`          | Get validation results + chart data |
| GET    | `/api/download/{job_id}/cleaned` | Download cleaned dataset            |
| GET    | `/api/download/{job_id}/report`  | Download validation report          |
| DELETE | `/api/job/{job_id}`              | Delete job and associated files     |

### Example Usage

```bash
# Upload a file
curl -X POST -F "file=@data.csv" http://localhost:8000/api/upload
# Response: {"job_id": "abc-123", "filename": "data.csv", "message": "..."}

# Check status
curl http://localhost:8000/api/status/abc-123
# Response: {"job_id": "abc-123", "status": "completed", "progress": 100}

# Get results
curl http://localhost:8000/api/results/abc-123

# Download cleaned file
curl -O http://localhost:8000/api/download/abc-123/cleaned
```

---

## Configuration

### Environment Variables

| Variable            | Description                   | Default          |
| ------------------- | ----------------------------- | ---------------- |
| `STRIPE_SECRET_KEY` | Stripe API key for payments   | None (test mode) |
| `STRIPE_PRICE_ID`   | Stripe price ID for paid tier | None             |

### Tier Limits

| Tier | Row Limit | Features                          |
| ---- | --------- | --------------------------------- |
| Free | 100 rows  | Watermarked exports               |
| Paid | Unlimited | Full exports, priority processing |

### Rate Limiting

- 10 uploads per minute per IP address
- Configurable in `utils/rate_limiter.py`

### File Retention

- Uploaded files auto-delete after 30 minutes
- Configurable in `utils/file_manager.py`

---

## Testing

Use the included test file:

```bash
# Upload test data
curl -X POST -F "file=@test_data.csv" http://localhost:8000/api/upload
```

The `test_data.csv` includes intentional issues for testing:

- Whitespace in names (`John Doe`)
- Empty row (row 7)
- Missing salary (Bob Johnson)
- Invalid date (`invalid-date`)
- Invalid number (`not_a_number`)
- Duplicate row (John Doe appears twice)

---

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill the process if needed
kill -9 <PID>
```

### Frontend won't start

```bash
# Check if port is in use
lsof -i :5173
# Or try a different port
npm run dev -- --port 3000
```

### File upload fails

- Check file size (max 10MB)
- Ensure file is CSV or XLSX format
- Check backend logs for errors

### Charts not displaying

- Ensure Plotly.js is loaded in frontend
- Check browser console for JavaScript errors

---

## Tech Stack

**Backend:**

- FastAPI (Python web framework)
- Pandas (data manipulation)
- Matplotlib/Seaborn (static charts)
- Plotly (interactive charts)
- OpenPyXL (Excel file handling)

**Frontend:**

- React 18
- Vite (build tool)
- Plotly.js (chart rendering)
- Axios (HTTP client)

---

## License

MIT License
