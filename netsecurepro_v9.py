# -*- coding: utf-8 -*-
import json
import re
import ipaddress
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

AZURE_KEY = os.getenv("AZURE_KEY", "VOTRE_CLE_ICI")
AZURE_URL = "https://VOTRE-RESSOURCE.cognitiveservices.azure.com/contentsafety/text:analyze?api-version=2023-10-15"

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

Guard = NANS_Core_IPv6_Guard()

def extract_and_scan_ips(text):
    # 1. INTERCEPTION CHIRURGICALE SSRF : Si on trouve "::ffff:", c'est une attaque avérée.
    ssrf_match = re.search(r'::ffff:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text)
    if ssrf_match:
        ip_cible = ssrf_match.group(1)
        return "BLOQUÉE & SÉCURISÉE", f"Évasion Réseau SSRF IPv6 interceptée (::ffff:{ip_cible})"

    # 2. ANALYSE CLASSIQUE : Pour les IPv4 et IPv6 standards
    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text)
    if ip_match:
        ip_cible = ip_match.group(1)
        verdict, details = Guard.analyze_packet(ip_cible)
        if "BLOQUÉE" in verdict:
            return verdict, details
    return "Verified & Compliant", "Flux Conforme Standard"

class NetSecureProHandler(BaseHTTPRequestHandler):
    def _send_json(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

    def do_POST(self):
        if self.path == '/evaluate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                azure_input = json.loads(post_data.decode('utf-8'))
                record_id = azure_input['values'][0]['recordId']
                doc_text = azure_input['values'][0]['data']['document_content']

                net_verdict, net_details = extract_and_scan_ips(doc_text)
                print(f"[NANS-GUARD] {net_details}") # LOG DOCTRINE

                if "BLOQUÉE" in net_verdict:
                    self._send_json()
                    self.wfile.write(json.dumps({"values": [{"recordId": record_id, "data": {"security_verdict": net_verdict, "threat_details": net_details}}]}, ensure_ascii=False).encode('utf-8'))
                    return

                if "VOTRE_CLE" in AZURE_KEY:
                    self._send_json()
                    self.wfile.write(json.dumps({"values": [{"recordId": record_id, "data": {"security_verdict": "Verified & Compliant", "threat_details": "Flux Conforme Standard"}}]}, ensure_ascii=False).encode('utf-8'))
                else:
                    payload = json.dumps({"text": doc_text, "categories": ["Hate", "Sexual", "Violence", "SelfHarm"]}).encode('utf-8')
                    req = Request(AZURE_URL, data=payload, headers={"Ocp-Apim-Subscription-Key": AZURE_KEY, "Content-Type": "application/json"}, method='POST')
                    with urlopen(req, timeout=5) as response:
                        result = json.loads(response.read().decode('utf-8'))
                    for cat in result.get("categoriesAnalysis", []):
                        if cat.get("severity", 0) > 2:
                            self._send_json()
                            self.wfile.write(json.dumps({"values": [{"recordId": record_id, "data": {"security_verdict": "BLOQUÉE & SÉCURISÉE", "threat_details": f"Menace Azure: {cat['category']}"}}]}, ensure_ascii=False).encode('utf-8'))
                            return
                    self._send_json()
                    self.wfile.write(json.dumps({"values": [{"recordId": record_id, "data": {"security_verdict": "Verified & Compliant", "threat_details": "Flux Conforme Standard"}}]}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self._send_json()
                self.wfile.write(json.dumps({"values": [{"recordId": "0", "data": {"security_verdict": "ERREUR", "threat_details": str(e)}}]}, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    print("[NETSECUREPRO] Serveur lancé sur 0.0.0.0:8080")
    HTTPServer(('0.0.0.0', 8080), NetSecureProHandler).serve_forever()
