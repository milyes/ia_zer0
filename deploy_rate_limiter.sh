#!/bin/bash
set -e

echo -e "\033[1;34m[*] Déploiement du limiteur de trafic autonome (rate_limiter.py)...\033[0m"

cat << 'INNER_EOF' > rate_limiter.py
import time

class TokenBucketRateLimiter:
    def __init__(self, capacite_max=5, taux_recharge_seconde=1.0):
        # Configuration des limites du compartiment de jetons
        self.capacite_max = float(capacite_max)
        self.taux_recharge_seconde = float(taux_recharge_seconde)
        self.jetons_actuels = float(capacite_max)
        self.dernier_check = time.time()

    def consommer_jeton(self):
        # Algorithme de calcul du compartiment glissant sans persistance externe
        maintenant = time.time()
        temps_ecoule = maintenant - self.dernier_check
        self.dernier_check = maintenant

        # Recharge des jetons proportionnellement au temps écoulé
        self.jetons_actuels = min(
            self.capacite_max, 
            self.jetons_actuels + (temps_ecoule * self.taux_recharge_seconde)
        )

        # Validation de l'accès
        if self.jetons_actuels >= 1.0:
            self.jetons_actuels -= 1.0
            return True, "Requête autorisée."
        return False, "ALERTE TRAFIC : Débit maximal dépassé. Requête rejetée par rate_limiter.py."

def executer_test_limiteur():
    limiter = TokenBucketRateLimiter(capacite_max=3, taux_recharge_seconde=0.5)
    print("=====================================================================")
    print("⏱️ NETSECUREPRO IA V9 - TEST DE CHARGE DU NOYAU [RATE_LIMITER]")
    print("Validation de la résilience anti-DoS locale")
    print("=====================================================================")
    
    # Simulation d'un bombardement de 5 requêtes instantanées (Capacité max = 3)
    for i in range(1, 6):
        autorise, message = limiter.consommer_jeton()
        statut_visuel = f"\033[1;32m[OK]\033[0m" if autorise else f"\033[1;31m[REJETÉ]\033[0m"
        print(f"Requête #{i} -> {statut_visuel} : {message}")
        time.sleep(0.1) # Rafale rapide
        
    print("=====================================================================")

if __name__ == "__main__":
    executer_test_limiteur()
INNER_EOF

python3 rate_limiter.py
