# GARDAVU 1.1.0 — Interface et mode sombre

La navigation latérale présente les sept étapes du travail et l'état du projet.
La page affiche son titre, son explication et des actions plus espacées. Les
commandes principales sont mises en évidence et les barres de boutons passent
à la ligne quand la largeur disponible diminue.

## Utilisation

- **Apparence → Clair / Sombre**, en haut à droite : changement immédiat,
  mémorisé dans le fichier `.gardavu` et retrouvé à sa réouverture. Les saisies
  en cours restent présentes. Aucune préférence dans AppData ou le registre.
- Recherche des médecins par nom, identifiant ou alias, avec compteur des
  résultats. Les identifiants restent stables après filtrage et tri.
- Tri des tableaux par leurs en-têtes, notamment des pondérations numériques.
  Lignes alternées et mise en évidence des éléments à configurer ou non affectés.
- Formulaires défilants, avec **Enregistrer** et **Annuler** accessibles en bas.
- Calendrier mensuel défilant, mois précédent/suivant et détail d'une date.
- Aide intégrée dans **Autres actions**, également accessible par F1.
  Ctrl+N : nouveau projet ; Ctrl+O : ouvrir ; Ctrl+S : sauvegarder une copie.

Les confirmations, messages, assistants d'import et formulaires suivent le
thème. Les sélecteurs de fichiers natifs restent gérés par Windows et suivent
son apparence. Aucun réglage du système n'est modifié.

Les règles de calcul, pondérations, horaires et historiques restent ceux du
projet. Le changement de thème enregistre uniquement une préférence dans ses
métadonnées. Les anciens projets sont ouverts sans changement de schéma.

## Vérifications exécutées

- **60 tests réussis, aucun échec ni scénario ignoré**. Bilan et journaux :
  `artifacts/tests-20261029-094419-1ed773/summary.json`.
  La suite couvre les règles métier, les imports/exports, la persistance, les
  boutons de configuration et de pondération, la navigation, la recherche,
  le tri numérique, le contraste des palettes, la conservation des saisies
  pendant le basculement et les réponses explicites aux confirmations sombres.
- Chaque scénario d'interface s'exécute une seule fois dans son propre processus
  avec un seul interpréteur Tk, via `scripts/run_tests.py`. Cette organisation
  évite les réinitialisations successives de Tk sous Windows. Aucun réessai ni
  masquage d'erreur n'est effectué.
- Inspection visuelle native Windows sur une **copie fictive** : planning et
  calendrier en clair et sombre, navigation, passage à la ligne des commandes
  dans une fenêtre plus étroite, fiche médecin défilante et boutons fixes.
  Aucun projet réel n'a été utilisé pour cette recette.
- Compilation syntaxique Python et contrôle syntaxique du script PowerShell.
- Recette directe de l'exécutable autonome : démarrage Tk, basculement sombre
  puis clair, mémorisation des préférences et maintien des 32 lignes du planning.
  Génération de **32 affectations**, validation indépendante, sauvegarde,
  réouverture d'une copie et exports Excel/CSV réussis.
  Rapport : `artifacts/recette-v1-1-0-finale/rapport.json`.

La livraison portable est dans `dist/v1.1.0/`. Le runtime Python et les images
de l'interface sont embarqués ; les données réelles ne sont pas incluses dans
l'exécutable ni dans les archives de distribution.
