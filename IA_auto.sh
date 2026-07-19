# -----------------------------------------------------------------
# 5. GÉNÉRATION DE L'INTERFACE INTERACTIVE (INDEX.HTML)
# -----------------------------------------------------------------
echo -e "📦 Écriture de : ${BOLD}index.html${NC}..."
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>NetSecurePro IA v9 — Console Autonome Z-CORE</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; padding: 40px; margin: 0; }
        .box { max-width: 800px; margin: 0 auto; background: #1e293b; padding: 32px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        h2 { color: #38bdf8; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 12px; }
        textarea { width: 100%; height: 140px; background: #0f172a; color: #fff; padding: 14px; border-radius: 8px; border: 1px solid #475569; box-sizing: border-box; font-family: monospace; font-size: 14px; }
        textarea:focus { border-color: #38bdf8; outline: none; }
        button { background: #38bdf8; color: #0f172a; padding: 14px; border: none; width: 100%; font-weight: bold; cursor: pointer; margin-top: 15px; border-radius: 8px; font-size: 15px; transition: opacity 0.2s; }
        button:hover { opacity: 0.9; }
        pre { background: #0f172a; padding: 20px; border-radius: 8px; color: #a7f3d0; overflow-x: auto; margin-top: 25px; border: 1px solid #334155; font-family: monospace; font-size: 13px; line-height: 1.5; }
    </style>
</head>
<body>
<div class="box">
    <h2>⚡ NetSecurePro IA v9 — Console Autonome Z-CORE</h2>
    <p style="color:#94a3b8; font-size:14px; margin-bottom:20px;">Soumettez vos flux de documents textuels pour exécution des filtres logiques, des guardrails et de l'anonymisation.</p>
    <textarea id="inp" placeholder="Entrez le texte du document (Ex: Facture #102. Contact: admin@secure.local. TVA: 20%)..."></textarea>
    <button onclick="run()">Analyser le Document</button>
    <pre id="out" style="display:none;"><code id="code_out"></code></pre>
</div>
<script>
async function run() {
    const txt = document.getElementById("inp").value;
    if(!txt.trim()) return;
    try {
        const res = await fetch('/api/analyze', { 
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({text: txt}) 
        });
        document.getElementById("out").style.display = "block";
        document.getElementById("code_out").textContent = JSON.stringify(await res.json(), null, 2);
    } catch(e) {
        alert("Erreur de communication avec le serveur Z-CORE.");
    }
}
</script>
</body>
</html>
EOF

# -----------------------------------------------------------------
# 6. SÉCURISATION DES PERMISSIONS & VÉRIFICATION COMPILATION
# -----------------------------------------------------------------
echo -e "\n⚙️  Vérification de la syntaxe et compilation du code..."
python3 -m py_compile app_ia_production.py ipv6_guard.py rate_limiter.py secure_logger.py

echo -e "\n${GREEN}${BOLD}✔ ÉCOSYSTÈME IA_ZER0 DÉPLOYÉ AVEC SUCCÈS !${NC}"
echo -e "${CYAN}-----------------------------------------------------------------${NC}"
echo -e "Tous les modules natifs ont été générés sans dépendances tierces."
echo -e "Pour démarrer votre serveur de service immédiatement, exécutez :"
echo -e "👉 ${BOLD}python3 app_ia_production.py${NC}"
echo -e "${CYAN}=================================================================${NC}"
