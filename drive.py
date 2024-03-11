from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 

gauth = GoogleAuth() #Default file is client_secrets.json
drive = GoogleDrive(gauth)

path = "https://drive.google.com/drive/folders/13JitBJQLNgMvFwx4QJcvrmDwKOYAShVx"

folder_id = path.split('/')[-1]

file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()

for file in file_list:
    print('title: %s, id: %s' % (file['title'], file['id']))

