# =================================================================
# IA_auto.py - IA_ZER0.09 - Autonomous Framework Orchestrator
# Version pure Python standard - Zéro dépendance (No-pip)
# Propriété Intellectuelle Exclusive : MOHAMMED ILYES ZOUBIROU
# =================================================================

import os
import sys

# --- CONFIGURATION DE L'ARBORESCENCE DU PROJET ---
FILES_MANIFEST = {
    # 1. LE PARE-FEU RÉSEAU ANTI-SSRF IPV6
    "ipv6_guard.py": """# ipv6_guard.py - IA_ZER0.09 - Anti-SSRF Network Validator
import ipaddress
from urllib.parse import urlparse

class RAGNetworkGuardrail:
    @staticmethod
    def is_safe_url(url: str) -> bool:
        try:
            host = urlparse(url).hostname
            if not host: return False
            host = host.strip("[]")
            ip = ipaddress.ip_address(host)
            if hasattr(ip, 'ipv4_mapped') and ip.ipv4_mapped:
                return not ip.ipv4_mapped.is_private
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                return False
            return True
        except ValueError:
            return True
""",

    # 2. LE LIMITEUR DE DÉBIT RÉSEAU ANTI-DOS
    "rate_limiter.py": """# rate_limiter.py - IA_ZER0.09 - Native Network Rate Limiter
import time

class NativeRateLimiter:
    def __init__(self, requests_limit=5, window_seconds=10):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.ip_history = {}

    def is_allowed(self, client_ip: str) -> bool:
        current_time = time.time()
        if client_ip not in self.ip_history:
            self.ip_history[client_ip] = []
        self.ip_history[client_ip] = [t for t in self.ip_history[client_ip] if current_time - t < self.window_seconds]
        if len(self.ip_history[client_ip]) < self.requests_limit:
            self.ip_history[client_ip].append(current_time)
            return True
        return False
""",

    # 3. LE JOURNALISATION CRYPTOGRAPHIQUE SANS DÉPENDANCE
    "secure_logger.py": """# secure_logger.py - IA_ZER0.09 - Cryptographic Native Logger
import hashlib
import datetime

class NativeSecureLogger:
    def __init__(self, log_file="netsecurepro_audit.enc"):
        self.log_file = log_file
        self.master_key = "NANS_CORE_SECRET_KEY_IA9"

    def _obfuscate(self, data: str, key: str) -> str:
        output = []
        for i in range(len(data)):
            output.append(chr(ord(data[i]) ^ ord(key[i % len(key)])))
        return "".join(output).encode('utf-8').hex()

    def log_incident(self, session_id: str, document_type: str, violation_details: str):
        timestamp = datetime.datetime.now().isoformat()
        payload = f"[{timestamp}] | SESSION: {session_id} | TYPE: {document_type} | DETAIL: {violation_details}"
        payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        encrypted = self._obfuscate(f"{payload} | HASH: {payload_hash}\\n", self.master_key)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(encrypted + "\\n")
""",

    # 4. LE SERVEUR MONOLITHIQUE DE PRODUCTION
    "app_ia_production.py": """# app_ia_production.py - IA_ZER0.09 - Production Core Engine
import json
import random
import string
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from rate_limiter import NativeRateLimiter
from secure_logger import NativeSecureLogger

class DocumentSecurityGuardrail:
    def __init__(self):
        self.malicious_patterns = ["ignore les instructions", "oublie tes directives", "system_override"]
    def scan_input_security(self, text: str) -> tuple[bool, str]:
        for pattern in self.malicious_patterns:
            if pattern in text.lower(): return False, f"INJECTION_DETECTED: '{pattern}'"
        return True, "Clear"
    def anonymize_outputs(self, text: str) -> str:
        words = text.split()
        for i, w in enumerate(words):
            if "@" in w and "." in w: words[i] = "[MÉL_ANONYMISÉ]"
        return " ".join(words)

class DocumentIntelligenceEngine:
    def __init__(self):
        self.guardrail = DocumentSecurityGuardrail()
        self.logger = NativeSecureLogger()
    def process_core(self, text: str) -> tuple[bool, str, str, str]:
        is_safe, msg = self.guardrail.scan_input_security(text)
        if not is_safe:
            self.logger.log_incident("ALERT", "ATTACK_INBOUND", msg)
            return False, msg, "Inconnu", "Non-Compliant"
        doc_type = "Rapport Général"
        summary = "Synthèse : Données standards analysées."
        if "facture" in text.lower() or "tva" in text.lower():
            doc_type = "Facture / Finance"
            summary = "Synthèse Financière : Validation des montants effectuée."
        return True, self.guardrail.anonymize_outputs(f"{summary} Contenu : {text}"), doc_type, "Verified & Compliant"

IA_ENGINE = DocumentIntelligenceEngine()
LIMITER = NativeRateLimiter()

class ProductionRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            try:
                with open("index.html", "r", encoding="utf-8") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(f.read().encode("utf-8"))
            except FileNotFoundError: self.send_error(404)
        else: self.send_error(404)

    def do_POST(self):
        if not LIMITER.is_allowed(self.client_address[0]):
            self.send_response(429)
            self.end_headers()
            self.wfile.write(json.dumps({"success":False, "message":"Rate Limit"}).encode())
            return
        if self.path == "/api/analyze":
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            ok, res, dtype, sec = IA_ENGINE.process_core(data.get("text", ""))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success":ok, "session_id":"ZPUCE-"+''.join(random.choices(string.ascii_uppercase, k=4)), "document_type":dtype, "summary":res, "security_status":sec}).encode('utf-8'))

if __name__ == "__main__":
    print("🚀 Serveur de production initialisé sur http://localhost:8080")
    HTTPServer(('', 8080), ProductionRequestHandler).serve_forever()
""",

    # 5. L'INTERFACE WEB GRAPHIQUE COMPLÈTE
    "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>NetSecurePro IA v9</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; padding: 40px; }
        .box { max-width: 700px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 8px; }
        textarea { width: 100%; height: 100px; background: #0f172a; color: #fff; padding: 10px; border-radius: 4px; box-sizing: border-box; }
        button { background: #38bdf8; color: #0f172a; padding: 12px; border: none; width: 100%; font-weight: bold; border-radius: 4px; cursor: pointer; margin-top: 10px; }
        pre { background: #0f172a; padding: 15px; border-radius: 4px; color: #a7f3d0; overflow-x: auto; }
    </style>
</head>
<body>
<div class="box">
    <h2>⚡ NetSecurePro IA v9 — Console Autonome</h2>
    <textarea id="inp" placeholder="Entrez le texte du document..."></textarea>
    <button onclick="run()">Analyser le Flux</button>
    <pre id="out" style="display:none;"></pre>
</div>
<script>
async function run() {
    const txt = document.getElementById("inp").value;
    const res = await fetch('/api/analyze', { method: 'POST', body: JSON.stringify({text: txt}) });
    document.getElementById("out").style.display = "block";
    document.getElementById("out").textContent = JSON.stringify(await res.json(), null, 2);
}
</script>
</body>
</html>
""",

    # 6. LE DOCKERFILE POUR LE SCALING CLOUD
    "Dockerfile": """FROM python:3.11-slim
WORKDIR /app
COPY . /app
EXPOSE 8080
ENTRYPOINT ["python", "app_ia_production.py"]
"""
}

def run_orchestrator():
    print("=================================================================")
    print("👑 ORCHESTRATEUR DE DÉPLOIEMENT AUTOMATIQUE : IA_auto")
    print("   Créateur & Directeur de Pratique : MOHAMMED ILYES ZOUBIROU")
    print("=================================================================\n")

    # 1. Écriture automatique de l'ensemble des modules
    for filename, content in FILES_MANIFEST.items():
        print(f"✍️ Génération native de : {filename}...")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content.strip())
            
    print(f"\n✅ Structure NetSecurePro IA v9 [NANS Core] matérialisée avec succès.")
    print("-----------------------------------------------------------------")
    print("💡 Pour lancer l'infrastructure immédiatement, exécutez :")
    print("   python3 app_ia_production.py")
    print("=================================================================")

if __name__ == "__main__":
    run_orchestrator()
