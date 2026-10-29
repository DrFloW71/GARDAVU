# Rapport de recette — 29 octobre 2026

## Environnement et livraison

Construction native sur Windows 11 x64 (10.0.26300), Python 3.12.10, Tk 8.6,
OR-Tools 9.15.6755, openpyxl 3.1.5, PyInstaller 6.16.0.
Versions transitives : `requirements-lock.txt`. Licences : `licenses/manifest.json`.
Le fichier `dist/GARDAVU.exe` est un véritable exécutable Windows construit avec
PyInstaller, avec les DLL et Python embarqués. Taille et empreintes exactes dans
`dist/distribution.json` ; environ 54 Mio pour l'exécutable (à vérifier dans le manifeste).
Le ZIP contient logiciel, documentation, licences et modèles, sans données de projet.

## Vérifications exécutées

Commande finale, dans le dépôt :

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=artifacts\pytest-tmp-distribution --junitxml=artifacts\pytest-final.xml --durations=5
```

**42 tests réussis en 26,53 secondes.** Le rapport XML fait foi. Le dossier temporaire
a été placé explicitement dans le dépôt : un essai intermédiaire avait échoué
pendant la création des dossiers temporaires du bac à sable Windows, avant les
tests concernés. Le nouvel emplacement a permis d'exécuter toute la suite.
La compilation syntaxique `compileall` a aussi été exécutée sur les sources.

| Critère demandé | Preuve exécutée |
|---|---|
| 30 médecins, six mois | `test_six_months_30_doctors`, benchmarks JSON |
| 4 semaines = 32 affectations, 28 × 1 et 2 × 2 | calendrier et `test_homogeneous_32_assignments` |
| Horaires absents / espacement non confirmé | `test_missing_hours_and_confirmation` |
| Suspension, retour sans dette, arrivée, départ | `test_participation_absences_and_return` |
| Coefficients et absence ponctuelle sans diminution de cible | `test_weighted_targets_no_punctual_discount` |
| Cibles entières sans perte d'arrondi | `test_largest_remainders_conserve_sum` |
| Diversité, seuil proportionnel et catégories | `test_weekday_threshold_and_categories`, test exhaustif de catégories |
| Frontières jeudi/mardi et garde future connue | `test_history_boundary_before_and_after` |
| Noël deux ans avant, jour/nuit, STRICT impossible | `test_christmas_rotation_and_strict_impossibility` |
| Priorité à l'occurrence la plus ancienne | `test_oldest_known_holiday_preferred` |
| Historique incomplet / couverture non inférée | tests de couverture et avertissements des recettes |
| Compensation récente sans dette du nouvel arrivant | `test_complete_recent_history_compensates_without_newcomer_debt` |
| Samedi/dimanche férié, collision de fêtes | `test_holiday_collision_and_weekend` |
| Minuit, bissextile, années, milieux de mois | tests du calendrier |
| Modèles datés, exceptions | `test_exceptions_and_effective_versions` |
| Réimport sans doublon, accent, homonymes | tests d'import et de rapprochement |
| Tableaux et lignes, horaires inconnus | tests matrix, formats et réimport de l'export |
| Conflits : choix explicite, remplacement effectif unique | tests d'import et versions |
| Échanges / modifications invalides visibles et non validables | validation indépendante et test d'interface |
| Verrous contradictoires / doubles postes / effectif | tests de contraintes et réparation |
| Annulation avant et après solution, UNKNOWN | tests cancellation et timeout |
| Petits optimums vérifiés par énumération exhaustive | charge globale et catégories |
| Sauvegarde, restauration, réouverture, transaction | tests storage et recette du binaire |
| Chemins avec espaces et accents | tests storage et recette `Recette éç.gardavu` |
| Copie transportable du projet | copie puis ouverture vers un autre chemin |
| Formules refusées / exports protégés | tests formules, Excel et CSV |
| Statistiques historiques figées après changement de coefficient | `test_validated_statistics_frozen_when_doctor_changes` |
| Vue mensuelle, filtres, aperçu d'import | `test_ui_project_plan_filter_and_import_preview` |

## Mesures sur un semestre

Période : 01/11/2026–30/04/2027 inclus. 30 médecins fictifs, même coefficient,
espacement sept jours, deux médecins distincts les dimanches et fériés.
Horaires **fictifs de test** : semaine 19 h–minuit. Un travailleur, graine 42,
budget 30 secondes.

- 211 créneaux et 211 affectations nécessaires ; toutes couvertes.
- Totaux : 29 médecins à sept gardes, un à huit ; écart maximal d'une garde.
- Sans historique : environ 23,22 secondes, rapport
  `artifacts/benchmark-ameliore/benchmark.json`.
- Avec 4 272 gardes fictives de 2016–2025 : **23,172 secondes**, rapport final
  `artifacts/benchmark-historique-release/benchmark.json`.
- Aucun contrôle impératif en échec, aucune répétition de fête dans ce dernier cas.
- Rotation des fêtes et charge globale : optimum prouvé sur le cas avec historique.
- Catégories, charge mensuelle, diversité : solutions FEASIBLE, optimalité non démontrée.
- Régularité par quinzaine : optimum prouvé sous les bornes précédemment trouvées.
- Statut de l'ensemble : **FEASIBLE**, conformément à cette limite de preuve.

Un essai initial avec historique dépassait le budget pendant la préparation.
Le parcours a été corrigé (dates mises en cache, historique indexé par médecin,
recherche de fêtes évitée pour les créneaux sans fête). La mesure ci-dessus est
celle effectuée après correction. Les résultats ne sont pas une garantie de
temps ou d'optimalité sur toutes les indisponibilités réelles.

## Recette de l'exécutable

Exécutée directement avec `dist/GARDAVU.exe --self-test <dossier neuf>`.
`artifacts/recette-livraison/rapport.json` confirme :

- `frozen: true`, runtime Python embarqué ;
- Tkinter ouvert et fermé correctement ;
- 32 affectations conformes en février 2027 ;
- enregistrement et validation dans un projet SQLite ;
- copie cohérente puis réouverture avec 32 gardes effectives ;
- exports Excel et CSV ;
- application graphique chargée avec les 32 lignes du planning.

La première construction avait une DLL MSVC partagée entre NumPy/pandas introuvable
au premier import. Le hook de chargement des DLL a corrigé ce défaut et la recette
du binaire a ensuite réussi. Le binaire final a été reconstruit après les corrections.
L'écran initial du binaire a également été contrôlé visuellement via Computer Use.
Les quatre feuilles d'un export fictif ont été rendues et inspectées ; cellules
typées, filtres et identifiants de réimportation sont aussi contrôlés par les tests.

## Limites de validation restantes

- Aucun second ordinateur ni machine Windows vierge de Python/Excel disponible :
  le test sur une autre machine reste à effectuer. Une copie sur un autre chemin
  et l'exécution autonome du binaire local ne constituent pas cette preuve.
- La recette visuelle ne remplace pas une utilisation complète par le coordonnateur
  sur ses vrais fichiers. Aucun import réel du groupe n'a été testé.
- Aucune signature éditeur, ni test de réputation Windows ou distribution publique.
- Les dates et catégories passent les tests définis ; aucune règle professionnelle
  ou réglementaire non fournie n'est inventée. L'espacement est organisationnel.
- Les optimisations secondaires ne sont pas toutes prouvées optimales au budget
  mesuré. Augmenter le temps ne garantit pas une preuve d'optimalité.
- Pas de validation de calendriers graphiques arbitraires, `.xls`, régionaux
  automatiques ou de coefficients historiques variables dans le temps.
- Seul le schéma initial est actuellement déployé ; les versions futures inconnues
  sont refusées. Aucun scénario de migration d'une ancienne version distribuée
  n'existe encore à tester.
