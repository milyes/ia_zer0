#!/usr/bin/env python3
import re

file_path = "app_ia_production.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_patterns = '''patterns_evasion = [r'\\[::ffff:127\\.', r'\\[::1\\]', r'127\\.0\\.0\\.1']'''

new_patterns = '''patterns_evasion = [
    # Loopback
    r'::ffff:127\\.',
    r'\\[::ffff:127\\.',
    r'::1',
    r'\\[::1\\]',
    r'127\\.0\\.0\\.1',
    
    # Cloud Metadata (Azure / AWS)
    r'::ffff:169\\.254\\.',
    r'\\[::ffff:169\\.254\\.',
    r'169\\.254\\.169\\.254',
    
    # Private ranges
    r'::ffff:10\\.',
    r'\\[::ffff:10\\.',
    r'::ffff:192\\.168\\.',
    r'\\[::ffff:192\\.168\\.',
    r'::ffff:172\\.(1[6-9]|2[0-9]|3[0-1])\\.',
    r'\\[::ffff:172\\.(1[6-9]|2[0-9]|3[0-1])\\.',
    
    # Link-local
    r'fe80:',
    r'\\[fe80:',
]'''

if old_patterns in content:
    content = content.replace(old_patterns, new_patterns)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Patch appliqué avec succès !")
    print("→ patterns_evasion a été mis à jour.")
else:
    print("⚠️  Ancien pattern non trouvé exactement.")
    print("→ Affichage des lignes contenant 'patterns_evasion' :")
    for i, line in enumerate(content.splitlines(), 1):
        if "patterns_evasion" in line:
            print(f"Ligne {i}: {line.strip()}")
