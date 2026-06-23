# 🚀 DÉMARRAGE RAPIDE

## ⚡ Pour Windows

Double-cliquez sur `run.bat` dans le dossier BANQUE

```
double-clic sur run.bat
```

Puis ouvrez votre navigateur à: **http://localhost:5000**

---

## ⚡ Pour Mac/Linux

Ouvrez un terminal dans le dossier BANQUE et exécutez:

```bash
bash run.sh
```

Puis ouvrez votre navigateur à: **http://localhost:5000**

---

## ⚡ Démarrage Manuel

Si les scripts ne fonctionnent pas, suivez ces étapes:

### 1. Créer l'environnement virtuel

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Installer les dépendances

```
pip install -r requirements.txt
```

### 3. Lancer l'application

```
python app.py
```

### 4. Accéder à l'application

Ouvrez votre navigateur à: **http://localhost:5000**

---

## 👤 Créer un compte de test

1. Cliquez sur "Créer un compte"
2. Remplissez les informations:
   - **Nom complet**: Jean Dupont
   - **Email**: jean@example.com
   - **Nom d'utilisateur**: jean_dupont
   - **Mot de passe**: password123

3. Cliquez sur "Créer mon compte"
4. Connectez-vous avec vos identifiants

---

## ✨ Fonctionnalités à tester

### 1. Tableau de bord
- Consultez votre solde (1000€ initialement)
- Consultez vos informations
- Consultez votre IBAN généré

### 2. Dépôt
- Cliquez sur "Dépôt"
- Entrez un montant (ex: 500€)
- Confirmez

### 3. Virement
- Cliquez sur "Virement"
- Créez un autre compte pour tester
- Utilisez l'IBAN du second compte pour effectuer le virement

### 4. Historique
- Consultez toutes vos transactions avec les dates

---

## ❌ Problèmes courants

### "Flask n'est pas trouvé"
```
pip install Flask
```

### "Le port 5000 est déjà utilisé"
Modifiez dans `app.py` à la fin:
```python
app.run(debug=True, port=5001)  # Changez le port
```

### "Les fichiers CSS/JS ne se chargent pas"
- Recharger la page avec Ctrl+F5
- Vérifier que le dossier `static/` existe

---

## 📞 Support

Consultez le README.md pour plus d'informations!
