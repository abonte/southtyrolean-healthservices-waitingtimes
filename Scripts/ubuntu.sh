#update and installation of curl and pip for python 3
apt-get update
apt-get install -y build-essential curl python3-pip python3-dev

#Set python3 as default
echo "alias python='python3' " >> ~/.bashrc
source ~/.bashrc


echo "Python version"
python --version

#going in the main folder
cd ..

#Install requirements
echo "Install requirements"
pip3 install -r requirements.txt
