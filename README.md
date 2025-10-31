# MLDS-Data-Engineering-Titanic-Disaster-Analysis

### MLDS 400: Data Engineering Homework 3

## Repository Overview
Repository for modeling survivability on the Titanic. Done both in Python and R with dedicated Docker images/containers for both. The survivorship rate of 
individuals on the Titanic are modeled using a Logistic Regression.

## Directory Structure
```
MLDS-Data-Engineering-Titanic-Disaster-Analysis:.
|   .gitignore
|   README.md
|
+---.github
|       CODEOWNERS
|
+---data                            # NOT IN REPO; You will need to create and load the data directory like so.
|   \---titanic
|           gender_submission.csv
|           test.csv
|           train.csv
|
\---src
    +---analysis_py
    |       analysis.py
    |       Dockerfile
    |       requirements.txt
    |
    \---analysis_R
            analysis.R
            Dockerfile
            install_packages.R
```

## Directory Folders & Files
- **MLDS-Data-Engineering-Titanic-Disaster-Analysis:** This is the repository name, it will serve as the name of the root directory when setting up this repo.
    - Contains .github, \data\titanic, and \src directories. Also contains README.md and .gitignore.
- **.github:** This directory contains the CODEOWNERS file, allows only myself, the repo creator, to approve any pull requests and assigns all the files to myself.
- **\data\titanic:** This directory is found in the .gitignore. As such, you must create the data folder yourself and load the data in this structure. Exact steps provided later.
- **\src:** Contains two sub directories , \src\analysis_py and \src\analysis_R. The analysis_py directory contains the Dockerfile, requirements.txt, and analysis.py required for the logistic regression model in python. Likewise, for \src\analysis_R, we have its corresponding Dockerfile, analysis.R, and install_packages.R.
- **.gitignore:** Contains a list of directories and files that are not tracked by git. In our case, we are not tracking \data. 
- **README.md:** Current document; Serves as a form of documentation.

## Resources:
**The Titanic dataset:** [Titanic Survivor Data](https://www.kaggle.com/competitions/titanic/data) 

## Getting Started:
1. Clone this repository. Set the repository directory, **MLDS-Data-Engineering-Titanic-Disaster-Analysis** as working directory.
2. Within the working directory, at the root, create a new `data` folder. Download the Titanic data, listed in the [Resources](#resources) section.
3. Unzip the Titanic dataset, and load it into the `data` folder. Ensure that the three CSV files are within a directory called `titanic`, as seen in [Directory Structure](#directory-structure). Ensure that this `titanic` folder is within data. This completes the set up.
4. Ensure that the Docker engine is running; Open Docker Desktop and ensure that it says "Engine running" on the status bar in the bottom left. 
5. To run logistic regression in python, run the following commands from the root of the working directory:
    - a. `docker build -t titanic-disaster-python -f src/analysis_py/Dockerfile .`
    - b. `docker run -it titanic-disaster-python`
6. To run logistic regression in R, run the following commands from the root of the working directory:
    - a. `docker build -t titanic-disaster-r -f src/analysis_R/Dockerfile .`
    - b. `docker run -it titanic-disaster-r`