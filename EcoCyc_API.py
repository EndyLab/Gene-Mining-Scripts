# %load ~/Downloads/EcoCyc_API.py
#Edited by Akshay
import xml.etree.ElementTree as ET
import requests

def showReactionPathway(reaction):
    resp = requests.get("http://websvc.biocyc.org/getxml?id=ECOLI:%s&detail=full" % reaction)
    root = ET.fromstring(resp.text)

    pathways = root.findall(".//Pathway")
    if len(pathways) == 0:
        print "No pathway found for %s" % reaction
        
    for pathway in pathways:
        pathID = pathway.attrib['frameid']
        display(Image(url="http://biocyc.org/ECOLI/diagram-only?type=PATHWAY&object=%s" % pathID))
        print "Pathway:", "http://ecocyc.org/ECOLI/NEW-IMAGE?type=PATHWAY&object=%s" % pathID        
        
    print "HiReaction:", "http://ecocyc.org/ECOLI/NEW-IMAGE?type=NIL&object=%s&redirect=T" % reaction