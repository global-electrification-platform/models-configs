import os
import subprocess

for f in os.listdir('./data'):
    model = f.split('.')[0]
    print ("Updating %s" %model)
    subprocess.check_call(['sed', '-i', 's#mapbox://devseed\..*#mapbox://derilinx.%s#;' % model, os.path.join('./data',f)])

                           
                    
                        
