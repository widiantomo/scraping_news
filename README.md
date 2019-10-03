Setup virtualenv

virtualenv venv

Activate virtualenv

. venv/bin/activate

First create a directory for your new shiny isolated environment
mkdir ~/virtualenvironment
To create a folder for your new app that includes a clean copy of Python,
simply run:
virtualenv ~/virtualenvironment/my_new_app
To begin working with your project, you have to cd into your directory (project)
and activate the virtual environment.
cd ~/virtualenvironment/my_new_app/bin
Lastly, activate your environment:
source activate

Install requirements

pip install -r requirements.txt

How to use
Open the specific project, example

cd republika

Run crawl command, example

scrapy crawl republika -o sampleResult.json -t json

