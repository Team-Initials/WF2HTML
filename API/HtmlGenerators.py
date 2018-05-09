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


def _getScalingFactor( wireframeData, imageLayoutDirection ):
    sizeToScaleTo = 700.0
    if imageLayoutDirection == "Vertical":
        scalingFactor = wireframeData["imageDetails"]["width"] / sizeToScaleTo
    else:
        scalingFactor = wireframeData["imageDetails"]["height"] / sizeToScaleTo
    return scalingFactor

def createHtml( wireframeData, cssFilename=None, cssContent=None, imageLayoutDirection="Vertical" ):
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
        leftOffset, topOffset = 0, 0
        for index, eachWireFrameData in enumerate( wireframeData ):
            #  Adding style for each element if cssType == Inline
            if cssContent == None and cssFilename == None:
                scalingFactor = _getScalingFactor(eachWireFrameData, imageLayoutDirection)
                for boxName, detail in eachWireFrameData["divDetails"].iteritems():
                    style = "border:1px solid black; position: absolute; "
                    style += " height: {0:.2f}px; width: {1:.2f}px; top: {2:.2f}px; left: {3:.2f}px;".format(
                        detail["height"] / scalingFactor,
                        detail["width"] / scalingFactor,
                        detail["lowestY"] / scalingFactor + topOffset,
                        detail["lowestX"] / scalingFactor + leftOffset)
                    div(_class="box", _id=boxName, _style=style)
                if imageLayoutDirection == "Vertical":
                    topOffset = topOffset + eachWireFrameData["imageDetails"]["height"] / scalingFactor
                else:
                    leftOffset = leftOffset + eachWireFrameData["imageDetails"]["width"] / scalingFactor
            else:
                # Only divs are added for the other cssTypes
                for boxName in eachWireFrameData["divDetails"].keys():
                    div(_class="box", _id=boxName)
    return doc


def createCss( wireframeData, imageLayoutDirection ):
    cssContent = ".box{ border:1px solid black; position: absolute; }"
    leftOffset, topOffset = 0, 0
    for index, eachWireFrameData in enumerate(wireframeData):
        scalingFactor = _getScalingFactor( eachWireFrameData, imageLayoutDirection )
        for name, detail in eachWireFrameData["divDetails"].iteritems():
            # TODO: Implement rotation
            cssContent += "#{0}{{height: {1:.2f}px; width: {2:.2f}px; top: {3:.2f}px; left: {4:.2f}px; }}".format(
                name,
                detail["height"]/scalingFactor,
                detail["width"]/scalingFactor,
                detail["lowestY"]/scalingFactor + topOffset,
                detail["lowestX"]/scalingFactor + leftOffset)
        if imageLayoutDirection == "Vertical":
            topOffset = topOffset + eachWireFrameData["imageDetails"]["height"] / scalingFactor
        else:
            leftOffset = leftOffset + eachWireFrameData["imageDetails"]["width"] / scalingFactor
    return cssContent


def generateHtmlFile( wireframeData, imageFilePath, cssType, imageLayoutDirection="Vertical" ):
    if cssType == "Internal":
        cssContent = createCss( wireframeData, imageLayoutDirection=imageLayoutDirection )
        htmlContent = createHtml( wireframeData, cssContent=cssContent ) # cssFilename=None
    elif cssType=="External":
        cssFileName = FileManagers.changeExtension(imageFilePath, targetExtension="css")
        htmlContent = createHtml( wireframeData, cssFilename=cssFileName ) # cssContent=None
    else:
        htmlContent = createHtml( wireframeData ) # cssFilename=None, cssContent=None
    exportHtml( htmlContent, FileManagers.changeExtension( imageFilePath, targetExtension="html" ))


def generateHtmlFromWireframeData( wireFrameData, imageFilePath, cssType, imageLayoutDirection ):
    if cssType == "External":
        cssContent = createCss( wireFrameData, imageLayoutDirection=imageLayoutDirection )
        cssFilePath = FileManagers.changeExtension( imageFilePath, targetExtension="css" )
        exportCss( cssContent, cssFilePath )
    generateHtmlFile( wireFrameData, imageFilePath, cssType, imageLayoutDirection=imageLayoutDirection )
    #TODO : Remove later
    cssContent = createCss(wireFrameData, imageLayoutDirection=imageLayoutDirection)
    cssFilePath = FileManagers.changeExtension(imageFilePath, targetExtension="css")
    exportCss(cssContent, cssFilePath)

