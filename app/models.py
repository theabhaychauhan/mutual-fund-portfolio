from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    family_id = Column(Integer, ForeignKey('families.id'))

    family = relationship("Family", back_populates="users")

class Family(Base):
    __tablename__ = 'families'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    schemes = relationship('MutualFundScheme', back_populates="family", lazy=True)
    users = relationship('User', back_populates="family")

class MutualFundScheme(Base):
    __tablename__ = 'mutual_fund_schemes'

    id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(Integer, unique=True, index=True)
    isin_div_payout_growth = Column(String)
    isin_div_reinvestment = Column(String)
    scheme_name = Column(String)
    net_asset_value = Column(Float)
    date = Column(Date)
    scheme_type = Column(String)
    scheme_category = Column(String)
    mutual_fund_family = Column(String)
    family_id = Column(Integer, ForeignKey('families.id'))

    family = relationship("Family", back_populates="schemes")