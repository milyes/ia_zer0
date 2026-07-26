# ipv6_guard.py - IA_ZER0.09 - Anti-SSRF Network Validator
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