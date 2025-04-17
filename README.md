Bien sûr ! Voici un README complet, élégant et prêt à être copié-collé dans ton dépôt GitHub :

# 🚀 AWS Cloud App - User Profile & NASA APOD Integration

Bienvenue dans notre projet fullstack utilisant **AWS Amplify**, **Vue.js**, **DynamoDB**, et **Lambda**, conçu pour gérer des profils utilisateurs avec des adresses multiples, une page dédiée à la NASA "Astronomy Picture of the Day" (APOD), et une infrastructure de déploiement Dev/Prod complète.

---

## 🌟 Fonctionnalités principales

### ✅ Authentification & Gestion Utilisateur
- Authentification sécurisée via **AWS Cognito**
- 🔒 `signUp`, `confirm`, `signIn` déjà intégrés dans l'interface
- Lors du **postConfirmation** Cognito, l'utilisateur est automatiquement **inséré dans une table DynamoDB** `users`
- Possibilité de mettre à jour son profil utilisateur (prénom, nom, date de naissance, genre, orientation politique, etc.)

### 🏠 Gestion des Adresses
- Ajout d'adresses **multiples** par utilisateur
- Les adresses sont stockées dans une table DynamoDB séparée `addresses`, liée au `user_id`
- Suppression dynamique des adresses avec effet immédiat sur l'interface

### 🌌 NASA - Astronomy Picture of the Day (APOD)
- Lambda `updateApodData` exécutée chaque jour à **1h du matin UTC** (cron défini dans `parameters.json`)
- Cette lambda :
  - Fetch l’image du jour via l’API NASA
  - Formatte les données (titre, description, image, miniature, etc.)
  - **Écrase** les anciennes données de la table `nasaapod` pour ne conserver **qu’un seul objet par jour**
- Accès direct depuis `/apod` dans l'application

---

## 🧪 Tests & Qualité de Code

- 📦 Tests unitaires mis en place :
  - Pour un composant Vue : `Apod.vue`
  - Pour une Lambda : `getUser` dans tests/
- Pipeline de tests intégrée (via CodeBuild ou Amplify CI)

---

## 📦 Déploiements

Le projet est déployé sur deux environnements :

| Environnement | URL |
|---------------|-----|
| 🧪 Dev         | [Lien Dev](https://dev.d3isug3kri9t0e.amplifyapp.com) |
| 🚀 Prod        | [Lien Prod](https://main.d3isug3kri9t0e.amplifyapp.com) |

---

## ⚙️ Technologies utilisées

- ⚡ **Vue.js 3**
- 🧠 **AWS Cognito**
- 🔥 **AWS Lambda**
- 💾 **DynamoDB**
- 🚀 **AWS Amplify (CI/CD + Hosting)**
- 📡 **API REST (Amplify)**
- 🧪 **Vitest / Pytest** (pour tests frontend & backend)

---

## 🔗 Liens utiles

- 🧑‍💻 Dépôt GitHub : [https://github.com/GabrielLCSC/aws-cloud](https://github.com/GabrielLCSC/aws-cloud)
- 📄 Documentation NASA APOD : [https://api.nasa.gov/](https://api.nasa.gov/)
- ☁️ Console AWS Amplify : [https://eu-west-1.console.aws.amazon.com/amplify/](https://eu-west-1.console.aws.amazon.com/amplify/)

---

## 🙌 Auteurs

Projet réalisé dans le cadre de notre formation DevOps / Cloud & Frontend.

Enzo GIVERNAUD
Hugo MACEDO
Alban DE BRAQUILANGES  
Gabriel DAUTREPPE

Master 1 à l'IIM en IWID

> Pour toute suggestion ou PR, n'hésitez pas à contribuer !

---

🎉 Merci d’avoir scrollé jusqu’ici, et bon voyage à travers le cloud et les étoiles !
```