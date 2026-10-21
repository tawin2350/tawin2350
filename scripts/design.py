import base64, io, os
from fontTools import subset
from fontTools.ttLib import TTFont
FD=os.path.join(os.path.dirname(os.path.abspath(__file__)),"fonts")
def font(path, text):
    f=TTFont(path); o=subset.Options(); o.flavor="woff2"
    s=subset.Subsetter(o); s.populate(text=text); s.subset(f)
    b=io.BytesIO(); f.flavor="woff2"; f.save(b); return base64.b64encode(b.getvalue()).decode()
P={"sg":f"{FD}/space-grotesk-latin-700-normal.woff2",
   "sgm":f"{FD}/space-grotesk-latin-500-normal.woff2",
   "jb":f"{FD}/jetbrains-mono-latin-400-normal.woff2",
   "plx":f"{FD}/ibm-plex-sans-thai-thai-500-normal.woff2",
   "plxl":f"{FD}/ibm-plex-sans-thai-latin-500-normal.woff2"}
def css(svgtext):
    out=[]
    for fam,key in [("SG","sg"),("SGM","sgm"),("JB","jb"),("PLX","plx"),("PLX","plxl")]:
        out.append(f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{font(P[key],svgtext)}) format('woff2')}}")
    return "\n".join(out)
BG="#0D1117"; LINE="#21262D"; MUTED="#7D8590"; TXT="#E6EDF3"; AC="#2DD4BF"; AC2="#A78BFA"; WARM="#F59E0B"
def svg(w,h,body,extra=""):
    raw=body
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<style>{css(raw)}
.sg{{font-family:SG,PLX,sans-serif;font-weight:700}} .sgm{{font-family:SGM,PLX,sans-serif;font-weight:500}} .jb{{font-family:JB,ui-monospace,monospace}} .th{{font-family:PLX,SGM,sans-serif;font-weight:500}}
{extra}</style>
{body}
</svg>'''
def rise(inner,delay=0,dy=14,dur=.8):
    return (f'<g opacity="0" transform="translate(0 {dy})"><animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="{dur}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{delay}s" dur="{dur}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".16 1 .3 1"/>{inner}</g>')
def grid(w,h,step=24,op=.35):
    return f'<defs><pattern id="gd" width="{step}" height="{step}" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{LINE}"/></pattern></defs><rect width="{w}" height="{h}" fill="url(#gd)" opacity="{op}"/>'

# ---------- HERO ----------
def hero(lang):
    th=lang=="th"
    lines=[("whoami","THIRD — computer science student, Thammasat University" if not th else "THIRD — นักศึกษาวิทยาการคอมพิวเตอร์ ม.ธรรมศาสตร์"),
           ("cat focus.txt","full-stack web · AI &amp; automation · web games" if not th else "เว็บ Full-stack · AI และระบบอัตโนมัติ · เกมบนเว็บ"),
           ("ls projects/","spk-watch  greentrip  element-clash  smart-home  pdf-kit")]
    tag="I build web things people actually use." if not th else "ผมชอบทำเว็บที่คนใช้ได้จริงครับ"
    body=f'''<rect width="840" height="400" rx="18" fill="{BG}"/>{grid(840,400)}
