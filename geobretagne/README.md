10/08/2015
Maël REBOUX - Rennes Métropole pour le pôle métier INSPIRE de GéoBretagne

Ce script python permet de générer le thesaurus GéoBretagne v 2.x à partir de la liste des termes (liste_termes.txt).

La liste des termes et leur définition est accessible ici : http://kartenn.region-bretagne.fr/wiki/doku.php?id=pole_catalogage:thesaurus_geobretagne

Pour pouvoir être utilisable dans GeoNetwork, un thesaurus doit être au format RDF / SKOS.
Le seul logiciel libre connu disposant d'une interface graphique permettant de générer ou manipuler un tel format est thManager.

Après avoir générer le fichier RDF il convient donc de le charger dans thManager pour le valider. Très important, surtout si le thesaurus est hiérarchisé / hiérarchique. Ce qui n'est pas le cas du thesaurus GéoBretagne.

Ne pas oublier de surcharger le fichier produit avec les infos de version. thManager ne sait pas les lire mais GeoNetwork oui : elles apparaissent devant les mot-clés dans l'interface lors de la consultation d'une métadonnée.


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

<?xml version="1.0" encoding="UTF-8"?>
<!-- 
  Thesaurus GéoBretagne
  version 2.0 du 13/01/2014
-->
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:dcterms="http://purl.org/dc/terms/" >
  <skos:ConceptScheme rdf:about="http://www.geobretagne.fr/thesaurus">
    <dc:title>GéoBretagne v 2.0</dc:title>
    <dc:description>Thesaurus de la nomenclature thématique de GéoBretagne pour GeoNetwork.</dc:description>
    <dc:creator>
      <foaf:Organization>
        <foaf:name>GéoBretagne</foaf:name>
      </foaf:Organization>
    </dc:creator>
    <dcterms:issued>2014-01-13</dcterms:issued>
    <dcterms:modified>2014-01-13</dcterms:modified>
  </skos:ConceptScheme>

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++