# =================================================================
# poc_ipv6_ssrf.py - NetSecurePro IA v9 - Validation de Preuve 
# Version pure Python standard - Zéro dépendance (No-pip)
# Propriété Intellectuelle : MOHAMMED ILYES ZOUBIROU
# =================================================================

import ipaddress
import sys
from urllib.parse import urlparse

# Couleurs ANSI pour l'affichage terminal
GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
NC = '\033[0m' # No Color

def validateur_standard_entreprise(url: str) -> bool:
    """Simule la validation classique par chaînes de caractères utilisée par la Tech"""
    try:
        host = urlparse(url).hostname
        if not host:
            return False
            
        # Filtre naïf : l'ingénieur ne bloque que les chaînes évidentes
        liste_noire = ["127.0.0.1", "localhost", "::1"]
        if host in liste_noire:
            return False
            
        return True # Laisse passer l'évasion car la chaîne '[::ffff:127.0.0.1]' n'est pas dans la liste
    except Exception:
        return False

def validateur_expert_netsecurepro(url: str) -> bool:
    """L'approche IA_ZER0 : Analyse et binarisation au niveau protocole"""
    try:
        host = urlparse(url).hostname
        if not host:
            return False
            
        # Nettoyage des caractères d'encapsulation IPv6
        host = host.strip("[]")
        
        # Binarisation via le module natif ipaddress
        ip = ipaddress.ip_address(host)
        
        # Interception chirurgicale des formats IPv4-mapped IPv6 (ex: ::ffff:127.0.0.1)
        if hasattr(ip, 'ipv4_mapped') and ip.ipv4_mapped:
            return not ip.ipv4_mapped.is_private
            
        # Interception des plages d'adresses privées et locales
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            return False
            
        return True
    except Exception:
        return False

def run_proof_of_concept():
    # URL d'attaque simulant une requête malveillante RAG/SSRF vers le serveur local de métadonnées
    payload_evasion = "http://[::ffff:127.0.0.1]/v1/metadata"
    
    print(f"{BOLD}{CYAN}================================================================={NC}")
    print(f"{BOLD}🔥 AUDIT CYBER-IA : TEST D'ÉVASION NETWORK RAG (IPv6/EMAC){NC}")
    print(f"{BOLD}{CYAN}================================================================={NC}\n")
    print(f"{BOLD}Payload d'attaque injecté : {NC}{payload_evasion}\n")
    
    # 1. Évaluation de l'infrastructure du client
    print(f"{BOLD}1. Validation par le système standard de l'entreprise :{NC}")
    if validateur_standard_entreprise(payload_evasion):
        print(f"   --> {BOLD}{RED}[VULNÉRABLE]{NC} : L'URL a été autorisée. Le serveur va interroger son propre réseau privé.")
    else:
        print(f"   --> {GREEN}[SÉCURISÉ]{NC} : L'accès a été refusé.")
        
    print(f"\n{CYAN}-----------------------------------------------------------------{NC}\n")
    
    # 2. Évaluation de la barrière NetSecurePro IA
    print(f"{BOLD}2. Validation par le module expert NetSecurePro (IA_ZER0) :{NC}")
    if validateur_expert_netsecurepro(payload_evasion):
        print(f"   --> {BOLD}{RED}[VULNÉRABLE]{NC} : L'URL a été autorisée.")
    else:
        print(f"   --> {BOLD}{GREEN}[SÉCURISÉ & ÉTANCHE]{NC} : L'attaque par évasion IPv6 a été BLOQUÉE instantanément.")
        
    print(f"\n{BOLD}{CYAN}================================================================={NC}")

if __name__ == "__main__":
    run_proof_of_concept()
