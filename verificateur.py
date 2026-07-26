import hashlib
import json
import os

log_filename = "ia_zer0_security_log.json"
sig_filename = "ia_zer0_security_log.sig"

if not os.path.exists(log_filename) or not os.path.exists(sig_filename):
    print("\033[1;31m[ERREUR] Fichiers requis (log ou signature) introuvables pour l'audit.\033[0m")
    exit(1)

# 1. Lecture de la signature officielle
with open(sig_filename, "r", encoding="utf-8") as f:
    sig_data = json.load(f)
expected_hash = sig_data.get("sha256_checksum")

# 2. Lecture et recalcul du hash du fichier log actuel
with open(log_filename, "r", encoding="utf-8") as f:
    current_content = f.read()
current_hash = hashlib.sha256(current_content.encode('utf-8')).hexdigest()

print("=====================================================================")
print("🔬 RAPPORT D'AUDIT CONTINU V-II22")
print(f"Empreinte attendue (SIG) : {expected_hash}")
print(f"Empreinte calculée (LOG) : {current_hash}")
print("=====================================================================")

# 3. Verdict d'intégrité
if current_hash == expected_hash:
    print("\n--> \033[1;32m[AUDIT VALIDE]\033[0m : L'intégrité des données est 100% préservée.")
    print("Statut : AUTENTICITY_CONFIRMED & SECURE")
else:
    print("\n--> \033[1;31m[CRITICAL ALERT - CORRUPTION DETECTED]\033[0m : Le fichier de log a été altéré !")
    print("Action recommandée : Isolation du conteneur / Restauration de la matrice.")
print("=====================================================================")
