import os
import requests
from pathlib import Path
from db import fetch_scripts

def download(email,url):
    msg = {'flag':False}
    try:
        res = fetch_scripts.check_client_existance(email)
        if res['flag']:
            dest_folder = str(os.path.join(Path.home(), "Downloads"))
            filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
            file_path = os.path.join(dest_folder, filename)

            r = requests.get(url, stream=True)
            if r.ok:
                print("saving to", os.path.abspath(file_path))
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            os.fsync(f.fileno())
                msg= {'flag':True,'message':'file downloaded','download_link':url}
            else:  # HTTP status code 4XX/5XX
                msg = {'flag':False,'error':"Download failed: status code {}\n{}".format(r.status_code, r.text)}
        else:
            msg = {'flag':False,'error':'user does not exist'}
    except Exception as e:
        msg = {'flag':False,'error':e}

    return msg