<rect x=".5" y=".5" width="839" height="399" rx="18" fill="none" stroke="{LINE}"/>
{rise(f'<text x="48" y="64" class="jb" font-size="12" fill="{MUTED}" letter-spacing="2">PORTFOLIO / 2026</text><text x="792" y="64" class="jb" font-size="12" fill="{MUTED}" text-anchor="end" letter-spacing="2">BANGKOK · TH</text>',0,8)}
<g class="sg" font-size="132" letter-spacing="-4">
<text x="44" y="190" fill="none" stroke="{TXT}" stroke-width="1.2" stroke-dasharray="900" stroke-dashoffset="900">THIRD<animate attributeName="stroke-dashoffset" to="0" dur="1.8s" fill="freeze"/></text>
<text x="44" y="190" fill="{TXT}" opacity="0">THIRD<animate attributeName="opacity" from="0" to="1" begin="1.4s" dur=".8s" fill="freeze"/></text></g>
<rect x="400" y="166" width="16" height="16" fill="{AC}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.8s" dur=".3s" fill="freeze"/></rect>
{rise(f'<text x="48" y="230" class="{"th" if th else "sgm"}" font-size="20" fill="{MUTED}">{tag}</text>',1.2)}
<line x1="48" y1="262" x2="792" y2="262" stroke="{LINE}"/>'''
    y=294; t=2.0
    for i,(c,o) in enumerate(lines):
        w=40+len(c)*8.4
        body+=f'''<clipPath id="k{i}"><rect x="48" y="{y-14}" height="20" width="0"><animate attributeName="width" from="0" to="{w}" begin="{t}s" dur="{.25+len(c)*.03}s" fill="freeze"/></rect></clipPath>
<text x="48" y="{y}" class="jb" font-size="14" clip-path="url(#k{i})"><tspan fill="{AC}">→ </tspan><tspan fill="{TXT}">{c}</tspan></text>
<text x="{48+w+12}" y="{y}" class="{'th' if th and i<2 else 'jb'}" font-size="14" fill="{MUTED}" opacity="0">{o}<animate attributeName="opacity" from="0" to="1" begin="{t+.5+len(c)*.03}s" dur=".4s" fill="freeze"/></text>'''
        y+=28; t+=.9
    body+=f'<rect x="48" y="{y-13}" width="8" height="16" fill="{AC}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'
    return svg(840,400,body)

# ---------- SECTION HEADER ----------
def section(n,en,th_,lang):
    label=en if lang=="en" else th_
    cls="sg" if lang=="en" else "th"
    return svg(840,72,rise(f'''<text x="0" y="30" class="jb" font-size="13" fill="{AC}" letter-spacing="1">{n:02d}</text>
