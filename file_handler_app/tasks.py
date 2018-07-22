from celery import shared_task, current_task
from django.conf import settings
import os
import pandas as pd
from django.core.files.storage import default_storage
from file_handler_app.models import Document
import ntpath
from channels import Channel
import time
import json

@shared_task
def store_file_metadata_info(orig_file_path):
    """ This method to store the file metadata info for the later use
    """
    print("copying the path")
    second_line = None
    original_file_path = orig_file_path
    file_name = os.path.split(original_file_path)[1]
    with open(original_file_path, 'r') as org_file:
        first_line=org_file.readline()
        if (first_line.split('|')[0]) == "Author":
            second_line = org_file.readline()
    if second_line:
        file_path = settings.FILE_META_DATA_INFO_PATH
        file_full_path = os.path.join(file_path, 'file_meta_data.txt')
        with open(file_full_path, 'a') as f:
            f.write(file_name+ "|" +second_line)

def conn_check_existing_file(new_file_name):
    file_path = settings.FILE_META_DATA_INFO_PATH
    meta_data_file = os.path.join(file_path, 'file_meta_data.txt')
    df = pd.read_csv(meta_data_file, sep="|")
    # check if a matching value exists in the FileName column
    if new_file_name in df['FileName'].values:
        return True

@shared_task
def parallel_upload_the_doc(channel_name):
    #from_upload_dir = UserDirectory.objects.all()
    #for adir in from_upload_dir:
    walk_dir = os.walk('/Users/utkarsh/projects2/file_handler/async_file_manager/file_handler_app/from_upload')
    file_list = []
    for all_data in walk_dir:
        file_list = all_data[2]
        dir = all_data[0]
    for afile in file_list:
        file_exists = conn_check_existing_file(afile)
        if not file_exists:
            import pdb; pdb.set_trace()
            with open(os.path.join(dir, afile), 'r') as f:
                save_path = os.path.join(settings.MEDIA_ROOT, 'uploads' , afile)
                path = default_storage.save(save_path, f)
                # store the metadata info regarding the file while saving
                store_file_metadata_info(path)
                dir_path, file_name = ntpath.split(path)
                # use the model to save the link of the path
                #document = Document.objects.create(name=file_name, path=path)
                time.sleep(3)
    Channel(channel_name).send({'text': json.dumps({'msg': 'file uploaded' , 'status': 'loaded'})})
