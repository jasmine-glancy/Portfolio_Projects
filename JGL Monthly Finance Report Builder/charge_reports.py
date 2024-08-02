"""Imports quarterly_reports.db and allows queries"""

from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Define database URIs
CHARGE_REPORTS_URI = "sqlite:///quarterly_reports.db"
    
# Create engines for the database
charge_reports_engine = create_engine(CHARGE_REPORTS_URI)

# Create session for the database
ChargeReportsSession = sessionmaker(bind=charge_reports_engine)
CHARGE_REPORTS_SESSION = ChargeReportsSession()

class Base(DeclarativeBase):
    pass

# Define modules that map to the tables in the existing database
class WeekdayCharges2024(Base):
    __tablename__ = "WeekdayCharges2024"
    Charge_ID = Column(Integer, primary_key=True, autoincrement=True)
    ChargeDate = Column(String) 
    PatientID = Column(Integer)
    PatientName = Column(String)
    Doctor = Column(String)
    Item = Column(String)
    Notes = Column(String)
    Amount_Subtracted = Column(Float)
    Entered_Code = Column(String)
    Amount_Added = Column(Float)
    Correct_Code = Column(String)
 
class WeekendCharges2024(Base):   
    __tablename__ = "WeekendCharges2024"
    Charge_ID = Column(Integer, primary_key=True, autoincrement=True)
    ChargeDate = Column(String) 
    PatientID = Column(Integer)
    PatientName = Column(String)
    Doctor = Column(String)
    Item = Column(String)
    Notes = Column(String)
    Amount_Subtracted = Column(Float)
    Entered_Code = Column(String)
    Amount_Added = Column(Float)
    Correct_Code = Column(String)
    
class WeeknightCharges2024(Base):
    __tablename__ = "WeeknightCharges2024"
    Charge_ID = Column(Integer, primary_key=True, autoincrement=True)
    ChargeDate = Column(String) 
    PatientID = Column(Integer)
    PatientName = Column(String)
    Doctor = Column(String)
    Item = Column(String)
    Notes = Column(String)
    Amount_Subtracted = Column(Float)
    Entered_Code = Column(String)
    Amount_Added = Column(Float)
    Correct_Code = Column(String)

