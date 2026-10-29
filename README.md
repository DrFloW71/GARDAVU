# GARDAVU

Application Windows x64 locale pour répartir les gardes d'un groupe de médecins.
Interface française Tkinter, optimisation OR-Tools CP-SAT, projet SQLite `.gardavu`.
Aucun compte, réseau ou service système à l'exécution. Aucune donnée de patient.

Créé par le **Dr Florian Ronez**. Toute utilisation, même à titre gratuit, est
soumise à son autorisation préalable, expresse et écrite, et reste limitée à
des fins non commerciales. Voir [la licence d'utilisation](LICENSE).
Les composants tiers conservent leurs licences respectives.

## Utiliser la version portable

Décompresser `dist/GARDAVU-portable.zip` dans le dossier de votre choix, puis ouvrir
`GARDAVU.exe`. Python et Excel ne sont pas nécessaires sur le poste destinataire.
Choisir **Nouveau projet** et un emplacement inscriptible pour le fichier `.gardavu`.
Le logiciel ne choisit pas silencieusement AppData ou le registre.

1. Saisir ou importer les médecins et leurs participations.
2. Renseigner les suspensions neutralisantes et les indisponibilités ponctuelles.
3. Importer l'historique disponible avec aperçu et rapprochement explicite.
4. Dans **Créneaux et règles**, configurer le modèle `soir` (horaires non présumés)
   et confirmer l'espacement minimal proposé de sept jours.
5. Choisir les dates incluses, vérifier besoins et cibles, puis générer.
6. Examiner planning, équité, diagnostics et éventuelles répétitions de fêtes.
7. Modifier/verrouiller si nécessaire, valider puis exporter.

Voir [le guide](docs/GUIDE_UTILISATEUR.md), [le modèle d'équité](docs/EQUITE.md),
[les hypothèses](docs/HYPOTHESES.md) et [la recette](docs/RECETTE.md).

Depuis la version 1.1.0, les étapes sont accessibles dans la barre latérale.
Le sélecteur **Apparence → Clair / Sombre**, en haut à droite, change le thème
immédiatement et mémorise ce choix dans le projet. Les tableaux sont triables
par leurs en-têtes, la liste des médecins dispose d'une recherche et les fiches
longues défilent avec **Enregistrer** et **Annuler** toujours accessibles.
Voir [les nouveautés 1.1.0](docs/MISE_A_JOUR_1_1_0.md).

**Partager le logiciel** : transmettre l'archive portable avec ses notices.
**Partager aussi les données** : transmettre volontairement une sauvegarde du
projet obtenue avec **Sauvegarder**, dans le dossier `<nom du projet>_sauvegardes`.
L'exécutable seul ne contient
jamais les données enregistrées après sa distribution. Un projet n'est pas chiffré.
Le verrou d'écriture ne remplace pas un serveur : ne pas utiliser un projet dans
un dossier cloud synchronisé pendant son ouverture.

## Modèles d'import

Les modèles `.xlsx` sont dans `templates/` et peuvent être régénérés depuis l'interface.
Leur ligne fictive d'exemple doit être supprimée avant saisie réelle.

## Développement et construction Windows

Python 3.12 x64 avec Tkinter est requis pour développer. Les versions effectivement
installées sont figées dans `requirements-lock.txt`. Les textes de licences sont
dans `licenses/`, avec synthèse dans `THIRD_PARTY_NOTICES.md`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m gardavu
.\.venv\Scripts\python.exe scripts\run_tests.py
.\build_windows.ps1
```

Si ensurepip est indisponible, `uv venv --python 3.12 .venv`, puis
`uv pip sync --python .venv\Scripts\python.exe --cache-dir .build-cache requirements-lock.txt`.
`build_windows.ps1` arrête la construction si les tests échouent. Le `.spec`
construit un véritable exécutable Windows avec son environnement embarqué.
La taille et le SHA-256 réels sont dans `dist/distribution.json`.
Le lanceur de tests exécute les scénarios d'interface dans des processus distincts,
avec un seul interpréteur Tk par processus comme l'application. Il ne réessaie ni
ne masque les échecs ; les journaux et le bilan JSON sont dans `artifacts/tests-*`.

```powershell
.\dist\GARDAVU.exe --self-test 'C:\chemin\vers\un dossier de recette neuf'
```

Cette recette fictive écrit `rapport.json`, un projet, une copie et deux exports.
Elle ne doit pas être lancée dans un dossier de données réelles.

## Organisation

`domain` : entités ; `calendar` : fêtes et créneaux ; `targets` : cibles/statistiques ;
`solver` : contraintes et objectifs ; `validation` : contrôle indépendant ;
`storage` : SQLite, versions et sauvegardes ; `imports` / `exports` : Excel/CSV ;
`ui` : interface ; `tests` : tests de métier et de persistance.

Les statuts FEASIBLE et UNKNOWN ne sont jamais présentés comme une preuve
d'optimalité ou d'impossibilité. L'application ne modifie aucune règle impérative
pour obtenir une solution. Les limites de validation restantes sont indiquées
dans le rapport de recette.
