# À insérer au début des imports de app_ia_production.py
from secure_logger import NativeSecureLogger

# Instanciation du logger dans votre classe AzureCustomSkillEngine ou DocumentIntelligenceEngine
class DocumentIntelligenceEngine:
    def __init__(self):
        self.guardrail = DocumentSecurityGuardrail()
        self.audit_logger = NativeSecureLogger() # <-- Injection du composant crypto

    def process_core(self, input_text: str) -> tuple[bool, str, str, str]:
        is_safe, alert_msg = self.guardrail.scan_input_security(input_text)
        
        if not is_safe:
            # Enregistrement immédiat et silencieux de l'attaque sur le disque avant de couper le flux
            session_id = "ALERT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.audit_logger.log_incident(session_id, "ATTACK_INBOUND", alert_msg)
            return False, alert_msg, "Inconnu", "Non-Compliant"
            
        # ... Reste du code inchangé ...
      
from ipv6_guard import RAGNetworkGuardrail

# Au sein de votre route ou fonction d'extraction Web RAG :
def extraire_contenu_web_rag(url_cible: str):
    # Interception de sécurité immédiate avant émission du moindre paquet réseau
    if not RAGNetworkGuardrail.is_safe_url(url_cible):
        return {
            "success": False, 
            "error": "NETWORK_VIOLATION", 
            "message": "Accès refusé : L'adresse IP ciblée fait partie d'un segment réseau privé."
        }
        
    # ... Poursuite sécurisée de la requête HTTP vers le Web Public ...
    
