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

# AWS background run
nohop python main.py

# AWS Kill nohup
ps -ef |grep nohup
--bitnami    21361       1  0 Apr17 ?        00:06:00 python main.py
kill 21361



