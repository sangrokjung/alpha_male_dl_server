# build a schema using pydantic
from pydantic import BaseModel
from datetime import time, timedelta, date


class first_user_tbl(BaseModel):
    user_img: str
    age: date
    mbti: str
    class Config:
        schema_extra = {
            "example": {
                "user_img": "base64",
                "age": "2023-01-01",
                "mbti": "ESTJ",
            }
        }

class second_user_tbl(BaseModel):
    user_img_s3_url: str
    cft_result: str
    created_at: date
    created_by: str
    class Config:
        schema_extra = {
            "example": {
                "user_img_s3_url": "S3 URL",
                "cft_result": "alpha",
                "created_at": "2023-01-01",
                "created_by": "JSR",
            }
        }

class user_tbl(BaseModel):
    user_img_s3_url: str
    user_img: str
    cft_result: str
    age: date
    mbti: str
    created_at: date
    created_by: str

    class Config:
        schema_extra = {
            "example": {
                "user_img_s3_url": "S3 URL",
                "user_img": "jt43q9v5uiv9ntur90e",
                "cft_result": "alpha",
                "age": "1998-11-10",
                "mbti": "ESTJ",
                "created_at": "2023-01-01",
                "created_by": "JSR",
            }
        }


class male_tbl(BaseModel):
    male_id: int
    male_type: str
    cft_url: str
    dsc_text: str
    created_at: date
    created_by: str
    updated_at: date
    updated_by: str


    # class Config:
    #     orm_mode = True


class img_tbl(BaseModel):
    male_id: int
    url: str
    created_by: str
    created_at: date
    updated_by: str
    updated_at: date


    class Config:
        schema_extra = {
            "example": {
                "male_id": "1",
                "url": "jt43q9v5uiv9ntur90e",
                "created_by": "JSR",
                "created_at": "2023-01-01",
                "updated_by": "JSR",
                "updated_at": "2023-01-01",
            }
        }

class last_result(BaseModel):
    human: bool
    male_type: str
    dsc: str
    img1: str
    img2: str
    img3: str
    img4: str

    class Config:
        schema_extra = {
            "example": {
                "human": "False",
                "male_type": "null",
                "dsc": "null",
                "img1": "null",
                "img2": "null",
                "img3": "null",
                "img4": "null"
            }
        }