<text x="34" y="32" class="{cls}" font-size="26" fill="{TXT}">{label}</text>
<line x1="0" y1="56" x2="840" y2="56" stroke="{LINE}"/>
<line x1="0" y1="56" x2="0" y2="56" stroke="{AC}" stroke-width="2"><animate attributeName="x2" from="0" to="120" begin=".3s" dur="1s" fill="freeze"/></line>'''))

# ---------- LANGUAGE SWITCH ----------
def switch(active):
    on=lambda x: active==x
    def pill(x,lab,a):
        return f'<rect x="{x}" y="1" width="56" height="30" rx="15" fill="{TXT if a else "none"}"/><text x="{x+28}" y="21" text-anchor="middle" class="jb" font-size="12" fill="{BG if a else MUTED}" letter-spacing="1">{lab}</text>'
    return svg(118,32,f'<rect x=".5" y=".5" width="117" height="31" rx="16" fill="{BG}" stroke="{LINE}"/>'+pill(2,"EN",on("en"))+pill(60,"TH",on("th")))

# ---------- PROJECT CARD ----------
ILL={}
ILL["spk"]=f'''<g stroke="{LINE}">{"".join(f'<path d="M0 {y}H400"/>' for y in range(20,180,24))}{"".join(f'<path d="M{x} 0V180"/>' for x in range(20,400,24))}</g>
<path d="M0 130 Q60 115 120 128 T240 122 T400 126 V180 H0Z" fill="{AC}" opacity=".12"><animate attributeName="d" dur="5s" repeatCount="indefinite" values="M0 130 Q60 115 120 128 T240 122 T400 126 V180 H0Z;M0 124 Q60 136 120 120 T240 132 T400 120 V180 H0Z;M0 130 Q60 115 120 128 T240 122 T400 126 V180 H0Z"/></path>
<path d="M0 130 Q60 115 120 128 T240 122 T400 126" fill="none" stroke="{AC}" stroke-width="1.5"><animate attributeName="d" dur="5s" repeatCount="indefinite" values="M0 130 Q60 115 120 128 T240 122 T400 126;M0 124 Q60 136 120 120 T240 132 T400 120;M0 130 Q60 115 120 128 T240 122 T400 126"/></path>
{"".join(f'<g transform="translate({x} {y})"><circle r="4" fill="{c}"/><circle r="4" fill="none" stroke="{c}"><animate attributeName="r" values="4;18" dur="2s" begin="{d}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="2s" begin="{d}s" repeatCount="indefinite"/></circle></g>' for x,y,c,d in [(110,70,WARM,0),(250,92,AC,.7),(320,52,AC2,1.3)])}
<text x="122" y="66" class="jb" font-size="10" fill="{MUTED}">45cm</text><text x="262" y="88" class="jb" font-size="10" fill="{MUTED}">20cm</text>'''
ILL["green"]=f'''<circle cx="210" cy="90" r="58" fill="none" stroke="{AC}" stroke-dasharray="3 5" opacity=".7"><animateTransform attributeName="transform" type="rotate" from="0 210 90" to="360 210 90" dur="30s" repeatCount="indefinite"/></circle>
<circle cx="210" cy="90" r="58" fill="{AC}" opacity=".06"/>
<path id="rt" d="M40 160 C90 150 100 100 150 96 S200 90 210 90" fill="none" stroke="{TXT}" stroke-width="1.2" stroke-dasharray="2 5" opacity=".6"/>
<circle r="5" fill="{TXT}"><animateMotion dur="5s" repeatCount="indefinite"><mpath href="#rt"/></animateMotion></circle>
<rect x="290" y="40" width="88" height="44" rx="6" fill="none" stroke="{LINE}"/><text x="300" y="58" class="jb" font-size="10" fill="{AC}">CHECK-IN</text><text x="300" y="74" class="jb" font-size="10" fill="{MUTED}">09:42 · photo</text>
<rect x="290" y="96" width="88" height="44" rx="6" fill="none" stroke="{LINE}"/><text x="300" y="114" class="jb" font-size="10" fill="{AC2}">ZONE ENTER</text><text x="300" y="130" class="jb" font-size="10" fill="{MUTED}">gps · live</text>'''
cards=[("#EF4444","FIRE"),("#3B82F6","WATER"),("#22C55E","EARTH"),("#EAB308","VOLT")]
ILL["clash"]="".join(f'''<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="3s" begin="{i*.4}s" repeatCount="indefinite"/>
<g transform="rotate({(i-1.5)*7} {200} 260)"><rect x="{170}" y="30" width="60" height="88" rx="6" fill="{BG}" stroke="{c}" stroke-width="1.5"/>
<path d="M200 56 l12 18 l-12 18 l-12 -18z" fill="none" stroke="{c}" stroke-width="1.5"/><text x="200" y="110" text-anchor="middle" class="jb" font-size="8" fill="{c}" letter-spacing="1">{n}</text></g></g>''' for i,(c,n) in enumerate(cards))+f'<text x="200" y="160" text-anchor="middle" class="jb" font-size="11" fill="{MUTED}" letter-spacing="2">ROOM · 4F7K</text>'
nodes=[(80,50),(320,50),(80,130),(320,130)]
ILL["home"]=f'''<circle cx="200" cy="90" r="22" fill="none" stroke="{AC2}" stroke-width="1.5"/><circle cx="200" cy="90" r="22" fill="none" stroke="{AC2}"><animate attributeName="r" values="22;48" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="200" y="94" text-anchor="middle" class="jb" font-size="11" fill="{AC2}">LLM</text>'''+"".join(f'<path d="M{x} {y}L200 90" stroke="{LINE}" stroke-dasharray="3 4"><animate attributeName="stroke-dashoffset" from="14" to="0" dur="1s" repeatCount="indefinite"/></path><rect x="{x-26}" y="{y-12}" width="52" height="24" rx="12" fill="{BG}" stroke="{LINE}"/><text x="{x}" y="{y+4}" text-anchor="middle" class="jb" font-size="9" fill="{MUTED}">{l}</text>' for (x,y),l in zip(nodes,["light","voice","temp","plug"]))
ILL["pdf"]=f'''<rect x="60" y="30" width="110" height="120" rx="6" fill="none" stroke="{LINE}"/>{"".join(f'<rect x="72" y="{44+k*14}" width="86" height="6" rx="2" fill="{AC if k==0 else LINE}"/>' for k in range(7))}
<path d="M188 90h30" stroke="{AC}" stroke-width="1.5"/><path d="M212 84l6 6-6 6" fill="none" stroke="{AC}" stroke-width="1.5"><animate attributeName="opacity" values=".3;1;.3" dur="1.4s" repeatCount="indefinite"/></path>
<g><animateTransform attributeName="transform" type="translate" values="0 8;0 0;0 0" dur="3s" repeatCount="indefinite"/><rect x="236" y="30" width="96" height="124" rx="6" fill="{TXT}"/>{"".join(f'<rect x="248" y="{48+k*14}" width="{72 if k%3 else 50}" height="6" rx="2" fill="#C9D1D9"/>' for k in range(6))}<text x="284" y="142" text-anchor="middle" class="jb" font-size="10" fill="{BG}">PDF · TH/EN</text></g>'''
PROJ={
 "spk":("SPK Watch",("Community flood reports for Samut Prakan — pin it, measure it, share it live.","เว็บรายงานน้ำท่วมสมุทรปราการ ปักหมุด บอกระดับน้ำ ดูได้แบบเรียลไทม์"),["map","realtime","mobile"]),
 "green":("GreenTrip",("Field-team tracking with geofenced zones, live GPS and photo check-ins.","ระบบติดตามทีมภาคสนาม กำหนดโซน ติดตาม GPS เช็กอินด้วยรูป"),["geofence","gps","traccar"]),
 "clash":("Element Clash",("A 2–5 player web card game. Room codes, no sign-up, bots welcome.","เกมการ์ดบนเว็บ 2–5 คน เข้าห้องด้วยรหัส ไม่ต้องสมัคร มีบอทให้เล่น"),["multiplayer","bots","game"]),
 "home":("Smart Home × AI",("Wiring smart-home gadgets to a local LLM. Talk to it, it does things.","เชื่อมอุปกรณ์สมาร์ตโฮมกับ AI ในเครื่อง สั่งด้วยเสียงได้"),["iot","voice","automation"]),
 "pdf":("PDF Kit",("Spreadsheets in, print-ready PDFs out — rosters, sign-in sheets, game cards.","แปลงสเปรดชีตเป็น PDF พร้อมพิมพ์ รายชื่อ ใบเซ็นชื่อ การ์ดเกม"),["python","pdf","thai-fonts"]),
}
def wrap(t,x,y,lang,mx=46):
    ws=t.split(" "); ls=[""]
    for w in ws:
        if len(ls[-1])+len(w)+1>mx: ls.append(w)
        else: ls[-1]=(ls[-1]+" "+w).strip()
    cls="th" if lang=="th" else "sgm"
    return "".join(f'<text x="{x}" y="{y+k*20}" class="{cls}" font-size="14" fill="{MUTED}">{l}</text>' for k,l in enumerate(ls[:2]))
def card(key,i,lang):
    name,desc,tags=PROJ[key]; d=desc[0 if lang=="en" else 1]
    tx="".join(f'<g transform="translate({24+sum(len(t)*7.2+28 for t in tags[:k])} 296)"><rect width="{len(t)*7.2+18}" height="22" rx="11" fill="none" stroke="{LINE}"/><text x="9" y="15" class="jb" font-size="11" fill="{MUTED}">{t}</text></g>' for k,t in enumerate(tags))
    return svg(410,336,rise(f'''<rect x=".5" y=".5" width="409" height="335" rx="14" fill="{BG}" stroke="{LINE}"/>
