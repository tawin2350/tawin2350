"""Generate assets/stats-terminal.svg from real GitHub data (run by GitHub Actions)."""
import json, os, urllib.request, datetime
USER = os.environ.get("GH_USER", "tawin2350")
TOKEN = os.environ["GH_TOKEN"]
Q = """query($u:String!){user(login:$u){
 repositories(ownerAffiliations:OWNER,first:100,isFork:false){totalCount nodes{stargazerCount
  languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
 contributionsCollection{totalCommitContributions contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
req = urllib.request.Request("https://api.github.com/graphql",
    data=json.dumps({"query": Q, "variables": {"u": USER}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
u = json.load(urllib.request.urlopen(req))["data"]["user"]
repos = u["repositories"]; stars = sum(r["stargazerCount"] for r in repos["nodes"])
langs = {}
for r in repos["nodes"]:
    for e in r["languages"]["edges"]:
        n = e["node"]["name"]; langs.setdefault(n, [0, e["node"]["color"] or "#888"]); langs[n][0] += e["size"]
top = sorted(langs.items(), key=lambda x: -x[1][0])[:6]; tot = sum(v[0] for _, v in top) or 1
days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
today = datetime.date.today().isoformat(); streak = 0
for d in reversed(days):
    if d["date"] > today: continue
    if d["contributionCount"] > 0: streak += 1
    elif d["date"] != today: break
commits = u["contributionsCollection"]["totalCommitContributions"]

F = "'JetBrains Mono','Fira Code','Cascadia Code',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
rows = [("OS", "Thailand 🇹🇭 · Thammasat CS"), ("Repos", str(repos["totalCount"])),
        ("Commits", f"{commits:,} this year"), ("Streak", f"🔥 {streak} days"),
        ("Stars", f"★ {stars}"), ("Top lang", " · ".join(n for n, _ in top[:3]) or "-")]
b = []
for rw, l in enumerate(["11111", "00100", "00100", "00100", "00100", "00100"]):
    for c, v in enumerate(l):
        if v == "1":
            b.append(f'<rect x="{50+c*26}" y="{66+rw*26}" width="22" height="22" rx="4" fill="url(#bd)" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{(rw*5+c)*0.04}s" dur=".2s" fill="freeze"/></rect>')
b.append('<text x="115" y="250" text-anchor="middle" class="d" style="font-size:12px">// THIRD</text>')
b.append('<text x="250" y="70"><tspan class="g">third</tspan><tspan class="d">@</tspan><tspan class="p">github</tspan></text><text x="250" y="88" class="d">─────────────────────</text>')
for k, (a, v) in enumerate(rows):
    b.append(f'<text x="250" y="{114+k*24}" opacity="0"><tspan class="k">{a}</tspan><tspan class="d">: </tspan><tspan class="c">{v}</tspan><animate attributeName="opacity" from="0" to="1" begin="{.3+k*.25}s" dur=".3s" fill="freeze"/></text>')
x = 250
for n, (sz, col) in top:
    w = sz / tot * 420
    b.append(f'<rect x="{x:.1f}" y="268" height="10" width="0" fill="{col}"><title>{n}</title><animate attributeName="width" from="0" to="{w:.1f}" begin="1.8s" dur=".8s" fill="freeze"/></rect>'); x += w
b.append('<g transform="translate(250 302)">' + "".join(f'<rect x="{k*24}" width="18" height="12" rx="2" fill="{c}"/>' for k, c in enumerate(["#FF5F57","#FEBC2E","#28C840","#22D3EE","#6366F1","#A855F7","#E2E8F0","#64748B"])) + '</g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 336" width="700" height="336">
<defs><linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06B6D4"/><stop offset=".5" stop-color="#6366F1"/><stop offset="1" stop-color="#A855F7"/></linearGradient></defs>
<style>text{{font-family:{F};font-size:15px}} .p{{fill:#22D3EE}} .c{{fill:#E2E8F0}} .d{{fill:#64748B}} .k{{fill:#C084FC}} .g{{fill:#4ADE80}}</style>
<rect x="1" y="1" width="698" height="334" rx="14" fill="#0B0F17" stroke="url(#bd)" stroke-width="2"/>
<path d="M2 15a13 13 0 0 1 13-13h670a13 13 0 0 1 13 13v23H2z" fill="#161B26"/>
<circle cx="24" cy="21" r="6.5" fill="#FF5F57"/><circle cx="46" cy="21" r="6.5" fill="#FEBC2E"/><circle cx="68" cy="21" r="6.5" fill="#28C840"/>
<text x="350" y="26" text-anchor="middle" style="font-size:13px" class="d">neofetch --github {USER}</text>
{chr(10).join(b)}
</svg>'''
open(os.path.join(os.path.dirname(__file__), "..", "assets", "stats-terminal.svg"), "w").write(svg)
print("ok", repos["totalCount"], commits, streak, stars)
