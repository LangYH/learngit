# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 17:27:50 2014

@author: Administrator
"""

from scipy.cluster.vq import *
import pickle
from numpy import *
from pylab import *
from PIL import Image, ImageDraw
import os

def testUsingPCA():
    imlist = [ os.path.join( 'selectedfontimages/', im ) for im in os.listdir( 'selectedfontimages/' ) ]
    imnbr =  len( imlist ) 
    with open( 'font_pca_modes.pkl', 'rb' ) as f:
        immean = pickle.load( f )
        V = pickle.load( f )
    immatrix = array( [ array( Image.open( im ) ).flatten() for im in imlist ], 'f' )
    immean = immean.flatten()
    projected = array( [ dot( V[[0,2]], immatrix[i]-immean ) for i in range( imnbr ) ] )
    projected = whiten( projected )
    k = 4
    centroids, distortion = kmeans( projected, k )
    code, distrance = vq( projected, centroids )
    for i in range(k):
        ind = where( code == i )[0]
        figure()
        gray()
        for j in range( minimum( len(ind), 40 ) ):
            subplot( 4, 10, j + 1 )
            imshow( immatrix[ ind[j] ].reshape( (25,25 ) ) )
            axis( 'off' )
    show()
    return projected,imlist
    
def drawInImage():
    imlist = [ os.path.join( 'selectedfontimages/', im ) for im in os.listdir( 'selectedfontimages/' ) ]
    imnbr =  len( imlist ) 
    with open( 'font_pca_modes.pkl', 'rb' ) as f:
        immean = pickle.load( f )
        V = pickle.load( f )
    immatrix = array( [ array( Image.open( im ) ).flatten() for im in imlist ], 'f' )
    immean = immean.flatten()
    projected = array( [ dot( V[[0,2]], immatrix[i]-immean ) for i in range( imnbr ) ] )
    projected = whiten( projected )
    
    h, w = 1200, 1200
    img = Image.new( 'RGB', (w,h), ( 255, 255,255))
    draw = ImageDraw.Draw(img)
    draw.line( ( 0, h/2, w, h/2), fill = (255, 0, 0 ) )
    draw.line( ( w/2, 0, w/2, h ) , fill = ( 255, 0, 0 ) )
    
    scale = abs( projected ).max(0)
    scaled = floor( array( [ ( p/scale)*(w/2-20,h/2-20) +(w/2,h/2) for p in projected]))
    
    for i in range( imnbr ):
        nodeim =Image.open( imlist[i] )
        nodeim.thumbnail( (25,25) )
        ns = nodeim.size
        img.paste( nodeim, (int(scaled[i][0]-ns[0]//2), int(scaled[i][1]-
            ns[1]//2), int(scaled[i][0]+int(ns[0]//2+1)), int(scaled[i][1]+ns[1]//2+1)))
            
    img.save( 'pca_font.jpg' )
        
    
    
    
    
    
    
    
    
    