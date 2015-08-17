﻿# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#
# Author:      Maël REBOUX, François Van der Biest
#
# Created:     17/08/2015
# Licence:     GNU GPL


# docs :
#       http://www.diveintopython3.net/xml.html
#       https://wiki.python.org/moin/Tutorials%20on%20XML%20processing%20with%20Python
#       http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree

#-------------------------------------------------------------------------------

import sys, os
import codecs
import xml.etree.ElementTree as etree
from array import array

rep_root = "."
fichier_xml_org = rep_root + "/fichier_org/test_commune.xml"
#fichier_xml_org = rep_root + "/fichier_org/donnees_thesaurus.xml"
fichier_rdf = rep_root + "/out/urbamet.rdf.skos.xml"

root_url = "http://notx.documentation.developpement-durable.gouv.fr/Urbanisme/thesaurus"

# tableau des TopConcept
TopConceptTab = []




def EcrireMotsCles(t):

    # load and parse
    tree = etree.ElementTree(file=fichier_xml_org)
    # root element  =  <resultset>
    root = tree.getroot()
    # on va à l'élélement enefant : <records>
    records = root[0]

    # compteur de mot-clé / concept
    iConcept = 0

    # boucle
    for record in records:
        #print record.tag, record.attrib
        # => record {'{http://www.w3.org/XML/1998/namespace}id': 'Urbanisme-0009532'}
        # pour <record xmlns:xlink="http://www.w3.org/1999/xlink" xml:id="Urbanisme-0009532">


        urbamet_id = ""
        hierarchie_brute = ""
        hierarchie_url = ""
        parent_hierarchie_url = ""
        label_fr = ""
        label_en = ""
        label_es = ""


        # maintenant on va boucler sur les mots-clés
        for urba_motcle in record:
            #print urba_motcle.tag, urba_motcle.attrib, urba_motcle.text
            #
            # on récupère l'ID du mot-clé
            if urba_motcle.tag == "CLE" : urbamet_id = urba_motcle.text

            # on récupère le mot-clé en langue FR
            if urba_motcle.tag == "DISPLAY" : label_fr = urba_motcle.text
            # on récupère le mot-clé en langue EN
            if urba_motcle.tag == "DE_ENG" : label_en = urba_motcle.text
            # on récupère le mot-clé en langue ES
            if urba_motcle.tag == "DE_ESP" : label_es = urba_motcle.text
            # la hierarchie
            if urba_motcle.tag == "HIERARCHIE": hierarchie_brute = urba_motcle.text

        # fin de la boucle sur chaque mot-clé pour récupérer les valeurs


        # on va maintenant traiter la hiérarchie pour créer l'url
        # on va passer de ça   :  <HIERARCHIE>différenciation sociale;sociologie;sciences humaines</HIERARCHIE>
        # à une url : /sciences_humaines/sociologie/différenciation_sociale

        if hierarchie_brute <> "" :
            # on fait un tableau avec les termes
            hierarchie_tab = hierarchie_brute.split(";")

            # on les lit en ordre inverse
            for concept in reversed(hierarchie_tab) :
                # on fait un ensemble de remplacement
                concept = unaccent(concept)
                hierarchie_url += concept + "/"

            for concept in list(reversed(hierarchie_tab))[0:-1] :
                # on fait un ensemble de remplacement
                concept = unaccent(concept)
                parent_hierarchie_url += concept + "/"

        if hierarchie_url == "" :
            # ça veut dire que l'on a potentiellement un TopConcept
            # donc on le rajoute au tableau
            TopConceptTab.append(label_fr)

        # maintenant on écrit le XML en RDF

        # on ouvre le fichier RDF en mode ajout
        f_rdf = codecs.open(fichier_rdf, 'a', 'utf-8')

        if hierarchie_url != "" :
            # les infos générales du mot-clé / concept
            # 1er tag contient l'url de hierarchie
            f_rdf.writelines(u"  <rdf:Description rdf:about=\"" + root_url + "/" + hierarchie_url + "\">\n")
            f_rdf.writelines(u"""    <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>\n""")
            f_rdf.writelines(u"    <skos:inScheme rdf:resource=\"" + root_url + "/\"/>\n")

            # FR
            f_rdf.writelines(u"    <skos:prefLabel xml:lang=\"fr\">" + label_fr + "</skos:prefLabel>\n")
            f_rdf.writelines(u"    <skos:scopeNote xml:lang=\"fr\">" + label_fr + "</skos:scopeNote>\n")

            # EN
            #f_rdf.writelines(u"    <skos:prefLabel xml:lang=\"en\">" + label_en + "</skos:prefLabel>\n")
            #f_rdf.writelines(u"    <skos:scopeNote xml:lang=\"en\">" + label_en + "</skos:scopeNote>\n")

            # ES
            #f_rdf.writelines(u"    <skos:prefLabel xml:lang=\"es\">" + label_es + "</skos:prefLabel>\n")
            #f_rdf.writelines(u"    <skos:scopeNote xml:lang=\"en\">" + label_es + "</skos:scopeNote>\n")

            f_rdf.writelines(u"    <skos:broader rdf:resource=\""+t["/"+hierarchie_url]["broader"]+"\" />\n")
            for n in t["/"+hierarchie_url]["narrower"]:
                f_rdf.writelines(u"    <skos:narrower rdf:resource=\""+n+"\" />\n")

            # write related
            if parent_hierarchie_url != "":
                for n in t["/"+parent_hierarchie_url]["narrower"]:
                    if n != root_url + "/" + hierarchie_url :
                        f_rdf.writelines(u"    <skos:related rdf:resource=\""+n+"\" />\n")

            # fin du concept
            f_rdf.writelines(u"  </rdf:Description>\n")

        # on ferme le fichier RDF
        f_rdf.close()

        # incrément du compteur
        iConcept += 1
        #print ""


    print str(iConcept) + " concepts traites"

    pass





