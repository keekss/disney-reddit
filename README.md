# ICS 438 Final Project

### Reddit Sentiment and Stock Price

The first part of this project is a python notebook consisting of a pipeline to get content from Reddit and the stock market, perform linear regression on the content, perform sentiment 
analysis on the content, then graph the two datasets. This notebook is fairly robust - each process takes in an iput file and writes to an output 
file, allowing you to enter the pipeline at any point and checkpoint as you go. 

All of the necessary code for this can be found in [this notebook](https://github.com/keekss/disney-reddit), 
which can be run as a Jupyter notebook on a local machine.

The final section of the notebook contains driver code to reconstruct our sample graphs using prepared data files, which can be found in the 
[sampleData](https://github.com/keekss/disney-reddit/tree/master/sampleData) directory. These graphs get posts and comments from 
[r/disney](https://www.reddit.com/r/disney/) and plots their sentiment alongside Disney stock. 

To smooth the sentiment analysis results, an API called [ASAP](https://dawn.cs.stanford.edu/2017/08/07/asap/) was used. This was written python2, so 
the modified version of this that we used can be found [here](https://github.com/keekss/disney-reddit/blob/master/ASAP.ipynb). 

### Google Docs for Description of Work

[Google Doc](https://docs.google.com/document/d/1KjXD3TtvkG8EO8RG5Te5ZTCl0uc-ZWNRbF9h-VweEh4/edit)

### Plotly Website

INSERT TEXT
