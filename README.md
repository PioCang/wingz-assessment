# wingz-assessment
## Prepping the venv to run the server
Let's prep a virtual env, I assume you have *pyenv* installed.
For a small application, I want to avoid the memory overhead involved with Docker containers.

1. Create the virtual env to sandbox all PIP changes. Needs [pyenv](https://formulae.brew.sh/formula/pyenv) and [pyenv-virtualenv](https://formulae.brew.sh/formula/pyenv-virtualenv) installed.
```
pyenv virtualenv 3.11.3 wingz
pyenv activate wingz
```

2. Clone the repository
```
git clone https://github.com/PioCang/wingz-assessment.git
```

3. We run everything inside this folder
```
cd wingz-assessment/wingz/
```

4. Install the requirements. (Ensure the `wingz` virtual env is activated.)
```
pip install -r requirements.txt
```

5. Run the migrations
```
python manage.py migrate
```

6. [Optional step] create a superuser. It's not necessary, but you can do so if you wish. Run this command and follow the prompts
```
python manage.py createsuperuser
```

7. Run the server
```
python manage.py runserver 8000
```
