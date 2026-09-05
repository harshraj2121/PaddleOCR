from .database import Base
from sqlalchemy import Column, Integer, String


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, index=True)
    application_number = Column(String(100))
    applicant_name = Column(String(100))
    form_id = Column(String(50))
    gender = Column(String(10))
    contact_number = Column(String(20))
    email = Column(String(50))
    city = Column(String(50))
    complete_address = Column(String(225))
    form_type = Column(String(200))
    submission_date = Column(String(25))
    martial_status = Column(String(25))
    source_file = Column(String(150))