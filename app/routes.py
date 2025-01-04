from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, utils, auth, database
from .database import get_db
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List
import requests

router = APIRouter()

load_dotenv()

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")

    hashed_password = utils.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth.login(db=db, user=user)

@router.get("/fetch-open-ended-schemes")
def fetch_and_save_open_ended_schemes(db: Session = Depends(get_db)):
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
    
    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        raise HTTPException(status_code=500, detail="RapidAPI credentials are missing")
    
    url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest?Scheme_Type=Open"
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        try:
            error_detail = response.json()
        except ValueError:
            error_detail = response.text
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch schemes from the API. Status: {response.status_code}, Error: {error_detail}"
        )
    
    schemes_data = response.json()
    for scheme in schemes_data:
        existing_scheme = db.query(models.MutualFundScheme).filter(
            models.MutualFundScheme.scheme_code == scheme["Scheme_Code"]
        ).first()

        if not existing_scheme:
            new_scheme = models.MutualFundScheme(
                scheme_code=scheme["Scheme_Code"],
                isin_div_payout_growth=scheme["ISIN_Div_Payout_ISIN_Growth"],
                isin_div_reinvestment=scheme["ISIN_Div_Reinvestment"],
                scheme_name=scheme["Scheme_Name"],
                net_asset_value=scheme["Net_Asset_Value"],
                date=datetime.strptime(scheme["Date"], "%d-%b-%Y").date(),
                scheme_type=scheme["Scheme_Type"],
                scheme_category=scheme["Scheme_Category"],
                mutual_fund_family=scheme["Mutual_Fund_Family"]
            )
            db.add(new_scheme)

    db.commit()
    return {"message": "Open-ended schemes fetched and saved successfully"}

@router.get("/investment-value/{mutual_fund_family}")
def get_investment_value(mutual_fund_family: str, db: Session = Depends(get_db)):
    schemes = db.query(models.MutualFundScheme).filter(
        models.MutualFundScheme.mutual_fund_family == mutual_fund_family
    ).all()

    if not schemes:
        raise HTTPException(
            status_code=404,
            detail=f"No schemes found for Mutual Fund Family: {mutual_fund_family}"
        )

    total_value = sum(scheme.net_asset_value for scheme in schemes)

    return {
        "mutual_fund_family": mutual_fund_family,
        "total_investment_value": total_value,
        "scheme_count": len(schemes)
    }
