

# This is run in AfterInstall stage in appspec - so required app folder is recursively copied to required location
# as specified in files: section. So need to cd into the location in ec2 it was copied and then install
cd /home/ec2-user/sample-app
sudo python3.8 -m pip install -r requirements.txt
