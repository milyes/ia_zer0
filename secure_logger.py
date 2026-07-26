# secure_logger.py - IA_ZER0.09 - Cryptographic Native Logger
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
        encrypted = self._obfuscate(f"{payload} | HASH: {payload_hash}\n", self.master_key)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(encrypted + "\n")