'''Convert an xml atlas description
to an atlas .meta description for unity3d 4.3'''
#@file json2meta.py 
#@author niroyb
#@date 2014-03-03
# Usage >> xml2meta.py inputfile.txt > outputfile.txt
import xml.etree.ElementTree as ET
import json
import os
import sys

# .meta formatting string
FMT = '''      rect:
        serializedVersion: 2
        x: {x}
        y: {y}
        width: {width}
        height: {height}
      alignment: 7
      pivot: {{x: .5, y: 0}}'''

def formartProp(**args):
    '''Returns the .meta formated string of the json atlas properties of a sprite'''
    
    #print args
    if 'invertY' in args:
        #invert y and push down
        args['y'] = str(int(args['invertY']) - int(args['y']) - int(args['height']))
        
    name = args['name']
    return '    - name: {}\n{}'.format(os.path.splitext(name)[0],
                                           FMT.format(**args))

def getAttribs(fname):
    '''Returns the properties of each sprite of the spritesheet'''
    tree = ET.parse(fname)
    attribs = [child.attrib for child in tree.getroot()]
    return attribs

def guessHeight(attribs):
    '''Guess the height of the texture from the attribs'''
    return max(int(a['y']) + int(a['height']) for a in attribs)

def addAttribParam(attribs, param, value):
    for a in attribs:
        a[param] = value

def getMeta(fname):
    '''Returns the complete json atlas description formatted to .meta'''
    attribs = getAttribs(fname)
    height = guessHeight(attribs)
    addAttribParam(attribs, 'invertY', height)
    out = []
    for a in attribs:
        out.append(formartProp(**a))
    out.sort()
    out = '\n'.join(out)
    return out

def main():
    fname = sys.argv[1]
    meta = getMeta(fname)
    print meta

main()
