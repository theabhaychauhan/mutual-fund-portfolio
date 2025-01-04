from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    family_id: int

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class MutualFundSchemeBase(BaseModel):
    scheme_code: int
    isin_div_payout_growth: str
    isin_div_reinvestment: str
    scheme_name: str
    net_asset_value: float
    date: date
    scheme_type: str
    scheme_category: str
    mutual_fund_family: str

    class Config:
        orm_mode = True

class MutualFundSchemeOut(MutualFundSchemeBase):
    class Config:
        orm_mode = True

class FamilyWithSchemes(BaseModel):
    id: int
    name: str
    schemes: List[MutualFundSchemeOut]

    class Config:
        orm_mode = True