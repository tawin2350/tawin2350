"""Fetch real GitHub data and redraw assets/stats-en.svg + stats-th.svg (run by GitHub Actions)."""
import json, os, sys, urllib.request, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design import stats_cards
USER = os.environ.get("GH_USER", "tawin2350")
Q = """query($u:String!){user(login:$u){
 repositories(ownerAffiliations:OWNER,first:100,isFork:false){totalCount nodes{stargazerCount
  languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
 contributionsCollection{totalCommitContributions contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
req = urllib.request.Request("https://api.github.com/graphql",
    data=json.dumps({"query": Q, "variables": {"u": USER}}).encode(),
    headers={"Authorization": f"bearer {os.environ['GH_TOKEN']}", "Content-Type": "application/json"})
res = json.load(urllib.request.urlopen(req))
if "errors" in res: sys.exit(res["errors"])
u = res["data"]["user"]; repos = u["repositories"]
langs = collections.defaultdict(lambda: [0, "#7D8590"])
for r in repos["nodes"]:
    for e in r["languages"]["edges"]:
        langs[e["node"]["name"]][0] += e["size"]; langs[e["node"]["name"]][1] = e["node"]["color"] or "#7D8590"
ranked = sorted(langs.items(), key=lambda x: -x[1][0])
top = [(n, c, s) for n, (s, c) in ranked[:3]]
rest = sum(s for _, (s, _) in ranked[3:])
if rest: top.append(("Other", "#7D8590", rest))
if not top: top = [("None", "#7D8590", 1)]
today = datetime.date.today().isoformat()
days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"] if d["date"] <= today]
streak = 0
for d in reversed(days):
    if d["contributionCount"] > 0: streak += 1
    elif d["date"] != today: break
monthly = collections.OrderedDict()
for d in days: monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["contributionCount"]
data = dict(commits=u["contributionsCollection"]["totalCommitContributions"],
            monthly=(list(monthly.values())[-12:] or [0, 0]), streak=streak,
            days=[1 if d["contributionCount"] else 0 for d in days[-14:]],
            repos=repos["totalCount"], stars=sum(r["stargazerCount"] for r in repos["nodes"]), langs=top)
if max(data["monthly"]) == 0: data["monthly"] = [m + 1 for m in data["monthly"]]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
for lang in ("en", "th"):
    open(os.path.join(out, f"stats-{lang}.svg"), "w").write(stats_cards(lang, data))
print("updated", {k: v for k, v in data.items() if k not in ("monthly", "days")})
