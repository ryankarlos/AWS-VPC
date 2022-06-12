
# This is run in Application Start stage in appspec - so required app folder is recursively copied to required location
# as specified in files: section. So need to cd into the location in ec2 it was copied to and then run app.
cd /home/ec2-user/sample-app
sudo python3.8 application.py
