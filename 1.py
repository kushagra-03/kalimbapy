from pyquery import PyQuery as pq
d = pq("http://hackerstreet.in/")

content = d("body > center > table > tr:nth-child(3) > td > table > tr").filter(lambda i: pq(this).text() != '').filter(lambda i: pq(this).text() != 'More')

for i in range(0, 60, 2):
    article = pq(content[i])
    title = article.find('td.title a').text()
    rank = int(float(pq(article.find('td')[0]).text()))
    link = article.find('td.title a').attr('href')
    link_origin = article.find('td.title span.comhead').text()
    description = "description"
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
    last_comment = ""
    last_comment_author = ""
    last_comment_author_url = ""
    print rank, title, link, link_origin, description, points, author, author_url, comments_count, hsi_url
