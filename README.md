# SGV Tribunes Daily Headlines Scraper

Demo Flask web app served with the following: Azure VM, sqlite3, Gunicorn

[Link](http://sgvheadline.westus.cloudapp.azure.com)

* Hosted on Azure VM using cron for automated daily scraping of news headlines from my local newspaper (SGV Tribune)
* Beautifulsoup4 for web scraper
* Data stored on sqlite3 db
* Dash framework to create the dashboard and data tables
* Wordcloud module for generating wordcloud visualizations
* Gensim's LDA for topic modeling
* SSL certificate obtained from Let's Encrypt and served with Gunicorn
