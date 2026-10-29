# GARDAVU 1.1.2 — Sauvegarder

Le bouton **Sauvegarder** et le raccourci Ctrl+S créent directement une sauvegarde
datée dans le dossier `<nom du projet>_sauvegardes`, à côté du projet. Le chemin
de la sauvegarde s'affiche en bas de la fenêtre. Il n'y a plus de commande ni
de fenêtre de copie ; le projet ouvert reste le même.

Chaque sauvegarde utilise l'API SQLite de sauvegarde et passe un contrôle
d'intégrité. Les sauvegardes précédentes sont conservées.

La livraison portable est dans `dist/v1.1.2/`.

Vérifications exécutées : test ciblé de sauvegarde/restauration/réouverture
avec chemins accentués, puis contrôle du bouton et du raccourci sur un projet
de test. Deux sauvegardes distinctes ont été relues et leur intégrité contrôlée,
sans fenêtre de copie et en conservant le projet ouvert.
Rapport : `artifacts/recette-sauvegarde-v1-1-2/rapport.json`.
Recette de l'exécutable : `artifacts/recette-v1-1-2/rapport.json`.
