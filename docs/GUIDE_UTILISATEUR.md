# Guide utilisateur

## Navigation et apparence

Les sept étapes restent accessibles dans la barre latérale. La page courante
est surlignée ; le bas de la barre indique le projet, l'effectif et l'état du
planning chargé. Les boutons du haut permettent de créer, ouvrir et sauvegarder
un projet. **Autres actions** regroupe la restauration et l'aide.

Choisir **Apparence → Sombre** ou **Clair** en haut à droite. Le changement
s'applique aussi aux formulaires, confirmations, imports et calendriers, sans
effacer les saisies en cours. Le choix est enregistré dans le fichier `.gardavu`
et revient à sa réouverture. Les fenêtres Windows de choix de fichier suivent
l'apparence du système ; GARDAVU ne modifie pas les réglages Windows.

- Cliquer sur un en-tête de tableau pour trier ; recliquer inverse l'ordre.
- Dans **Médecins et absences**, rechercher par nom, identifiant ou alias.
  **Effacer** réaffiche toute la liste.
- Les barres d'actions passent à la ligne si la fenêtre devient plus étroite.
- Les fiches longues défilent avec la barre ou la molette. Les boutons
  **Enregistrer** et **Annuler** restent en bas ; Échap annule la fiche,
  Ctrl+Entrée l'enregistre.
- Dans la vue mensuelle, parcourir les mois et cliquer sur une date pour lire
  le détail complet des gardes. La molette et la barre permettent de défiler.

Raccourcis : Ctrl+N crée un projet, Ctrl+O ouvre un projet, Ctrl+S sauvegarde
et F1 ouvre l'aide. Ces raccourcis ne s'exécutent pas pendant une fiche
modale. Les actions qui nécessitent un projet ou un planning restent grisées
tant que cette étape n'est pas disponible.

## Projet et données

L'icône **ⓘ**, en bas à droite, ouvre **Informations et licences** : version,
créateur, licence d'utilisation de GARDAVU et textes des composants tiers.
Ces documents sont consultables sans réseau, même sans projet ouvert.
Toute utilisation de GARDAVU, même gratuite, nécessite l'autorisation préalable,
expresse et écrite de son créateur, le **Dr Florian Ronez**, et reste limitée à
un usage non commercial. Voir [la licence](../LICENSE).

Créer ou ouvrir un fichier `.gardavu` avec les boutons du haut. Le chemin ouvert
est toujours visible. Un fichier est verrouillé pendant l'ouverture ; une seconde
instance ne peut pas l'écrire. Fermer l'application avant de déplacer l'original.
Les données sont enregistrées à chaque action, sans bouton de sauvegarde générale.

**Sauvegarder** crée immédiatement une sauvegarde datée dans le dossier
`<nom du projet>_sauvegardes`, à côté du projet. Son emplacement s'affiche en bas
de la fenêtre. Chaque clic conserve les sauvegardes précédentes ; le projet
ouvert reste le même. **Restaurer** ouvre une sauvegarde et la restaure vers un
nouveau fichier, sans écraser l'original. Les sauvegardes automatiques sont
également dans ce dossier, avec date et raison.
Elles précèdent imports et validations/remplacements. Les migrations futures
doivent aussi utiliser cette sauvegarde avant modification du schéma.

Les données ne sont pas chiffrées. Protéger l'accès au dossier, conserver une copie
sur un autre support, et partager volontairement le projet. Le logiciel n'utilise
ni AppData ni le registre pour les données. Le fichier `.lock` adjacent est un
support de verrou système, pas une seconde base : il peut rester après fermeture.

## Médecins et absences

Chaque médecin possède un identifiant stable. Le nom peut évoluer sans changer
ses anciennes gardes. La désactivation prend effet à la date choisie, sans
suppression de l'historique. Pour un retour, conserver la même fiche, retirer la
désactivation et compléter les périodes de participation ou de suspension.

Les périodes se saisissent une par ligne, sous la forme
`01/11/2026..30/04/2027` ou `2026-11-01..2027-04-30`, bornes incluses.
Des consignes et exemples restent visibles sous chaque champ de périodes.
Pour un seul jour, saisir la même date aux deux extrémités :
`24/12/2026..24/12/2026`. Pour plusieurs absences, ajouter une ligne par période.
Laisser les absences et indisponibilités vides s'il n'y en a pas.
Une fin vide signifie sans limite, par exemple `01/11/2026..` ; une date
saisie seule signifie aussi sans limite et ne doit donc pas servir pour un seul jour.

