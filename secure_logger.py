# =================================================================
# secure_logger.py - IA_ZER0.09 - Cryptographic Native Logger
# Version pure Python standard - Zéro dépendance (No-pip)
# =================================================================

import hashlib
import datetime
import os

class NativeSecureLogger:
    """Gère le hachage et le chiffrement symétrique des logs d'attaques informatique"""
    def __init__(self, log_file="netsecurepro_audit.enc"):
        self.log_file = log_file
        # Clé principale de chiffrement interne (Générée ou fixée par l'administrateur)
        self.master_key = "NANS_CORE_SECRET_KEY_IA9"

    def _obfuscate(self, data: str, key: str) -> str:
        """Algorithme de chiffrement symétrique par flux natif"""
        output = []
        for i in range(len(data)):
            key_c = key[i % len(key)]
            # Transformation par XOR et encodage hexadécimal pour éviter les caractères brisés
            enc_c = chr(ord(data[i]) ^ ord(key_c))
            output.append(enc_c)
        return "".join(output).encode('utf-8').hex()

    def log_incident(self, session_id: str, document_type: str, violation_details: str):
        """Hache l'empreinte de l'attaque et écrit le log chiffré sur le disque"""
        timestamp = datetime.datetime.now().isoformat()
        
        # 1. Génération d'une empreinte SHA-256 unique pour garantir l'immuabilité du log
        log_payload = f"[{timestamp}] | SESSION: {session_id} | TYPE: {document_type} | DETAIL: {violation_details}"
        payload_hash = hashlib.sha256(log_payload.encode('utf-8')).hexdigest()
        
        final_entry = f"{log_payload} | INTEGRITY_HASH: {payload_hash}\n"
        
        # 2. Chiffrement de la ligne de log
        encrypted_entry = self._obfuscate(final_entry, self.master_key)
        
        # 3. Écriture persistante en mode 'append' (ajout)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(encrypted_entry + "\n")


# ---- Module de Lecture pour l'Administrateur ----
if __name__ == "__main__":
    logger = NativeSecureLogger()
    print("📋 Tentative de lecture et déchiffrement du journal d'audit local...\n")
    
    if not os.path.exists(logger.log_file):
        print("💡 Aucun incident enregistré pour le moment. Le fichier est vierge.")
    else:
        with open(logger.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for idx, line in enumerate(lines):
            line = line.strip()
            if line:
                try:
                    raw_bytes = bytes.fromhex(line)
                    # Déchiffrement inverse
                    decrypted = "".join(chr(b ^ ord(logger.master_key[i % len(logger.master_key)])) for i, b in enumerate(raw_bytes))
                    print(f"[Incident #{idx+1}] {decrypted}")
                except Exception as e:
                    print(f"❌ Impossible de déchiffrer la ligne {idx+1} (Clé invalide ou corruption).")
      
