""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-02-10 10:47:32
Project:	 Explorer App
Description: Provide function to perform operation on volumes.
"""

import os
import shutil
import tempfile
import datetime
from django.core.files.storage import FileSystemStorage

class ActionOperations():
    def __init__(self, volume_info, location_path) -> None:
        """Constructor."""
        self.volume_info = volume_info
        self.location_path = location_path
        self._message = None
        return None
    
    def getMessage(self):
        """Returning private message."""
        return self._message
    
    def updateMessage(self, message):
        """Update the message if any problem occur."""
        self._message = message
        return None
    
    def getVolumeLocation(self):
        """Making complete location using volume path and relative location."""
        return os.path.join(self.volume_info['path'], self.location_path)
    
    def _deleteFiles(self, path_list):
        """Deleting file or dir."""
        for file_path in path_list:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path, ignore_errors=True)
            except:
                pass
        return None

    def _zipFiles(self, file_paths):
        """Zip file or dir."""
        # CHECKING FILE
        if len(file_paths) == 1:
            # CHECKING FILE OR DIR
            if os.path.isfile(file_paths[0]):
                return file_paths[0]

        # MAKING COPY OF FILE IN TEMP DIR
        tmp_dir = tempfile.gettempdir()
        content_dir = os.path.join(tmp_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(content_dir)

        # IF SINGLE DIRECTORY
        if len(file_paths) == 1:
            file_name = os.path.basename(file_paths[0])
            zip_dir = os.path.join(content_dir, file_name)
        else:
            zip_dir = content_dir

        # COPYING FILE TO ZIP DIR
        for file_path in file_paths:
            # GETTING FILE NAME
            file_name = os.path.basename(file_path)

            # COPYING FILES
            dst_path = os.path.join(content_dir, file_name)
            if os.path.isfile(file_path):
                shutil.copy(file_path, dst_path)
            else:
                shutil.copytree(file_path, dst_path)

        # ZIPPING LOCATION
        shutil.make_archive(zip_dir, 'zip', zip_dir)
        return zip_dir + '.zip'
    
    def _saveFile(self, upload_data):
        """Save the single file that is uploaded to define path."""
        # GETTING DAVE DIRECTORY
        root_dir = self.getVolumeLocation()
        
        # SAVING EACH FILE
        upload_files = upload_data.getlist('file_data')
        fs = FileSystemStorage(location=root_dir)
        for file in upload_files:
            fs.save(file.name, file)
        return None

    def performAction(self, action, path_list, file):
        """Performing action on the paths."""
        # PERFORMING OPERATION
        zip_file_path = None
        if action == 'delete':
            self._deleteFiles(path_list)
        elif action == 'download':
            try:
                zip_file_path = self._zipFiles(path_list)
            except:
                self.updateMessage('Unable to download.')
        elif action == 'upload':
            try:
                self._saveFile(file)
            except:
                self.updateMessage('Unable to upload.')
        else:
            pass
        return zip_file_path