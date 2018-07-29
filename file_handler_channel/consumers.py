from django.core.files import File
from file_handler_app import tasks as tsk
import json
from file_handler_app.models import UserDirectory
import os
import pandas as pd
from django.conf import settings
from django.core.files.storage import default_storage
import ntpath
from channels import Channel
import time

def connect(message):
    """ Connects the web socket
    """
    message.reply_channel.send({'accept': True})

def receive(message):
    """ Send and receives the message
    """
    # Send the message as file upload is in progress and continue
    # the file upload in the background
    message.reply_channel.send({'text': json.dumps({'msg': 'files upload started',
                                                  'status': 'in progress'})}, immediately=True)

    # Continue the file upload process in the background
    parallel_upload_the_doc(message.reply_channel.name)

def store_file_metadata_info(orig_file_path):
    """ This method to store the file metadata info for the later use
        so that later we can avoid duplication of file upload .
    """
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
    """ Read from the metadata file to get the info whether
        the file has been already uploaded
    """
    file_path = settings.FILE_META_DATA_INFO_PATH
    meta_data_file = os.path.join(file_path, 'file_meta_data.txt')
    df = pd.read_csv(meta_data_file, sep="|")
    # check if a matching value exists in the FileName column
    if new_file_name in df['FileName'].values:
        return True

def parallel_upload_the_doc(channel_name):
    from_upload_dir = UserDirectory.objects.all()
    #for adir in from_upload_dir:
    walk_dir = os.walk('/Users/utkarsh/projects2/file_handler/async_file_manager/file_handler_app/from_upload')
    file_list = []
    for all_data in walk_dir:
        file_list = all_data[2]
        dir = all_data[0]
    for afile in file_list:
        file_exists = conn_check_existing_file(afile)
        if not file_exists:
            with open(os.path.join(dir, afile), 'r') as f:
                # send the information to front end as file is getting uploaded
                file_name = os.path.split(f.name)[1]
                Channel(channel_name).send({'text': json.dumps({'msg': 'uploading the file - %s'%file_name,
                                                                'status': 'in progress'})}, immediately=True)
                save_path = os.path.join(settings.MEDIA_ROOT, 'uploads' , afile)
                path = default_storage.save(save_path, f)
                # store the metadata info regarding the file while saving
                store_file_metadata_info(path)
                dir_path, file_name = ntpath.split(path)
                # use the model to save the link of the path
                # document = Document.objects.create(name=file_name, path=path)
                time.sleep(3)
                Channel(channel_name).send({'text': json.dumps({'msg': 'file -%s uploaded'%file_name , 'status': 'loaded'})})
    Channel(channel_name).send({'text': json.dumps({'msg': 'file upload finished' , 'status': 'loaded'})})
