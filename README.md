# Web2Keyword
Extract Most Relevant Keywords from Webpage to the given list of sentences or words.

## Sequence Diagram
```mermaid
sequenceDiagram
    user->>+GunicornWSGI: POST Request
    GunicornWSGI->>+FlaskAPI: input_data
    FlaskAPI->>+Scraper: URL
    FlaskAPI->>+Purificator: Product/Service list
    Purificator->>+Word2Vec: Product/Service list pure
    Scraper->>+Purificator: URL text body
    Purificator->>+Word2Vec: URL text pure
    Word2Vec->>+FlaskAPI: Matched Keywords
    FlaskAPI->>GunicornWSGI: Json.dumps(Matched Keywords)
    GunicornWSGI->>+user: Json.loads(Matched Keywords)
```

## GunicornWSGI
Gunicorn Web Service Gateway Interface runs Flask application API production friendly

## FlaskAPI
Generates RESTfulAPI application via Flask package ready for Client/Server requests through POST/GET methods.

## Scraper
Publish crawling web spiders to capture URL text body via Selenium automation and Chrome/Firefox latest Web Drivers in order to generate most accurate rendering of all human readable text body of input URL Webpage.
#### Liberaries
+ Selenium: great rendering of static and dynamic pages with the capability to generate dedicated contex-aware scrapers for specific websites. 
+ BeautifulSoup: powerful yet simple featureful HTML parser. 
 
## Purificator
Performing text cleaning, with removing English stop words. Also it will double check existence of each word in NLP model vocabulary corpus. 

## Word2Vec
Runs Pre-Trained Google Word2Vec NLP model in order to convert word space to vector space and perform Similarity comparision of cross referenced input text corpus.

# FAQ
## How to install and use
First of all, clone Web2Keyword repository on your system
```bash
$ git clone https://gitlab.com/remirab/Web2Keyword.git
```
and then change into package root directory
```bash
$ cd /path/to/Word2Vec
```
**Important: Please install latest version of FireFox borwser (driver>=0.29.0)**. The `Scraper` module uses Firefox [geckodriver](https://github.com/mozilla/geckodriver) to artificially renders full webpage regarding JavaScript objects that rendered server-side, not inside static HTMLs pages. For future improvements I considered to use `PhantomJS headless driver` that hopefully overcomes this issue.
```bash
$ sudo apt install firefox
```
Initialize the package with bash script `initializer.sh`. Make it executable and then run. Please pay attention that this initializer needs `sudo` privileges for some parts to perform correctly. You can take look at the script contents in the root path of the package. Considering [GenSim](https://pypi.org/project/gensim/) usage as core engine and [Word2Vec](https://en.wikipedia.org/wiki/Word2vec) as vocabulary corpus of all models, downloading approximately 1.8 GB will happen at the end of initializer. You can skip this step, but with first package startup, the download process will run automatically. 
```bash
$ chmod +x initializer.sh
$ ./initializer.sh
```
After successful package initializing, the environment is ready to run the Web Server Gateway Interface. Please consider server resources utilization. Because this version of package is somehow hugely resource intensive:

| CPU cores     | RAM           |
| ------------- | ------------- |
| 4 cores       | 16 GB         |
| at least      | at least      |

This script will start GunicornWSGI application with number of `ceil(n_process_cores / 2)` workers and `settings.HOST:settings.PORT` options considering `workers_timeout = 60s` each. If you need to change this options please make changes to `settings.py` in root folder.

> defaults: Host= "127.0.0.1", Port= "8080", workers_timeout= 60

```bash
$ ./run_server.sh
```
