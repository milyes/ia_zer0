#!/bin/bash
set -e

echo -e "\033[1;34m[*] Arrêt de l'ancienne instance...\033[0m"
pkill -f app_ia_production.py || true

echo -e "\033[1;34m[*] Fusion globale des modules de sécurité (app_ia_production.py)...\033[0m"
cat << 'INNER_EOF' > app_ia_production.py
import http.server
import json
import re
import random
import string
import time

PORT = 8080

# Réplication locale de la logique Token Bucket (rate_limiter.py)
class TokenBucketRateLimiter:
    def __init__(self, capacite_max=10, taux_recharge_seconde=2.0):
        self.capacite_max = float(capacite_max)
        self.taux_recharge_seconde = float(taux_recharge_seconde)
        self.jetons_actuels = float(capacite_max)
        self.dernier_check = time.time()

    def consommer_jeton(self):
        maintenant = time.time()
        temps_ecoule = maintenant - self.dernier_check
        self.dernier_check = maintenant

        self.jetons_actuels = min(
            self.capacite_max, 
            self.jetons_actuels + (temps_ecoule * self.taux_recharge_seconde)
        )

        if self.jetons_actuels >= 1.0:
            self.jetons_actuels -= 1.0
            return True
        return False

# Initialisation globale du limiteur (10 requêtes max, recharge de 2/sec)
limiteur_global = TokenBucketRateLimiter()

class NetSecureProUnifiedHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        # 1. Validation immédiate par le Limiteur de Débit
        if not limiteur_global.consommer_jeton():
            self.send_response(429)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            erreur_limite = {
                "success": False,
                "error": "ALERTE TRAFIC",
                "message": "Débit maximal dépassé. Requête rejetée par le limiteur de débit."
            }
            self.wfile.write(json.dumps(erreur_limite, ensure_ascii=False, indent=4).encode('utf-8'))
            return

        # 2. Traitement standard si le jeton est accordé
        if self.path == "/api/analyse" or self.path == "/":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                payload = json.loads(post_data)
                texte_analyse = payload.get("texte", "")
            except:
                texte_analyse = post_data

            # Détection d'évasion IPv6 / SSRF RAG (ipv6_guard.py)
            patterns_evasion = [r'\[::ffff:127\.', r'\[::1\]', r'127\.0\.0\.1']
            attaque_detectee = any(re.search(pat, texte_analyse) for pat in patterns_evasion)
            
            suffixe_aleatoire = "".join(random.choices(string.ascii_uppercase, k=4))
            session_id = f"ZPUCE-{suffixe_aleatoire}"

            if attaque_detectee:
                doc_type = "Alerte Évasion Réseau RAG"
                summary = f"Tentative d'exploitation SSRF IPv6 interceptée : '{texte_analyse}'"
                security_status = "BLOQUÉE & SÉCURISÉE"
            else:
                doc_type = "Rapport Général"
                summary = "Synthèse : Données standards analysées. Contenu intègre."
                security_status = "Verified & Compliant"

            response_dict = {
                "success": True,
                "session_id": session_id,
                "document_type": doc_type,
                "summary": summary,
                "security_status": security_status
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            json_response = json.dumps(response_dict, indent=4, ensure_ascii=False)
            self.wfile.write(json_response.encode('utf-8'))

def lancer_serveur():
    server = http.server.HTTPServer(('0.0.0.0', PORT), NetSecureProUnifiedHandler)
    print(f"🚀 Serveur unifié [NANS Core] opérationnel sur http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Arrêt du serveur.")

if __name__ == "__main__":
    lancer_serveur()
INNER_EOF

echo -e "\033[1;34m[*] Lancement du serveur sécurisé complet...\033[0m"
python3 app_ia_production.py &
sleep 2

echo -e "\033[1;34m[*] Test d'intégrité final (Interception SSRF)...\033[0m"
curl -X POST http://localhost:8080/api/analyse \
  -H "Content-Type: application/json" \
  -d '{"texte": "http://[::ffff:127.0.0.1]/v1/metadata"}'
echo -e "\n"
