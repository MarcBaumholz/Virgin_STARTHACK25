from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from vector_store import build_qdrant_vectorstore
from agent import create_advanced_qa_agent, analyze_trends, suggest_collaborations
import pandas as pd
import json
from pathlib import Path
import os
from analysis import extract_companies, extract_challenges, rate_initiatives

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Only mount static files if directory exists
static_dir = Path("static")
if (static_dir.exists()):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize on startup
CSV_PATH = "Virgin_StartHack_Sample_Initiatives.csv"
vectorstore = build_qdrant_vectorstore(CSV_PATH)
agent = create_advanced_qa_agent(vectorstore, CSV_PATH)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        # Try loading the CSV with error handling
        try:
            df = pd.read_csv(CSV_PATH, encoding='cp1252')  # Explicitly use Windows encoding
        except UnicodeDecodeError:
            # Fallback encodings
            for encoding in ['utf-8-sig', 'utf-8', 'latin1', 'iso-8859-1']:
                try:
                    df = pd.read_csv(CSV_PATH, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
        
        if df is None:
            raise ValueError("Could not read CSV file with any supported encoding")
        
        # Continue with data preparation
        initiatives_by_company = df['Virgin Company'].value_counts().to_dict()
        trends = analyze_trends(CSV_PATH)
        collaborations = suggest_collaborations(CSV_PATH)
        
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "chart_data": json.dumps(initiatives_by_company),
                "trends": trends,
                "collaborations": collaborations,
                "total_initiatives": len(df),
                "error": None
            }
        )
    except Exception as e:
        # Return the dashboard template with error message
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "error": str(e),
                "chart_data": "{}",
                "trends": "Error loading trends",
                "collaborations": "Error loading collaborations",
                "total_initiatives": 0
            },
            status_code=200  # Still return 200 to show error in dashboard
        )

@app.post("/query")
async def query(query: str = Form(...)):
    try:
        result = agent.run(query)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/initiatives")
async def get_initiatives(company: str = None):
    df = pd.read_csv(CSV_PATH)
    if company:
        df = df[df['Virgin Company'] == company]
    return df.to_dict(orient='records')

@app.get("/api/analysis")
async def get_analysis(type: str = None):
    """Get comprehensive analysis of Virgin initiatives"""
    try:
        if type == "summarize":
            return {
                "result": {
                    "companies": extract_companies(CSV_PATH),
                    "challenges": extract_challenges(CSV_PATH),
                    "ratings": rate_initiatives(CSV_PATH)
                }
            }
        elif type == "labels":
            return {"result": agent.run("Use Assign_Labels to categorize all projects")}
        elif type == "trends":
            return {"result": analyze_trends(CSV_PATH)}
        else:
            return {
                "companies": extract_companies(CSV_PATH),
                "challenges": extract_challenges(CSV_PATH),
                "ratings": rate_initiatives(CSV_PATH),
                "trends": analyze_trends(CSV_PATH)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
