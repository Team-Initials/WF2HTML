"""
    This file deals with managing the HTML text like updating tags and deleting tags
"""

from bs4 import BeautifulSoup

def _importSoupFromHtml( htmlFilePath ):
    with open(htmlFilePath, "r") as htmlFile:
        htmlContent = htmlFile.read()
    soup = BeautifulSoup(htmlContent, "html.parser")
    return soup

def _exportSoupToHtml( soup, htmlFilePath ):
    output = str(soup.prettify(formatter="minimal"))
    with open(htmlFilePath, "w") as htmlFile:
        htmlFile.write(output)


def deleteHtmlElement( htmlFilePath, id ):
    soup = _importSoupFromHtml( htmlFilePath )
    elementToDelete = soup.find(id=id)
    elementToDelete.decompose()
    _exportSoupToHtml( soup, htmlFilePath )

def prettifyHtml( htmlFilePath ):
    soup = _importSoupFromHtml( htmlFilePath )
    _exportSoupToHtml( soup, htmlFilePath )

def changeHtmlTag( htmlFilePath, id, targetTagType ):
    soup = _importSoupFromHtml(htmlFilePath)
    elementToDelete = soup.find(id=id)
    elementToDelete.name = targetTagType
    print targetTagType
    _exportSoupToHtml(soup, htmlFilePath)
