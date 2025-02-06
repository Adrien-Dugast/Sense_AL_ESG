import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def create_graph_from_name(Company_name):
    conn = sqlite3.connect('database_ratings.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ESG_ratings WHERE Company_name= ?", (Company_name,))
    rows = cursor.fetchall()

    dates = []
    ratings = []
    for row in rows:
        dates.append(datetime.strptime(row[2], '%Y-%m-%d'))
        ratings.append(row[3])

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.figure(figsize=(10, 5))
    ax.plot(dates, ratings, marker='o', linestyle='-', color='b')
    ax.set_title(f'ESG rating of {Company_name}')
    ax.set_ylabel('ESG score')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    plt.tight_layout()
    plt.show()

    return(fig)