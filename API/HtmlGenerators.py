"""
Generates HTML FIle using wireframe data
"""

from dominate import document, tags
from dominate.tags import *
from API import FileManagers
import os

def _exportFile( content, filePath ):
    with open( filePath, 'w' ) as htmlFile:
        htmlFile.write( content )


def exportHtml( htmlContent, htmlFilePath ):
    _exportFile( content=htmlContent.render(), filePath=htmlFilePath )


def exportCss( cssContent, cssFilePath):
    _exportFile( content=cssContent, filePath=cssFilePath )


def _getScalingFactor( wireframeData ):
    sizeToScaleTo = 700.0
    scalingFactor_height = wireframeData["imageDetails"]["height"] / sizeToScaleTo
    scalingFactor_width = wireframeData["imageDetails"]["width"] / sizeToScaleTo
    scalingFactor = max(scalingFactor_height, scalingFactor_width)
    return scalingFactor

def createHtml( wireframeData, cssFilename=None, cssContent=None ):
    doc = document( title='HTML File' )

    # Adding the style tag if cssType == Internal
    if cssContent != None and cssFilename == None:
        with doc.head:
            tags.style( cssContent )

    # Adding the link tag for the css file if csstype == External
    if cssFilename != None and cssContent == None:
        with doc.head:
            link( rel='stylesheet', href=cssFilename )

    with doc:
        if cssContent == None and cssFilename == None:
            #  Adding style for each element if cssType == Inline
            for boxName, detail in wireframeData["divDetails"].iteritems():
                style = "border:2px solid black; position: absolute; ";
                scalingFactor = _getScalingFactor(wireframeData)
                style += " height: {0:.2f}px; width: {1:.2f}px; top: {2:.2f}px; left: {3:.2f}px;".format(
                    detail["height"] / scalingFactor,
                    detail["width"] / scalingFactor,
                    detail["lowestY"] / scalingFactor,
                    detail["lowestX"] / scalingFactor)
                div(_class="box", _id=boxName, _style=style)

        else:
            # Only divs are added for the other cssTypes
            for boxName in wireframeData["divDetails"].keys():
                div(_class="box", _id=boxName)
    return doc


def createCss( wireframeData ):
    cssContent = ".box{ border:2px solid black; position: absolute; }"
    scalingFactor = _getScalingFactor( wireframeData )
    for name, detail in wireframeData["divDetails"].iteritems():
        # TODO: Implement rotation
        cssContent += "#{0}{{height: {1:.2f}px; width: {2:.2f}px; top: {3:.2f}px; left: {4:.2f}px; }}".format(name,
                                                                                         detail["height"]/scalingFactor,
                                                                                         detail["width"]/scalingFactor,
                                                                                         detail["lowestY"]/scalingFactor,
                                                                                         detail["lowestX"]/scalingFactor )
    return cssContent


def generateHtmlFile( wireframeData, imageFilePath, cssType ):
    if cssType == "Internal":
        cssContent = createCss( wireframeData )
        htmlContent = createHtml( wireframeData, cssContent=cssContent, cssFilename=None )
    elif cssType=="External":
        cssFileName = FileManagers.changeExtension(imageFilePath, targetExtension="css")
        htmlContent = createHtml( wireframeData, cssContent=None, cssFilename=cssFileName )
    else:
        htmlContent = createHtml( wireframeData, cssFilename=None, cssContent=None )
    exportHtml( htmlContent, FileManagers.changeExtension( imageFilePath, targetExtension="html" ))


def generateHtmlFromWireframeData( wireFrameData, imageFilePath, cssType ):
    if cssType == "External":
        cssContent = createCss( wireFrameData )
        cssFilePath = FileManagers.changeExtension( imageFilePath, targetExtension="css" )
        exportCss( cssContent, cssFilePath )
    generateHtmlFile( wireFrameData, imageFilePath, cssType )
    #TODO : Remove later
    cssContent = createCss(wireFrameData)
    cssFilePath = FileManagers.changeExtension(imageFilePath, targetExtension="css")
    exportCss(cssContent, cssFilePath)

