import os
from db import insert_data

def create_user_folders(user_name,subfolders):
    # TO create folders for storing Photo, UID, Prescription, Diagnostic reports
    try:
        root_path = "static/" +str(user_name)
        list_url = []
        for c in subfolders:
            path = os.path.join(root_path, c)
            os.makedirs(path, exist_ok=True)
            list_url.append(path)
        return list_url

    except OSError as error:
        print("Directory '%s' can not be created:{}".format(error))


def allowed_file(file_name):
    ALLOWED_EXTENSIONS = set(['pptx','docx','xlsx'])
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload(f,filename,user_name,file_type):
    try:
        rootpath = create_user_folders(user_name,[file_type])
        f.save(os.path.join(rootpath[0],filename))
        file_path = os.path.join(rootpath[0],filename)
        res = insert_data.insert_file(file_path,user_name)
        if res['flag']:
            message='file added to database'
    except Exception as e:
        msg = {'error': e}
    else:
        msg = {'message':'File uploaded successfully','file_path':file_path,'file_name':filename}
    
    return msg



