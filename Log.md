# Log

## 01/07/2024 (lundi) - Premier jour
- Présentation du sujet par Lucio
- Présentation de la méthode des éléments spectraux
- Présentation de GMSH
- Découverte de l'API Python de GMSH
- Création d'un premier code Python pour générer un maillage de barrage simple
### Remarques
- `barrage_simple.py`: Le code Python permet de créer un modèle 3D de barrage, mais il n'est pas correctement maillé.
- `barrage_simple2.py`: Le code Python permet de créer un maillage héxa mais il n'est pas conforme et est incompatible avec la méthode des éléments spectraux.
- `barrage_simple3.py`: Le maillage est conforme mais les groupes physiques ne sont pas correctement définis.

## 02/07/2024 (mardi) - Deuxième jour
- Finitions sur le code `barrage_simple3.py`
- Séminaire sur l'IA dans la simulation mécanique
- Début du travail sur un maillage de barrage plus complexe (inclinaison des parois)

## 03/07/2024 (mercredi) - Troisième jour
- Finalisation du code de `barrage.py` et travail sur l'API.
- Découverte de l'accès au calculateur de AMU (Copernicus).
- Lancement du premier calcul sur le maillage de `barrage.py`. (4h 32p)
- Configuration de l'environnement de travail sur le serveur de l'AMU.

## 04/07/2024 (jeudi) - Quatrième jour
- Découverte des résultats du calcul sur le maillage de `barrage.py`. (50% des itérations du calcul réalisées)
- Premier lancement de ParaView pour visualiser les résultats.
- Le calcul n'étant pas terminé, le code a été relancé à partir du point d'arrêt. (5h 32p)
- Traduction d'un code MATLAB en Python pour la création automatique de matériaux.

## 05/07/2024 (vendredi) - Cinquième jour
- Découverte deuxième partie des résultats du calcul sur le maillage de `barrage.py`. (100% des itérations du calcul réalisées)
- Visualisation des résultats avec ParaView.
- Début d'un nouveau maillage plus optimisé.
- Maillage `barrage2.py` terminé : ~10 000 éléments, PMLs, groupes physiques corrects.
### Remarques
- Le maillage actuel comporte 170 000 hexaèdres. L'objectif à terme serait d'avoisiner les 30 000 hexaèdres en se focalisation sur les zones intéressantes.
- Certains éléments de la partie supérieure du mur sont excessivement petits et augmentent inutilement les temps de calcul.
- Réduire le nombre d'éléments peut se faire en réduisant la taille des listes `elements` du code Python.

## 08/07/2024 (lundi) - Sixième jour
- Accès au serveur de Visualisation et test de Paraview.
- Découverte de l'API Python de Paraview.
- Lancement d'un calcul sur le maillage `barrage.py` avec l'eau sans PML (5s ~4h)

## 09/07/2024 (mardi) - Septième jour
- Découverte des résultats du calcul sur le maillage de `barrage.py` avec l'eau sans PML.
- Découverte d'une erreur dans le maillage. Erreur corrigée, lancement d'un nouveau calcul.
