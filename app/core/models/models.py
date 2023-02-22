from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.models.database import Base



class Users(Base):
    __tablename__ = "user_tbl"

    #id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True)
    user_img_s3_url = Column(String, nullable=True)
    user_img = Column(String)
    cft_result = Column(String, nullable=True)
    age = Column(Date)
    mbti = Column(String)
    created_at = Column(Date, nullable=True)
    created_by = Column(String, nullable=True)

class Male(Base):
    __tablename__ = "male_tbl"

    male_id = Column(Integer, primary_key=True)
    male_type = Column(String)
    cft_url = Column(String)
    dsc_text = Column(String)
    created_at = Column(Date)
    created_by = Column(String)
    updated_at = Column(Date)
    updated_by = Column(String)



class Male_IMG(Base):
    __tablename__ = "img_tbl"

    id = Column(Integer, primary_key=True)
    male_id = Column(Integer, ForeignKey("male_tbl.male_id"))
    url = Column(String)
    created_by = Column(String)
    created_at = Column(Date)
    updated_by = Column(String)
    updated_at = Column(Date)


# class final_result(Base):
#
#
#     human: bool
#     male_type: str
#     dsc: str
#     img: str