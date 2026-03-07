# EDA and Dashboard of an e-commerce dataset
This is a Python implementation of Exploratory Data Analysis (EDA) of the O-List e-commerce dataset.

This will be then visualized through a dashboard onto a web browser by utilizing `flask` and `dash`.

Currently working on the `README.md`.

# TODO
* Note to self, project directory is in: `~/python/`.
* __Show some pictures!__
* Create `requirements.txt`.
* Publish a clean file which only outputs the dashboard. 
* As always, update `README.md`,


# Dependencies
* Python 3 (version 3.1+) - Programming Language
* jupyter-notebook - Notebook application
* pandas - Data manipulation
* numpy - Number calcs
* sqlite3 - Execytubg SQL queries with the relational database (olist.sqlite)
* matplotlib - data charts, graphs, etc.
* plotly - data charts, graphs, etc.
* folium - Rendering geospatial map for CLV and logistics.
* dash - building and deploying web dashboard


# Installtion
Obtain the the O-list dataset through Kaggle:
[https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database](https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database)

Once downloaded, unzip `archive.zip`. Move the unzipped `olist.sqlite` into the same folder (or directory) as the 

Install a notebook viewer. I recommend Jupyter-Notebook, otherwise Google Colab offers an online notebook viewer for free.

Once your notebook viewer is setup, open the `olist-eda.ipynb` file into your viewer.

## Linux
```
# Clone repository
$ cd ~/Downloads # (or any folder of your choice)
$ git clone https://github.com/kenmbo/olist-eda-dashboard.git
$ cd olist-eda-dashboard

# Set up python virtual environment (recommended)
$ python3 -m venv .venv
$ source .venv/bin/activate

# Setup notebook viewer (OPTIONAL, only do this if you had not yet installed a notebook viewer yet)
$ pip install notebook

# Open work
$ notebook olist-eda.ipynb

# Get the olist.sqlite file after unzipping the from Archive.zip
# https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database/data
# (Please see Installtion for details)

# Install required packages
pip install pandas numpy matplotlib plotly folium dash
```
