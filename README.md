# Vélib' sous tension : Prévoir les stations en difficulté

Ce dépôt contient le code de préparation, d'analyse et de modélisation pour le projet "Vélib' sous tension". 

## Définition de la cible (Question A : Départ impossible)
L'objectif est d'anticiper l'état futur des 80 stations étudiées[cite: 3]. La cible exacte est définie ainsi : **la station disposera-t-elle de moins de deux vélos (mécaniques ou électriques) disponibles à un horizon de 30 (ou 60) minutes ?**[cite: 2, 3, 5]

## Données et attribution
Le jeu de données provient d'une collecte régulière du flux de disponibilité en temps réel de **Vélib' Métropole** mis à disposition par **Paris Data**[cite: 2].
- **Licence :** Open Database License (ODbL)[cite: 2, 5].
- **Période collectée :** Du 25 août au 8 octobre 2026[cite: 2].

Conformément aux consignes, le fichier compressé figé n'est pas versionné dans ce dépôt[cite: 5]. 
- **URL de téléchargement :** `https://docs.ambroise.cloud/velib/velib-2026-10-08.csv.gz`[cite: 2, 5]
- **Empreinte MD5 :** `02ab1e3fdac10579e4ce93d1540a5dc7`[cite: 2, 5]

### Procédure de récupération
Pour télécharger les données dans le répertoire `data/raw/` et vérifier automatiquement l'empreinte MD5, exécutez[cite: 5] :
```bash
python src/data/download.py