<svg x="5" y="5" width="400" height="180">{ILL[key]}</svg>
<line x1="0" y1="190" x2="410" y2="190" stroke="{LINE}"/>
<text x="24" y="222" class="jb" font-size="11" fill="{AC}">{i:02d}</text>
<text x="52" y="224" class="sg" font-size="22" fill="{TXT}">{name}</text>
{wrap(d,24,256,lang)}
{tx}''',((i-1)%2)*.18+.1,24,1.0))

# ---------- STATS ----------
def stats(lang, data=None):
    d=data or dict(repos=24,commits=1248,streak=37,stars=56,langs=[("TypeScript","#3178C6",38),("JavaScript","#F1E05A",27),("PHP","#4F5D95",15),("HTML","#E34C26",10),("CSS","#663399",6),("C++","#F34B7D",4)])
    L=(["repos","commits / yr","day streak","stars"] if lang=="en" else ["รีโพ","คอมมิต / ปี","วันติดต่อกัน","ดาว"])
    vals=[d["repos"],d["commits"],d["streak"],d["stars"]]
    b=f'<rect x=".5" y=".5" width="839" height="232" rx="14" fill="{BG}" stroke="{LINE}"/>'
    for k,(l,v) in enumerate(zip(L,vals)):
        x=24+k*200
        b+=f'''<text x="{x+12}" y="98" class="sg" font-size="52" fill="{TXT}" opacity="0">{v:,}<animate attributeName="opacity" from="0" to="1" begin="{k*.15}s" dur=".5s" fill="freeze"/></text>
