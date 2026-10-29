# GARDAVU 1.0.3 — Pondération des médecins

Dans **Médecins et absences**, sélectionner une ligne puis cliquer sur
**Pondérer le médecin**. Saisir `2` pour ×2, `3` pour ×3, ou une valeur décimale
positive comme `0,5`, puis enregistrer. La fiche **Modifier** propose le même champ.

Le moteur utilise les pondérations proportionnellement à chaque date : ×2 compte
pour deux parts par rapport à ×1. Il applique cette répartition au total, aux
mois et aux catégories. Un cas simple à neuf gardes donne six gardes au médecin
à ×2 et trois à celui à ×1, lorsque les contraintes le permettent.

Les indisponibilités, participations, espacement, maximums individuels,
verrouillages et rotation des fêtes restent respectés. Le médecin conserve son
identifiant et son historique ; aucune fiche artificielle supplémentaire n'est
créée. Les cibles et leurs écarts restent visibles si une contrainte empêche le
rapport exact entre nombres de gardes.

La pondération apparaît dans la liste des médecins, les besoins théoriques,
les statistiques et la feuille **Équité** de l'export Excel.
Après modification, générer ou régénérer le planning. Les affectations d'un
brouillon existant ne sont pas changées sans calcul ; sa précédente preuve
d'optimalité n'est plus présentée comme valable et une indication de régénération
est affichée. Les versions validées conservent la pondération utilisée à leur
validation. Les projets existants restent compatibles : le coefficient déjà
enregistré est réutilisé, sans changement de schéma ni réinitialisation.

Le coefficient n'est pas daté dans les fiches. Comme pour toute déclaration de
couverture historique complète, vérifier les coefficients de la période avant
d'activer une compensation récente. Si l'ancienne pondération était différente,
ne pas attester cette fenêtre comme complète avec le coefficient actuel ;
la rotation des fêtes et l'espacement utilisent toujours les gardes connues.

La livraison est dans `dist/v1.0.3/`, avec l'icône de menottes.
Les tests dédiés sont dans `tests/test_weights.py`, et la recette du binaire
dans `artifacts/recette-v1-0-3/rapport.json`.

## Vérifications exécutées

- Suite complète : **54 tests réussis en 28,62 secondes**,
  rapport `artifacts/pytest-v1-0-3.xml`. Exécution hors du bac à sable après des
  erreurs intermittentes de lecture de fichiers Tcl/Tk existants dans celui-ci ;
  aucun contournement de contrôle métier ni modification de l'installation Python.
- Vérifications de ×2 et ×3, cibles par mois et catégorie, suspensions,
  unicité du médecin, espacement et rejet des valeurs nulles, négatives ou non finies.
- Enregistrement depuis le bouton, réouverture du projet, indication de
  régénération et conservation des affectations du brouillon en attendant.
- Export Excel : pondération numérique et cibles/attributions ; une version
  validée conserve ses valeurs après modification ultérieure de la fiche.
  Les feuilles du cas fictif ont été rendues pour inspection visuelle.
- Cas de six mois avec 30 médecins dont un à ×2 : **211 affectations conformes**,
  13 pour le médecin pondéré, six ou sept pour les autres. Cibles respectives :
  13,613 et 6,806. Durée mesurée : 23,094 secondes, statut FEASIBLE ; l'optimalité
  de l'ensemble des objectifs n'est pas démontrée.
  Rapport : `artifacts/benchmark-ponderation/benchmark.json`.
- Recette directe du binaire : succès avec runtime embarqué, interface,
  32 affectations, sauvegarde, copie, réouverture et exports.
