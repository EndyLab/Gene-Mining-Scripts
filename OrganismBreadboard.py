
# coding: utf-8

# In[15]:

from IPython.display import display, Image
import xml.etree.ElementTree as ET
import requests
import pythoncyc as pc
from HTMLParser import HTMLParser
from lxml import html
#import biopython

# this function finds all pathways associated with the molecule of interest. needs work on front end to 
# allow user to define G.O. function associated with molecule.
def pathwayFromCompound(compound):
    pathIDs = []
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
            break
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
        page = requests.get("http://biocyc.org/gene?orgid=ECOLI&id=EG11879")
        #print(page.content)
        #tree = html.fromstring(page.content)
        #mapPost = tree.find("./Map Position")
        #print(mapPost)
        #root1 = ET.fromstring(resp1.text)
        
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
        absPositPlusOne = promoter.find('absolute-plus-1-pos').text
        #regulon = ecoli.containing_chromosome(pID)
        print "promoter: ",pID
        print(absPositPlusOne)
        #print(regulon)

#ecoli = pc.select_organism("ECOLI")
#pathwayFromCompound("SER")
genesFromPathway("HISTSYN-PWY")


# In[6]:

from IPython.display import display, Image
import xml.etree.ElementTree as ET
import requests
import pythoncyc as pc
from HTMLParser import HTMLParser
from lxml import html
#import biopython

# this function finds all pathways associated with the molecule of interest. needs work on front end to 
# allow user to define G.O. function associated with molecule.
def pathwayFromCompound(compound):
    pathWays = {}
    #request pathway xml from ecocyc server
    resp = requests.get("http://ecocyc.org/apixml?fn=pathways-of-compound&id=ECOLI:{}".format(compound))
    #builds element tree from the response xml text file
    root = ET.fromstring(resp.text)
    #pulls all elements associated with Pathway tag
    pathways = root.findall("./Pathway")
    #pulls all pathway IDs
    for pathway in pathways:
        pathID = pathway.attrib['frameid']
        pathWays[pathID] = pathway.findall("common-name")[0].text
        #print (pathWays)
    #return dictionary with pathway ID: common name as key:value pairs
    #print pathWays
    return pathWays

# this function pulls all geneIDs associated with the pathwayID passed into it
def genesFromPathway(pathwayID):
    resp  = requests.get("http://ecocyc.org/apixml?fn=genes-of-pathway&id=ECOLI:{}".format(pathwayID))
    root = ET.fromstring(resp.text)
    #print(resp.text)
    genes = root.findall("./Gene")
    genesDict = {}
    for gene in genes:
        geneID = gene.attrib['frameid']
        geneName = gene.findall("common-name")[0].text
        #print "Gene: " + geneName + ", GeneID: " + geneID
        #page = requests.get("http://biocyc.org/gene?orgid=ECOLI&id=EG11879")
        genesDict[geneID] = geneName
    return genesDict
# this function pulls the promoterIDs associated with the geneID passed into it
def getPromoter(geneID):
    resp  = requests.get("http://ecocyc.org/apixml?fn=transcription-units-of-gene&id=ECOLI:{}".format(geneID))
    root=ET.fromstring(resp.text)
    #print(resp.text)
    promoters=root.findall("./Transcription-Unit/component/Promoter")
    #print promoters
    for promoter in promoters:
        pID = promoter.attrib['frameid']
        absPositPlusOne = promoter.find('absolute-plus-1-pos').text
        #regulon = ecoli.containing_chromosome(pID)
        print "promoter: ",pID
        print absPositPlusOne
        #print(regulon)

#ecoli = pc.select_organism("ECOLI")
allPathways = pathwayFromCompound("HIS")
#genesFromPathway("HISTSYN-PWY")

for pathway in allPathways:
    print allPathways[pathway]
    userPath = raw_input("Do you want to knockdown this function? yes or no.")
    if userPath == "yes":
        genes = genesFromPathway(pathway)
        for gene in genes:
            print genes[gene], gene
            getPromoter(gene)
        break
    else:
        continue


# In[ ]:



