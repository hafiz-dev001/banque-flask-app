#!/bin/bash

echo ""
echo "========================================"
echo "    BANQUE NATIONALE - Demarrage"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python3 n'est pas installe"
    echo "Installez Python3 depuis: https://www.python.org"
    exit 1
fi

echo "[OK] Python3 detecte"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[INFO] Creation de l'environnement virtuel..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Impossible de creer l'environnement virtuel"
        exit 1
    fi
fi

# Activate virtual environment
echo "[INFO] Activation de l'environnement virtuel..."
source venv/bin/activate

# Install requirements
echo "[INFO] Installation des dependances..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERREUR] Impossible d'installer les dependances"
    exit 1
fi

# Start the application
echo ""
echo "[OK] Tout est pret!"
echo ""
echo "========================================"
echo "    Demarrage de l'application..."
echo "========================================"
echo ""
echo "Ouvrez votre navigateur et allez a:"
echo "http://localhost:5000"
echo ""
echo "Appuyez sur Ctrl+C pour arreter le serveur"
echo ""

python3 app.py
