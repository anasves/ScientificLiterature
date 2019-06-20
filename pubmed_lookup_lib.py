__author__ = 'anastasia'
import pubmed_lookup

from pubmed_lookup import PubMedLookup

# NCBI will contact user by email if excessive queries are detected
email = ''
url = 'http://www.ncbi.nlm.nih.gov/pubmed/22331878'
lookup = PubMedLookup(url, email)

#Create a Publication object:
from pubmed_lookup import Publication

publication = Publication(lookup)    # Use 'resolve_doi=False' to keep DOI URL

#Access the Publication object’s attributes:
print(
"""
TITLE:\n{title}\n
AUTHORS:\n{authors}\n
JOURNAL:\n{journal}\n
YEAR:\n{year}\n
MONTH:\n{month}\n
DAY:\n{day}\n
URL:\n{url}\n
PUBMED:\n{pubmed}\n
CITATION:\n{citation}\n
MINICITATION:\n{mini_citation}\n
ABSTRACT:\n{abstract}\n
"""
.format(**{
    'title': publication.title,
    'authors': publication.authors,
    'journal': publication.journal,
    'year': publication.year,
    'month': publication.month,
    'day': publication.day,
    'url': publication.url,
    'pubmed': publication.pubmed_url,
    'citation': publication.cite(),
    'mini_citation': publication.cite_mini(),
    'abstract': repr(publication.abstract),
}))