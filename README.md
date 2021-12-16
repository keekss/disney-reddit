# ICS 438 Final Project

### Reddit Sentiment and Stock Price

The first part of this project is a python notebook consisting of a pipeline to get content from Reddit and the stock market, perform linear regression on the content, perform sentiment 
analysis on the content, then graph the two datasets. This notebook is fairly robust - each process takes in an iput file and writes to an output 
file, allowing you to enter the pipeline at any point and checkpoint as you go. 

All of the necessary code for this can be found in [this notebook](https://github.com/keekss/disney-reddit/blob/master/project_writeup.ipynb), 
which can be run as a Jupyter notebook on a local machine.

The final section of the notebook contains driver code to reconstruct our sample graphs using prepared data files, which can be found in the 
[sampleData](https://github.com/keekss/disney-reddit/tree/master/sampleData) directory. These graphs get posts and comments from 
[r/disney](https://www.reddit.com/r/disney/) and plots their sentiment alongside Disney stock. 

To smooth the sentiment analysis results, an API called [ASAP](https://dawn.cs.stanford.edu/2017/08/07/asap/) was used. This was written python2, so 
the modified version of this that we used can be found [here](https://github.com/keekss/disney-reddit/blob/master/ASAP.ipynb). 

### Google Docs for Description of Work

[Google Doc](https://docs.google.com/document/d/1KjXD3TtvkG8EO8RG5Te5ZTCl0uc-ZWNRbF9h-VweEh4/edit)

### Google Drive for Raw Data

Only accessible by those with an @hawaii.edu

[Google Drive](https://drive.google.com/drive/folders/1jhhzseiX2Qi78ElHTuxlTIhRogJp4CAS?usp=sharing)

### Docker Image

The docker image creates a docker container that runs the applicaiton and jupyter notebook at the same time.  There is no software limit to the number of containers that can be run at the same time.  

The container is built on a slim-python build and the neccesary python packages.  All of these required files are loaded automatically in to the container by the image.

To retrieve the docker image from GitHub, in your terminal enter:

```
git clone https://github.com/fredstraub/ICS-438-Final-Dockerfile.git
```

Go to the directory with the docker-compose.yaml file, in your terminal enter

```
cd ICS-438-Final-Dockerfile/disney_datascience_analysis
```

To start the docker container in your terminal enter

```
docker-compose up
```

Watch build output for the jupyter notebook link with token to access notebook.
It will be something like http://127.0.0.1:8888?token...
View the app at http://127.0.0.1:8050/

### Plotly Website

The results from the Reddit Sentiment and Stock Price notebook above has been included in a plotly website (coded in Python using Dash). We also included a bar graph depicting which Disney characters were discussed the most on the r/Disney subreddit, as well as an interactive map of Disneyland with each ride's sentiment (taken from r/Disneyland) being displayed. 

In order to access the website, the python application must be running. This can be done by cloning this repository locally: 

```
git clone git@github.com:keekss/disney-reddit.git
```

After cloning, navigate into the repository's directory:

```
cd disney-reddit
```

Run the python program (note: make sure python3 is installed on your computer):

```
python3 app.py
```

At this point you will need to pip install all libraries that you get an error for.

Finally, run the app again and view the following url in your browswer:

```
http://localhost:8050/
```

Alternatively, you can email <clark37@hawaii.edu> to schedule a viewing.
