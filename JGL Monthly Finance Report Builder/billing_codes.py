"""Imports billing_codes.db and allows queries"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Define database URI
BILLING_CODES_URI = "sqlite:///billing_codes.db"

# Create engines for the database
billing_codes_engine = create_engine(BILLING_CODES_URI)

# Create session for the database
BillingCodesSession = sessionmaker(bind=billing_codes_engine)
billing_code_session = BillingCodesSession()

class Base(DeclarativeBase):
    pass

# Define modules that map to the tables in the existing database
class BloodAndTransfusion(Base):
    __tablename__ = "BloodAndTransfusion"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)
 
class ConsultationsAndTransfers(Base):   
    __tablename__ = "ConsultationsAndTransfers"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)
    
class ControlledDrugs(Base):
    __tablename__ = "ControlledDrugs"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class FluidAdditives(Base):    
    __tablename__ = "FluidAdditives"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class Food(Base):    
    __tablename__ = "Food"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class HospitalizationCodes(Base):    
    __tablename__ = "HospitalizationCodes"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class InHouseImaging(Base):        
    __tablename__ = "InHouseImaging"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class InHouseLabs(Base):        
    __tablename__ = "InHouseLabs"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class Monitoring(Base):        
    __tablename__ = "Monitoring"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class Oxygen(Base):        
    __tablename__ = "Oxygen"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class SendOut_RegerenceLabs(Base):        
    __tablename__ = "SendOut_RegerenceLabs"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)

class SpecialtyImaging(Base):        
    __tablename__ = "SpecialtyImaging"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String)
    item_description = Column(String)
    
billing_codes = billing_code_session.query(HospitalizationCodes).all()
