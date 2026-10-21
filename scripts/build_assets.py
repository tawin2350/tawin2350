import os,sys
sys.path.insert(0,os.path.dirname(__file__))
from design import *
out=os.path.join(os.path.dirname(__file__),'..','assets')
os.makedirs(out,exist_ok=True)
SECT=[("About","เกี่ยวกับผม"),("Toolbox","เครื่องมือ"),("Selected work","ผลงาน"),("Activity","สถิติ"),("Right now","ช่วงนี้")]
for lang in ["en","th"]:
    open(f"{out}/hero-{lang}.svg","w").write(hero(lang))
    open(f"{out}/switch-{lang}.svg","w").write(switch(lang))
    open(f"{out}/stats-{lang}.svg","w").write(stats_cards(lang))
    open(f"{out}/about-{lang}.svg","w").write(about(lang))
    open(f"{out}/now-{lang}.svg","w").write(now(lang))
    open(f"{out}/footer-{lang}.svg","w").write(footer(lang))
    for n,(e,t) in enumerate(SECT,1): open(f"{out}/sec{n}-{lang}.svg","w").write(section(n,e,t,lang))
    for i,k in enumerate(PROJ,1): open(f"{out}/card-{k}-{lang}.svg","w").write(card(k,i,lang))
print("done")
