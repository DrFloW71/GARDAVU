# Hypothèses et références

## Périmètre et conventions

- Windows x64, Python 3.12.10 ; interface Tkinter/ttk. Pas de serveur ni d'application web.
- Calendrier national métropolitain. Extensions régionales possibles par exceptions
  explicites ; pas de calendrier Alsace-Moselle activé par défaut.
- Calendrier grégorien calculé, algorithme Meeus/Jones/Butcher pour Pâques.
- Les jours de participation et d'absence sont inclus aux deux extrémités.
- Sans date de participation importée : participation depuis 1900 sans fin ;
  cette convention doit être corrigée avant d'attester une couverture historique.
- Coefficients strictement positifs ; pour une absence complète, utiliser une suspension.
- Une fin à minuit est le lendemain. Les autres gardes traversant minuit exigent
  une extension explicite du modèle et ne sont pas acceptées silencieusement.
- Aucun horaire de semaine dans un projet neuf ; les horaires des tests sont fictifs.
- Une exception de journée peut désactiver tous les besoins à cette date ; une
  période entièrement désactivée est refusée comme sans créneau.
- Le nombre de mois sert au calcul de la date de fin ; la fin saisie fait foi.
- Les limites individuelles sont celles de la période calculée et du mois civil.
- Les imports au statut autre que validé/archivé/effectif sont ignorés avec avertissement.
- Les horaires historiques absents restent inconnus : aucune heure théorique ajoutée.
- Une correction importée d'une garde passée est explicite et auditée ; la génération
  et le remplacement de planning ne réécrivent pas les gardes passées déjà connues.
- La compensation récente exige que les participations et coefficients enregistrés
  décrivent aussi correctement la période attestée. Les coefficients ne sont pas
  versionnés dans le temps ; si leur valeur passée diffère, ne pas attester la fenêtre.
- Les `.xlsx` et CSV tabulaires sont pris en charge. Les `.xls`, macros et mises en
  page graphiques arbitraires nécessitent une conversion au modèle.
- La base n'est pas chiffrée. Le fichier `.gardavu` est un projet personnel,
  non un conteneur de distribution et non une base multi-utilisateur.
- Le binaire n'est pas signé. Une signature éditeur n'est pas revendiquée.

## Références vérifiées pendant le développement

Les onze fêtes nationales et les dates 2026 ont été vérifiées auprès de
[Service Public, fiche F2405](https://www.service-public.gouv.fr/particuliers/vosdroits/F2405).
Les règles mobiles concordent avec la
[circulaire FP 2172 du 17 décembre 2008](https://www.fonction-publique.gouv.fr/files/files/Autres%20pages/Textes%20de%20r%C3%A9f%C3%A9rence/2008/C_20081217_FP2172.pdf).
Ces références portent sur le calendrier ; aucune durée de repos médical ou
obligation professionnelle n'en est déduite.

Les licences déclarées sont collectées depuis les distributions réellement
installées ; voir `THIRD_PARTY_NOTICES.md`, `licenses/manifest.json` et les textes
complets correspondants. PyInstaller autorise la distribution de programmes
construits via son exception de licence ; aucune modification de PyInstaller.

La documentation est incluse dans la distribution. Aucun de ces sites n'est
consulté par GARDAVU pendant son utilisation.
