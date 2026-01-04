from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# CONSTANTS
API_KEY = os.getenv("MARKETAUX_API_KEY")
URL = "https://api.marketaux.com/v1/news/all"
LANGUAGE = "en"
LIMIT = 10

# ETF Categories
# Defense & Aerospace ETFs (including European exposure)
DEFENSE_AEROSPACE_ETFS = "ITA,PPA,XAR,DFEN,EUAD,EUDF"  # US Aerospace & Defense ETFs

# Cloud, Tech & AI ETFs
CLOUD_TECH_AI_ETFS = "CLOU,SKYY,WCLD,BOTZ,ROBT,AIQ,ARKK,QQQ,IGV,VGT"

# Semiconductor ETFs
SEMICONDUCTOR_ETFS = "SMH,SOXX,XSD,SOXL,PSI"

# Combined default ETF list
DEFAULT_ETFS = f"{DEFENSE_AEROSPACE_ETFS},{CLOUD_TECH_AI_ETFS},{SEMICONDUCTOR_ETFS}"

# Stock symbols for these sectors (optional, can be used alongside ETFs)
DEFENSE_STOCKS = "BA,LMT,NOC,RTX,GD,TXT,HII"
TECH_AI_STOCKS = "AAPL,MSFT,GOOGL,META,NVDA,AMZN,TSLA,PLTR,C3AI"
SEMICONDUCTOR_STOCKS = "NVDA,AMD,INTC,AVGO,QCOM,TXN,MU,AMAT,LRCX,KLAC"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/news")
def get_news(
    symbols: str = None,
    limit: int = 10,
    include_etfs: bool = False,
    include_stocks: bool = True,
    filter_entities: bool = False,
    industries: str = "Technology,Industrials"
):
    """
    Get latest market news from Marketaux API filtered by industries and optionally by symbols
    
    Args:
        symbols: Comma-separated symbols (ETFs/stocks). If None, uses defaults based on flags
        limit: Number of articles to return (default: 10)
        include_etfs: Include ETFs in default symbols (default: False)
        include_stocks: Include individual stocks in default symbols (default: True)
        filter_entities: If True, only show news mentioning the symbols (default: False, more results)
        industries: Industry categories to filter by (default: Technology,Industrials)
    
    ETF Categories available:
    - Defense & Aerospace: ITA, PPA, XAR, DFEN
    - Cloud/Tech/AI: CLOU, SKYY, WCLD, BOTZ, ROBT, AIQ, ARKK, QQQ, IGV, VGT
    - Semiconductors: SMH, SOXX, XSD, SOXL, PSI
    """
    # Build default symbols list based on flags
    if symbols is None and (include_etfs or include_stocks):
        symbol_list = []
        if include_etfs:
            symbol_list.append(DEFAULT_ETFS)
        if include_stocks:
            symbol_list.append(f"{DEFENSE_STOCKS},{TECH_AI_STOCKS},{SEMICONDUCTOR_STOCKS}")
        symbols = ",".join(symbol_list) if symbol_list else None
    
    params = {
        "api_token": API_KEY,
        "language": LANGUAGE,
        "limit": limit,
        "industries": industries,
    }
    
    # Only add symbols filter if provided
    if symbols:
        params["symbols"] = symbols
        if filter_entities:
            params["filter_entities"] = "true"
    
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "status": "success",
            "total_articles": len(data.get("data", [])),
            "filters": {
                "industries": industries,
                "symbols": symbols,
                "limit": limit,
                "include_etfs": include_etfs,
                "include_stocks": include_stocks,
                "filter_entities": filter_entities
            },
            "news": data
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@app.get("/news/defense-aerospace")
def get_defense_aerospace_news(limit: int = 10, filter_entities: bool = False):
    """Get news for Defense & Aerospace sector"""
    params = {
        "api_token": API_KEY,
        "language": LANGUAGE,
        "limit": limit,
        "industries": "Industrials",
        "symbols": f"{DEFENSE_AEROSPACE_ETFS},{DEFENSE_STOCKS}",
    }
    if filter_entities:
        params["filter_entities"] = "true"
    
    response = requests.get(URL, params=params)
    response.raise_for_status()
    return {"status": "success", "category": "Defense & Aerospace", "news": response.json()}


@app.get("/news/cloud-tech-ai")
def get_cloud_tech_ai_news(limit: int = 10, filter_entities: bool = False):
    """Get news for Cloud, Tech & AI sector"""
    params = {
        "api_token": API_KEY,
        "language": LANGUAGE,
        "limit": limit,
        "industries": "Technology",
        "symbols": f"{CLOUD_TECH_AI_ETFS},{TECH_AI_STOCKS}",
    }
    if filter_entities:
        params["filter_entities"] = "true"
    
    response = requests.get(URL, params=params)
    response.raise_for_status()
    return {"status": "success", "category": "Cloud, Tech & AI", "news": response.json()}


@app.get("/news/semiconductors")
def get_semiconductor_news(limit: int = 10, filter_entities: bool = False):
    """Get news for Semiconductor sector"""
    params = {
        "api_token": API_KEY,
        "language": LANGUAGE,
        "limit": limit,
        "industries": "Technology",
        "symbols": f"{SEMICONDUCTOR_ETFS},{SEMICONDUCTOR_STOCKS}",
    }
    if filter_entities:
        params["filter_entities"] = "true"
    
    response = requests.get(URL, params=params)
    response.raise_for_status()
    return {"status": "success", "category": "Semiconductors", "news": response.json()}

    