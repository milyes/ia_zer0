# =================================================================
# test_ssrf.py - NetSecurePro IA v9 - Validation de Preuve 
# Version pure Python standard - Zéro dépendance (No-pip)
# =================================================================

import ipaddress
from urllib.parse import urlparse

# --- 1. LE CODE VULNÉRABLE STANDARD (Ce que la majorité de la Tech utilise) ---
def validateur_standard_entreprise(url: str) -> bool:
    """Validateur classique basé sur des chaînes de caractères (Sceptique & Faible)"""
    try:
        host = urlparse(url).hostname
        if not host:
            return False
            
        # Filtre naïf : l'ingénieur bloque les syntaxes locales évidentes
        liste_noire = ["127.0.0.1", "localhost", "::1"]
        if host in liste_noire:
            return False # Bloqué
            
        return True # Autorisé (Laisse passer l'évasion IPv6 mappée)
    except Exception:
        return False

# --- 2. LA SÉCURITÉ NETSECUREPRO (L'approche IA_ZER0 de Mohammed Ilyes Zoubirou) ---
def validateur_expert_netsecurepro(url: str) -> bool:
    """Validateur de niveau recherche binarisant les adresses IP (Étanche)"""
    try:
        host = urlparse(url).hostname
        if not host:
            return False
            
        # Nettoyage des crochets IPv6
        host = host.strip("[]")
        
        # Binarisation et analyse stricte via ipaddress
        ip = ipaddress.ip_address(host)
        
        # Interception immédiate des formats IPv4-mapped IPv6 (ex: ::ffff:127.0.0.1)
        if hasattr(ip, 'ipv4_mapped') and ip.ipv4_mapped:
            return not ip.ipv4_mapped.is_private
            
        # Interception des plages privées, de boucles et réservées
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            return False
            
        return True
    except Exception:
        return False

# --- 3. EXÉCUTION DU CHOC DE LA DÉMONSTRATION EN DIRECT ---
def executer_demo_technique():
    # Payload d'attaque : Une adresse IPv4 privée encapsulée dans une notation IPv6
    payload_evasion_ssrf = "http://[::ffff:127.0.0.1]/v1/metadata"
    
    print("=================================================================")
    print("🔥 SIMULATION DE SÉCURITÉ CYBER-IA : AUDIT EMAC/IPV6 RAG")
    print("=================================================================\n")
    print(f"Payload d'attaque soumis au pipeline RAG : {payload_evasion_ssrf}\n")
    
    # Étape A : Test du système du client
    resultat_client = validateur_standard_entreprise(payload_evasion_ssrf)
    print("❌ Test du validateur standard de l'entreprise :")
    if resultat_client:
        print("   --> [VULNÉRABLE] : L'URL a été AUTORISÉE. Le RAG va exécuter la requête interne.")
    else:
        print("   --> [SÉCURISÉ] : L'attaque a été interceptée.")
        
    print("\n-----------------------------------------------------------------\n")
    
    # Étape B : Test de la barrière NetSecurePro (IA_ZER0)
    resultat_netsecurepro = validateur_expert_netsecurepro(payload_evasion_ssrf)
    print("🛡️ Test du validateur expert NetSecurePro IA v9 :")
    if resultat_netsecurepro:
        print("   --> [VULNÉRABLE] : L'URL a été autorisée.")
    else:
        print("   --> [SÉCURISÉ] : L'attaque par évasion IPv6 a été BLOQUÉE instantanément.")
    print("=================================================================")

if __name__ == "__main__":
    executer_demo_technique()
  
