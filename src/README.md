Dependencies: sqlite3, sys, pandas, fastapi, uvicorn
# Running the API server
```bash
git clone https://github.com/kenmbo/olist-eda-dashboard.git
cd olist-eda-dashboard/

# Create virtual environment (to prevent cross-contamination)
python3 -m venv .venv
source .venv/bin/activate

# Install depndencies
pip install pandas statsmodels fastapi uvicorn dotenv

# Run API server
uvicorn src.main:app --reload
```
