# SGV Tribunes Daily Headlines Scraper

Demo Flask web app served with the following: Azure VM, sqlite3, Apache

[Link](https://sgvheadlines.westus.cloudapp.azure.com:8080/)

* Hosted on Azure VM using cron for automated daily scraping of news headlines from my local newspaper (SGV Tribune)
* Beautifulsoup4 for web scraper
* Data stored on sqlite3 db
* Dash framework to create the dashboard and data tables
* Wordcloud module for generating wordcloud visualizations
* Gensim's LDA for topic modeling
* SSL certificate obtained from Let's Encrypt and served with Gunicorn