<text x="{x+14}" y="126" class="{'th' if lang=='th' else 'jb'}" font-size="12" fill="{MUTED}" letter-spacing="1">{l.upper() if lang=='en' else l}</text>'''
        if k: b+=f'<line x1="{x-6}" y1="40" x2="{x-6}" y2="132" stroke="{LINE}"/>'
    x=36; tot=sum(p for *_,p in d["langs"])
    for n,c,p in d["langs"]:
        w=p/tot*768
        b+=f'<rect x="{x:.1f}" y="164" height="8" width="0" fill="{c}"><animate attributeName="width" from="0" to="{w-2:.1f}" begin=".8s" dur=".8s" fill="freeze"/></rect>'; x+=w
    x=36
    for n,c,p in d["langs"]:
        b+=f'<circle cx="{x+4}" cy="200" r="4" fill="{c}"/><text x="{x+14}" y="204" class="jb" font-size="11" fill="{MUTED}">{n} {round(p/tot*100)}%</text>'; x+=len(f"{n} {p}%")*7+34
    return svg(840,233,b)

# ---------- FOOTER ----------
def footer(lang):
    q="Less noise. More creativity. Better code." if lang=="en" else "เสียงรบกวนน้อยลง ความคิดสร้างสรรค์มากขึ้น โค้ดที่ดีขึ้น"
    return svg(840,120,rise(f'''<line x1="0" y1="1" x2="840" y2="1" stroke="{LINE}"/>