- Participation : dates d'appartenance au groupe.
- Suspension / absence longue : interdit l'affectation et neutralise la cible
  pendant la période. Aucun motif médical n'est nécessaire, aucune dette de retour.
- Indisponibilité ponctuelle : interdit la date sans diminuer automatiquement la cible.
- Pondération : ×1 par défaut, ×2 pour deux parts de garde, ×3 pour trois,
  ×0,5 pour moitié. Sélectionner un médecin puis **Pondérer le médecin**, saisir
  le multiplicateur et enregistrer. Le même réglage est disponible dans **Modifier**.
- Maximums total et mensuel : limites impératives sur la période calculée.

Un médecin à ×2 a une charge cible deux fois plus élevée qu'un médecin à ×1
ayant les mêmes périodes de participation. Les cibles sont pondérées au total,
par mois et par catégorie. Le nombre effectivement attribué dépend des arrondis
et des contraintes : indisponibilités, espacement, limites et rotation des fêtes
restent applicables à la même personne.

La pondération est visible dans la liste, les besoins théoriques, le tableau
d'équité et sa feuille Excel. Après modification, **générer ou régénérer** le
planning pour répartir les gardes à nouveau. Un brouillon déjà calculé garde ses
affectations en attendant et signale cette étape ; les plannings validés restent
inchangés avec leur pondération de validation. L'import Excel conserve le nom
de colonne **Coefficient** pour ce multiplicateur.

## Besoins et règles

Sélectionner `soir` puis **Configurer le créneau** pour renseigner les horaires
réellement décidés et cliquer sur **Enregistrer**. Un double-clic sur la ligne,
ou un clic droit puis **Configurer le créneau…**, ouvre la même fenêtre.
Cette commande modifie la version sélectionnée à sa date d'effet affichée :
la configuration initiale ne laisse donc pas une ancienne version sans horaires.
Pour un changement applicable seulement à partir d'une nouvelle date, utiliser
**Nouvelle version d'un modèle**. Les horaires historiques restent enregistrés
indépendamment. Une nouvelle version désactivée
permet d'arrêter un modèle à partir d'une date.

Les fériés remplacent la journée ordinaire : deux créneaux, jamais un doublon de
samedi ou dimanche. Nuit signifie 19 h à minuit, sans créneau minuit–8 h.
Minuit s'écrit `24:00` ou `00:00` en fin de garde : il s'agit du lendemain.

**Exception à une date** remplace l'ensemble des modèles de cette journée.
Pour deux créneaux exceptionnels, saisir successivement deux identifiants distincts.
Le récapitulatif affiche toutes les exceptions ; la commande permet de supprimer
l'exception ou de désactiver toute la date.

**Fêtes / dates particulières** ajoute ou retire des identifiants stables à une date.
Une correction de date nécessite un retrait à l'ancienne date puis un ajout à la
nouvelle. Pour une veille soumise à rotation, utiliser par exemple `VEILLE_NOEL`.
Les 24 et 31 décembre ne sont pas fériés automatiquement. Deux identifiants le
même jour partagent la couverture sans ajouter des créneaux.

Dans **Paramètres du calcul**, confirmer l'espacement minimal. Sept jours est une
proposition organisationnelle, aucune obligation réglementaire n'est affirmée.
L'espacement s'applique avant et après la période à toutes les gardes effectives
connues. Le mode STRICT interdit la même fête dans la fenêtre ; PRIORITAIRE la
défavorise et impose une confirmation des répétitions avant validation.

## Importer

Deux assistants distincts : médecins et historique. Choisir le fichier `.xlsx` ou
CSV UTF-8, la feuille, la ligne des en-têtes et la correspondance des colonnes.
L'aperçu expose les erreurs, avertissements et rapprochements nécessaires.
Les formules sont refusées ; coller les valeurs avant l'import. Les fichiers
`.xls`, macros et calendriers graphiques non tabulaires ne sont pas interprétés.

Pour les médecins : ID facultatif pour une création. Pour une fiche déjà connue,
fournir l'ID explicite ; un nom identique ne provoque aucune fusion automatique.
Pour les homonymes, fournir des ID distincts.

