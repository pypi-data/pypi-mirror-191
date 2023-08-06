# ETL Project 
Extract, Transform, Load (ETL). All the scripts (glue and sagemaker) and custom libs.

## 1. Setup:
* clone the git project
```
git clone https://<your-git-user-name>@bitbucket.org/ashishgenerico/etl.git
```
* go inside the `./etl/` directory
```commandline
cd etl
```
* Request the `zeno_secrets.py` file from your fellow team members and paste that file inside `secret` directory 

## 2. Glue
* Create `python3.6` virtual env and activate
```commandline
python3 -m venv etl_env
```
* Activate the virtual env
```commandline
source etl_env/bin/activate
```
* Install the `requirements.txt` inside the virtual env 
```commandline
pip install -r requirements.txt 
```
* Write your ETL script inside the `glue-jobs/src/scripts/<your_script_name>/` folder

## 3. Sagemaker
* Create `python3.7` (or **greater**) virtual env and activate
```commandline
python3 -m venv etl_env
```
* Activate the virtual env
```commandline
source etl_env/bin/activate
```
* Install the `requirements-ml.txt` inside the virtual env 
```commandline
pip install -r requirements-ml.txt 
```
* Write your ETL jupyter lab notebooks inside the `sagemaker-jobs/src/scripts/<your_script_name>/` folder
* Refer the demo notebooks inside the `sagemaker-jobs/src/scripts/experiments/`

## 4. Deployment
### 4.1 Glue
* Add your script details in `.\templates\templetes.json` file 
* Push your code to bitbucket and raise PR 
* Don't forget to enjoy. 🍺🍺
### 4.2 Sagemaker
* If there are changes in `zeno_etl_libs` custom library then we need to publish it on PyPI
* Increase the version in `etl/setup.py` present in `etl` folder
* Run the below command to build the package
```commandline
python setup.py sdist bdist_wheel
```
**Check the zeno_etl_libs_v3_x.y.z.tar.gz and zeno_etl_libs_v3_x.y.z.py3-none-any.whl files inside the `dist` folder and make sure not `usernames` and `passwords` getting pushed in public domain.** 
* Run the below command to publish the new version on PyPI
```commandline
twine upload dist/* --verbose -u <user_name> -p <password>
```
* Add the below command at the start of jupyter notebook
```commandline
!pip install zeno_etl_libs==new.version.number
```

## 5. Troubleshooting
1. Don't forget to include the custom library folder(`./zeno_etl_libs`) to the python search path before `import zeno_etl_libs` it for local development
```python
import sys
sys.path.append('../../../..')
```
2. Use **conda**, if there are any issue while installing the python package or virtual environment creation 
## 6. Rules
* Follow the proper git flow, given here: [here](https://docs.google.com/document/d/1SnT_UKCj1Da07S-FFgvTxk30WbRbb-MFX89kEnMIKbk/edit)

## 7. Container image update (for DevOps)
* Set these options in case of **UnicodeEncodeError: 'ascii' codec can't encode characters** error
```commandline
export LC_ALL=en_US.utf-8 && export LANG=en_US.utf-8 && export PYTHONIOENCODING=utf8
```
* Delete the code build project container
```commandline
aws codebuild delete-project --name create-sagemaker-container-env_name-notebook-runner
```
* Copy the modified Docker file present at `./extra_dependency/Dockerfile` to virtual environment's site package at `./site-packages/sagemaker_run_notebook/container/Dockerfile`, basically add these extra command in the file.
```commandline
RUN apt-get update
RUN pip3 install --upgrade pip
RUN apt-get install -y gcc g++ build-essential python3-dev
```
* Update the
```commandline
run-notebook create-container env_name-notebook-runner --requirements requirements-ml.txt
```