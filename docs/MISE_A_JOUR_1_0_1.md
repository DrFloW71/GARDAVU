# GARDAVU 1.0.1 — Configuration des créneaux

Dans **Créneaux et règles**, sélectionner la ligne `soir`, puis :

- cliquer sur **Configurer le créneau** ;
- ou double-cliquer sur la ligne ;
- ou faire un clic droit puis **Configurer le créneau…**.

Renseigner **Début**, **Fin** et **Effectif**, puis cliquer sur **Enregistrer**.
Minuit en fin de garde peut être saisi `24:00`.
Les horaires doivent être ceux décidés par le groupe ; aucun n'est imposé par cette mise à jour.

La commande de configuration modifie la version sélectionnée à la date d'effet
affichée. La configuration initiale ne crée plus une seconde version laissant
l'ancienne ligne sans horaires. Pour un changement applicable seulement à une
nouvelle date, utiliser **Nouvelle version d'un modèle**, qui reste disponible
aussi au clic droit. Les gardes historiques gardent leurs horaires enregistrés.

Les commandes sont réparties sur deux lignes pour rester accessibles sur une
fenêtre étroite. Un clic droit sélectionne la ligne visée, indépendamment de la
sélection précédente ; un clic dans la zone vide ne configure aucune autre ligne.

La version précédente proposait la saisie sous **Nouvelle version d'un modèle**,
sans bouton de configuration explicite, double-clic ou menu au clic droit.

## Installation et vérifications

La livraison est dans `dist/v1.0.1/`. Fermer l'ancienne application, lancer le nouvel
exécutable puis ouvrir le fichier `.gardavu` existant avec **Ouvrir**.
Le format du projet reste compatible ; aucun projet utilisateur n'a été modifié
pendant la construction de cette mise à jour.

Suite complète : **44 tests réussis**, rapport `artifacts/pytest-v1-0-1.xml`.
Les nouveaux contrôles vérifient l'enregistrement effectif des premiers horaires,
la génération correspondante, la création distincte d'une version datée, et la
sélection du bon modèle au double-clic et au clic droit.
Recette du binaire : `artifacts/recette-v1-0-1/rapport.json`.
