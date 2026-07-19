# =================================================================
# ipv6_guard.py - IA_ZER0.09 - Anti-SSRF Network Validator
# Version pure Python standard - Zéro dépendance (No-pip)
# =================================================================

import ipaddress
from urllib.parse import urlparse

class RAGNetworkGuardrail:
    """Pare-feu réseau natif contre les attaques SSRF par évasion IPv4/IPv6"""
    
    @staticmethod
    def is_safe_url(url: str) -> bool:
        """
        Détermine si l'URL ciblée par le module RAG pointe vers l'internet public.
        Bloque impérativement les segments locaux, privés et mappés.
        """
        try:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            if not host:
                return False
                
            # Nettoyage des formats enveloppés IPv6 (ex: [::1])
            host = host.strip("[]")
            
            # Résolution/Analyse de l'objet IP natif via la bibliothèque standard
            ip = ipaddress.ip_address(host)
            
            # 1. Interception des adresses IPv4-mapped IPv6 (ex: ::ffff:10.0.0.1)
            if hasattr(ip, 'ipv4_mapped') and ip.ipv4_mapped:
                # Extraction et vérification de l'adresse IPv4 encapsulée
                return not ip.ipv4_mapped.is_private
                
            # 2. Vérification des plages réservées, privées, loopback et link-local
            if (ip.is_private or 
                ip.is_loopback or 
                ip.is_link_local or 
                ip.is_reserved or 
                ip.is_multicast):
                return False
                
            return True
            
        except ValueError:
            # Si l'hôte est un nom de domaine (ex: entreprise.local), la validation 
            # doit être couplée à une résolution DNS stricte avant l'appel HTTP.
            return True
          
