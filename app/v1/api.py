import json
from datetime import datetime
from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
# from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from app.core.models import models
from app.core.models.database import Base, engine, SessionLocal
from app.core.schemas.schema import first_user_tbl, user_tbl, second_user_tbl, male_tbl, img_tbl, last_result
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT
from app.v1.load import encoding
import os
import random
from app.v1.s3 import handle_upload_img
import requests
from Model.detection import run

Base.metadata.create_all(bind=engine)
Session = sessionmaker(engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={401: {"user": "Not authorized"}}
)
@router.get("/")
async def root():
    return {"message": "hello world  "}
@router.get("/read/user")
async def read_user(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.post("/RegisterResult")
async def RegisterResult(first_user: first_user_tbl, result: last_result, db: Session = Depends(get_db)):
    c_first_user = models.Users()
    c_first_user.user_img = first_user.user_img
    c_first_user.age = first_user.age
    c_first_user.mbti = first_user.mbti

    Model_rst = run(first_user.user_img)

    if Model_rst == 0 or Model_rst == 6:
        # user = db.query(models.Users).filter_by(user_img=first_user.user_img).first()
        # db.delete(user)
        # db.commit()
        return result
    elif Model_rst >= 1 and Model_rst < 6:
        # Model_rst = model3('/Users/snagrockjung/alpha_male_Back/test_img/', '/Users/snagrockjung/alpha_male_Back/Model/model249.pth')
        s3_url = handle_upload_img(first_user.user_img)  # S3에 파일을 전송함과 동시에\ 주소 획득.
        Model_rst = Model_rst
        result.human = "True"
        type = conv_type(Model_rst)
        if Model_rst == 1:
            result.male_type = "Alpha"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "alpha").first().dsc_text
            ID = make_4_num(27, 36)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 2:
            result.male_type = "Beta"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "beta").first().dsc_text
            ID = make_4_num(37, 49)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 3:
            result.male_type = "Gamma"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "gamma").first().dsc_text
            ID = make_4_num(50, 62)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 4:
            result.male_type = "Delta"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "delta").first().dsc_text
            ID = make_4_num(63, 73)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 5:
            result.male_type = "Omega"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "omega").first().dsc_text
            ID = make_4_num(74, 84)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        c_first_user.user_img_s3_url = s3_url
        c_first_user.cft_result = type
        c_first_user.created_at = datetime.now()
        c_first_user.created_by = "JSR"
        db.add(c_first_user)
        db.commit()

        return result

@router.post("/RegisterUserImg")
async def RegisterUserImg(first_user: first_user_tbl, result: last_result, db: Session = Depends(get_db)):
    c_first_user = models.Users()
    c_first_user.user_img = first_user.user_img
    c_first_user.age = first_user.age
    c_first_user.mbti = first_user.mbti

    # db.add(c_first_user)
    # db.commit()

    # model_1_rst = model1('/Users/snagrockjung/alpha_male_Back/test_img/', '/Users/snagrockjung/alpha_male_Back/Model/alphav1.pth')

    url = 'http://127.0.0.1:8000/api/GetModelResult'  # Replace with the actual API endpoint
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}  # Replace with the actual request headers
    data = {"bs64_str": f"{first_user.user_img}"}

    Model_rst = request_model(url, headers, data)

    if Model_rst == 0 or Model_rst == 6:
        # user = db.query(models.Users).filter_by(user_img=first_user.user_img).first()
        # db.delete(user)
        # db.commit()
        return result
    elif Model_rst >= 1 and Model_rst < 6:
        # Model_rst = model3('/Users/snagrockjung/alpha_male_Back/test_img/', '/Users/snagrockjung/alpha_male_Back/Model/model249.pth')
        s3_url = handle_upload_img(first_user.user_img)  # S3에 파일을 전송함과 동시에\ 주소 획득.
        Model_rst = Model_rst
        result.human = "True"
        type = conv_type(Model_rst)
        if Model_rst == 1:
            result.male_type = "Alpha"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "alpha").first().dsc_text
            ID = make_4_num(27, 36)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 2:
            result.male_type = "Beta"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "beta").first().dsc_text
            ID = make_4_num(37, 49)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 3:
            result.male_type = "Gamma"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "gamma").first().dsc_text
            ID = make_4_num(50, 62)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 4:
            result.male_type = "Delta"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "delta").first().dsc_text
            ID = make_4_num(63, 73)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 5:
            result.male_type = "Omega"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "omega").first().dsc_text
            ID = make_4_num(74, 84)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst,
                                                           models.Male_IMG.id == ID[3]).first().url
        c_first_user.user_img_s3_url = s3_url
        c_first_user.cft_result = type
        c_first_user.created_at = datetime.now()
        c_first_user.created_by = "JSR"
        db.add(c_first_user)
        db.commit()

        return result


