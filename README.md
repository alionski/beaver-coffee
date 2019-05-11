Usage:
- `$ cd beaver-cofee`, i.e. the repo dir
- get virtualenv for Python3, see here: https://gist.github.com/frfahim/73c0fad6350332cef7a653bcd762f08d. 
Since it has to be python3, `python3 -m venv myvenv`
- PyCharm can create a venv for you, check it in: File -> Settings -> Project: beaver-coffee -> Project interpreter. 
You might need to activate it then on then command line anyway
- Activate venv by typing `$ source venv/bin/activate`
- double check on the command line: `$which python`. Should be something like this: `/home/alionski/cs/db/project/beaver_coffee/venv/bin/python
` ( in my case, it has to be so in PyCharm's settings too), not `/usr/bin/python` (which means you are using the system Python).
- `$ cd backend`
- `$ pip install -r requirements.txt`
- `$ uwsgi --http :3031 -s /tmp/yourapplication.sock --manage-script-name --mount /=app:app
` (NB: this has to be run from `root (beaver-coffee)` dir)
- go to `localhost:3031/`

My environment: (Python 3.7, pip 19.1)