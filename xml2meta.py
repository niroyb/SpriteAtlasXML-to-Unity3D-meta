'''Convert an xml atlas description
to an atlas .meta description for Unity3d 4.3'''
#@author niroyb
#@date 2014-03-03
# Usage: xml2meta.py inputfile.xml > outputfile.meta
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

def attribTometa(**args):
    '''Returns the .meta formated string of the atlas properties of a sprite'''
    #print args
    if 'invertY' in args:
        #invert y and push down
        args['y'] = str(int(args['invertY']) - int(args['y']) - int(args['height']))
        
    name = args['name']
    return '    - name: {}\n{}'.format(os.path.splitext(name)[0],
                                           FMT.format(**args))
def attribsToMeta(attribs):
    '''Converts the atlas description to a .meta formatted string'''
    out = []
    for a in attribs:
        out.append(attribTometa(**a))
    out.sort()
    return '\n'.join(out)

def getAttribs(fname):
    '''Returns the properties of each sprite in the xml spritesheet'''
    tree = ET.parse(fname)
    attribs = [child.attrib for child in tree.getroot()]
    return attribs

def guessHeight(attribs):
    '''Guess the height of the original texture from the attribs'''
    return max(int(a['y']) + int(a['height']) for a in attribs)

def setAttribParam(attribs, param, value):
    '''Sets the param attribute on all attribs'''
    for a in attribs:
        a[param] = value

def main(fname):
    attribs = getAttribs(fname)
    height = guessHeight(attribs)
    #We want to invert y for the demo
    setAttribParam(attribs, 'invertY', height)
    meta = attribsToMeta(attribs)
    print meta

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        raise Exception('Missing input file argument')
