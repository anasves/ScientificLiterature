__author__ = 'anastasia'
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

key_words = ['fba','tfa', 'kinetic', 'stochastic', 'models', 'expression' 'community']

def readAuthorList():
    doc = 'AutorsList__ '
    author_list = list()
    with open(doc) as f:
        for line in f:
            author = line.split('"')[1].split('”')[0]
            author_list.append(author)

    return author_list

def readTempAuthorList():
    author_list = list()
    with open('autors_ids.txt') as f:
        for line in f:
            author = line.split()[2].strip()
            author_list.append(author)

    return author_list

#print()

def initialiseScopus():
    ## Load configuration
    con_file = open("config.json")
    config = json.load(con_file)
    con_file.close()

    ## Initialize client
    client = ElsClient(config['apikey'])
    return client

def retrivePublicationForAuthor(author, client, output_file):
    doc_srch = ElsSearch("AUTHOR-NAME({}) AND PUBYEAR > 2018".format(author),'scopus')
    doc_srch.execute(client, get_all = True)
    print(author)
    print ("doc_srch has", len(doc_srch.results), "results.")

    for res in doc_srch.results:
        if any(i in res['dc:title'] for i in key_words):
            try:
                doi = res['prism:doi']
            except:
                try:
                    doi = res['prism:url']
                except: doi = ''
            output_file.write('{}\t{}\t{}\t{}\t{}\n'.format(res['dc:title'], doi, res['prism:coverDate'], res['subtypeDescription'], res['prism:publicationName']))




def initAuthor(author_id):
    # Initialize author with uri
    my_auth = ElsAuthor(
        uri = 'https://api.elsevier.com/content/author/author_id/{}'.format(author_id))
    print('https://api.elsevier.com/content/author/author_id/{}'.format(author_id))
    # Read author data, then write to disk
    if my_auth.read(client):
        print('OR AU-ID("{}” {})'.format(my_auth.data['author-profile']['preferred-name']['indexed-name'], author_id))
        return my_auth.data['author-profile']['preferred-name']['indexed-name']
    else:
        print ("Read author failed.")

def requestAllAuthors():
    output_file = open('Articles_PASB_Scopus__.tsv', 'w')
    output_file.write('Title\tDOI\tDate\tPublicationType\tJournal\n')
    for author in readAuthorList():
        retrivePublicationForAuthor(author, client, output_file)


client = initialiseScopus()
output_file = open('Articles_PASB_Scopus__.tsv', 'w')
output_file.write('Title\tDOI\tDate\tPublicationType\tJournal\n')

for author_id in readTempAuthorList():
    author = initAuthor(author_id)
    retrivePublicationForAuthor(author, client, output_file)