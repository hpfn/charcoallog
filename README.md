# charcoallog

Financial-accounting. Domestic use.

First project using Django. After saw Gileno's videos,<br>
but not all videos. And DjangoGirls tutorial too. Trying<br>
to improve code after WTTD.

It is not a new idea. I am using mymoneylog (github)<br>
to manager my bank account and want to change to a <br>
Python program.

Transfer between accounts will not appear after a search<br>
(second form - only one field to fill and two dates to<br>
set) if category starts with 'transfer'. Unless you search<br>
for 'all'.


## How to contribute?

* Clone this repository.
* Create virtualenv with Python 3.
* Active the virtualenv.
* Install dependences.
* Run the migrations.

```
git clone https://github.com/hpfn/charcoallog.git
cd charcoallog
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

