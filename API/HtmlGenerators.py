"""
Generates HTML FIle using wireframe data
"""

from dominate import document, tags
from dominate.tags import *
from API import FileManagers, HtmlManager
import os

def _exportFile( content, filePath ):
    with open( filePath, 'w' ) as htmlFile:
        htmlFile.write( content )


def exportHtml( htmlContent, htmlFilePath ):
    _exportFile( content=htmlContent.render(), filePath=htmlFilePath )


def exportCss( cssContent, cssFilePath):
    _exportFile( content=cssContent, filePath=cssFilePath )


def exportJs( jsContent, jsFilePath ):
    _exportFile( content=jsContent, filePath=jsFilePath )


def _getScalingFactor( wireframeData, imageLayoutDirection ):
    sizeToScaleTo = 700.0
    if imageLayoutDirection == "Vertical":
        scalingFactor = wireframeData["imageDetails"]["width"] / sizeToScaleTo
    else:
        scalingFactor = wireframeData["imageDetails"]["height"] / sizeToScaleTo
    return scalingFactor

def createHtml( wireframeData, js, cssFilename=None, cssContent=None, imageLayoutDirection="Vertical" ):
    doc = document( title='HTML File' )

    with doc.head:
        # Adding the style tag if cssType == Internal
        if cssContent != None and cssFilename == None:
            tags.style( cssContent )

        #   Adding the link tag for the css file if csstype == External
        if cssFilename != None and cssContent == None:
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
        script(js)
    return doc


def createCss( wireframeData, imageLayoutDirection ):
    cssContent = ".box{ border:1px solid black; position: absolute; }"
    leftOffset, topOffset = 0, 0
    for index, eachWireFrameData in enumerate(wireframeData):
        scalingFactor = _getScalingFactor( eachWireFrameData, imageLayoutDirection )
        for name, detail in eachWireFrameData["divDetails"].iteritems():
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


def generateHtmlFile( wireframeData, js, imageFilePath, cssType, imageLayoutDirection="Vertical" ):
    if cssType == "Internal":
        cssContent = createCss( wireframeData, imageLayoutDirection=imageLayoutDirection )
        htmlContent = createHtml( wireframeData, js, cssContent=cssContent ) # cssFilename=None
    elif cssType=="External":
        cssFileName = FileManagers.changeExtension(imageFilePath, targetExtension="css")
        htmlContent = createHtml( wireframeData, js, cssFilename=cssFileName ) # cssContent=None
    else:
        htmlContent = createHtml( wireframeData, js) # cssFilename=None, cssContent=None
    exportHtml( htmlContent, FileManagers.changeExtension( imageFilePath, targetExtension="html" ))
    HtmlManager.prettifyHtml( FileManagers.changeExtension( imageFilePath, targetExtension="html" ) )


def generateHtmlFromWireframeData( wireFrameData, imageFilePath, cssType, imageLayoutDirection ):
    if cssType == "External":
        cssContent = createCss( wireFrameData, imageLayoutDirection=imageLayoutDirection )
        cssFilePath = FileManagers.changeExtension( imageFilePath, targetExtension="css" )
        exportCss( cssContent, cssFilePath )
    js = generateJsFile( imageFilePath )
    generateHtmlFile( wireFrameData, js, imageFilePath, cssType, imageLayoutDirection=imageLayoutDirection )
    #TODO : Remove later
    cssContent = createCss(wireFrameData, imageLayoutDirection=imageLayoutDirection)
    cssFilePath = FileManagers.changeExtension(imageFilePath, targetExtension="css")
    exportCss(cssContent, cssFilePath)


def generateJsFile(imageFilePath):
    jsContent = """
        var tagOptions = ['div', 'span', 'section', 'nav'];
        var selectedId = '';

        function cancelTagChange() {
            if( document.getElementById( 'tagSelectionForm' ) )
                document.getElementById( 'tagSelectionForm' ).remove();
        };

        function confirmTagChange() {
            targetTagType = document.getElementById( 'tagSelectionDropdown' ).value;
            WebViewController.changeHtmlTag( selectedId, targetTagType );
            cancelTagChange();
        };
        
        var allDivs = document.getElementsByClassName('box');
        
        for(var divIndex=0; divIndex != allDivs.length; divIndex++ )
        {
            // Single click used to select the item
            allDivs[divIndex].addEventListener('click', function(event) {
                targetId = event.target.id;
                if(targetId == selectedId)
                    selectedId = '';
                else {
                    document.getElementById( targetId ).style.borderColor = 'red';
                    selectedId = targetId;
                    WebViewController.logJs( selectedId );
                }
            });
                        
            // Double click to show the tag selection form
            allDivs[divIndex].addEventListener('dblclick', function(event) {
                cancelTagChange();
                var left = event.pageX;
                var top = event.pageY;
                var targetId = event.target.id;
                if( targetId ) {
                    selectedId = targetId;
                    console.log('#'+selectedId);
                    var form = document.createElement( 'form' );
                    form.id = 'tagSelectionForm';

                    var select = document.createElement( 'select' );
                    select.id = 'tagSelectionDropdown';
                    for(var index=0; index != tagOptions.length; index++) {
                        var option = document.createElement('option');
                        option.value = tagOptions[ index ];
                        option.appendChild( document.createTextNode( tagOptions[ index ] ) );
                        select.appendChild( option );
                    }

                    submitButton = document.createElement( 'button' );
                    submitButton.type = 'submit';
                    submitButton.id = 'confirm-tag-change';
                    submitButton.addEventListener('click', function(event) {
                        event.preventDefault();
                        confirmTagChange();
                    });
                    submitButton.appendChild( document.createTextNode( 'Confirm' ) );

                    cancelButton = document.createElement( 'button' );
                    cancelButton.type = 'cancel';
                    cancelButton.id = 'cancel-tag-change';
                    cancelButton.addEventListener('click', function(event) {
                        event.preventDefault();
                        cancelTagChange();
                    });
                    cancelButton.appendChild( document.createTextNode( 'Cancel' ) );

                    form.appendChild( select );
                    form.appendChild( submitButton );
                    form.appendChild( cancelButton );

                    form.style.position = 'absolute';
                    form.style.top = top + 'px';
                    form.style.left = left + 'px';

                    document.body.appendChild( form );
                }
            });
        }
        
        // Pressing delete to delete the selected element
        document.body.addEventListener('keyup', function(event) {
            cancelTagChange();
            if( event.which == 46 ) // i.e. If delete key is pressed
            {
                if( selectedId == '' )
                    return;
                WebViewController.deleteHtmlElement( selectedId );
                selectedId = '';
            }
        });
        
    """
    return jsContent
    # exportJs(jsContent, FileManagers.changeExtension(imageFilePath, targetExtension='js'))
    # return FileManagers.changeExtension( imageFilePath, targetExtension='js')