def EcrireDebutFichierRDF():

    # on crée un nouveau fichier encodé en UTF-8
    f_rdf = codecs.open(fichier_rdf, 'w', 'utf-8')
    #
    f_rdf.writelines(u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f_rdf.writelines(u"""<!--
  Thesaurus URBAMET
  version 0.1 du 04/08/2015 créée par GéoBretagne
  basée sur la version XX du thesaurus original fourni par le Ministère de l'Écologie, du Développement durable et de l'Énergie

  http://www.urbamet.com/banque-de-donnees-urbamet-r9.html
  accès au thesaurus original en mode web : http://notx.documentation.developpement-durable.gouv.fr/Urbanisme/thesaurus/navigation.xhtml
-->
""")
    #
    # on écrit le début du SKOS
    f_rdf.writelines(u"""<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:dcterms="http://purl.org/dc/terms/" >
  <skos:ConceptScheme rdf:about="http://www.geobretagne.fr/thesaurus">
    <dc:title>URBAMET v 0.1</dc:title>
    <dc:description>Thesaurus URBAMET créé par GéoBretagne.</dc:description>
    <dc:creator>
      <foaf:Organization>
        <foaf:name>GéoBretagne</foaf:name>
      </foaf:Organization>
    </dc:creator>
    <dcterms:issued>2015-08-05</dcterms:issued>
    <dcterms:modified>2015-08-05</dcterms:modified>
  </skos:ConceptScheme>
""")

    # on ferme le fichier
    f_rdf.close()

    pass


def EcrireHierarchie():

    # on ouvre le fichier en mode ajout
    f_rdf = codecs.open(fichier_rdf, 'a', 'utf-8')

    # exemple
    str_ex = """
  <rdf:Description rdf:about="http://www.metropole.rennes.fr/thesaurus/sig/rm_services/rm.dgepib.di/">
    <skos:narrower rdf:resource="http://www.metropole.rennes.fr/thesaurus/sig/rm_services/rm.dgepib.di.moe/"/>
    <skos:narrower rdf:resource="http://www.metropole.rennes.fr/thesaurus/sig/rm_services/rm.dgepib.di.cop/"/>
    <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>
    <skos:scopeNote xml:lang="fr">Direction des Infrastructures (DI)</skos:scopeNote>
    <skos:inScheme rdf:resource="http://iaaa.unizar.es/thesaurus/rm_services"/>
    <skos:prefLabel xml:lang="fr">rm.dgepib.di</skos:prefLabel>
    <skos:broader rdf:resource="http://www.metropole.rennes.fr/thesaurus/sig/rm_services/rm.dgepib/"/>
  </rdf:Description>
"""
    f_rdf.writelines(u"  <!-- TODO : faire la hiérarchie -->\n")

    # les mot-clés de 1er niveau doivent être déclarés comme TopConcept
    TopConcept_ex = """
  <rdf:Description rdf:about="http://iaaa.unizar.es/thesaurus/rm_services">
    <skos:hasTopConcept rdf:resource="http://www.metropole.rennes.fr/thesaurus/sig/rm_services/rm.dgcult/"/>
    <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#ConceptScheme"/>
    <skos:hasTopConcept rdf:resource="http://www.metropole.rennes.fr/thesaurus/sig/rm_services/rm.dgfsi/"/>
    <skos:hasTopConcept rdf:resource="http://www.metropole.rennes.fr/thesaurus/sig/rm_services/vdr.dgs/"/>
  </rdf:Description>"""

    # fin
    #f_rdf.writelines(u"  </rdf:Description>\n")

    # on ferme le fichier
    f_rdf.close()

    pass


def EcrireTopConcepts() :

    # on ouvre le fichier en mode ajout
    f_rdf = codecs.open(fichier_rdf, 'a', 'utf-8')

    # début du descripteur
    f_rdf.writelines(u"  <!-- TopConcepts -->\n")
    f_rdf.writelines(u"  <rdf:Description rdf:about=\"" + root_url + "/" + "\">\n")

    iTopConcept = 0

    for TopConcept in TopConceptTab :
        if TopConcept <> "" :
            TopConcept = unaccent(TopConcept)
            f_rdf.writelines(u"    <skos:hasTopConcept rdf:resource=\"" + root_url + "/" + TopConcept + "/" + "\"/>\n")
            iTopConcept += 1

    # on ferme le descripteur
    f_rdf.writelines(u"  </rdf:Description>\n")

    # on ferme le fichier
    f_rdf.close()

    print str(iTopConcept) + u" TopConcept trouvés / traités"

    pass


def EcrireFinFichierRDF():

    # on écrit la fin du fichier
    f_rdf = codecs.open(fichier_rdf, 'a', 'utf-8')
    #
    f_rdf.writelines(u"</rdf:RDF>\n")
    f_rdf.close()

    pass



def unaccent(concept):
    concept = concept.replace(" ","_")
    concept = concept.replace("-","_")
    concept = concept.replace("'","_")
    concept = concept.replace("__","_")
    concept = concept.replace("___","_")
    concept = concept.replace(u"é","e")
    concept = concept.replace(u"è","e")
    concept = concept.replace(u"ê","e")
    concept = concept.replace(u"ë","e")
    concept = concept.replace(u"à","a")
    concept = concept.replace(u"â","a")
    concept = concept.replace(u"ù","u")
    concept = concept.replace(u"û","u")
    concept = concept.replace(u"ô","o")
    concept = concept.replace(u"î","i")
    concept = concept.replace(u"ï","i")
    return concept


def CreerStructHierarchie():
    #
    # on va lire une première fois le fichier XML pour en retirer uniquement les infos
    # de dépendance parents (broader) / enfant (narrower)

    # load and parse
    tree = etree.ElementTree(file=fichier_xml_org)
    root = tree.getroot()
    records = root[0]

    newtree = {}

    for record in records:

        hierarchie_brute = ""
        hierarchie_url = ""

        for urba_motcle in record:
            if urba_motcle.tag == "HIERARCHIE": hierarchie_brute = urba_motcle.text

        if hierarchie_brute <> "" :
            hierarchie_tab = hierarchie_brute.split(";")

            for concept in reversed(hierarchie_tab) :
                concept = unaccent(concept)
                hierarchie_url += concept + "/"

            r = list(reversed(hierarchie_tab))
            broader = '/' + unaccent('/'.join(r[0:-1])) + "/"

            if not newtree.has_key('/' + hierarchie_url):
                newtree['/' + hierarchie_url] = {
                    "broader": root_url + broader,
                    "narrower": [] # to be filled later
                }
            else:
                newtree['/' + hierarchie_url]["broader"] = root_url + broader

            if len(hierarchie_tab) > 1:
                # populate narrower records of parent nodes
                if newtree.has_key(broader):
                    newtree[broader]["narrower"].append(root_url + '/' + hierarchie_url)
                else:
                    newtree[broader] = {
                        "broader": "", # to be filled later
                        "narrower": [root_url + '/' + hierarchie_url]
                    }


    return newtree

#-------------------------------------------------------------------------------

def main():

    print ""
    print ""
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print ""
    print fichier_xml_org

    tree = CreerStructHierarchie()

    # écriture du début du fichier RDF
    print u"Ecriture du début du fichier RDF"
    EcrireDebutFichierRDF()

    EcrireMotsCles(tree)

    EcrireHierarchie()

    EcrireTopConcepts()

    # écriture de la fin du fichier RDF
    print u"Ecriture de la fin du fichier RDF"
    EcrireFinFichierRDF()

    pass

if __name__ == '__main__':
    main()



