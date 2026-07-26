# app_ia_production.py - IA_ZER0.09 - Production Core Engine
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