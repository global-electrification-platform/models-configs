import sys
import os
import shutil

def sync_to_fs(base_path):
    files = os.listdir('./data')

    for path in files:
        model_name = os.path.splitext(os.path.basename(path))[0]
        dest_dir = os.path.join(base_path,model_name,'explorer')
        try:
            os.makedirs(dest_dir)
        except:
            pass # likely just already there
        shutil.copyfile(os.path.join('./data', path),
                        os.path.join(dest_dir, path)
                        )
        print ("Copied %s" % path)
    
if __name__ == '__main__':
    if sys.argv[1]:
        base_path = sys.argv[1]
    sync_to_fs(base_path)
    



