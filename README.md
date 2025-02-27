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


## Some Design choices
1. In the spec, primary keys take on the format `id_<model_name`. I've simplified them to use `id` that's readily supplied by Django to be the default primary key on any table.
2. Similarly, Foreign Keys will use just `<model_name>` as the foreign key (but under the hood Django uses `<model_name>_id`).
3. The instructions' wording leads me to believe that a majority of the optimization concerns center around the Ride List API. Therefore, I want to make it clear that my approach to this coding assessment places emphasis on the performance and optimization efforts _solely_ towards the **Ride List API**. With that said, no such optimization efforts were expended towards the rest of the CRUD operations on the rest of the models.


## 2 Using the app's APIs
Please refer to [ENDPOINTS.md](./ENDPOINTS.md)




## 3 Teardown
1. Stop the Django server with `Ctrl + C`
2. Delete the environment with
```
pyenv virtualenv-delete wingz
```
3. Delete the `wingz-assessment` folder

# -- END