Historique en lignes : date, médecin ou ID, catégorie ; horaires, fête, statut et
ID de créneau facultatifs. Catégories : SEMAINE, SAMEDI, DIMANCHE_JOUR,
DIMANCHE_NUIT, FERIE_JOUR, FERIE_NUIT (les libellés français sont aussi acceptés).
Historique en tableau : date en ligne, une colonne par catégorie, une cellule =
un médecin ou ID. Pour plusieurs postes d'un créneau, utiliser le format en lignes
avec un ID de créneau commun et l'effectif requis.

Les noms ambigus exigent un rapprochement explicite. Si plusieurs personnes ont
exactement le même texte source, compléter le fichier avec leurs identifiants
avant import pour distinguer chaque affectation. Les horaires manquants restent
inconnus. Les dates servent à l'espacement, mais les heures et certains
chevauchements historiques ne peuvent pas être reconstitués.

Un conflit avec une garde existante bloque par défaut. Choisir explicitement
**Ignorer** ou **Remplacer / corriger**, puis confirmer. Les versions antérieures
restent tracées sans compter dans les gardes effectives. Le même fichier avec
les mêmes paramètres et les mêmes lignes s'importe sans doubler les gardes.

La déclaration de **couverture connue complète** est manuelle. Elle exige le
contrôle de toutes les gardes ET des participations/coefficient correspondants.
Une plage entre première et dernière date ne démontre pas cette couverture.
Sans attestation suffisante, l'historique sert à l'espacement et aux fêtes,
sans imposer une compensation de charge ancienne à un nouvel arrivant.

## Calcul et examen

La fin saisie fait foi. Le bouton de calcul des mois indique la fin incluse avant
génération. Exemple : 01/11/2026–30/04/2027 = six mois. Une date en milieu de mois
est conservée ; si son anniversaire n'existe pas dans le mois cible, il est ramené
au dernier jour, puis exclu (la veille est la fin incluse).

Vérifier les besoins : quatre semaines sans férié nécessitent 32 affectations
pour les modèles initiaux. « Environ une garde par mois » est un objectif,
pas un plafond de 30 gardes. Des mois avec deux gardes sont donc normaux.

Le calcul s'exécute dans un fil séparé. Annuler demande l'arrêt et conserve la
meilleure solution conforme déjà obtenue par CP-SAT. Sans solution trouvée,
UNKNOWN signifie absence de conclusion. Les diagnostics précisent si un conflit
est prouvé ou si seule une piste d'analyse est proposée. Ne pas valider un planning
incomplet. FEASIBLE indique une solution conforme avec optimalité non démontrée.

Dans le planning, filtrer par médecin ou catégorie. Les vues chronologique et
mensuelle suivent les mêmes filtres. Sélectionner une ligne pour modifier le
médecin, deux lignes (Ctrl-clic) pour échanger deux affectations. Libérer les
verrous avant de modifier leurs affectations. Chaque changement est enregistré
en brouillon, contrôlé et répercuté dans les statistiques.

**Régénérer** conserve les verrous de la version affichée.
**Modifier le moins possible** place la conservation des affectations futures
avant les objectifs souples. Les gardes passées connues sont gelées et ne peuvent
pas être échangées ou réécrites par la validation d'un remplacement.

## Valider, archiver et exporter

Dans **Équité et exports**, sélectionner un seul médecin puis cliquer sur
**Détail du médecin sélectionné**. Une fenêtre défilante affiche sa pondération,
sa cible, ses gardes par mois et les fêtes concernées avec les occurrences
antérieures connues. Cette fenêtre reste accessible même si le bas de la page
est hors écran. Pour une version validée, les valeurs sont celles de sa validation.

Les contrôles indépendants bloquent les affectations incomplètes, indisponibles,
hors participation, chevauchantes, trop rapprochées, sur quota ou contraires aux
verrous. Une répétition de fête en mode PRIORITAIRE exige une confirmation.
Un remplacement de période exige aussi une confirmation distincte.

Une version validée est immuable : sa modification crée un nouveau brouillon.
Archiver conserve les gardes dans l'historique effectif. Un remplacement conserve
les anciens enregistrements, mais une seule affectation reste effective.

Les exports portent leur état, période et version. Un brouillon reste identifié
**BROUILLON — NON VALIDÉ** ; une ligne sans affectation reste marquée incomplète.
L'Excel contient Planning, Équité, Jours fériés, Paramètres et avertissements.
Les identifiants masqués du planning restent disponibles pour réimportation
(choisir la troisième ligne comme en-têtes). Le CSV porte aussi état et IDs.
Les textes pouvant ressembler à des formules sont protégés. Aucun motif d'absence
n'est demandé ni transmis.
