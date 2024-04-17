### PyCham Environments Setup Guide ####

# GIT CONNECTION
# connnect your git with venv environment

git init
git remote add origin https://github.com/linst77/telecom001.git
git pull origin main --allow-unrelated-histories


# git clone origin https://github.com/linst77/telecom001.git .


# PIP CONNECTION
pip freeze > requirements.txt

pip install -r requirements.txt

# Time is UTC timeline