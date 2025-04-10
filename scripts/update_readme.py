import os
import re
import feedparser
from typing import List, Tuple

RSS_FEED_URL = "https://medium.com/feed/@le_Tomassini"  
NUM_POSTS = 5
README_PATH = "README.md"


def get_latest_posts(feed_url: str, count: int) -> List[Tuple[str, str]]:
    """
    Fetch the latest blog posts from an RSS feed.

    This function parses the given RSS feed and returns a list of tuples, each containing the title 
    and the URL of the most recent posts.

    :param feed_url: URL of the RSS feed.
    :param count: Number of posts to return.
    :return: List of tuples (post title, post URL).
    """
    feed = feedparser.parse(feed_url)
    return [(entry.title, entry.link) for entry in feed.entries[:count]]


def update_readme(blog_posts: List[Tuple[str, str]], readme_path: str) -> None:
    """
    Update the README file with the latest blog post titles as clickable links.

    This function searches for markers in the README file (between <!-- BLOG_START --> and <!-- BLOG_END -->)
    and replaces the content with a formatted list of blog post titles as Markdown links.

    :param blog_posts: List of tuples (post title, post URL).
    :param readme_path: Path to the README file.
    """
    if not os.path.isfile(readme_path):
        print(f"README file not found at {readme_path}.")
        return

    with open(readme_path, "r", encoding="utf-8") as file:
        readme_content = file.read()

    pattern = r"(<!-- BLOG_START -->)(.*?)(<!-- BLOG_END -->)"
    formatted_posts = "\n".join([f"- [{title}]({link})" for title, link in blog_posts])
    new_section = f"<!-- BLOG_START -->\n{formatted_posts}\n<!-- BLOG_END -->"
    new_readme_content, count = re.subn(pattern, new_section, readme_content, flags=re.DOTALL)

    if count == 0:
        print("Blog markers not found in README. Please add <!-- BLOG_START --> and <!-- BLOG_END --> markers.")
        return

    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(new_readme_content)


def main() -> None:
    """
    Fetch the latest blog posts from the Medium RSS feed and update the README file with clickable links.
    """
    posts = get_latest_posts(RSS_FEED_URL, NUM_POSTS)
    if posts:
        update_readme(posts, README_PATH)
    else:
        print("No posts found in RSS feed.")

if __name__ == "__main__":
    main()
