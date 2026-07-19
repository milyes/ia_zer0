#!/bin/bash
# start.sh - Lanceur automatisé pour IA_ZER0

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0;2m'

echo "🔍 Vérification de l'environnement système..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Erreur : Python 3 est requis mais n'est pas installé.${NC}"
    exit 1
fi

echo -e "${GREEN}🚀 Initialisation du serveur NetSecurePro v9...${NC}"
python3 app_ia_production.py
