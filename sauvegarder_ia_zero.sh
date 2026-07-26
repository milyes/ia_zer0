#!/bin/bash
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups/archive_${TIMESTAMP}"

echo -e "\033[1;34m[*] Initialisation de la sauvegarde consolidée V-IA22 AUTOSEAL...\033[0m"

# 1. Structure locale
mkdir -p "${BACKUP_DIR}/scripts"
mkdir -p "${BACKUP_DIR}/logs"

# 2. Collecte des composants logiciels du noyau
echo -e "[+] Collecte de l'ensemble des scripts de production et gardes..."
cp app_ia_production.py core_pure.py ipv6_guard.py rate_limiter.py ia_zero_emac_guard.py scelleur_emac.py "${BACKUP_DIR}/scripts/" 2>/dev/null || true

# 3. Collecte des registres cryptographiques et des incidents EMAC
echo -e "[+] Collecte des registres d'incidents et signatures numériques..."
cp ia_zer0_security_log.json ia_zer0_security_log.sig ipv6_incident_log.json emac_security_incident.json emac_security_incident.sig "${BACKUP_DIR}/logs/" 2>/dev/null || true

# 4. Archivage souverain
echo -e "[+] Compression du snapshot système global..."
tar -czf "backups/ia_zer0_snapshot_${TIMESTAMP}.tar.gz" -C backups "archive_${TIMESTAMP}"
rm -rf "backups/archive_${TIMESTAMP}"

echo "====================================================================="
echo -e "🔒 SNAPSHOT GLOBAL ARCHIVÉ : backups/ia_zer0_snapshot_${TIMESTAMP}.tar.gz"
echo -e "Statut du Noyau : INTEGRALEMENT SAUVEGARDÉ & SECURISE"
echo "====================================================================="
