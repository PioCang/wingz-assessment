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
