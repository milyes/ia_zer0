#!/bin/bash
mkdir -p ia_zer0
cd ia_zer0

# 1. INDEX.HTML - Z-CORE v9.2 AVEC NANS INTEGRÉ
cat > index.html << 'EOH'
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Z-CORE v9.2 // NANS SYSTEM LOCAL</title>
<style>
body{background:#000;color:#0f0;font-family:'Courier New',monospace;padding:20px}
.box{border:1px solid #0f0;padding:15px;margin-bottom:10px}
.btn{background:#000;color:#0f0;border:1px solid #0f0;padding:8px 15px;margin:5px;cursor:pointer}
.btn:hover{background:#0f0;color:#000}
.btn-wipe{border-color:#f00;color:#f00}
.btn-wipe:hover{background:#f00;color:#000}
.heap{position:fixed;top:10px;right:10px;font-size:12px;color:#ff0}
.log{font-size:11px;color:#555;margin-top:10px;height:120px;overflow-y:auto;border-top:1px dashed #0f0;padding-top:5px}
</style>
</head>
<body>
<div class="heap" id="heap">HEAP: 0.00 MB</div>
<h1>Z-CORE v9.2 // NANS SYSTEM</h1>
<div class="box">
<div>MODE: SUPER_ZERO_LOCAL | ZERO CLOUD | MAXIMUM ISOLATION</div><hr>
<div>ÉTAT: <span id="state">IDLE</span></div>
<div>UTILISATEURS: <span id="users">[]</span></div>
<div>LOGS NANS: <span id="logs">0</span></div>
<button class="btn" onclick="handleFetch()">LANCER FETCH</button>
<button class="btn" onclick="handleAdd()">AJOUTER AGENT</button>
<button class="btn btn-wipe" onclick="handleWipe()">WIPE MEMORY</button>
<div class="log" id="log"></div>
</div>

<script>
const LocalNansConfig = {mode:"SUPER_ZERO_LOCAL",zeroCloudDependency:true,latencyMs:0,securityLevel:"MAXIMUM_ISOLATION"};
class LocalNeuralCore{constructor(){this.status="OPERATIONAL_LOCAL";this.config=LocalNansConfig;this.memoryLog=[];log("[NANS V9 LOCAL] Core initialized")}
processPrompt(input){const ts=Date.now();log(`[NANS] Executing: ${input}`);this.memoryLog.push(`[${ts}] ${input}`);if(this.memoryLog.length>100)this.memoryLog.shift();return{status:"SUCCESS_ZERO_LATENCY",timestamp:ts,result:`Processed: ${input}`}}
getStatus(){return{status:this.status,logs:this.memoryLog.length}}
purgeMemory(){this.memoryLog=[];log("[NANS] Memory purged. Zero trace.")}}
let context={users:[],loading:false};let state='IDLE';const core=new LocalNeuralCore();
function setState(s){state=s;update()}
function update(){document.getElementById('state').innerText=state;document.getElementById('users').innerText=JSON.stringify(context.users);document.getElementById('logs').innerText=core.getStatus().logs}
function log(msg){const t=new Date().toLocaleTimeString();document.getElementById('log').innerHTML=`[${t}] ${msg}<br>`+document.getElementById('log').innerHTML}
const produce=(base,recipe)=>{const draft=JSON.parse(JSON.stringify(base));recipe(draft);return draft};
function handleFetch(){setState('LOADING');core.processPrompt("FETCH_USERS");setTimeout(()=>{const newUsers=[{id:1,name:'Agent_Alpha'},{id:2,name:'Agent_Beta'}];context.users=produce(context.users,d=>d.push(...newUsers));setState('IDLE');log("Fetch terminé. +2 agents")},1500)}
function handleAdd(){const agent={id:Date.now(),name:'Agent_'+Date.now().toString().slice(-4)};context.users=produce(context.users,d=>d.push(agent));core.processPrompt("ADD_AGENT");update()}
function handleWipe(){context.users=[];core.purgeMemory();setState('IDLE');update()}
setInterval(()=>{if(performance.memory){let mb=(performance.memory.usedJSHeapSize/1024/1024).toFixed(2);document.getElementById('heap').innerText=`HEAP: ${mb} MB`;if(mb>100)document.getElementById('heap').style.color='#f00'}},2000);
update();
</script>
</body>
</html>
EOH

# 2. README.md - DOCTRINE
cat > README.md << 'EOR'
# Z-CORE v9.2 NANS SYSTEM
`MODE: SUPER_ZERO_LOCAL` - 100% Air-Gap

## Spécifications
- **State Machine**: Classe locale sans XState
- **Noyau NANS**: `LocalNeuralCore` JS pur
- **Sécurité**: `MAXIMUM_ISOLATION`, `zeroCloudDependency: true`
- **Dépendances**: 0. Fonctionne offline

## Utilisation
Ouvrir `index.html` dans navigateur. 0 build, 0 serveur.

## Preuve d'exécution
Voir screenshot: 0ms latency, 0 appel externe.
EOR

echo "Dossier ia_zer0 cree avec index.html et README.md"
echo "Prochaine etape: git push vers https://github.com/milyes/ia_zer0"