@router.post("/RegisterUserImg_sample")
async def RegisterUserImg_sample(first_user: first_user_tbl, Model_rst:int, result: last_result, db: Session = Depends(get_db)):
    c_first_user = models.Users()
    c_first_user.user_img = first_user.user_img
    c_first_user.age = first_user.age
    c_first_user.mbti = first_user.mbti

    # db.add(c_first_user)
    # db.commit()

    # model_1_rst = model1('/Users/snagrockjung/alpha_male_Back/test_img/', '/Users/snagrockjung/alpha_male_Back/Model/alphav1.pth')
    Model_rst


    if Model_rst == 0 or Model_rst == 6:
        # user = db.query(models.Users).filter_by(user_img=first_user.user_img).first()
        # db.delete(user)
        # db.commit()
        return result
    elif Model_rst >= 1 and Model_rst < 6:
        # Model_rst = model3('/Users/snagrockjung/alpha_male_Back/test_img/', '/Users/snagrockjung/alpha_male_Back/Model/model249.pth')
        s3_url = handle_upload_img(first_user.user_img) # S3에 파일을 전송함과 동시에\ 주소 획득.
        Model_rst = Model_rst
        result.human = "True"
        type = conv_type(Model_rst)
        if Model_rst == 1:
            result.male_type = "alpha"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "alpha").first().dsc_text
            ID = make_4_num(27, 36)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 2:
            result.male_type = "beta"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "beta").first().dsc_text
            ID = make_4_num(37, 49)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 3:
            result.male_type = "gamma"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "gamma").first().dsc_text
            ID = make_4_num(50, 62)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 4:
            result.male_type = "delta"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "delta").first().dsc_text
            ID = make_4_num(63, 73)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[3]).first().url
        elif Model_rst == 5:
            result.male_type = "omega"
            result.dsc = db.query(models.Male).filter(models.Male.male_type == "omega").first().dsc_text
            ID = make_4_num(74, 84)
            result.img1 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[0]).first().url
            result.img2 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[1]).first().url
            result.img3 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[2]).first().url
            result.img4 = db.query(models.Male_IMG).filter(models.Male_IMG.male_id == Model_rst, models.Male_IMG.id == ID[3]).first().url
        c_first_user.user_img_s3_url = s3_url
        c_first_user.cft_result = type
        c_first_user.created_at = datetime.now()
        c_first_user.created_by = "JSR"
        db.add(c_first_user)
        db.commit()

        return result


@router.delete("/delete/first_post/{id}")
async def first_del(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter_by(id=id).first()
    db.delete(user)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.patch("/patch/second/user_tbl/{id}")
async def second_patch(id: int, second_user: second_user_tbl, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id)
    db_note = user.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {id} found')
    update_data = second_user.dict(exclude_unset=True)
    user.filter(models.Users.id == id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_note)
    return {"status": "success", "note": db_note}


@router.post("/create/user")
async def create_new_user(new_user: user_tbl, db: Session = Depends(get_db)):
    c_new_user = models.Users()
    c_new_user.user_img_s3_url = new_user.user_img_s3_url
    c_new_user.user_img = new_user.user_img
    c_new_user.cft_result = new_user.cft_result
    c_new_user.age = new_user.age
    c_new_user.mbti = new_user.mbti
    c_new_user.created_at = new_user.created_at
    c_new_user.created_by = new_user.created_by

    db.add(c_new_user)
    db.commit()

@router.post("/create/male")
async def create_male(male: male_tbl, db: Session = Depends(get_db)):
    Male = models.Male()
    Male.male_id = male.male_id
    Male.male_type = male.male_type
    Male.cft_url = male.cft_url
    Male.dsc_text = male.dsc_text
    Male.created_at = male.created_at
    Male.created_by = male.created_by
    Male.updated_at = male.updated_at
    Male.updated_by = male.updated_by

    db.add(Male)
    db.commit()

@router.post("/create/male_img")
async def create_male_img(male_img: img_tbl, db: Session = Depends(get_db)):
    Male_IMG = models.Male_IMG()
    Male_IMG.male_id = male_img.male_id
    Male_IMG.url = male_img.url
    Male_IMG.created_by = male_img.created_by
    Male_IMG.created_at = male_img.created_at
    Male_IMG.updated_by = male_img.updated_by
    Male_IMG.updated_at = male_img.updated_at

    db.add(Male_IMG)
    db.commit()

@router.post("/create/type_male_img")
async def create_type_male_img(type: str, db: Session = Depends(get_db)):
    #dir_path = f"/Users/werther/Downloads/male_img/{type}"
    dir_path = f"/Users/snagrockjung/Downloads/male_img/{type}"
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            Male_IMG = create_male_img(file_path, type)
            db.add(Male_IMG)
            db.commit()



def create_male_img(path: str, type: str):
    Male_IMG = models.Male_IMG()
    Male_IMG.male_id = select_type(type)
    Male_IMG.url = str(encoding(path)).replace('b', '', 1).replace("'", "")
    Male_IMG.created_by = "JSR"
    Male_IMG.created_at = "2023-02-17"
    Male_IMG.updated_by = "JSR"
    Male_IMG.updated_at = "2023-02-17"
    return Male_IMG

def select_type(type: str):
    id="null"
    if type == 'alpha':
        id=1
    elif type == 'beta':
        id=2
    elif type == 'gamma':
        id=3
    elif type == 'delta':
        id=4
    elif type == 'omega':
        id=5
    return id



def make_4_num(lower_bound:int, upper_bound:int):
    # choose four non-overlapping random integers within the range
    int1 = random.randint(lower_bound, upper_bound - 3)
    int2 = random.randint(int1 + 2, upper_bound - 1)
    int3 = random.randint(lower_bound, int1 - 1)
    int4 = random.randint(int2 + 1, upper_bound)

    # print the four non-overlapping integers
    return [int1, int2, int3, int4]


def conv_type(type):
    rst = 'null'
    if type == 1: rst = "alpha"
    elif type == 2: rst = "beta"
    elif type == 3: rst = "gamma"
    elif type == 4: rst = "delta"
    elif type == 5: rst = "omega"
    return rst

def request_model(url, headers, data):
    response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False, indent="\t"))

    if response.ok:
        # The API call was successful
        print(response.json())
        return response.json()
    else:
        # The API call failed
        print(response.text)