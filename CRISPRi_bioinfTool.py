
# coding: utf-8

# In[ ]:

from IPython.display import display, Image
import xml.etree.ElementTree as ET
import requests
import pythoncyc as pc
#import untangle
#import biopython

# this function finds all pathways associated with the molecule of interest. needs work on front end to 
# allow user to define G.O. function associated with molecule.
def pathwayFromCompound(compound):
    #request pathway xml from ecocyc server
    resp = requests.get("http://ecocyc.org/apixml?fn=pathways-of-compound&id=ECOLI:{}".format(compound))
    #builds element tree from the response xml text file
    root = ET.fromstring(resp.text)
    #pulls all elements associated with Pathway tag
    pathways = root.findall("./Pathway")
    #pulls all pathway IDs
    for pathway in pathways:
        pathID = pathway.attrib['frameid']
        print (pathID)
        print "Pathway: ", pathway.findall("common-name")[0].text
        #instead of this we can present a tree of the biokernel
        userPath = raw_input("Do you want to knockdown this function? yes or no.")
        if userPath == "yes":
            genesFromPathway(pathID)
        else:
            continue

# this function pulls all geneIDs associated with the pathwayID passed into it
def genesFromPathway(pathwayID):
    resp  = requests.get("http://ecocyc.org/apixml?fn=genes-of-pathway&id=ECOLI:{}".format(pathwayID))
    root = ET.fromstring(resp.text)
    #print(resp.text)
    genes = root.findall("./Gene")
    
    for gene in genes:
        geneID = gene.attrib['frameid']
        geneName = gene.findall("common-name")[0].text
        print "Gene: " + geneName + ", GeneID: " + geneID
        getPromoter(geneID)

# this function pulls the promoterIDs associated with the geneID passed into it
def getPromoter(geneID):
    resp  = requests.get("http://ecocyc.org/apixml?fn=transcription-units-of-gene&id=ECOLI:{}".format(geneID))
    root=ET.fromstring(resp.text)
    #print(resp.text)
    promoters=root.findall("./Transcription-Unit/component/Promoter")
    #print promoters
    for promoter in promoters:
        pID = promoter.attrib['frameid']
        #regulon = ecoli.containing_chromosome(pID)
        print "promoter: ",pID 
        #print(regulon)

ecoli = pc.select_organism("ECOLI")
pathwayFromCompound("SER")
#genesFromPathway("HISTSYN-PWY")


# In[ ]:



