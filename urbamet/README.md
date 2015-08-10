10/08/2015
Maël REBOUX - Rennes Métropole pour le pôle métier INSPIRE de GéoBretagne

URBAMET est un thesaurus est très connu des urbanistes mais nous n’avons jamais pu gérer ses mots-clés dans nos catalogue car il n’existe pas de version RDF/ SKOS disponible.

J’ai réussi à récupérer auprès du Ministère de l’écologie un export en XML du thesaurus URBAMET.
http://notx.documentation.developpement-durable.gouv.fr/Urbanisme/thesaurus/navigation.xhtml 

Le jeu est de traiter ce fichier pour créer un fichier XML RDF / SKOS.


J’ai à peu près réussi mais il reste à traiter la hiérarchie entre les termes pour que ce soit opérationnel.
Pour ceux à qui ça parle, il s’agit des descripteur narrower et broader. C’est obligatoire pour avoir un fichier SKOS valide.
Je me sers de thmanager pour valider. J’ai procédé ainsi pour le thesaurus de GéoBretagne (non hiérarchique) et mes 2 thésaurus internes (dont 1 hiérarchique).

Et là je ne sais pas trop comment m’y prendre en terme de méthodologie donc j’appelle à l’aide !

Je pense qu’il faut faire en 3 étapes. La première est faite cf le script python et les résultats.
La 2e consisterait à reparcourir tous les concepts / mot-clés et à établir les relations parents-enfants.
La 3e consisterait à refaire un parcours pour déterminer les relations de voisinage (termes au même niveau / sous le même terme).

