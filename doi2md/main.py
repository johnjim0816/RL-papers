import sys
import urllib.request
from urllib.error import HTTPError
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from mdutils.mdutils import MdUtils
BASE_URL = 'http://dx.doi.org/'

def doi2bibtex_str(doi):
    """
    Convert a DOI to a BibTeX entry.
    """
    url = BASE_URL + doi
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/x-bibtex')
    try:
        with urllib.request.urlopen(req) as f:
            bibtex_str = f.read().decode()
    except HTTPError as e:
        if e.code == 404:
            print('DOI not found.')
        else:
            print('Service unavailable.')
        sys.exit(1)
    return bibtex_str
md_file = MdUtils(file_name='output')
with open('doi.txt') as doi_f:
    for line in doi_f.readlines():
        doi,short_name,proceed = line[:-1].split(',') # .[-1]去掉换行符
        bibtex_str = doi2bibtex_str(doi)
        parser = BibTexParser()
        parser.ignore_nonstandard_types = True
        bibdb = bibtexparser.loads(bibtex_str)
        entry, = bibdb.entries
        title = entry['title']
        year = entry['year']
        first_author = entry['author'].split(',')[0]
        url = entry['url']
        if short_name != '' and proceed != '':
            md_file.write(f"* **{short_name}**: [{title}]({url}), {first_author} et al {year}, {proceed}.\n")
        elif short_name != '':
            md_file.write(f"* **{short_name}**: [{title}]({url}), {first_author} et al {year}.\n")
        elif proceed != '':
            md_file.write(f"* [{title}]({url}), {first_author} et al {year}, {proceed}.\n")
        else:
            md_file.write(f"* [{title}]({url}), {first_author} et al {year}.\n")
        # md_file.write()
md_file.create_md_file()
