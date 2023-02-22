import boto3
import os
import base64
import natsort


def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id='AKIAV276ELAGBWVWO52B',
            aws_secret_access_key='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'
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3



def check_file_list(s3, BUCKET_NAME):
    # 원하는 bucket 과 하위경로에 있는 object list
    obj_list = s3.list_objects(Bucket=BUCKET_NAME)  # dict type
    # object listol Contents
    contents_list = obj_list['Contents']
    # Content list 출력
    for content in contents_list:
        print(content)

    # 파일명 추출
    file_list = []
    for content in contents_list:
        key = content['Key']
        file_list.append(key)
    # 파일명 출력
    for file in file_list:
        print(file)
    return file_list



def handle_upload_img(bs64_str):
    BUCKET_NAME = 'alpha-user-img'

    # with open("/Users/werther/alpha_male_Back/app/v1/resultBase64.txt", "r") as file:
    #     encoded_text = file.read()

    img_data = base64.b64decode(bs64_str)

    file_num = 1

    s3 = s3_connection()

    file_list = natsort.natsorted(check_file_list(s3, BUCKET_NAME))

    for file in file_list:
        if file_num <= int(file.split('.')[0]):
            file_num += 1

    filename = f'{file_num}.png'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(img_data)

    try:
        s3.upload_file(f'./{filename}', BUCKET_NAME, f"{filename}")
    except Exception as e:
        print(e)
    os.remove(f'./{filename}')
    return f"s3://alpha-user-img/{filename}"
