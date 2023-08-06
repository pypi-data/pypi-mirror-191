import setuptools

with open("README.md","r",encoding="utf-8") as f:
    long_desc = f.read()

__version__ = "0.1.7"

REPO_NAME = "simplegoogle_scraper_python"
AUTHOUR_USER_NAME = "biswa-mohapatra"
SRC_REPO = "simplegoogle_scraper_python"
AUTHOR_EMAIL = "jeetmohapatra98@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOUR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for scraping google search results.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOUR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker":f"https://github.com/{AUTHOUR_USER_NAME}/{REPO_NAME}/issues"
    },
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
)
