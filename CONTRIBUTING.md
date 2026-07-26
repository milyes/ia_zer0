# Contribution à IA_ZER0 (NANS Core)

Merci de l'intérêt que vous portez au projet IA_ZER0 ! Pour maintenir la qualité industrielle de ce dépôt, toutes les contributions doivent respecter des critères stricts.

## 🚫 La Règle d'Or : Zéro Dépendance

Toute Pull Request (PR) introduisant une modification ou un ajout dans le gestionnaire de paquets (`pip`, `requirements.txt`, etc.) sera **immédiatement rejetée**. 

Toute logique métier, de sécurité ou réseau doit être codée exclusivement avec les modules natifs de la **bibliothèque standard de Python**.

## 🛠️ Processus de Soumission

1. **Fork & Branch** : Créez une branche thématique descriptive à partir de la branche `main` (ex: `feature/anti-jailbreak-regex`).
2. **Qualité du code** : Assurez-vous que votre code respecte les standards PEP 8 et qu'il n'augmente pas la latence du noyau au-delà de 0.05 ms.
3. **Tests locaux** : Exécutez le cahier de recette décrit dans le `README.md` pour valider l'étanchéité des filtres avant de soumettre.
4. **Pull Request** : Décrivez précisément le gain en sécurité ou en performance apporté par votre modification.

## ⚖️ Alignement Juridique

En soumettant une contribution, vous acceptez que votre code soit placé sous la licence MIT du projet.
