"""
This file contains all the function used to operate on images
"""

import math
import imutils
from imutils import perspective
from imutils import contours
import numpy as np
import cv2


def getLowestX( boundingBox ):
    return min( [ point[0] for point in boundingBox ] )


def getLowestY( boundingBox ):
    return min( [ point[1] for point in boundingBox ] )


def findBoundingBoxData( boundingBox ):
    point1 = boundingBox[ 0 ]
    point2 = boundingBox[ 1 ]
    point3 = boundingBox[ 2 ]
    point4 = boundingBox[ 3 ]

    boundingBoxData = dict()

    boundingBoxData[ "width" ] = math.sqrt(  ( math.pow( point1[ 0 ] - point2[ 0 ], 2 ) )
                                           + ( math.pow( point1[ 1 ] - point2[ 1 ], 2 ) ) )

    boundingBoxData[ "height" ] = math.sqrt( ( math.pow( point1[ 0 ] - point4[ 0 ], 2 ) )
                                           + ( math.pow( point1[ 1 ] - point4[ 1 ], 2 ) ) )

    radian = math.atan2( point2[ 1 ] - point1[ 1 ], point2[ 0 ] - point1[ 0 ] )
    boundingBoxData[ "rotation" ] = math.degrees( radian )

    # As the bounding areas are rectangles, the centre of each axis is at the mean distance of each point
    boundingBoxData[ "centreX" ] = (point1[ 0 ] + point2[ 0 ] + point3[ 0 ] + point4[ 0 ]) / 4
    boundingBoxData[ "centreY" ] = (point1[ 1 ] + point2[ 1 ] + point3[ 1 ] + point4[ 1 ]) / 4
    boundingBoxData[ "lowestX" ] = getLowestX( boundingBox )
    boundingBoxData[ "lowestY" ] = getLowestY( boundingBox )
    return boundingBoxData


def getBoundingBox( contour ):
    boundingBox = cv2.minAreaRect( contour )
    if imutils.is_cv2():
        boundingBox = cv2.cv.BoxPoints( boundingBox )
    else:
        boundingBox = cv2.boxPoints( boundingBox )
    boundingBox = np.array( boundingBox, dtype="int" )
    boundingBox = perspective.order_points( boundingBox )
    return boundingBox


def getDivDetailsFromContours( contoursObtained, startingDivIndex ):

    wireframeData = dict()
    for index, contour in enumerate( contoursObtained ):
        boundingBox = getBoundingBox( contour )
        boundingBoxData = findBoundingBoxData( boundingBox )
        wireframeData[ 'Obj%s' % (index + startingDivIndex) ] = boundingBoxData
    return wireframeData


def getContours( edges ):
    contoursObtained = cv2.findContours( edges.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE )

    # Selecting tuples based on openCV version
    return contoursObtained[ 0 ] if imutils.is_cv2() else contoursObtained[ 1 ]


def getEdges( image_clearedShapes ):
    # Canny edge detection
    edges = cv2.Canny( image_clearedShapes, 50, 100 )
    # dilation & erosion to close gaps in between object edges
    edges_dilated = cv2.dilate( edges, None, iterations=1 )
    edges_eroded = cv2.erode( edges_dilated, None, iterations=1 )

    return edges_eroded


def makeShapesClear( image ):
    # convert it to grayscale
    image_gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    # Blur image to reduce noise
    image_blurred = cv2.GaussianBlur( image_gray, (7, 7), 0 )
    # FIXME: Why isn't a threshold applied ???
    return image_blurred


def getWireframeDataFromImage( imageFilePath, startingDivIndex ):
    image = cv2.imread( imageFilePath )

    imageDetails = dict()
    imageDetails["height"], imageDetails["width"] = image.shape[:2]
    image_clearedShapes = makeShapesClear( image )
    edges = getEdges( image_clearedShapes )
    contoursObtained = getContours( edges )
    (contoursObtained, _) = contours.sort_contours( contoursObtained )
    divDetails = getDivDetailsFromContours( contoursObtained, startingDivIndex )
    wireframeData = {
        "divDetails": divDetails,
        "imageDetails": imageDetails
    }
    return (wireframeData, len(wireframeData))



