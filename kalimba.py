from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from pyquery import PyQuery as pq
from lxml import etree


# configuration
DATABASE = '/tmp/kalimba.db'
DEBUG = True
SECRET_KEY = "kalimba"

# creating app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('KALIMBA_SETTINGS', silent=True)

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            print f
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    g.db.close()
    return response


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, description from articles order by rank asc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/update')
def update():
    d = pq("http://hackerstreet.in/")
    content = d("body > center > table > tr:nth-child(3) > td > table > tr").filter(lambda i: pq(this).text() != '').filter(lambda i: pq(this).text() != 'More')
    g.db.execute("delete from articles")
    g.db.commit()
    for i in range(0, 60, 2):
        article = pq(content[i])
        title = article.find('td.title a').text()
        rank = int(float(pq(article.find('td')[0]).text()))
        link = article.find('td.title a').attr('href')
        link_origin = article.find('td.title span.comhead').text()
        if link_origin == None:
            link_origin = ""
        article = pq(content[i+1])
        points = int(article.find('td.subtext span').text().split()[0])
        author = pq(article.find('td.subtext a')[0]).text()
        author_url = "http://hackerstreet.in/" + pq(article.find('td.subtext a')[0]).attr('href')
        comments_count = pq(article.find('td.subtext a')[1]).text().split()[0]
        hsi_url = "http://hackerstreet.in/" + pq(article.find('td.subtext a')[1]).attr('href')
        if comments_count == 'discuss':
            comments_count = 0
        else:
            comments_count = int(comments_count)

        article = pq(hsi_url)
        # fetch the following information from article
        description = "description"
        last_comment = "/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td.default/span.comment/font"
        last_comment_author = ""
        last_comment_author_url = ""
        print rank, title, link, link_origin, description, points, author, author_url, comments_count, hsi_url
        g.db.execute("insert into articles (rank, title, link, link_origin,\
                description, points, author, author_url,\
                comments_count,last_comment, last_comment_author,\
                last_comment_author_url) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,\
                        ?, ?)", [rank, title,link, link_origin, description,
                points, author, author_url, comments_count, last_comment,
                last_comment_author, last_comment_author_url])
        g.db.commit()
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
