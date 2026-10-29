# GARDAVU 1.1.3 — Aide à la saisie des absences

La fiche médecin affiche des consignes sous les champs de participation,
d'absences longues et d'indisponibilités : effet sur la charge attendue,
format des dates, période complète, journée isolée et plusieurs périodes.
Les exemples sont des textes d'aide, jamais des absences préremplies.

Une période se saisit avec deux points entre les dates, par exemple
`10/02/2027..24/02/2027`, dates incluses. Pour une seule journée, répéter
la date : `24/12/2026..24/12/2026`. Plusieurs périodes se mettent sur des lignes
distinctes. Les champs d'absences et d'indisponibilités peuvent rester vides.

La livraison portable est dans `dist/v1.1.3/`.

Vérifications : trois tests ciblés réussis (périodes, formulaire/thèmes et
pondérations), puis saisie et enregistrement des exemples depuis une fiche
de test. Les journées isolées, bornes incluses, périodes multiples et champs
initialement vides sont confirmés. Les consignes suivent les thèmes clair/sombre.
Rapport : `artifacts/recette-aide-absences-v1-1-3/rapport.json`.
Recette de l'exécutable : `artifacts/recette-v1-1-3/rapport.json`.
