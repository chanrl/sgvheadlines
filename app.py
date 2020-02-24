from flask import Flask
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
from datetime import datetime
from wordcloud import WordCloud, STOPWORDS
import base64
from main import *

def prepare_image(filename):
    encoded_image = base64.b64encode(open(filename, 'rb').read())
    return encoded_image.decode()

def serve_layout():
    cum_corpus = []
    daily_corpus = [] # only docs from current day
    readSqliteTable(cum_corpus, daily_corpus)

    # create wordcloud for the day
    create_wordcloud(cum_corpus, 'full')
    create_wordcloud(daily_corpus, 'daily')

    cum_model, common_corpus, common_dictionary, daily_common_corpus = create_lda_assets(cum_corpus, daily_corpus)

    daily_df = format_daily_df(cum_model, daily_common_corpus, daily_corpus)
    topics_df = format_topics_df(cum_model)

    dateformat = '%B %d, %Y'
    date = datetime.now().strftime(dateformat)

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("GitHub Link", href="https://www.github.com/chanrl/sgvheadlines"))
        ],
        brand=f"SGV Tribune Daily Headline Scraper: Today's Date: {date}",
        brand_href="#",
        sticky="top",
    )


    daily_image = 'daily.png'
    cum_image = 'full.png'

    tab1_content = dbc.Card(dbc.CardBody([
                                html.P(f"This is {date}'s wordcloud!", className="card-text"),
                                html.Div([
                                    html.Img(src='data:image/png;base64,{}'.format(prepare_image(daily_image)))
                                ])]), className="mt-4",)

    tab2_content = dbc.Card(dbc.CardBody([
                                html.P("This is the cumulative wordcloud!", className="card-text"),
                                html.Div([
                                    html.Img(src='data:image/png;base64,{}'.format(prepare_image(cum_image)))
                                ])]), className="mt-4",)

    tabs = dbc.Tabs([dbc.Tab(tab1_content, label="Daily"),dbc.Tab(tab2_content, label="Cumulative")])

    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in daily_df.columns],
        data=daily_df.to_dict('records'),
    )

    table2 = dash_table.DataTable(
        id='table2',
        columns=[{"name": i, "id": i} for i in topics_df.columns],
        data=topics_df.to_dict('records'),
    )

    size = len(cum_corpus)

    body = dbc.Container([dbc.Row([
                            dbc.Col([
                                html.H2("Summary"),
                                html.P(f"""
                                        This is a demo Flask app that scrapes article headlines from SGV Tribune every day at 6:00 AM and 6:00 PM. 
                                        Topic modeling will ideally improve as the dataset size increases. Current dataset size is: {size}
                                        """),
                                html.P("""
                                        Hosted on Azure VM, using Beautifulsoup as the web scraper, 
                                        wordcloud is created with wordcloud module, topic modeling is achieved with gensim's LDA,
                                        scheduler is ran with cron, server ran with Nginx.
                                        """)]),
                            dbc.Col(tabs),])], className="mt-6",)

    table_container = dbc.Container([dbc.Row(html.H4("Today's Headlines with Dominant Topics")),dbc.Row(dbc.Col(table))], className='mt-4')
    table2_container = dbc.Container([dbc.Row(html.H4("LDA Model Topics with Keywords")),dbc.Row(dbc.Col(table2))], className='mt-4')
    return html.Div([navbar, body, table_container, table2_container])

app = Flask(__name__)

dash_app = dash.Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP])

dash_app.layout = serve_layout

if __name__ == "__main__":
    # app.run_server(port='5000',debug=True)
    app.run(port='5000', debug=True)