<text x="0" y="60" class="{'sgm' if lang=='en' else 'th'}" font-size="20" fill="{TXT}">{q}</text>
<text x="0" y="92" class="jb" font-size="12" fill="{MUTED}" letter-spacing="1">github.com/tawin2350 · built by THIRD · 2026</text>
<rect x="824" y="46" width="16" height="16" fill="{AC}"/>''',.2))


def stats_cards(lang,d=None):
    d=d or dict(commits=1248,monthly=[42,61,38,90,120,84,66,140,118,96,152,141],streak=37,days=[1,1,0,1,1,1,1,1,1,1,1,1,1,1],repos=24,stars=56,
        langs=[("TypeScript","#3178C6",38),("JavaScript","#F1E05A",27),("PHP","#4F5D95",15),("Other","#7D8590",20)])
    T=dict(en=["COMMITS · 12 MO","DAY STREAK","REPOSITORIES","LANGUAGES","stars","last 14 days"],
           th=["คอมมิต · 12 เดือน","วันติดต่อกัน","รีโพ","ภาษาที่ใช้","ดาว","14 วันล่าสุด"])[lang]
    lab="th" if lang=="th" else "jb"
    W,H,G=201,168,12
    ic={ # line icons
     0:f'<circle cx="10" cy="10" r="4" fill="none" stroke="{AC}" stroke-width="1.6"/><path d="M0 10h6M14 10h6" stroke="{AC}" stroke-width="1.6"/>',
     1:f'<path d="M11 1L3 12h6l-1 7 8-11h-6z" fill="none" stroke="{WARM}" stroke-width="1.6" stroke-linejoin="round"/>',
     2:f'<path d="M3 2h11a2 2 0 0 1 2 2v14H5a2 2 0 0 1-2-2zM3 15a2 2 0 0 1 2-2h11" fill="none" stroke="{AC2}" stroke-width="1.6" stroke-linejoin="round"/>',
     3:f'<path d="M7 4L2 10l5 6M13 4l5 6-5 6" fill="none" stroke="{TXT}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'}
    b=""
    for k in range(4):
        x=k*(W+G)
        b+=f'<g transform="translate({x} 0)">'+f'<g opacity="0" transform="translate(0 16)"><animate attributeName="opacity" from="0" to="1" begin="{k*.15}s" dur=".8s" fill="freeze"/><animateTransform attributeName="transform" type="translate" from="0 16" to="0 0" begin="{k*.15}s" dur=".8s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".16 1 .3 1"/>'
        b+=f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="{LINE}"/><g transform="translate(18 18)">{ic[k]}</g>'
        b+=f'<text x="46" y="33" class="{lab}" font-size="10.5" fill="{MUTED}" letter-spacing="{0 if lang=="th" else 1}">{T[k]}</text>'
        if k==0:
            b+=f'<text x="18" y="88" class="sg" font-size="40" fill="{TXT}">{d["commits"]:,}</text>'
            m=max(d["monthly"]); pts=" ".join(f'{18+i*(W-36)/11:.1f},{150-v/m*36:.1f}' for i,v in enumerate(d["monthly"]))
            b+=f'<polyline points="{pts}" fill="none" stroke="{AC}" stroke-width="1.8" stroke-linejoin="round" stroke-dasharray="400" stroke-dashoffset="400"><animate attributeName="stroke-dashoffset" from="400" to="0" begin=".5s" dur="1.4s" fill="freeze"/></polyline>'
            lx,ly=pts.split()[-1].split(","); b+=f'<circle cx="{lx}" cy="{ly}" r="3" fill="{AC}"><animate attributeName="r" values="3;5;3" dur="1.6s" repeatCount="indefinite"/></circle>'
        if k==1:
            b+=f'<text x="18" y="88" class="sg" font-size="40" fill="{TXT}">{d["streak"]}</text><text x="{18+len(str(d["streak"]))*24+6}" y="88" class="{lab}" font-size="12" fill="{MUTED}">{"days" if lang=="en" else "วัน"}</text>'
            for i,v in enumerate(d["days"]):
                b+=f'<rect x="{18+i*12}" y="128" width="8" height="18" rx="2" fill="{WARM if v else LINE}" opacity="0"><animate attributeName="opacity" from="0" to="{1 if v else .8}" begin="{.5+i*.06}s" dur=".2s" fill="freeze"/></rect>'
            b+=f'<text x="18" y="118" class="{lab}" font-size="10" fill="{MUTED}">{T[5]}</text>'
        if k==2:
            b+=f'<text x="18" y="88" class="sg" font-size="40" fill="{TXT}">{d["repos"]}</text>'
            b+=f'<line x1="18" y1="112" x2="{W-18}" y2="112" stroke="{LINE}"/>'
            b+=f'<path transform="translate(18 126)" d="M8 0l2.4 5 5.6.8-4 3.9 1 5.5L8 12.6 3 15.2l1-5.5-4-3.9 5.6-.8z" fill="none" stroke="{AC2}" stroke-width="1.4" stroke-linejoin="round"/>'
            b+=f'<text x="44" y="140" class="sg" font-size="18" fill="{TXT}">{d["stars"]}</text><text x="{48+len(str(d["stars"]))*11}" y="140" class="{lab}" font-size="11" fill="{MUTED}">{T[4]}</text>'
        if k==3:
            tot=sum(p for *_,p in d["langs"]); y=62
            for i,(n,c,p) in enumerate(d["langs"]):
                w=(W-36)*p/tot
                b+=f'<text x="18" y="{y+i*24}" class="jb" font-size="10.5" fill="{TXT}">{n}</text><text x="{W-18}" y="{y+i*24}" text-anchor="end" class="jb" font-size="10.5" fill="{MUTED}">{round(p/tot*100)}%</text>'
                b+=f'<rect x="18" y="{y+6+i*24}" width="{W-36}" height="3" rx="1.5" fill="{LINE}"/><rect x="18" y="{y+6+i*24}" width="0" height="3" rx="1.5" fill="{c}"><animate attributeName="width" from="0" to="{w:.1f}" begin="{.6+i*.12}s" dur=".7s" fill="freeze"/></rect>'
        b+='</g></g>'
    return svg(4*W+3*G,H+4,b)

def textlines(t,mx):
    ws=t.split(" "); ls=[""]
    for w in ws:
        if len(ls[-1])+len(w)+1>mx: ls.append(w)
        else: ls[-1]=(ls[-1]+" "+w).strip()
    return ls
ABOUT={"en":["Hey, I'm THIRD — a CS student at Thammasat who likes turning random ideas into stuff that actually works.","Mostly full-stack web, a bit of AI and automation, and the occasional game when I should probably be studying."],
"th":["สวัสดีครับ ผม THIRD นักศึกษา CS ธรรมศาสตร์ ชอบเอาไอเดียแปลกๆ มาทำให้ใช้ได้จริงครับ","ส่วนใหญ่ทำเว็บ Full-stack เล่นกับ AI และระบบอัตโนมัติบ้าง แล้วก็แอบทำเกมตอนที่ควรอ่านหนังสือ"]}
def about(lang):
    cls="th" if lang=="th" else "sgm"; y=30; b=""; n=0
    for para in ABOUT[lang]:
        for l in textlines(para,82 if lang=="en" else 70):
            b+=rise(f'<text x="0" y="{y}" class="{cls}" font-size="17" fill="#C9D1D9">{l}</text>',.15+n*.12,10); y+=28; n+=1
        y+=10
    return svg(840,y-10,b)
NOW={"en":[("EXPLORING","AI agents, realtime web"),("BUILDING","Element Clash, GreenTrip"),("LEARNING","OS, architecture, networks")],
"th":[("กำลังสำรวจ","AI agents, เว็บเรียลไทม์"),("กำลังสร้าง","ธาตุปะทะ, GreenTrip"),("กำลังเรียน","OS, สถาปัตยกรรม, เครือข่าย")]}
def now(lang):
    b=""; cols=[AC,WARM,AC2]
    for k,(a,v) in enumerate(NOW[lang]):
        x=k*284
        b+=rise(f'<rect x="{x+.5}" y=".5" width="272" height="91" rx="12" fill="{BG}" stroke="{LINE}"/><rect x="{x+20}" y="24" width="8" height="8" rx="2" fill="{cols[k]}"/>'
                f'<text x="{x+38}" y="32" class="{"th" if lang=="th" else "jb"}" font-size="11" fill="{MUTED}" letter-spacing="{0 if lang=="th" else 1.5}">{a}</text>'
                f'<text x="{x+20}" y="66" class="{"th" if lang=="th" else "sgm"}" font-size="16" fill="{TXT}">{v}</text>',.1+k*.15,16)
    return svg(840,96,b)
