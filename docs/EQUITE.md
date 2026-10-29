# Modèle d'équité et contraintes

## Cibles

Pour chaque créneau s, d'effectif n, le médecin i reçoit une part théorique
`n × coefficient_i / somme(coefficients des participants à la date s)`.
Un participant est dans sa période de participation, non désactivé, hors suspension
neutralisante. Les indisponibilités ponctuelles n'enlèvent pas sa part.
Les parts sont calculées avec des fractions rationnelles, puis agrégées par
médecin, mois, catégorie principale, total et total fériés.

Le coefficient est présenté comme une **pondération** : ×2 équivaut à deux parts
de charge, ×3 à trois parts. Exemple : pour neuf gardes et deux participants de
poids 2 et 1, les cibles sont six et trois. Cela ne crée pas de deuxième identité :
un même médecin ne remplit pas deux postes du même créneau, et ses contraintes
restent celles d'une seule personne. Les écarts d'arrondi et les incompatibilités
éventuelles restent visibles dans la comparaison entre cible et attribué.

Pour CP-SAT, les cibles sont exprimées en millièmes par la méthode des plus forts
restes : somme conservée, erreur individuelle inférieure à 0,001 garde. Le
départage du dernier millième utilise une empreinte de l'identifiant et de la
période, jamais l'ordre des noms. Il varie d'une période à l'autre pour ne pas
favoriser systématiquement les mêmes identifiants.
Il peut départager des solutions presque équivalentes ; les cibles affichées
restent les fractions d'origine. Aucune troncature répétée par créneau.

Une suspension neutralise la charge pendant l'absence : aucun rattrapage calculé
sur cette durée. Les arrivées, départs et retours sont pris en compte à chaque date.

## Contraintes impératives

Variables binaires médecin/créneau ; somme de chaque créneau égale à l'effectif.
Les candidats hors participation, indisponibles, incompatibles avec l'historique
ou exclus par STRICT ne reçoivent aucune variable. Chaque paire ou clique de
gardes trop rapprochées a au plus une affectation par médecin. Le début de deux
gardes doit être séparé d'au moins N jours calendaires, frontières incluses.
L'historique extérieur à la période est considéré avant ET après celle-ci.
Chevauchements, doubles postes, verrous et quotas impératifs sont contrôlés.

Les journées ne sont pas doublées quand elles sont fériées. La catégorie principale
est férié ; elle ne reçoit pas simultanément une pénalité de dimanche. Le total
fériés est un indicateur/objective explicite complémentaire des catégories jour/nuit.

Le validateur recalcule couverture, participations, indisponibilités, chevauchements,
espacement, fêtes STRICT, quotas et verrous sans consulter les variables du modèle.
Une validation en base relance ces contrôles avec les données du projet.

## Optimisation hiérarchique

Les étapes sont résolues successivement. La meilleure valeur trouvée à l'étape
précédente devient une borne supérieure impérative pour les suivantes : une
préférence secondaire ne dégrade jamais une priorité déjà obtenue.

1. En mode réparation demandé : minimiser les affectations futures modifiées.
2. Rotation des fêtes : minimiser d'abord le nombre d'affectations répétant au
   moins une fête connue, puis préférer l'occurrence la plus ancienne.
3. Charge globale : somme des écarts absolus entre nombres attribués et cibles.
4. Catégories : écarts absolus par catégorie et sur le total fériés.
5. Charge mensuelle : écarts absolus par mois.
6. Diversité lundi–vendredi : minimiser d'abord les dépassements du seuil, puis
   les répétitions au-delà de la première. Seuil proposé = plafond de
   `nombre_de_mois_calendaires_équivalents / 3`, au moins un et modifiable.
   Un mois complet compte un ; les mois de bord sont pris au prorata des jours.
   Six mois complets proposent donc deux, même s'ils comptent 181 ou 184 jours.
7. Régularité : réduire les gardes excédant une affectation par quinzaine.

Dans l'objectif des fêtes, la base d'une répétition est supérieure à toute la
variation possible des termes d'ancienneté sur le problème : aucune accumulation
de petits gains de récence ne compense une répétition supplémentaire.
Même principe pour le seuil hebdomadaire puis les répétitions simples.
Les autres priorités utilisent des résolutions distinctes, sans gros coefficients
arbitraires entre les étapes. Les noms n'entrent jamais dans les objectifs.

Un amorçage heuristique accélère CP-SAT. Il n'est jamais livré seul : CP-SAT doit
obtenir sa propre solution, et le validateur doit la contrôler. Cet amorçage n'est
ni une rotation alphabétique ni un tirage utilisé comme résultat final.

## Historique

Trois usages séparés : espacement, équité récente, rotation des fêtes.
Fenêtre de fêtes : dix ans, configurable ; identité indépendante du jour/nuit.
Seules les occurrences antérieures à la garde et incluses dans la fenêtre sont
retenues pour les répétitions. Les gardes effectives à venir servent à l'espacement.

Fenêtre d'équité récente : douze mois par défaut. Une compensation des écarts
réels/cibles sur cette fenêtre ne s'applique que si la couverture complète est
explicitement attestée, avec participations et coefficients corrects. La correction
porte sur le total et les catégories ; elle est ajoutée à l'écart de la nouvelle
période. Sans attestation, aucune dette ancienne n'est inventée. La rotation et
l'espacement fonctionnent même sur un historique incomplet, avec avertissement.

Brouillons et versions remplacées ne sont jamais comptés comme des affectations
effectives supplémentaires. L'archivage d'une version validée n'annule pas ses gardes.

## Statuts et preuves

OPTIMAL exige une preuve d'optimalité à **chaque** étape. Une étape FEASIBLE fige
la meilleure borne trouvée mais l'ensemble reste FEASIBLE, même si toutes les
étapes suivantes sont optimales. UNKNOWN signifie qu'aucune solution n'a été
obtenue dans le budget, INFEASIBLE un conflit démontré, MODEL_INVALID un modèle
ou un résultat invalide. Les valeurs, bornes et statuts sont conservés par étape.

Le temps limite inclut la préparation ; l'arrêt du solveur et le contrôle final
peuvent entraîner un léger dépassement mural. Un travailleur et une graine fixe
servent aux tests ; un arrêt sur temps mural peut néanmoins varier suivant la
machine. Un calcul parallèle sous limite de temps n'est pas strictement reproductible.

Les petits problèmes énumérables sont comparés à l'optimum exhaustif, et les
statistiques donnent cibles, totaux, catégories, heures, mois et jours de semaine,
sans score composite présenté comme une explication causale.
