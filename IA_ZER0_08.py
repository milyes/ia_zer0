#=================================================================
# IA_ZER0.08.py - NetSecurePro IA - NANS Core + SSRF IPv6 Guard
# Pure Python + Détection prioritaire ::ffff: + Azure Content Safety
# Écoute uniquement sur localhost (127.0.0.1)
# =================================================================

import json
import re
import ipaddress
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# === CONFIGURATION ===
HOST = "127.0.0.1"
PORT = 8080
AZURE_KEY = "VOTRE_CLE_ICI"
AZURE_URL = "https://VOTRE-RESSOURCE.cognitiveservices.azure.com/contentsafety/text:analyze?api-version=2023-10-15"
MAX_PAYLOAD_SIZE = 100 * 1024

class NANS_Core_IPv6_Guard:
    def analyze_packet(self, raw_ip_str):
        if not raw_ip_str:
            return "Verified & Compliant", "Aucune IP"
        raw_ip_str = raw_ip_str.strip(".,;:()'\" ")
        try:
            ip_obj = ipaddress.ip_address(raw_ip_str)
            if isinstance(ip_obj, ipaddress.IPv4Address):
                if ip_obj.is_private or ip_obj.is_loopback or str(ip_obj).startswith("169.254."):
                    return "BLOQUÉE & SÉCURISÉE", f"Accès réseau interne bloqué ({ip_obj})"
            elif isinstance(ip_obj, ipaddress.IPv6Address):
                if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
                    return "BLOQUÉE & SÉCURISÉE", f"Accès réseau interne bloqué ({ip_obj})"
        except ValueError:
            pass
        return "Verified & Compliant", "Flux Conforme Standard"


def extract_and_scan_ips(text: str):
    # Détection prioritaire du vecteur ::ffff:
    ssrf_match = re.search(r'::ffff:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text, re.IGNORECASE)
    if ssrf_match:
        ip_cible = ssrf_match.group(1)
        return "BLOQUÉE & SÉCURISÉE", f"Évasion Réseau SSRF IPv6 interceptée (::ffff:{ip_cible})"
    
    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text)
    if ip_match:
        ip_cible = ip_match.group(1)
        guard = NANS_Core_IPv6_Guard()
        verdict, details = guard.analyze_packet(ip_cible)
        if "BLOQUÉE" in verdict:
            return verdict, details
    return "Verified & Compliant", "Flux Conforme Standard"


class NetSecureProHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        return

    def _send_json(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('X-Powered-By', 'NetSecurePro-NANS-Core')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _send_html(self, html: str, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_GET(self):
        if self.path in ["/", "/health", "/status"]:
            data = {
                "status": "online",
                "service": "NetSecurePro IA_ZER0.08",
                "mode": "Local-first + SSRF Guard (::ffff:)",
                "compliance": "Loi 25 Strict",
                "endpoint": "/evaluate (POST)",
                "timestamp": datetime.datetime.now().isoformat()
            }
            # Réponse JSON propre
            self._send_json(data)
        else:
            self._send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        if self.path != '/evaluate':
            self._send_json({"error": "Endpoint not found"}, 404)
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except ValueError:
            content_length = 0

        if content_length > MAX_PAYLOAD_SIZE:
            self._send_json({"error": "Payload too large"}, 413)
            return

        try:
            post_data = self.rfile.read(content_length)
            azure_input = json.loads(post_data.decode('utf-8'))
            
            record_id = azure_input['values'][0]['recordId']
            doc_text = azure_input['values'][0]['data'].get('document_content', '')

            net_verdict, net_details = extract_and_scan_ips(doc_text)
            
            if "BLOQUÉE" in net_verdict:
                response = {
                    "values": [{
                        "recordId": record_id,
                        "data": {
                            "security_verdict": net_verdict,
                            "threat_details": net_details,
                            "timestamp": datetime.datetime.now().isoformat()
                        }
                    }]
                }
                self._send_json(response)
                return

            if "VOTRE_CLE" in AZURE_KEY or not AZURE_KEY:
                response = {
                    "values": [{
                        "recordId": record_id,
                        "data": {
                            "security_verdict": "Verified & Compliant",
                            "threat_details": "Flux Conforme Standard (Mode Local)",
                            "timestamp": datetime.datetime.now().isoformat()
                        }
                    }]
                }
                self._send_json(response)
                return

            # Azure Content Safety (optionnel)
            payload = json.dumps({
                "text": doc_text,
                "categories": ["Hate", "Sexual", "Violence", "SelfHarm"]
            }).encode('utf-8')

            req = Request(AZURE_URL, data=payload, headers={
                "Ocp-Apim-Subscription-Key": AZURE_KEY,
                "Content-Type": "application/json"
            }, method='POST')

            with urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                for cat in result.get("categoriesAnalysis", []):
                    if cat.get("severity", 0) > 2:
                        resp = {
                            "values": [{
                                "recordId": record_id,
                                "data": {
                                    "security_verdict": "BLOQUÉE & SÉCURISÉE",
                                    "threat_details": f"Menace Azure: {cat['category']}",
                                    "timestamp": datetime.datetime.now().isoformat()
                                }
                            }]
                        }
                        self._send_json(resp)
                        return

            resp = {
                "values": [{
                    "recordId": record_id,
                    "data": {
                        "security_verdict": "Verified & Compliant",
                        "threat_details": "Flux Conforme Standard",
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                }]
            }
            self._send_json(resp)

        except Exception as e:
            self._send_json({
                "values": [{
                    "recordId": "0",
                    "data": {
                        "security_verdict": "ERREUR",
                        "threat_details": str(e)
                    }
                }]
            }, 500)


if __name__ == '__main__':
    print(f"[NetSecurePro] IA_ZER0.08 - NANS Core + SSRF Guard")
    print(f"[NetSecurePro] Écoute sécurisée sur http://{HOST}:{PORT}")
    print(f"[NetSecurePro] Mode : Local-first + Détection ::ffff:")
    print("-" * 60)
    
    server = HTTPServer((HOST, PORT), NetSecureProHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[NetSecurePro] Arrêt sécurisé.")
        server.server_close()
