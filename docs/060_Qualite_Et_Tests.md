# Qualité et tests

## Risques prioritaires

- {{QUALITY_RISK_1}}
- {{QUALITY_RISK_2}}

## Preuve proportionnée au régime

| Régime | But de la validation | Minimum attendu |
| --- | --- | --- |
| Exploration | confirmer ou invalider une hypothèse | observation traçable, rejouable lorsque pertinent, aucune promesse de couverture |
| Construction | protéger le comportement principal | contrôle ciblé du critère d’acceptation et erreur principale observée |
| Intégration | vérifier les frontières réelles | tests des contrats, données, configurations, migrations et parcours touchés ou applicables |
| Stabilisation | réduire le risque résiduel | régressions pertinentes, cas limites et contrôles non fonctionnels applicables |

Un test exploratoire peut être jetable. Une preuve conservée pour l’intégration
doit devenir reproductible ou être remplacée par un contrôle équivalent.

## Stratégie de stabilisation

| Niveau | Ce qui est validé | Outil ou protocole | Fréquence |
| --- | --- | --- | --- |
| Statique | types, style, erreurs évidentes | {{STATIC_CHECK}} | chaque changement intégré |
| Unitaire | règles isolées | {{UNIT_TEST}} | chaque changement intégré |
| Intégration | frontières et données | {{INTEGRATION_TEST}} | {{INTEGRATION_FREQUENCY}} |
| Parcours | cas d’usage critiques | {{E2E_TEST}} | {{E2E_FREQUENCY}} |
| Manuel | UX et cas difficiles à automatiser | {{MANUAL_PROTOCOL}} | {{MANUAL_FREQUENCY}} |
| Visuel | responsive, thèmes, composants et états | captures ou recette | avant fin d’intégration et en stabilisation si une interface est active |

## Critères de transition

### Sortie de l’exploration

- [ ] hypothèse ou question explicitée ;
- [ ] observation traçable conservée, rejouable lorsque pertinent ;
- [ ] piste retenue pour construction ou exploration close avec abandon documenté.

### Construction vers intégration

- [ ] comportement principal observable ;
- [ ] critère d’acceptation relié ;
- [ ] contrôle ciblé exécutable ;
- [ ] raccourcis temporaires consignés.

### Intégration vers stabilisation

- [ ] frontières et données réelles raccordées ;
- [ ] mocks retirés ou conservés comme fixtures explicites ;
- [ ] compatibilité, migration et retour arrière traités si nécessaires ;
- [ ] erreurs et états importants couverts.

### Sortie de la stabilisation

- [ ] critères d’acceptation satisfaits ;
- [ ] invariants préservés ;
- [ ] erreurs importantes couvertes ;
- [ ] documentation cohérente ;
- [ ] états visuels et formats cibles vérifiés si une interface est active ;
- [ ] clavier, focus, contraste et mouvement réduit vérifiés si une interface est active ;
- [ ] aucune donnée sensible ou secret ajouté ;
- [ ] migration et retour arrière définis si nécessaires ;
- [ ] risques restants et révision source explicités.
- [ ] applicabilité de la portée `release` décidée ; sinon la tranche est close sans release.
