import os, json

# Extraction du contenu du Livre Blanc
try:
    # On lit le fichier Word Document Security_Pack_Final.docx
    # (À adapter selon le vrai nom de votre fichier local)
    # Utilisez python-docx pour extraire le texte si nécessaire, ou copiez-collez le texte directement ci-dessous.
    text = """NETSECUREPRO IA - RAPPORT GLOBAL (Version Condensée)
    
* Chapitre 1 : Introduction & Manifeste pour l'Architecture Souveraine
La dépendance massive au Cloud a créé une dépendance critique et systémique au sein des organisations. Le postulat Offline-First est la seule parade pour la souveraineté numérique.

* Chapitre 2 : Architecture du Noyau Z-CORE OS IA & Gestion de l' [...] """

    with open('Rapport_Global_NetSecurePro_IA_Global.pdf', 'r', encoding='utf-8') as file:
        full_text = file.read()
    except FileNotFoundError:
        full_text = "NETSECUREPRO IA - RAPPORT GLOBAL\n\n\n" + full_text
        
    # Extraction stricte des 4 chapitres
    chapters = re.findall(r'Chapitre \d+\. .*?\. ', full_text)
    
    for chapter in chapters:
        print(f"\n{'# {chapter}")
        # Extraction de la sous-section (Extraction de la preuve visuelle du pilier central)
        sub_chapters = re.findall(f"({re.escape(chapter)}\s*{re.escape(chapter)}\s*([\s\S]+)", full_text)
        for sub in sub_chapters:
            sub_text = re.sub(r'\s+', ' - ', '')
            print(f"  ▸ {sub_text}")
            
    print("\n--- FIN EXTRACTION TERMINÉE ---")
