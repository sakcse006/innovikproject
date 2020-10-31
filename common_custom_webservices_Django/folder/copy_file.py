import shutil,os
import yaml

current_directory = os.path.dirname(os.getcwd())
print(current_directory)
app_path = current_directory+'/folder/file_path.yml'
with open(app_path,'r') as fp:
    cfg = yaml.load(fp)
    print(cfg)
    #print(cfg['from_path'])
    #data = yaml.safe_load(open('file_path.yml'))
    cfg['from_path']


#os.chdir('/home/arunkumar')
#shutil.copy('/home/arunkumar/abcd/files','/home/arunkumar/acde')