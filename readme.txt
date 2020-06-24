This is a short script that connects to newsapi.org and retrieves news articles.

The script was created using python 3.7.7.  A list of requirements for this script can be found in requirements.txt.
It is good practice to create a virtual environment for this script before installing the requirements.  To create
a new virtual environment, you can do the following commands:
python -m venv venv     (this creates the new virt. env. in the venv folder)

To activate the new environment (in windows):
.\venv\Scripts\activate.bat
To deactivate the new environment (in windows):
.\venv\Scripts\deactivate

With the virt. env. activated, you can install the requirements listed in requirements.txt and they will only be
installed in this virtual environment - this will not affect any other python script in your computer.  Install these
requirements by using the following pip command in this directory:
pip install -r requirements.txt

You need to obtain your own newsapi key to access this service. The newsapi key must be stored in a separate file
in this directory.  The name of the file must be placed in config.py.  The contents of the file should include a line
with the following content - please note that your newsapi key should be enclosed by quotation marks:
api_key = your_newsapi_key_here

For licensing please check license.txt.