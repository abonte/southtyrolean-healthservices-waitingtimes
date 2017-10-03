#update and installation of curl and pip for python 3
sudo apt-get update
sudo apt-get install -y build-essential curl python3-pip python3-dev authbind


#Installation for requirements for the project
#cd /vagrant

echo "alias python='python3' " >> .bashrc
source .bashrc

echo "Python version"
python --version

echo "Go to folder /vagrant/projects/"
cd /vagrant/projects/

echo "Clone reporsitory"
#curl -O https://github.com/abonte/southtyrolean-healthservices-waitingtimes/blob/master/requirements.txt
git clone https://github.com/abonte/southtyrolean-healthservices-waitingtimes.git healthservices-waitingtimes
cd healthservices-waitingtimes

echo "Install requirements"
pip3 install -r requirements.txt

#u="$USER"

#echo "Create the file /etc/authbind/byport/8000"
sudo touch /etc/authbind/byport/8000

#sudo -i
#echo "$USER"

#To open and set the port where the service will start
#echo "Set permissions for authbind"
#chown vagrant /etc/authbind/byport/8000
#chmod 500 /etc/authbind/byport/8000


cd /vagrant/projects/healthservices-waitingtimes
echo "Changing directory folder"
pwd

echo "Create deployment.run script"
touch deployment.run

ls -l

echo "mkdir .log 2> /dev/null" >> deployment.run

echo "DEBUG=True authbind gunicorn -b 0.0.0.0:8000 app:app --reload --access-logfile .log/access.log --error-logfile .log/general.log --log-file=-" >> deployment.run

chmod +x deployment.run

echo "deployment.run script"
cat deployment.run









