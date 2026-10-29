# GARDAVU 1.0.2 — Icône de menottes

La plume par défaut de Tkinter est remplacée par une paire de menottes.
La même icône est utilisée pour le fichier exécutable Windows et comme icône
par défaut de la fenêtre et de ses boîtes de dialogue.

Le dessin source est `gardavu/assets/gardavu.svg`. Le fichier `.ico` contient
les résolutions 16, 24, 32, 48, 64, 128 et 256 pixels avec transparence.
Le script `scripts/build_icon.ps1` les reconstruit avec System.Drawing,
sans service réseau ni nouvelle dépendance d'exécution. La construction Windows
inclut cette étape et embarque l'icône dans le binaire.

La version est livrée dans `dist/v1.0.2/`. Fermer l'ancienne application,
lancer le nouvel exécutable puis ouvrir le projet `.gardavu` existant.
Aucune donnée de projet n'est modifiée par cette mise à jour.

Vérifications : quatre tests de l'interface réussis, chargement de l'icône par
Tkinter, contrôle des tailles ICO et des ressources d'icône de l'exécutable.
La recette du binaire est conservée dans `artifacts/recette-v1-0-2/rapport.json`.
