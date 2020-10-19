import feedparser,re, calendar
from datetime import datetime

medium_url = 'https://medium.com/feed/@petrousov'
html_table_start = """
<!-- posts feed starts -->
<table class="blog-table">
"""
html_table_row = """
  <tr>
    <td class="blog-date-column">{pub_date}</td>
    <td class="blog-post-column">
      <a href="{pub_url}">
        {pub_title}
      </a>
    </td>
  </tr>
"""
html_table_end = """
</table>
<!-- posts feed ends -->
"""


def fetch_feed_from_medium():
    return feedparser.parse(medium_url)


def remove_comments_from_feed(feed_data):
    
    feed_without_comments = []
    for entry in feed_data.entries:
        if entry.has_key('category'):
            title = entry.title
            pub_date = entry.published
            link = entry.link
            feed_without_comments.append({'title':title, 'pub_date':pub_date, 'link':link})

    return feed_without_comments


def craft_html_table_with_posts(posts):

    html_blog_table = html_table_start
    for post in posts:
        title = post['title']
        link = post['link']
        full_pub_date = datetime.strptime(post['pub_date'], '%a, %d %b %Y %X %Z')
        pub_date = str(full_pub_date.day) + ' ' + calendar.month_abbr[full_pub_date.month] + ' ' + str(full_pub_date.year)
        html_blog_table += html_table_row.format(pub_date=pub_date, pub_url=link, pub_title=title)
    html_blog_table += html_table_end

    return html_blog_table


def write_html_table_with_posts_into_website(html_text):
    with open("index.html", "r") as index_file:
        index_file_content = index_file.read()
    updated_content = re.sub('\n<!-- posts feed starts -->.*?<!-- posts feed ends -->\n', html_text, index_file_content, flags=re.DOTALL)
    with open("index.html", "w") as index_file:
        index_file.write(updated_content)
    return


if __name__ == "__main__":
    # Fetch feed
    medium_feed = fetch_feed_from_medium()

    # Remove comments from feed
    posts = remove_comments_from_feed(medium_feed)

    # Craft HTML text with posts table
    html_table_with_posts = craft_html_table_with_posts(posts)

    # Write HTML text with posts into website
    write_html_table_with_posts_into_website(html_table_with_posts)

