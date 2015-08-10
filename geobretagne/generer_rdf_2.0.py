# -*- coding:Utf-8 -*-

# génération du thesaurus GéoBretagne à partir de la liste des termes

import shutil
import os
import os.path
import codecs

# les variables
rep_home = "D:/metadonnees/thesaurus/generer_th_bzh"
url_racine = "http://www.geobretagne.fr/thesaurus/"
url_thmanager = "http://www.geobretagne.fr/thesaurus"

# les variables pour créer le xml

xml_debut = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
xml_debut += "<!-- \n"
xml_debut += "  Thesaurus GéoBretagne\n"
xml_debut += "  version 2.0 du 13/01/2014\n"
xml_debut += "-->\n"
xml_debut += "<rdf:RDF\n"
xml_debut += "    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" \n"
xml_debut += "    xmlns:skos=\"http://www.w3.org/2004/02/skos/core#\" >\n"
xml_debut += "  <rdf:Description rdf:about=\"" + url_thmanager + "\">\n"
xml_debut += "    <rdf:type rdf:resource=\"http://www.w3.org/2004/02/skos/core#ConceptScheme\"/>\n"

xml_fin = "</rdf:RDF>\n"

xml = ""
xml_topConcept = ""


# ouverture des fichiers
f_termes = open( rep_home + "/liste_termes.txt",'r')
f_rdf = open( rep_home + "/geobretagne.rdf.xml.skos.xml",'w')

# on commence l'écriture du fichier rdf
f_rdf.write( codecs.BOM_UTF8 )


# boucle sur les termes
for line in f_termes:
	
	ligne = line[0:-1]
	a = ligne.split("|")
	#print a

	terme = a[0]
	#print terme

	terme_url = terme

	# les accents
	terme_url = terme_url.replace("à","a")
	terme_url = terme_url.replace("â","a")  
	terme_url = terme_url.replace("é","e")
	terme_url = terme_url.replace("è","e")
	terme_url = terme_url.replace("ê","e")
	terme_url = terme_url.replace("ë","e")
	terme_url = terme_url.replace("î","i")
	terme_url = terme_url.replace("ï","i")
	terme_url = terme_url.replace("ô","o")
	
	terme_url = terme_url.replace("'","_")
	terme_url = terme_url.replace("’","_")
	terme_url = terme_url.replace(" ","_")
	terme_url = terme_url.replace(" ","_")
	terme_url = terme_url.replace(" ","_")
	terme_url = terme_url.replace("_:_","/")

	# la défintion du terme
	definition = a[1].replace("#","\n")
	#definition = ""

	#-----------------------------

	xml_topConcept += "    <skos:hasTopConcept rdf:resource=\"" + url_racine + terme_url + "/\"/>\n"
	
	xml += "  <rdf:Description rdf:about=\"" + url_racine + terme_url + "/\">\n"
	xml += "    <skos:prefLabel xml:lang=\"fr\">" + terme + "</skos:prefLabel>\n"
	xml += "    <skos:scopeNote xml:lang=\"fr\">" + definition + "</skos:scopeNote>\n"
	xml += "    <rdf:type rdf:resource=\"http://www.w3.org/2004/02/skos/core#Concept\"/>\n"
	xml += "    <skos:inScheme rdf:resource=\"" + url_thmanager + "\"/>\n"
	xml += "  </rdf:Description>\n"
	

# fin de la boucle

# on écrit dans le fichier
f_rdf.write( xml_debut )
f_rdf.write( xml_topConcept )
f_rdf.write( "  </rdf:Description>\n" )
f_rdf.write( xml )
f_rdf.write( xml_fin )

# fermeture des fichiers
f_rdf.close()
f_termes.close()

print "fini"
