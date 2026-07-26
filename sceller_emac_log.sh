#!/bin/bash
set -e

echo -e "\033[1;34m[*] Verrouillage cryptographique du registre EMAC (AUTOSEAL)...\033[0m"

cat << 'INNER_EOF' > scelleur_emac.py
import hashlib
import json
import os
from datetime import datetime

log_filename = "emac_security_incident.json"
sig_filename = "emac_security_incident.sig"

if not os.path.exists(log_filename):
    print(f"[ERREUR] Le fichier {log_filename} est introuvable.")
    exit(1)

with open(log_filename, "r", encoding="utf-8") as f:
    log_content = f.read()

# Calcul du condensat SHA-256
sha256_hash = hashlib.sha256(log_content.encode('utf-8')).hexdigest()

signature_data = {
    "scellage_timestamp": datetime.now().isoformat(),
    "target_file": log_filename,
    "sha256_checksum": sha256_hash,
    "gouvernance_status": "AUTOSEAL_EMAC_LOCKED",
    "signature_protocol": "V-IA22_STANDARDS"
}

with open(sig_filename, "w", encoding="utf-8") as f:
    json.dump(signature_data, f, indent=4)

print("=====================================================================")
print(f"🔒 REGISTRE EMAC SCELLÉ AVEC SUCCÈS : {sig_filename}")
print(f"Empreinte SHA-256 du Noyau : {sha256_hash}")
print("=====================================================================")
INNER_EOF

python3 scelleur_emac.py
cat emac_security_incident.sig
