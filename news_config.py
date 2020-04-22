"""
User settings for news.
"""
import os

# Toggle today's news. Set to True if you only want to pull today's news.
# Default: False
todays_news = False


# Number of news articles (top headlines) you want to pull per category.
# Default: 5
headline_count = 20

# Categories to pull top headlines from.
# Comment to exclude category; decomment to include it.
st_categories = [
    ("Singapore", "http://www.straitstimes.com/singapore"),
    ("Politics", "http://www.straitstimes.com/politics"),
    ("Asia", "http://www.straitstimes.com/asia"),
    ("World", "http://www.straitstimes.com/world"),
    ("Lifestyle", "http://www.straitstimes.com/lifestyle"),
    ("Food", "http://www.straitstimes.com/lifestyle/food"),
    ("Business", "http://www.straitstimes.com/business"),
    ("Sport", "http://www.straitstimes.com/sport"),
    ("Tech", "http://www.straitstimes.com/tech")
]

# Specific tags to pull latest news from.
# Comment to exclude category; decomment to include it.
# Included tags will be added to main categories.
st_tags = [
    # ("Scientific Research", "http://www.straitstimes.com/tags/scientific-research")
    # ("Science", "http://www.straitstimes.com/tags/science"),
    # ("US Politics", "http://www.straitstimes.com/tags/us-politics")
]

for tag in st_tags:
    st_categories.append(tag)
