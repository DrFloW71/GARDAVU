# GARDAVU 1.1.4 — Menottes de la barre latérale

Le visuel au-dessus de GARDAVU est remplacé par une paire de menottes en acier
plus réaliste, sur fond transparent. Une source haute définition est réduite
avec interpolation bicubique de haute qualité, au lieu du sous-échantillonnage
sans lissage de l'ancien pictogramme. L'image intégrée mesure 88 × 66 pixels.

La source est `gardavu/assets/handcuffs-source.png` et l'image affichée est
`gardavu/assets/handcuffs-sidebar.png`. Le script
`scripts/build_sidebar_image.ps1` reconstruit cette dernière sans réseau ni
dépendance supplémentaire à l'exécution.

La livraison portable est dans `dist/v1.1.4/`.

Génération : outil ImageGen intégré, fond transparent. Le prompt final et les
fichiers résultants sont décrits dans `gardavu/assets/handcuffs-generation.md`.

Vérifications : inspection de la source et du rendu réduit, contrôle des
dimensions et de l'alpha (transparence et pixels de contours lissés), syntaxe
des scripts PowerShell, test ciblé de navigation et démarrage de l'interface.
La recette de l'exécutable est dans `artifacts/recette-v1-1-4/rapport.json`.
