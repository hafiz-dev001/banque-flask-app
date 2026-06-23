# 🏦 BANQUE NATIONALE - Site Web de Banque

Un site web bancaire complet avec fonctionnalités de gestion de compte, virements et historique de transactions.

## 📋 Fonctionnalités

- ✅ **Authentification**: Inscription et connexion sécurisée
- ✅ **Gestion de compte**: Consultation du solde et des informations personnelles
- ✅ **Historique**: Visualisation complète des transactions
- ✅ **Virements**: Transfert d'argent entre comptes
- ✅ **Dépôts**: Effectuer des dépôts sur votre compte
- ✅ **Interface responsive**: Fonctionne sur desktop et mobile
- ✅ **Design moderne**: Interface utilisateur professionnelle

## 🛠️ Installation

### Prérequis
- Python 3.7+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Ouvrir un terminal** dans le dossier `BANQUE`

2. **Installer les dépendances**:
   ```
   pip install -r requirements.txt
   ```

3. **Démarrer l'application**:
   ```
   python app.py
   ```

4. **Accéder au site**: Ouvrir votre navigateur et aller à:
   ```
   http://localhost:5000
   ```

## 👤 Comptes de test

L'application crée une base de données automatiquement au premier lancement.

Pour tester, créez un nouveau compte directement depuis la page d'inscription.

### Exemple d'identifiants de test:
- **Utilisateur**: jean_dupont
- **Mot de passe**: password123
- **Email**: jean@example.com
- **Nom**: Jean Dupont

## 💻 Pages principales

### 1. **Connexion** (`/login`)
- Authentification avec nom d'utilisateur et mot de passe
- Lien vers la page d'inscription

### 2. **Inscription** (`/register`)
- Création d'un nouveau compte
- Validation des données
- Numéro IBAN généré automatiquement

### 3. **Tableau de bord** (`/dashboard`)
- Affichage du solde
- Informations personnelles et IBAN
- Historique des transactions
- Boutons d'actions rapides

## 🔧 API Endpoints

### Authentification
- `POST /login` - Connexion utilisateur
- `POST /register` - Création de compte
- `GET /logout` - Déconnexion

### Profil
- `GET /api/user/profile` - Récupérer les infos utilisateur

### Transactions
- `GET /api/transactions` - Historique des transactions
- `POST /api/deposit` - Effectuer un dépôt
- `POST /api/transfer` - Effectuer un virement

## 📁 Structure du projet

```
BANQUE/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── bank.db               # Base de données (créée automatiquement)
├── static/
│   ├── css/
│   │   └── style.css     # Styles CSS
│   └── js/
│       └── script.js     # Utilitaires JavaScript
└── templates/
    ├── login.html        # Page de connexion
    ├── register.html     # Page d'inscription
    └── dashboard.html    # Tableau de bord
```

## 🎨 Personnalisation

### Changer la clé secrète
Dans `app.py`, ligne ~20:
```python
app.secret_key = 'your_secret_key_change_this'
```

Remplacez par une clé secrète unique pour la production.

### Modifier les couleurs
Dans `static/css/style.css`:
```css
:root {
    --primary-color: #1e3a8a;      /* Couleur principale */
    --secondary-color: #3b82f6;    /* Couleur secondaire */
    /* ... */
}
```

## 🔒 Sécurité

- Les mots de passe sont hashés avec Werkzeug
- Sessions utilisateur gérées avec Flask
- Protection CSRF (à implémenter pour la production)
- Validation des entrées utilisateur

## 🚀 Déploiement

Pour déployer en production:

1. Désactiver le mode debug dans `app.py`:
   ```python
   app.run(debug=False)
   ```

2. Utiliser un serveur WSGI comme Gunicorn:
   ```
   pip install gunicorn
   gunicorn app:app
   ```

3. Configurer un reverse proxy (nginx) pour HTTPS

## 📝 Notes

- Les montants sont en euros (€)
- Les IBAN sont générés au format français
- Les transactions sont horodatées automatiquement
- La limite de transactions affichées est de 20

## 🐛 Dépannage

**L'application ne démarre pas?**
- Vérifier que Python est installé: `python --version`
- Vérifier que Flask est installé: `pip install Flask`

**Les fichiers CSS/JS ne se chargent pas?**
- Vérifier que les dossiers `static/css` et `static/js` existent
- Recharger la page (Ctrl+F5)

**La base de données n'est pas créée?**
- La base de données est créée automatiquement au premier lancement
- Vérifier que vous avez les permissions d'écriture dans le dossier BANQUE

## 📞 Support

Pour toute question ou problème, consultez le code commenté dans les fichiers source.

## 📄 Licence

Ce projet est fourni à titre d'exemple éducatif.

---

Bon développement! 🚀
