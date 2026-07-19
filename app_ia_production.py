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
      
