# GARDAVU 1.1.5 — Détail du médecin sélectionné

Le bouton de détail écrivait son résultat dans un panneau sous le tableau,
qui pouvait être complètement masqué à petite hauteur de fenêtre. Le défaut
a été reproduit à 1040 × 720 : contenu présent, panneau invisible, aucune
fenêtre de détail. Rapport : `artifacts/diagnostic-detail-equite/rapport.json`.

Le clic ouvre désormais une fenêtre dédiée, défilante et adaptée au thème.
Elle affiche le médecin sélectionné, la période, l'état du planning, la
pondération, les gardes mensuelles, la cible et les fêtes. Une sélection absente
ou multiple donne une consigne explicite. Les versions validées conservent
leurs valeurs de validation.

La livraison portable est dans `dist/v1.1.5/`.

Vérifications : **sept tests ciblés réussis**, dont cinq régressions sur ce
bouton (clair/sombre, absence de sélection, sélection multiple et fenêtre
réelle à 1040 × 720). Le détail conserve les valeurs de validation quand la
fiche actuelle a changé. Les deux contrôles complémentaires couvrent l'export
d'équité validée et le parcours interface/planning/import.
Bilan du bouton : `artifacts/tests-detail-equite-v1-1-5/summary.json`.
Recette de l'exécutable : `artifacts/recette-v1-1-5/rapport.json`.
