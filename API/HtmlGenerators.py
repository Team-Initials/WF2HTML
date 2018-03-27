"""
Generates HTML FIle using wireframe data
"""

from dominate import document
from dominate.tags import *
import os

def _exportFile( content, filePath ):
    with open( filePath, 'w' ) as htmlFile:
        htmlFile.write( content )


def exportHtml( htmlContent, htmlFilePath ):
    _exportFile( content=htmlContent.render(), filePath=htmlFilePath )


def exportCss( cssContent, cssFilePath):
    _exportFile( content=cssContent, filePath=cssFilePath )


def createHtml( wireframeData, cssFilename="style.css" ):
    doc = document( title='HTML File' )

    with doc.head:
        link( rel='stylesheet', href=cssFilename )

    with doc:
        for boxName in wireframeData["divDetails"].keys():
            div(_class="box", _id=boxName)
    return doc


def createCss( wireframeData ):
    cssContent = ".box{ border:2px solid black; position: absolute; }"

    sizeToScaleTo = 700.0
    scalingFactor_height = wireframeData["imageDetails"]["height"] / sizeToScaleTo
    scalingFactor_width  = wireframeData["imageDetails"]["width"] / sizeToScaleTo
    scalingFactor = max( scalingFactor_height, scalingFactor_width )
    for name, detail in wireframeData["divDetails"].iteritems():
        # TODO: Implement rotation
        cssContent += "#{}{{height: {}px; width: {}px; top: {}px; left: {}px; }}".format(name,
                                                                                 detail["height"]/scalingFactor,
                                                                                 detail["width"]/scalingFactor,
                                                                                 detail["lowestY"]/scalingFactor,
                                                                                 detail["lowestX"]/scalingFactor )
    return cssContent

def generateHtmlFromWireframeData( wireFrameData, htmlFilePath, cssFilePath ):
    htmlContent = createHtml( wireFrameData, cssFilename=os.path.basename(cssFilePath) )
    exportHtml( htmlContent, htmlFilePath )

    cssContent = createCss( wireFrameData )
    exportCss( cssContent, cssFilePath )