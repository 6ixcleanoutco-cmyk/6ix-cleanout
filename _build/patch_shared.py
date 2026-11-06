"""Applies the 2026 refresh (black + lime brand, call/text buttons, launch pricing,
lead-source tracking, footer links, SEO fixes) to the 5 hand-written pages.

It always starts from the pages as they were in commit BASE, so running it again
gives the same result instead of patching twice.
Run:  python _build/patch_shared.py   (from the repo root or anywhere)
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "a39242c"
PAGES = ["index", "services", "realtors-landlords", "areas", "about"]
TEL = "+16475172721"
SMS_HREF = "sms:" + TEL + "?&amp;body=Hi%206ix%20Cleanout%2C%20here%20are%20photos%20of%20what%20needs%20to%20go.%20My%20area%3A%20"

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
MSG_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
ICO_PHONE = f'<span class="ico">{PHONE_SVG}</span>'
ICO_MSG = f'<span class="ico">{MSG_SVG}</span>'
CALL_BTN = f'<a class="btn alt" data-call href="tel:{TEL}">{ICO_PHONE}Call</a>'
SMS_BTN = f'<a class="btn alt" data-sms href="{SMS_HREF}">{ICO_MSG}Text photos</a>'
TAMIL = '<span lang="ta">தமிழிலும் பேசலாம்</span>'

CITY_PAGES = [("junk-removal-scarborough.html", "Scarborough"), ("junk-removal-markham.html", "Markham"),
              ("junk-removal-unionville.html", "Unionville"),
              ("junk-removal-north-york.html", "North York"), ("junk-removal-east-york.html", "East York"),
              ("junk-removal-pickering.html", "Pickering"),
              ("junk-removal-richmond-hill.html", "Richmond Hill"), ("junk-removal-ajax.html", "Ajax")]
ITEM_PAGES = [("couch-furniture-removal.html", "Couch and furniture removal"), ("mattress-removal.html", "Mattress removal"),
              ("appliance-removal.html", "Appliance removal"), ("garage-basement-cleanout.html", "Garage and basement cleanouts")]

TOKENS_OLD_LIGHT = "--bg:#F1F5F3; --surface:#FFFFFF; --surface2:#E8EEEB; --ink:#0D1B19; --muted:#506360; --line:#D3DDD9;\n  --brand:#0B5C55; --brand-ink:#FFFFFF; --hivis:#F5C518; --hivis-ink:#201A00;"
TOKENS_NEW_LIGHT = "--bg:#F5F6F2; --surface:#FFFFFF; --surface2:#ECEEE8; --ink:#0A0F0D; --muted:#55605A; --line:#DADDD5;\n  --brand:#0A0F0D; --brand-ink:#FFFFFF; --hivis:#B8F334; --hivis-ink:#0A0F0D;"
TOKENS_OLD_DARK = "--bg:#0A1312; --surface:#111E1C; --surface2:#182927; --ink:#E7F0EE; --muted:#9BB0AC; --line:#243633;\n  --brand:#3FC9B9; --brand-ink:#04211E; --hivis:#F5C518; --hivis-ink:#201A00;"
TOKENS_NEW_DARK = "--bg:#0A0F0D; --surface:#121915; --surface2:#1A231E; --ink:#EEF3EC; --muted:#9DA89F; --line:#26302A;\n  --brand:#B8F334; --brand-ink:#0A0F0D; --hivis:#B8F334; --hivis-ink:#0A0F0D;"

EXTRA_CSS = r"""
/* ===== 2026 refresh: black + lime brand. Lime is only ever a fill or sits on black, never text on white. ===== */
:root{--night:#0A0F0D;--lime:#B8F334}
.hband,header.top{--bg:#0A0F0D;--surface:#141B17;--surface2:#1B241F;--ink:#F1F5EE;--muted:#A3AEA6;--line:#2A342E;--brand:#B8F334;--brand-ink:#0A0F0D;color:var(--ink)}
header.top{background:color-mix(in srgb,#0A0F0D 94%,transparent);border-bottom-color:#1D2621}
.hband{background:#0A0F0D;position:relative;overflow:hidden;isolation:isolate;margin-inline:calc(-1*max(16px,env(safe-area-inset-left,0px)));padding-inline:max(16px,env(safe-area-inset-left,0px))}
.hband::before,.hband::after{content:"";position:absolute;border-radius:50%;border:clamp(18px,3vw,34px) solid rgba(184,243,52,.08);z-index:-1;pointer-events:none}
.hband::before{width:min(75vw,640px);aspect-ratio:1;right:-14%;top:-48%}
.hband::after{width:min(60vw,520px);aspect-ratio:1;left:-16%;bottom:-60%}
.hband .hero{padding-block:60px 56px}
.hband .phero{padding-block:52px 48px}
.hband .phero h1{max-width:22ch}
.lime{color:var(--lime)}
h1 .kick{display:block;font:700 clamp(.95rem,1.7vw,1.15rem)/1.3 var(--body);letter-spacing:.01em;color:var(--lime);margin-bottom:12px}
.hband .factrow div{border-top-color:var(--lime)}
.hband .btn.alt{border-color:#3A463F;color:#fff}
.hband .btn.alt:hover{border-color:var(--lime)}
.hband .qe{--bg:#F5F6F2;--surface:#FFFFFF;--surface2:#ECEEE8;--ink:#0A0F0D;--muted:#55605A;--line:#DADDD5;--brand:#0A0F0D;--brand-ink:#FFFFFF;color:var(--ink);box-shadow:0 24px 60px rgba(0,0,0,.5)}
.launch{display:inline-flex;align-items:center;gap:8px;background:rgba(184,243,52,.12);border:1px solid rgba(184,243,52,.4);color:var(--lime);border-radius:99px;padding:6px 13px;font:600 .82rem var(--body);margin:0 0 16px}
.launch.on-light{background:var(--night);border-color:var(--night);color:var(--lime)}
.sec .head p.launch{color:var(--lime);font-size:.82rem}  /* beats '.sec .head p' (muted grey), which made the badge text grey on black */
.sec .head p.launch.on-light{color:var(--lime)}
.launch[hidden]{display:none}
.launch .dot{position:relative;width:8px;height:8px;border-radius:50%;background:var(--lime)}
.launch .dot::after{content:"";position:absolute;inset:0;border-radius:50%;background:var(--lime);animation:pulse 2s infinite;will-change:transform,opacity}
@keyframes pulse{0%{transform:scale(1);opacity:.7}70%,100%{transform:scale(2.8);opacity:0}}
@media (prefers-reduced-motion:reduce){.launch .dot::after{animation:none}}
/* footer headings are h3 (the page goes h2 then footer), styled like the old h4 */
footer h3{margin:0 0 10px;font:600 .72rem var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
footer .fine a{text-decoration:underline;text-underline-offset:2px}
.steps button small{opacity:1}
/* phones: the bottom bar already has Call / Text / estimate, so the header drops its estimate button and scrolls away */
nav.links{scrollbar-width:none}
nav.links::-webkit-scrollbar{display:none}
@media (max-width:980px){header.top{position:relative}section{scroll-margin-top:12px}}
@media (max-width:560px){header.top .bar>.btn.hv.sm{display:none}}
/* phones: price tables fit the screen and wrap, instead of hiding a column off to the side */
@media (max-width:600px){table{min-width:0}th,td{padding-inline:10px}td{font-size:.9rem}.bar8{width:56px}}
@media (max-width:380px){th,td{padding-inline:7px}}
.ico{display:inline-flex;width:18px;height:18px;flex:none}
.ico svg{width:100%;height:100%}
.hcall{border-color:#3A463F!important;color:#fff!important}
@media (max-width:700px){.hcall .num{display:none}.hcall{padding-inline:10px}}
.trust{max-width:1180px;margin:22px auto 0;display:flex;flex-wrap:wrap;gap:8px 10px;justify-content:center}
.trust>span{display:inline-flex;align-items:center;gap:7px;background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:7px 13px;font-weight:600;font-size:.88rem}
.trust>span::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--lime);box-shadow:inset 0 0 0 1.5px var(--night);flex:none}
.why{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
@media (max-width:980px){.why{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.why{grid-template-columns:1fr}}
.why>div{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:22px;display:grid;gap:8px;align-content:start}
.why .num{width:42px;height:42px;border-radius:12px;background:var(--night);color:var(--lime);display:grid;place-items:center;font:800 1.05rem var(--display)}
.why p{color:var(--muted);font-size:.95rem}
.save{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:18px}
@media (max-width:1100px){.save{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:600px){.save{grid-template-columns:1fr}}
.save>div{border:1.5px dashed var(--line);border-radius:14px;padding:16px 18px;background:var(--surface)}
.save b{display:block;font-size:1.02rem;margin-bottom:4px}
.save p{color:var(--muted);font-size:.92rem}
.revs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
@media (max-width:900px){.revs{grid-template-columns:1fr}}
.rev{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;display:grid;gap:10px}
.rev blockquote{margin:0}
.rev .stars{color:#D99A00;letter-spacing:2px}
.rev cite{font-style:normal;font-weight:700;font-size:.9rem;color:var(--muted)}
.mact{display:flex;gap:8px;align-items:center}
.mbar .icob{width:46px;padding:0}
.mbar.sub{gap:8px}
.mbar.sub .btn{flex:1;padding-inline:10px;font-size:.92rem}
.guide{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.guide a{display:flex;justify-content:space-between;align-items:center;gap:10px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;text-decoration:none;color:var(--ink);font-weight:700}
.guide a:hover{border-color:var(--ink)}
.guide a::after{content:"\2192";color:var(--muted)}
.prose{display:grid;gap:12px;max-width:68ch;color:var(--muted)}
.prose b{color:var(--ink)}
footer{grid-template-columns:1.5fr repeat(4,minmax(0,1fr))}
footer p.tam{margin-top:12px;color:var(--ink)}
@media (max-width:980px){footer{grid-template-columns:repeat(2,minmax(0,1fr))}footer>div:first-child{grid-column:1/-1}}
@media (max-width:520px){footer{grid-template-columns:1fr}}
.head .launch{justify-self:start}
.langpill{border-color:#3A463F!important;color:var(--lime)!important;font-weight:800;padding-inline:12px}
@media (max-width:420px){.langpill{padding-inline:9px}}
.trust{margin-bottom:28px}
@media (max-width:1500px){.hcall .num{display:none}.hcall{padding-inline:10px}}
@media (max-width:1120px){.hcall{display:none}}
@media (max-width:620px){.trust{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;scrollbar-width:none;padding-bottom:2px}.trust::-webkit-scrollbar{display:none}.trust>span{font-size:.82rem;padding:6px 11px;white-space:nowrap}.cta .btn.hv{flex-basis:100%}.cta .btn.alt{flex:1}}
[data-until][hidden]{display:none!important}
.gb{background:var(--night);color:#eef3ec;border-radius:20px;padding:clamp(22px,4vw,38px);display:grid;grid-template-columns:1fr auto;gap:20px 28px;align-items:center;position:relative;overflow:hidden;isolation:isolate}
.gb::after{content:"";position:absolute;width:340px;aspect-ratio:1;border-radius:50%;border:28px solid rgba(184,243,52,.09);right:-110px;top:-150px;z-index:-1}
.gb h2{color:#fff}
.gb p{color:#c9d2ca;max-width:62ch;margin-top:10px}
.gb .eyebrow{color:var(--lime)}
.gb .cta{margin:0}
@media (max-width:760px){.gb{grid-template-columns:1fr}}
.gbcards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
@media (max-width:860px){.gbcards{grid-template-columns:1fr}}
.gbcards>div{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:22px;display:grid;gap:8px;align-content:start}
.gbcards p{color:var(--muted);font-size:.95rem}
.gbn{width:42px;height:42px;border-radius:12px;background:var(--night);color:var(--lime);display:grid;place-items:center;font:800 1.05rem var(--display)}
.chk{display:flex;gap:10px;align-items:flex-start;margin-top:16px;font-weight:600}
.chk input{width:20px;height:20px;margin-top:2px;flex:none;accent-color:var(--night)}
.hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}
"""

CONFIG_ADD = """
  phoneE164: "+16475172721", /* used for the tap-to-call and tap-to-text buttons */
  launchSpotsLeft: 25, launchSpotsTotal: 25, /* launch pricing badge: lower launchSpotsLeft by hand after each booked job, the badge hides itself at 0 */
  metaPixelId: "", /* paste the Meta Pixel ID here to turn on Facebook and Instagram ad tracking. Empty = nothing loads */
  clarityId: "", /* paste the Microsoft Clarity project ID here to turn on heatmaps and session recordings. Empty = nothing loads */
  reviews: [], /* real Google reviews only, for example {name:"Priya S.", city:"Markham", stars:5, text:"..."}. The reviews section stays hidden while this is empty */"""

EXTRAS_JS = r"""<script>
/* ---------- 2026 extras: call and text links, launch badge, reviews, lead source, optional tracking ---------- */
(function(){
  const C=(typeof CONFIG!=="undefined")?CONFIG:{};
  const e2=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const tel=C.phoneE164||"+16475172721";
  const body="Hi 6ix Cleanout, here are photos of what needs to go. My area: ";
  document.querySelectorAll("[data-call]").forEach(a=>{a.href="tel:"+tel;});
  document.querySelectorAll("[data-sms]").forEach(a=>{a.href="sms:"+tel+"?&body="+encodeURIComponent(body);});
  const left=+C.launchSpotsLeft||0, total=+C.launchSpotsTotal||25;
  document.querySelectorAll("[data-launch]").forEach(n=>{ n.hidden=!(left>0); const b=n.querySelector("[data-spots]"); if(b) b.textContent=left+(b.dataset.of||" of ")+total; });
  /* time-limited sections (the launch giveback) hide themselves from the date in data-until */
  document.querySelectorAll("[data-until]").forEach(n=>{ const u=new Date(n.dataset.until+"T00:00:00"); if(!isNaN(u)&&new Date()>=u) n.hidden=true; });
  const R=Array.isArray(C.reviews)?C.reviews:[];
  document.querySelectorAll("[data-reviews]").forEach(sec=>{
    sec.hidden=!R.length; if(!R.length) return;
    sec.querySelector(".revs").innerHTML=R.map(r=>{const n=Math.max(1,Math.min(5,+r.stars||5)); return `<figure class="rev"><span class="stars" role="img" aria-label="${n} out of 5 stars">${"★".repeat(n)}</span><blockquote>${e2(r.text)}</blockquote><cite>${e2(r.name)}${r.city?", "+e2(r.city):""}</cite></figure>`;}).join("");
  });
  /* Lead source: remembers how this visitor first arrived, so the tracker shows which marketing works. */
  const KEY="6ix-src";
  try{ if(!localStorage.getItem(KEY)){ const q=new URLSearchParams(location.search); let ref=""; try{ if(document.referrer){ const h=new URL(document.referrer).hostname; if(h!==location.hostname) ref=h; } }catch(x){}
    localStorage.setItem(KEY,JSON.stringify({s:q.get("utm_source")||(q.get("fbclid")?"facebook-ad":q.get("gclid")?"google-ad":""),c:q.get("utm_campaign")||"",r:ref,d:new Date().toISOString().slice(0,10)})); } }catch(x){}
  window.leadSourceText=function(){ let o={}; try{ o=JSON.parse(localStorage.getItem(KEY)||"{}"); }catch(x){}
    const p=[]; if(o.s) p.push(o.s+(o.c?"/"+o.c:"")); if(o.r) p.push("from "+o.r); if(!p.length) p.push("direct");
    return "Source: "+p.join(", ")+(o.d?" (first visit "+o.d+")":""); };
  /* Optional tracking. Nothing loads until an ID is pasted into CONFIG. */
  if(C.metaPixelId){ !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,"script","https://connect.facebook.net/en_US/fbevents.js"); fbq("init",C.metaPixelId); fbq("track","PageView"); }
  if(C.clarityId){ (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script",C.clarityId); }
  window.track6=function(ev,data){ try{ if(window.fbq) fbq("track",ev,data||{}); if(window.clarity) clarity("event",ev); }catch(x){} };
  document.addEventListener("click",ev=>{ const a=ev.target.closest("[data-call],[data-sms]"); if(a) track6("Contact",{method:a.hasAttribute("data-call")?"call":"text"}); });
})();
</script>"""

# Shown from the first paint (no "hidden"), so the hero never jumps when the script runs; the script hides it at 0 spots.
LAUNCH_TEXT = "Founding 25 · launch prices"
LAUNCH_DARK = f'<p class="launch" data-launch><span class="dot"></span>{LAUNCH_TEXT} · <b data-spots>25 of 25</b> spots left</p>'
LAUNCH_LIGHT = f'<p class="launch on-light" data-launch><span class="dot"></span>{LAUNCH_TEXT} · <b data-spots>25 of 25</b> spots left</p>'

# Self-hosted fonts (SIL Open Font License, from Google Fonts, latin subset). The fallback faces are
# Arial / Courier New stretched to the same width and line height, so nothing moves when the real font arrives.
GFONTS_OLD = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">')
FONT_PRELOAD = ('<link rel="preload" href="fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>\n'
                '<link rel="preload" href="fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>\n'
                '<link rel="preload" href="fonts/plexmono-500.woff2" as="font" type="font/woff2" crossorigin>')
FONT_VARS_OLD = '--display:"Bricolage Grotesque","Segoe UI",system-ui,sans-serif; --body:"Figtree","Segoe UI",system-ui,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;'
FONT_VARS_NEW = '--display:"Bricolage Grotesque","Bricolage FB",sans-serif; --body:"Figtree","Figtree FB",sans-serif; --mono:"IBM Plex Mono","Plex FB",monospace;'
UR = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
FONT_CSS = (
    f'@font-face{{font-family:"Figtree";src:url(fonts/figtree.woff2) format("woff2");font-weight:300 900;font-display:swap;unicode-range:{UR}}}\n'
    f'@font-face{{font-family:"Bricolage Grotesque";src:url(fonts/bricolage.woff2) format("woff2");font-weight:200 800;font-display:swap;unicode-range:{UR}}}\n'
    + "".join(f'@font-face{{font-family:"IBM Plex Mono";src:url(fonts/plexmono-{w}.woff2) format("woff2");font-weight:{w};font-display:swap;unicode-range:{UR}}}\n' for w in (400, 500, 600))
    + '@font-face{font-family:"Figtree FB";src:local("Arial"),local("ArialMT"),local("Liberation Sans"),local("Arimo"),local("Helvetica");font-weight:100 549;size-adjust:99.2%;ascent-override:95.8%;descent-override:25.2%;line-gap-override:0%}\n'
    '@font-face{font-family:"Figtree FB";src:local("Arial Bold"),local("Arial-BoldMT"),local("Liberation Sans Bold"),local("Arimo Bold"),local("Helvetica Bold");font-weight:550 900;size-adjust:95.7%;ascent-override:99.3%;descent-override:26.1%;line-gap-override:0%}\n'
    '@font-face{font-family:"Bricolage FB";src:local("Arial Bold"),local("Arial-BoldMT"),local("Liberation Sans Bold"),local("Arimo Bold"),local("Helvetica Bold");font-weight:100 900;size-adjust:97.6%;ascent-override:95.3%;descent-override:27.7%;line-gap-override:0%}\n'
    '@font-face{font-family:"Plex FB";src:local("Courier New"),local("CourierNewPSMT"),local("Liberation Mono"),local("Cousine"),local("DejaVu Sans Mono");font-weight:100 900;size-adjust:100%;ascent-override:102.5%;descent-override:27.5%;line-gap-override:0%}\n')

SAVE_HTML = ('<div class="save">'
             '<div><b>Single items on route days</b><p>Choose "Flexible" timing and we add you to our next route day. That is how we keep single pickups at <span data-min>$129</span>.</p></div>'
             '<div><b>Neighbour bundle: $20 off each</b><p>Book with a neighbour on the same street for the same day and you both save $20.</p></div>'
             '<div><b>Refer a friend: $25 off</b><p>Get $25 off your next job for every friend who books with us.</p></div>'
             '<div><b>Seniors save 10%</b><p>Customers 65 and older get 10% off, down to the <span data-min>$129</span> minimum. Tick the box in the estimate.</p></div></div>')

TRUST_HTML = ('<div class="trust" aria-label="What you get with every job"><span>No tax added</span><span>Price confirmed before we start</span>'
              f'<span>Loaded, hauled and swept</span><span>Donate and recycle first</span><span>{TAMIL}&nbsp;· English and Tamil</span></div>')

TITLES = {
    "index": ("Junk Removal Scarborough &amp; Markham | 6ix Cleanout Co.",
              "Junk removal in Scarborough, Markham and the GTA. Your price in 2 minutes, no tax added. Furniture, appliances, garages, cleanouts. Call (647) 517-2721."),
    "services": ("Junk Removal Services and Prices | 6ix Cleanout Co.",
                 "Junk removal across the GTA: home cleanouts, move-outs, single items, estates, garages and reno debris. Prices from $129, no tax added."),
    "realtors-landlords": ("Junk Removal for Realtors &amp; Landlords | 6ix Cleanout Co.", None),
    "areas": ("Junk Removal Service Areas Across the GTA | 6ix Cleanout Co.", None),
    "about": ("About Us and FAQ | 6ix Cleanout Co. Junk Removal", None),
}

SITE_URL = "https://6ixcleanoutco-cmyk.github.io/6ix-cleanout/"

# ---------- Business details for Google and AI assistants (structured data) ----------
# Same hours as the Google Business Profile. Change both together.
HOURS_LD = [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "08:00", "closes": "18:00"}]
# Paste the Facebook Page and Instagram profile links here (full https:// links). They tell Google the
# website, the Business Profile and the social pages are one business. Empty = left out.
SOCIAL = []
AREAS_ALL = ["Scarborough", "Markham", "Unionville", "North York", "East York", "Toronto", "Pickering", "Richmond Hill", "Vaughan",
             "Etobicoke", "Ajax", "Whitby", "Stouffville", "Mississauga", "Brampton", "Oshawa", "Oakville"]


def biz_extra():
    d = {"logo": SITE_URL + "apple-touch-icon.png", "openingHoursSpecification": HOURS_LD,
         "founder": [{"@type": "Person", "name": n} for n in OWNERS]}
    if SOCIAL:
        d["sameAs"] = SOCIAL
    return d


def biz_ld(area, min_price=129):
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "name": "6ix Cleanout Co.", "url": SITE_URL,
            "image": SITE_URL + "og-image.png", "telephone": "+1-647-517-2721", "email": "6ixcleanoutco@gmail.com",
            "priceRange": f"${min_price} to $1,250 CAD", "paymentAccepted": "Cash, Interac e-Transfer", "knowsLanguage": ["en", "ta"],
            "address": {"@type": "PostalAddress", "addressLocality": "Scarborough", "addressRegion": "ON", "addressCountry": "CA"},
            "areaServed": area, **biz_extra()}


def ld_tag(*objs):
    return "".join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>" for o in objs)


# ---------- Launch-week Giveback Cleanout (hidden automatically from GIVEBACK_UNTIL) ----------
GIVEBACK_UNTIL = "2026-11-21"
GIVEBACK_HTML = ('<section id="giveback" class="sec" data-until="' + GIVEBACK_UNTIL + '"><div class="gb">'
                 '<div><p class="eyebrow">Launch week giveback · Nov 23</p><h2>The Scarborough Giveback Cleanout.</h2>'
                 '<p>Know someone who deserves a fresh start? A senior who can no longer lift the heavy things, a busy single parent, a family that just arrived. '
                 'Nominate them and we clear it for free, up to a quarter truck. Nominations close November 20.</p></div>'
                 '<div class="cta"><a class="btn hv" href="giveback.html">Nominate someone</a></div></div></section>')

LEGAL_LINKS = ' <a href="privacy.html" style="display:inline">Privacy</a> · <a href="terms.html" style="display:inline">Terms</a></p></footer>'


def social_tags(s):
    """Make the Facebook/WhatsApp preview match each page: og:title and og:description copy the
    page's own title and description, and og:url copies the canonical link."""
    t = re.search(r"<title>([^<]*)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)">', s).group(1)
    can = re.search(r'<link rel="canonical" href="([^"]*)">', s).group(1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', lambda m: f'<meta property="og:title" content="{t}">', s)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', lambda m: f'<meta property="og:description" content="{d}">', s)
    s = re.sub(r'<meta property="og:url" content="[^"]*">\n?', "", s)
    s = s.replace('<meta property="og:type" content="website">', f'<meta property="og:type" content="website">\n<meta property="og:url" content="{can}">', 1)
    return s


def base(page):
    out = subprocess.run(["git", "show", f"{BASE}:{page}.html"], cwd=ROOT, capture_output=True)
    if out.returncode:
        sys.exit(out.stderr.decode())
    return out.stdout.decode("utf-8")


def sub1(pattern, repl, s, flags=0, count=1, label=""):
    """re.sub that fails loudly when the pattern is missing, so a changed page never patches silently wrong."""
    new, n = re.subn(pattern, repl, s, count=count, flags=flags)
    if n == 0:
        sys.exit(f"pattern not found: {label or pattern[:60]}")
    return new


def rep1(old, new, s, label="", count=1):
    if old not in s:
        sys.exit(f"text not found: {label or old[:60]}")
    return s.replace(old, new, count)


def footer_html():
    cities = "".join(f'<a href="{f}">{c}</a>' for f, c in CITY_PAGES) + '<a href="areas.html">All service areas</a>'
    items = "".join(f'<a href="{f}">{t}</a>' for f, t in ITEM_PAGES + [COST_PAGE, TAKE_PAGE])
    contact = (f'<div><h4>Contact</h4><a class="mono" data-call href="tel:{TEL}"><span data-phone>(647) 517-2721</span></a>'
               f'<a class="mono" data-sms href="{SMS_HREF}">Text us photos</a>'
               '<a class="mono" href="mailto:6ixcleanoutco@gmail.com"><span data-email>6ixcleanoutco@gmail.com</span></a>'
               f'<p class="tam">{TAMIL}<br>We speak English and Tamil.</p></div>')
    return f'<div><h4>Popular areas</h4>{cities}</div><div><h4>Popular jobs</h4>{items}</div>{contact}'


def shared(s, page):
    s = rep1(TOKENS_OLD_LIGHT, TOKENS_NEW_LIGHT, s, "light tokens")
    s = s.replace(TOKENS_OLD_DARK, TOKENS_NEW_DARK)  # appears twice (media query and data-theme)
    if TOKENS_OLD_DARK in s:
        sys.exit("dark tokens left")
    s = rep1("Hi-vis yellow is the single accent, used like a safety vest: sparingly.",
             "Brand: black with a lime accent, matching the logo and social pages.", s, "css comment")
    # extra CSS goes at the end of the main stylesheet (the one that holds the layout comment)
    i = s.index("/* Layout concept")
    j = s.index("</style>", i)
    s = s[:j] + EXTRA_CSS + s[j:]
    # fonts: self-hosted with matched fallbacks (no render-blocking Google Fonts request, no layout shift)
    s = rep1(GFONTS_OLD, FONT_PRELOAD, s, "google fonts link")
    s = rep1(FONT_VARS_OLD, FONT_VARS_NEW, s, "font vars")
    s = rep1("<style>", "<style>\n" + FONT_CSS, s, "first style")
    # header: Tamil page button, call button, then the existing estimate button
    s = sub1(r'(<a class="btn hv sm" href="[^"]*">Free estimate</a>)',
             '<a class="btn alt sm langpill" href="tamil.html" lang="ta" hreflang="ta" title="தமிழில் பார்க்க">தமிழ்</a>'
             f'<a class="btn alt sm hcall" data-call href="tel:{TEL}" aria-label="Call (647) 517-2721">{ICO_PHONE}<span class="num" data-phone>(647) 517-2721</span></a>\\1',
             s, label="header estimate button")
    # shorter header nav labels so the header fits on one line (the footer keeps the full names)
    s = sub1(r'<nav class="links" aria-label="Pages">.*?</nav>', lambda m: m.group(0)
             .replace(">Realtors and landlords</a>", ">Realtors</a>").replace(">Service areas</a>", ">Areas</a>")
             .replace(">About and FAQ</a>", ">About &amp; FAQ</a>"), s, flags=re.S, label="nav")
    if page == "index":
        s = rep1('<link rel="canonical" href="https://6ixcleanoutco-cmyk.github.io/6ix-cleanout/">',
                 '<link rel="canonical" href="https://6ixcleanoutco-cmyk.github.io/6ix-cleanout/">'
                 '<link rel="alternate" hreflang="en" href="https://6ixcleanoutco-cmyk.github.io/6ix-cleanout/">'
                 '<link rel="alternate" hreflang="ta" href="https://6ixcleanoutco-cmyk.github.io/6ix-cleanout/tamil.html">', s, "index canonical")
    # footer: replace the contact column with areas, jobs and a tappable contact column
    s = sub1(r'<div><h4>Contact</h4>.*?</div>', lambda m: footer_html(), s, flags=re.S, label="footer contact")
    s = sub1(r'<footer.*?</footer>', lambda m: m.group(0).replace("<h4>", "<h3>").replace("</h4>", "</h3>"), s, flags=re.S, label="footer headings")
    # mobile bar
    if page == "index":
        mbar = (f'<div class="mbar" id="mbar"><div><small>ESTIMATE</small><b id="mbar-price">--</b></div><span class="mact">'
                f'<a class="btn alt icob" data-call href="tel:{TEL}" aria-label="Call us">{ICO_PHONE}</a>'
                f'<a class="btn alt icob" data-sms href="{SMS_HREF}" aria-label="Text us photos">{ICO_MSG}</a>'
                '<a class="btn hv" href="#ticketcol">Ticket</a></span></div>')
    else:
        mbar = (f'<div class="mbar sub"><a class="btn alt" data-call href="tel:{TEL}">{ICO_PHONE}Call</a>'
                f'<a class="btn alt" data-sms href="{SMS_HREF}">{ICO_MSG}Text</a>'
                '<a class="btn hv" href="index.html#quote">Free estimate</a></div>')
    s = sub1(r'<div class="mbar".*?</a></div>', lambda m: mbar, s, flags=re.S, label="mbar")
    # config additions and fixes shared by every page's script
    s = sub1(r'(  phone: "\(647\) 517-2721",)', lambda m: m.group(1) + CONFIG_ADD, s, label="config phone")
    s = rep1('{id:"1/8", t:"A few items", frac:.125, price:130,', '{id:"1/8", t:"A few items", frac:.125, price:129,', s, "LOADS 1/8")
    s = rep1("After the work is finished, by card or e-transfer.", "After the work is finished, by cash or Interac e-Transfer.", s, "FAQ payment")
    # title and description
    t, d = TITLES[page]
    s = sub1(r"<title>[^<]*</title>", lambda m: f"<title>{t}</title>", s, label="title")
    if d:
        s = sub1(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{d}">', s, label="description")
    s = s.replace("from $130", "from $129").replace('<td class="p">$130</td>', '<td class="p">$129</td>')
    # privacy and terms links in the footer's small print
    s = rep1("</p></footer>", LEGAL_LINKS, s, "footer fine print")
    # extras script after the main script
    s = rep1("</body></html>", EXTRAS_JS + "</body></html>", s, "body end")
    return s


# ===== 2026-11-04: item picture grid, truck drawings, "what fits", "always included", "what we can't take" =====
NEW_ICONS = {
    "dresser": '<path d="M5 3h14v16H5zM5 8.3h14M5 13.6h14M10 5.6h4M10 11h4M10 16.3h4M6 19v2M18 19v2"/>',
    "boxes": '<path d="M3 12h8v8H3zM13 12h8v8h-8zM8 4h8v8H8zM12 4v3M7 12v2.5M17 12v2.5"/>',
    "yard": '<path d="M5 20c0-9 5-15 15-15 0 10-6 15-15 15zM5 20l9-9M10 15h4M12 12v-2"/>',
    "reno": '<path d="M3 6h18v12H3zM3 12h18M9 6v6M15 6v6M6 12v6M12 12v6M18 12v6"/>',
}
# (label, ITEMS id or None, icon, estimator link, note when not an ITEMS entry)
TAKE_TILES = [
    ("Couches and sofas", "couch", "couch", "item-couch", None),
    ("Mattresses and box springs", "mattress", "mattress", "item-mattress", None),
    ("Fridges and freezers", "fridge", "fridge", "item-fridge", None),
    ("Washers and dryers", "washer", "washer", "item-washer", None),
    ("TVs and electronics", "tv", "tv", "item-tv", None),
    ("Treadmills and gym gear", "treadmill", "treadmill", "item-treadmill", None),
    ("Tables, dressers and beds", None, "dresser", "pickup", "Priced by truck space"),
    ("Boxes, bags and clutter", None, "boxes", "cleanout", "Priced by truck space"),
    ("Yard waste and old fencing", None, "yard", "garage", "Priced by truck space"),
    ("Renovation debris", None, "reno", "reno", "Heavy loads: send photos"),
    ("Pianos", "piano", "piano", "item-piano", None),
    ("Hot tubs", "hottub", "hottub", "item-hottub", None),
]
DEPOTS = [("City of Toronto", "https://www.toronto.ca/services-payments/recycling-organics-garbage/household-hazardous-waste/", "Scarborough, North York, East York, Etobicoke, downtown"),
          ("York Region", "https://www.york.ca/environment/garbage-and-recycling/hazardous-waste-and-special-items-disposal", "Markham, Richmond Hill, Vaughan, Stouffville"),
          ("Durham Region", "https://www.durham.ca/living-here/garbage-green-bin-and-other-collection/waste-management-facilities/", "Pickering, Ajax, Whitby, Oshawa")]
TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
BIG_TRUCK = ('<svg class="tbig" viewBox="0 0 64 30" role="img" aria-label="A full truck"><rect x="2" y="3" width="40" height="19" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/>'
             '<rect x="3.6" y="4.6" width="36.8" height="15.8" rx="1" fill="#B8F334"/><path d="M44 22V9h9l7 7v6z" fill="currentColor"/>'
             '<circle cx="13" cy="25" r="3.6" fill="var(--surface)" stroke="currentColor" stroke-width="1.6"/><circle cx="52" cy="25" r="3.6" fill="var(--surface)" stroke="currentColor" stroke-width="1.6"/></svg>')
TRUCK_JS = ('function truckMini(f){let o="";for(let k=0;k<Math.ceil(f-1e-9);k++){const w=(Math.max(0,Math.min(1,f-k))*36.8).toFixed(1);'
            'o+=`<svg class="tmini" viewBox="0 0 64 30" aria-hidden="true"><rect x="2" y="3" width="40" height="19" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/>'
            '<rect x="3.6" y="4.6" width="${w}" height="15.8" rx="1" fill="#B8F334"/><path d="M44 22V9h9l7 7v6z" fill="currentColor"/>'
            '<circle cx="13" cy="25" r="3.6" fill="var(--surface)" stroke="currentColor" stroke-width="1.6"/><circle cx="52" cy="25" r="3.6" fill="var(--surface)" stroke="currentColor" stroke-width="1.6"/></svg>`;}'
            'return `<span class="tminis">${o}</span>`;}\n')
INCLUDED_HTML = ('<div class="pkg"><div class="inclbox"><h3>Always included in the price</h3><ul class="inc-list">'
                 + "".join(f"<li>{TICK}<span>{t}</span></li>" for t in [
                     "We do all the lifting and carrying",
                     "Loading, hauling and disposal fees",
                     "Drop-offs for donation and recycling",
                     "A sweep of the area when we finish",
                     "A price confirmed with you before we start",
                     "No tax added"])
                 + '</ul></div><div class="fits"><h3>What fits in a full truck?</h3>' + BIG_TRUCK
                 + '<p>About 16 cubic yards, roughly the box of a 10-foot moving truck. That is about:</p><ul class="fitlist">'
                 '<li><b>6</b> three-seat couches</li><li><b>12</b> queen mattresses</li><li><b>100</b> full garbage bags</li><li><b>6</b> pickup-truck loads</li></ul>'
                 '<p class="note">A half truck is half of that. Bigger jobs (1.5 or 2 loads) use the same truck with a second trip to the dump, or our 15 ft truck. Not sure? Text us a photo and we will tell you.</p></div></div>')
# services already has its own "Included in every job" section, so it gets only the truck panel
FITS_ONLY_HTML = '<div class="pkg one"><div class="fits">' + INCLUDED_HTML.split('<div class="fits">', 1)[1]
TAKE_CSS = r"""
.takes{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}
.tk{display:grid;gap:4px;align-content:start;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;text-decoration:none;color:var(--ink);transition:border-color .15s,transform .15s}
.tk:hover{border-color:var(--ink);transform:translateY(-2px)}
.tk:focus-visible{outline:3px solid var(--lime);outline-offset:2px}
.tki{width:58px;height:58px;border-radius:14px;background:var(--night);color:var(--lime);display:grid;place-items:center;margin-bottom:8px}
.tki svg{width:34px;height:34px}
.tk b{font-size:.98rem;line-height:1.25}
.tkp{font:700 .95rem var(--mono)}
.tk small{color:var(--muted);font-size:.8rem}
@media (prefers-reduced-motion:reduce){.tk,.tk:hover{transition:none;transform:none}}
@media (max-width:560px){.takes{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.tk{padding:13px}.tki{width:50px;height:50px}.tki svg{width:30px;height:30px}}
.notake{margin-top:18px;border:1.5px solid var(--line);border-left:6px solid var(--ink);border-radius:14px;padding:18px 20px;background:var(--surface);display:grid;gap:8px}
.notake p{color:var(--muted);font-size:.94rem}
.notake p b{color:var(--ink)}
.depots{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.depots a{display:inline-grid;gap:1px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;text-decoration:none;color:var(--ink);font-weight:700;font-size:.9rem}
.depots a small{font-weight:500;color:var(--muted);font-size:.76rem}
.depots a:hover{border-color:var(--ink)}
.tminis{display:inline-flex;gap:4px;color:var(--ink);vertical-align:middle}
.tmini{width:58px;height:28px;flex:none}
@media (max-width:600px){.tmini{width:42px;height:20px}.tminis{flex-wrap:wrap}}
.pkg{display:grid;grid-template-columns:1.1fr 1fr;gap:16px;margin-top:18px;align-items:start}
.inc-list li{font:500 1rem/1.4 var(--body);color:#eef3ec}
.pkg.one{grid-template-columns:minmax(0,560px)}
@media (max-width:820px){.pkg{grid-template-columns:1fr}}
.inclbox{background:var(--night);color:#eef3ec;border-radius:16px;padding:22px 24px}
.inclbox h3{color:#fff;margin-bottom:12px}
.inc-list{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.inc-list li{display:flex;gap:10px;align-items:flex-start}
.inc-list svg{width:20px;height:20px;flex:none;background:var(--lime);color:var(--night);border-radius:6px;padding:3px;margin-top:1px}
.fits{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:22px 24px;display:grid;gap:10px;align-content:start;color:var(--ink)}
.fits p{color:var(--muted);font-size:.94rem}
.tbig{width:150px;height:70px}
.fitlist{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:8px}
.fitlist li{border:1px dashed var(--line);border-radius:10px;padding:8px 10px;font-size:.9rem}
.fitlist b{display:block;font:800 1.3rem var(--display)}
"""


def truck_static(f):
    out = ""
    k = 0
    while k < f - 1e-9:
        w = max(0, min(1, f - k)) * 36.8
        out += BIG_TRUCK.replace('class="tbig"', 'class="tmini"').replace(' role="img" aria-label="A full truck"', ' aria-hidden="true"').replace('width="36.8"', f'width="{w:.1f}"')
        k += 1
    return '<span class="tminis">' + out + "</span>"


def page_icons(s):
    m = re.search(r"const ICONS=\{(.*?)\n\};", s, re.S)
    icons = dict(re.findall(r"(\w+):'([^']*)'", m.group(1))) if m else {}
    icons.update(NEW_ICONS)
    return icons


def take_tiles(s, prefix):
    items = {i: (int(solo), int(add)) for i, solo, add in re.findall(r'\{id:"(\w+)", t:"[^"]+", solo:(\d+), add:(\d+)', s)}
    mn = int(re.search(r"minCharge:\s*(\d+)", s).group(1))
    icons = page_icons(s)
    out = []
    for label, iid, ico, link, note in TAKE_TILES:
        if iid:
            if iid not in items:
                sys.exit("missing item " + iid)
            solo, add = items[iid]
            price, sub = f"from ${max(solo, mn):,}", (f"+${add} in a bigger load" if add else "No extra in a bigger load")
        else:
            price, sub = f"from ${mn}", note
        svg = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icons[ico]}</svg>'
        out.append(f'<a class="tk" href="{prefix}#quote-{link}"><span class="tki">{svg}</span><b>{label}</b><span class="tkp">{price}</span><small>{sub}</small></a>')
    return '<div class="takes">' + "".join(out) + "</div>"


def notake_html():
    links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}<small>{a}</small></a>' for n, u, a in DEPOTS)
    return ('<div class="notake"><h3>What we can\'t take</h3><p><b>Paint, solvents, fuel and chemicals, propane tanks, asbestos, and medical waste or needles.</b> '
            'Car batteries and tires: ask us first. Your city or region takes hazardous waste at its own drop-off depots, most of them free for residents:</p>'
            f'<div class="depots">{links}</div></div>')


ROUTE_ITEM_JS = ('  if(h.indexOf("quote-item-")===0){ const it=ITEMS.find(x=>x.id===h.slice(11)); if(!it) return;\n'
                 '    S.service="pickup"; S.mode="items"; S.items={}; S.items[it.id]=1; S.step=1; S.sent=null;\n'
                 '    render(); const q=document.getElementById("quote"); if(q) q.scrollIntoView(); return; }\n')


def price_visuals(s):
    """Truck drawings in the price table, the route for item tiles, and the extra CSS (all pages share renderStatic)."""
    # Nov 5: one rented truck per job, so jobs over a full truck are "loads" (a second trip to the dump, or the 15 ft truck), never "trucks"
    for a, b in [('t:"1.5 trucks"', 't:"1.5 loads"'), ('t:"2 trucks"', 't:"2 loads"'), ('<b>1.5 trucks</b>', '<b>1.5 loads</b>'), ('<b>2 trucks</b>', '<b>2 loads</b>'),
                 ('L.frac>1?L.id+" trucks"', 'L.frac>1?L.id+" loads"'), ('<span>2 trucks</span>', '<span>2 loads</span>'), ('5=1.5 trucks, 6=2 trucks', '5=1.5 loads, 6=2 loads'),
                 ('${c.loads} truck${c.loads>1?"s":""}</b><span>Loads to haul', '${c.loads>1?c.loads+" trips":"1 trip"}</b><span>Trips to the dump'),
                 ('Multi-truck job. We split it across trips or send a second truck.', 'Big job: one truck making a second trip to the dump, or our bigger 15 ft truck. The price already covers it.')]:
        s = s.replace(a, b)
    i = s.index("/* Layout concept")
    j = s.index("</style>", i)
    s = s[:j] + TAKE_CSS + OWNERS_CSS + s[j:]
    if 'id="pricetable"' in s:
        s = rep1("function renderStatic(){", TRUCK_JS + "function renderStatic(){", s, "truck js")
        s = rep1("<th>Fill</th>", "<th>How full</th>", s, "fill header", count=-1)
        s = rep1('<td><span class="bar8"><i style="width:${Math.min(100,l.frac*100)}%"></i></span></td>', "<td>${truckMini(l.frac)}</td>", s, "table trucks")
        s = rep1('<td><b>${LOADS[6].t}</b></td><td>A full house cleanout or hoarding clean-up</td><td><span class="bar8"><i style="width:100%"></i></span> x2</td>',
                 '<td><b>${LOADS[6].t}</b></td><td>A full house cleanout or hoarding clean-up</td><td>${truckMini(LOADS[6].frac)}</td>', s, "table 2 trucks")
        # the no-JS copy of the table gets the same drawings
        fr = iter([.125, .25, .5, .75, 1, 1.5, 2])
        s = re.sub(r'<td><span class="bar8"><i style="width:[\d.]+%"></i></span>(?: x2)?</td>', lambda m: "<td>" + truck_static(next(fr)) + "</td>", s)
    if "let low = r5(sub*lo), high = r5(sub*hi);" in s:
        # the low end of the range never goes under the minimum charge (or the outer-zone minimum)
        s = rep1("let low = r5(sub*lo), high = r5(sub*hi);",
                 "const floor = zone.z===4 ? CONFIG.farZoneMin : CONFIG.minCharge;\n  let low = Math.max(floor, r5(sub*lo)), high = Math.max(low, r5(sub*hi));", s, "range floor")
    if "function route(){" in s:
        s = rep1('  if(h.indexOf("quote-")!==0) return;\n', '  if(h.indexOf("quote-")!==0) return;\n' + ROUTE_ITEM_JS, s, "route items")
    return s


# ===== 2026-11-04 (round 2): real street map on the Areas page (Leaflet + OpenStreetMap), postal-code and location check =====
# Leaflet is self-hosted in vendor/leaflet (1.9.4, checksums match the official release). City outlines come from
# areas-map.json (make_map_data.py). Nothing loads until the map is about to scroll into view, so the page stays fast.
PC_HTML = ('<form class="pcbox" id="pcform" autocomplete="off"><label for="pc">Your postal code</label><div class="pcrow">'
           '<input type="text" id="pc" name="pc" maxlength="7" placeholder="e.g. M1B 2K3" autocapitalize="characters" spellcheck="false">'
           '<button class="btn hv" type="submit">Check my zone</button><button class="btn alt" type="button" id="locbtn">Use my location</button></div>'
           '<p id="pcout" class="pcout" aria-live="polite">We only look at the first 3 characters, and nothing is saved.</p></form>')
MAP_CSS = r"""
.mapbox.live{min-height:380px;background:#e9eef0}
.mapbox.live svg{position:static;inset:auto;width:auto;height:auto}  /* undo the old sketch rule (.mapbox svg) that broke Leaflet's shapes */
.pcrow input[type=text]::placeholder{text-transform:none;font-weight:500}
.mapbox.live .leaflet-container,.mapbox.live.leaflet-container{font:inherit}
.leaflet-tooltip.maptip{font:500 .82rem/1.35 var(--body);border-radius:8px;padding:6px 9px;box-shadow:0 4px 14px rgba(0,0,0,.18)}
.homepin span{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:#0A0F0D;color:#B8F334;font:800 .78rem var(--display);border:3px solid #B8F334;box-shadow:0 3px 10px rgba(0,0,0,.35)}
.maphint{position:absolute;left:50%;transform:translateX(-50%);top:10px;white-space:nowrap;z-index:1000;margin:0;background:rgba(10,15,13,.85);color:#fff;font-size:.78rem;padding:5px 11px;border-radius:99px;pointer-events:none}
.maphint[hidden]{display:none}
.legend .sw{display:inline-block;width:14px;height:14px;border-radius:4px;border:1px solid #0A0F0D;vertical-align:-2px;margin-right:6px}
.pcbox{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin-bottom:16px;display:grid;gap:8px}
.pcbox label{font-weight:700}
.pcrow{display:flex;gap:8px;flex-wrap:wrap}
.pcrow input[type=text]{flex:1 1 180px;width:auto;min-width:0;font:600 1.05rem var(--mono);text-transform:uppercase}
.pcout{color:var(--muted);font-size:.92rem}
.pcout b,.pcout a{color:var(--ink)}
.pcout a{font-weight:700}
@media (max-width:560px){.pcrow .btn{flex:1}}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .mapbox.live .leaflet-tile-pane{filter:invert(1) hue-rotate(180deg) brightness(.85) contrast(.9)}}
[data-theme="dark"] .mapbox.live .leaflet-tile-pane{filter:invert(1) hue-rotate(180deg) brightness(.85) contrast(.9)}
"""
MAP_JS = r"""<script>
/* ---------- Street map of the zones (loads only when it is about to scroll into view) ---------- */
(function(){
var box=document.getElementById("mapbox"); if(!box) return;
var FSA=__FSA__, SMSHREF="__SMS__";
var ZFILL={1:["#B8F334",.55],2:["#B8F334",.24],3:["#7C8C4C",.22],4:["#55605A",.16]};
var ALL=[[43.42,-79.82],[44.08,-78.80]];
var map=null, layers={}, data=null, started=false, current="Scarborough", hint=null;
function zoneFor(c){ for(var i=0;i<ZONES.length;i++){ if(ZONES[i].cities.indexOf(c)>=0) return ZONES[i]; } return ZONES[ZONES.length-1]; }
function pick(city){ var b=document.querySelector('#chips [data-city="'+city+'"]'); if(b) b.click(); else highlight(city); }
function style(city){ var z=zoneFor(city).z, f=ZFILL[z], on=city===current; return {color:"#0A0F0D",weight:on?3.5:(z===1?2:1),opacity:on?1:.55,fillColor:f[0],fillOpacity:f[1]}; }
function highlight(city){ current=city; if(!map) return; var hit=[];
  Object.keys(layers).forEach(function(c){ layers[c].forEach(function(l){ l.setStyle(style(c)); if(c===city){ l.bringToFront(); hit.push(l); } }); });
  if(hit.length) map.flyToBounds(L.featureGroup(hit).getBounds().pad(.35),{maxZoom:12,duration:.6});
  else map.flyToBounds(ALL,{duration:.6}); }
function start(){ if(started) return; started=true;
  var css=document.createElement("link"); css.rel="stylesheet"; css.href="vendor/leaflet/leaflet.css"; document.head.appendChild(css);
  var js=document.createElement("script"); js.src="vendor/leaflet/leaflet.js";
  js.onload=function(){ fetch("areas-map.json").then(function(r){ return r.json(); }).then(build).catch(function(){}); };
  document.head.appendChild(js); }
function build(d){ data=d; box.innerHTML=""; box.classList.add("live"); box.removeAttribute("role");
  map=L.map(box,{scrollWheelZoom:false,dragging:!L.Browser.mobile,tap:false,zoomSnap:.5,minZoom:8,maxZoom:17}).fitBounds(ALL);
  map.attributionControl.setPrefix(false);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
  d.areas.forEach(function(a){ var z=zoneFor(a.city), lyr=L.polygon(a.polys,style(a.city)).addTo(map);
    lyr.bindTooltip("<b>"+esc(a.label)+"</b><br>Zone "+z.z+" · "+(z.fee?"+"+money(z.fee)+" travel":"no travel charge"),{sticky:true,className:"maptip"});
    lyr.on("click",function(){ pick(a.city); });
    (layers[a.city]=layers[a.city]||[]).push(lyr); });
  L.marker([43.815,-79.255],{keyboard:false,icon:L.divIcon({className:"homepin",html:"<span>6ix</span>",iconSize:[38,38],iconAnchor:[19,19]})}).addTo(map)
    .bindTooltip("Our home base: Scarborough and Markham",{direction:"top",offset:[0,-16]});
  hint=document.createElement("p"); hint.className="maphint"; hint.textContent=L.Browser.mobile?"Tap the map to move it. Pinch to zoom.":"Click the map to zoom with your mouse wheel."; box.appendChild(hint);
  map.on("click",function(){ map.scrollWheelZoom.enable(); map.dragging.enable(); hint.hidden=true; });
  map.on("mouseout",function(){ map.scrollWheelZoom.disable(); });
  var lg=document.getElementById("maplegend");
  if(lg) lg.innerHTML=ZONES.map(function(z){ var f=ZFILL[z.z]; return '<span><i class="sw" style="background:'+f[0]+';opacity:'+Math.min(1,.3+f[1])+'"></i>Zone '+z.z+': '+z.name+(z.fee?" (+"+money(z.fee)+")":" (free)")+'</span>'; }).join("");
  highlight(current); }
document.addEventListener("click",function(e){ var b=e.target.closest&&e.target.closest("[data-city]"); if(b) highlight(b.dataset.city); });
if("IntersectionObserver" in window){ var io=new IntersectionObserver(function(es){ if(es.some(function(x){ return x.isIntersecting; })){ io.disconnect(); start(); } },{rootMargin:"400px"}); io.observe(box); } else start();
function inside(pt,ring){ var x=pt[1],y=pt[0],c=false; for(var i=0,j=ring.length-1;i<ring.length;j=i++){ var yi=ring[i][0],xi=ring[i][1],yj=ring[j][0],xj=ring[j][1]; if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi)) c=!c; } return c; }
var out=document.getElementById("pcout");
function say(h){ if(out) out.innerHTML=h; }
function result(city,label,prefix){ var z=zoneFor(city);
  say(prefix+" <b>"+esc(label)+"</b>: zone "+z.z+", "+(z.fee?"<b>+"+money(z.fee)+" travel</b>":"<b>no travel charge</b>")+(z.z===4?", larger jobs only":"")+'. <a href="index.html#quote-in-'+slug(city)+'">Price a job there</a>');
  pick(city); start(); }
var form=document.getElementById("pcform");
if(form) form.addEventListener("submit",function(e){ e.preventDefault();
  var v=(document.getElementById("pc").value||"").toUpperCase().replace(/[^A-Z0-9]/g,"").slice(0,3);
  if(!/^[A-Z][0-9][A-Z]$/.test(v)){ say("Type the first 3 characters of your postal code, like M1B."); return; }
  var hit=FSA[v];
  if(!hit){ say("<b>"+v+"</b> is outside our usual areas. We may still come for a larger job: <a data-sms href=\""+SMSHREF+"\">text us the address</a>."); pick("Other GTA"); return; }
  result(hit[0],hit[1],"<b>"+v+"</b> is in"); });
var loc=document.getElementById("locbtn");
if(loc){ if(!navigator.geolocation) loc.hidden=true; else loc.addEventListener("click",function(){ say("Finding you...");
  navigator.geolocation.getCurrentPosition(function(p){ var pt=[p.coords.latitude,p.coords.longitude];
    var go=function(){ var f=null; data.areas.forEach(function(a){ if(!f&&a.polys.some(function(poly){ return inside(pt,poly[0]); })) f=a; });
      if(f) result(f.city,f.label,"You are in"); else { say('You look to be outside our usual areas. <a href="index.html#quote">Start an estimate</a> and we will confirm.'); pick("Other GTA"); } };
    if(data) go(); else { start(); var n=0, t=setInterval(function(){ if(data){ clearInterval(t); go(); } else if(++n>60) clearInterval(t); },150); } },
  function(){ say("We could not get your location. Type your postal code instead."); },{timeout:10000,maximumAge:600000}); }); }
})();
</script>"""


def map_page(s):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from make_map_data import fsa_table
    i = s.index("/* Layout concept")
    j = s.index("</style>", i)
    s = s[:j] + MAP_CSS + s[j:]
    s = rep1('<h2>Tap your city to see the charge and how we book it.</h2></div>',
             '<h2>Type your postal code, or tap your city on the map.</h2></div>' + PC_HTML, s, "postal box")
    s = rep1("Tap a dot, or pick your city from the list below. The map is a simple sketch, not to scale.",
             "Tap an area on the map, or pick your city from the list below. Borders are approximate; we confirm the zone from your address.", s, "map note")
    s = rep1('<h2>Check your address</h2>', '<h2>Not sure of your zone?</h2>', s, "check address") if '<h2>Check your address</h2>' in s else s
    js = MAP_JS.replace("__FSA__", json.dumps(fsa_table(), separators=(",", ":"))).replace("__SMS__", SMS_HREF.replace("&amp;", "&"))
    return rep1("</body></html>", js + "</body></html>", s, "map js")


# ===== 2026-11-04 (round 2): the owners' story (names, no photo yet) and the cost guide link =====
OWNERS = ["Seythu", "Atheeshan"]
COST_PAGE = ("junk-removal-cost-toronto.html", "Junk removal cost guide")
TAKE_PAGE = ("what-can-junk-removal-take.html", "What we take and what we can't")
_OWNER_P = ('<p>We are two 21-year-olds from Scarborough and Markham, and 6ix Cleanout Co. is our business. There is no call centre and no crew you have never met: '
            'one of us gives you the price, the two of us do the lifting, and we sweep up before we leave.</p>'
            f'<p>We speak English and Tamil. If anything is not right, call or text either of us at <a data-call href="tel:{TEL}"><span data-phone>(647) 517-2721</span></a> and we will make it right.</p>')
def owners_html(extra=""):
    return ('<section id="owners" class="sec"><div class="owners"><div class="avatars" aria-hidden="true"><span>S</span><span>A</span></div><div>'
            '<p class="eyebrow">Who you will meet</p><h2>Hi, we are Seythu and Atheeshan.</h2>' + _OWNER_P + extra
            + '<p class="sig">Seythu &amp; Atheeshan, owners</p></div></div></section>')
OWNERS_ABOUT_EXTRA = ('<p>We launched in November 2026.<span data-launch> Our first 25 customers get launch prices.</span>'
                      '<span data-until="' + "2026-11-24" + '"> In launch week we are clearing one home for free: the <a href="giveback.html">Scarborough Giveback Cleanout</a>.</span></p>')
OWNERS_CSS = r"""
.owners{display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:start;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:clamp(22px,4vw,36px)}
.owners p{color:var(--muted);max-width:66ch;margin-top:10px}
.owners p a{color:var(--ink);font-weight:700}
.owners .sig{color:var(--ink);font-weight:800;font-family:var(--display)}
.avatars{display:flex}
.avatars span{width:76px;height:76px;border-radius:50%;display:grid;place-items:center;font:800 1.9rem var(--display);border:4px solid var(--surface)}
.avatars span:first-child{background:var(--night);color:var(--lime)}
.avatars span+span{background:var(--lime);color:var(--night);margin-left:-18px}
@media (max-width:640px){.owners{grid-template-columns:1fr}.avatars span{width:62px;height:62px;font-size:1.5rem}}
.exgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.exgrid>div{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;display:grid;gap:8px;align-content:start}
.exgrid p{color:var(--muted);font-size:.93rem}
.exgrid .tkp{color:var(--ink);font-size:1.15rem}
.costlink{display:inline-block;margin-top:10px;font-weight:700;color:var(--ink)}
"""


# ===== 2026-11-04 (round 2): seniors 10% off and "booking for someone else" in the estimator =====
SENIOR_PCT = 10
def estimator_extras(s):
    s = rep1('consent:false, sent:null', 'consent:false, senior:false, forOther:false, otherName:"", otherPhone:"", sent:null', s, "DEFAULT extras")
    s = rep1('.join("")}</select></label></div></div>`;\n  } else if(s.step===1){',
             '.join("")}</select></label></div>\n    <label class="check"><input type="checkbox" id="senior" ${s.senior?"checked":""}><span>Someone 65 or older lives here. '
             '<em style="color:var(--muted)">Seniors save ' + str(SENIOR_PCT) + '%, down to the ${money(CONFIG.minCharge)} minimum.</em></span></label></div>`;\n  } else if(s.step===1){',
             s, "senior checkbox")
    s = rep1('<div class="grid2"><div><label class="f" for="name"><span>Name</span></label>',
             '<label class="check"><input type="checkbox" id="forOther" ${s.forOther?"checked":""}><span>I am booking for someone else, like a parent or relative. '
             '<em style="color:var(--muted)">We will call you to arrange it.</em></span></label>\n    '
             '${s.forOther?`<div class="grid2"><div><label class="f" for="otherName"><span>Their name<em>the person at the address</em></span></label><input type="text" id="otherName" value="${esc(s.otherName)}"></div>'
             '<div><label class="f" for="otherPhone"><span>Their phone<em>optional</em></span></label><input type="tel" id="otherPhone" value="${esc(s.otherPhone)}"></div></div>`:""}\n    '
             '<div class="grid2"><div><label class="f" for="name"><span>${s.forOther?"Your name":"Name"}</span></label>', s, "for other")
    s = rep1('["notes","name","phone","email","date"].includes(t.id)', '["notes","name","phone","email","date","otherName","otherPhone"].includes(t.id)', s, "input extras")
    s = rep1('else if(t.id==="hoard"){S.hoard=t.checked; ticketOnly();}',
             'else if(t.id==="hoard"){S.hoard=t.checked; ticketOnly();}\n  else if(t.id==="senior"){S.senior=t.checked; ticketOnly();}\n  else if(t.id==="forOther"){S.forOther=t.checked; render(true);}', s, "change extras")
    # the discount: 10% of the job (before travel and priority), never taking it under the minimum charge
    s = rep1('  if(zone.fee){ sub+=zone.fee;',
             '  if(s.senior){ const d=Math.min(Math.round(sub*' + str(SENIOR_PCT / 100) + '), Math.max(0, sub-CONFIG.minCharge)); if(d>0){ sub-=d; L.push(["ln","Seniors 65+ (' + str(SENIOR_PCT) + '% off)","−"+money(d)]); } }\n'
             '  if(zone.fee){ sub+=zone.fee;', s, "senior calc")
    s = rep1('"Notes":["Contact: "+S.contact,"Language: "+S.lang,',
             '"Notes":["Contact: "+S.contact,"Language: "+S.lang,S.senior?"Seniors 65+: yes (' + str(SENIOR_PCT) + '% off)":"",S.forOther?"Booking for someone else. On-site contact: "+(S.otherName||"not given")+(S.otherPhone?" "+S.otherPhone:""):"",', s, "notes extras")
    s = rep1('`Contact by: ${S.contact} · Language: ${S.lang}`,',
             '`Contact by: ${S.contact} · Language: ${S.lang}`,...(S.senior?["Seniors 65+: yes, ' + str(SENIOR_PCT) + '% off"]:[]),...(S.forOther?["Booking for someone else. On-site contact: "+(S.otherName||"not given")+(S.otherPhone?" "+S.otherPhone:"")]:[]),', s, "summary extras")
    # Nov 5: "Other language" so the owners can see which languages customers need before adding more language pages
    s = rep1('lang:"English",', 'lang:"English", langOther:"",', s, "DEFAULT langOther")
    s = rep1('[["English","English"],["Tamil","தமிழ் (Tamil)"]]', '[["English","English"],["Tamil","தமிழ் (Tamil)"],["Other","Other language"]]', s, "lang options")
    s = rep1('.join("")}</select></div></div>\n    <label class="f" for="heard">',
             '.join("")}</select></div></div>\n    ${s.lang==="Other"?`<label class="f" for="langOther"><span>Which language?<em>we will do our best to help</em></span></label>'
             '<input type="text" id="langOther" value="${esc(s.langOther)}" placeholder="For example Mandarin, Punjabi, Tagalog">`:""}\n    <label class="f" for="heard">', s, "langOther field")
    s = rep1('else if(t.id==="lang"){S.lang=t.value;}', 'else if(t.id==="lang"){S.lang=t.value; render(true);}', s, "lang change")
    s = rep1('"date","otherName","otherPhone"]', '"date","otherName","otherPhone","langOther"]', s, "langOther input")
    LANG = '(S.lang==="Other"?"Other ("+(S.langOther||"not given")+")":S.lang)'
    s = rep1('"Language: "+S.lang,', '"Language: "+' + LANG + ',', s, "notes lang")
    s = rep1('Language: ${S.lang}`', 'Language: ${' + LANG + '}`', s, "summary lang")
    return s


def wrap_phero(s, extra_cta=True):
    s = rep1('<section class="phero">', '<div class="hband"><section class="phero">', s, "phero open")
    i = s.index('<div class="hband"><section class="phero">')
    j = s.index("</section>", i)
    s = s[:j] + "</section></div>" + s[j + len("</section>"):]
    if extra_cta:
        k = s.index('<div class="cta">', i)
        end = s.index("</div>", k)
        s = s[:end] + CALL_BTN + SMS_BTN + s[end:]
    return s


def index_page(s):
    hero_new = ('<div>\n    ' + LAUNCH_DARK + '\n'
                '    <h1><span class="kick">Junk removal in Scarborough, Markham &amp; the GTA</span>Junk gone. <span class="lime">Space back.</span></h1>\n'
                '    <p class="lead">Know your price in 2 minutes, before we show up. Couches, appliances, garages, basements and full cleanouts. We do all the lifting, haul it away and sweep up.</p>\n'
                f'    <div class="cta"><a class="btn hv" href="#quote">Get my free estimate</a>{CALL_BTN}{SMS_BTN}</div>\n'
                '  <div class="factrow">')
    s = sub1(r'<div>\s*<p class="eyebrow"><span data-tag>Cleanouts across the GTA</span>.*?<div class="factrow">', lambda m: hero_new, s,
             flags=re.S, label="index hero copy")
    s = rep1('<section class="hero">', '<div class="hband"><section class="hero">', s, "hero open")
    s = rep1('</aside></section><section id="quote"', '</aside></section></div>' + TRUST_HTML + '<section id="quote"', s, "hero close")
    why = ('<section id="why" class="sec"><div class="head"><p class="eyebrow">Why 6ix Cleanout</p><h2>Local, upfront and careful.</h2></div><div class="why">'
           '<div><span class="num">1</span><h3>Your price in 2 minutes</h3><p>Most junk removal companies only give a firm price once they are at your door. You see a range online and get a confirmed price before we start.</p></div>'
           '<div><span class="num">2</span><h3>The owners do the job</h3><p>We are two local owners from Scarborough and Markham, and we show up ourselves. No call centre and no strangers you did not book.</p></div>'
           '<div><span class="num">3</span><h3>We leave it swept</h3><p>We do all the lifting and carrying, protect floors and doorways on the way out, and sweep up before we leave.</p></div>'
           '<div><span class="num">4</span><h3>Donate and recycle first</h3><p>Usable items go to donation, and metal and electronics go to recycling. Only what is left goes to a licensed site.</p></div>'
           '</div></section>'
           + GIVEBACK_HTML +
           '<section id="reviews" class="sec" data-reviews hidden><div class="head"><p class="eyebrow">Reviews</p><h2>What customers say.</h2></div><div class="revs"></div></section>')
    s = rep1('</section><section id="pricing" class="sec">', '</section>' + why + '<section id="pricing" class="sec">', s, "why section")
    s = rep1('<div class="head"><p class="eyebrow">Typical prices</p>', '<div class="head">' + LAUNCH_LIGHT + '<p class="eyebrow">Typical prices</p>', s, "pricing launch")
    s = sub1(r'(<p class="note" id="addons"[^>]*>.*?</p>)', lambda m: m.group(1) + SAVE_HTML, s, flags=re.S, label="addons note")
    # JSON-LD fixes
    s = rep1('"priceRange":"$130 to $1,250 CAD"', '"priceRange":"$129 to $1,250 CAD"', s, "priceRange")
    s = rep1('"paymentAccepted":"Credit card, Interac e-Transfer"', '"paymentAccepted":"Cash, Interac e-Transfer","knowsLanguage":["en","ta"],'
             + json.dumps(biz_extra(), ensure_ascii=False, separators=(",", ":"))[1:-1], s, "payment")
    s = s.replace('content="6ix Cleanout Co. | Junk removal and property clean outs, Toronto and the GTA"',
                  'content="6ix Cleanout Co. | Junk removal in Scarborough, Markham and the GTA"')
    # lead source: "how did you hear" question, saved into the Notes column of the tracker
    s = rep1('const TOD = ["Any time","Morning","Afternoon","Evening"];',
             'const TOD = ["Any time","Morning","Afternoon","Evening"];\n'
             'const HEARD = ["Choose one","Google search or Maps","Facebook or Instagram","TikTok","Facebook Marketplace","Flyer or door hanger","Friend, family or neighbour","Realtor or property manager","Other"];',
             s, "TOD")
    s = rep1('confirm:"photos", notes:"",', 'confirm:"photos", notes:"", heard:"", contact:"Text", lang:"English",', s, "DEFAULT heard")
    # coming from the Tamil page (?lang=ta) preselects Tamil
    s = rep1('let S = JSON.parse(JSON.stringify(DEFAULT));',
             'try{ if(new URLSearchParams(location.search).get("lang")==="ta") DEFAULT.lang="Tamil"; }catch(e){}\n'
             'let S = JSON.parse(JSON.stringify(DEFAULT));', s, "S init")
    s = rep1('<label class="f" for="notes"><span>Anything else we should know?',
             '<div class="grid2"><div><label class="f" for="contact"><span>Best way to reach you</span></label><select id="contact">${["Text","Call","Email"].map(h=>`<option ${h===s.contact?"selected":""}>${h}</option>`).join("")}</select></div>'
             '<div><label class="f" for="lang"><span>Language<em>மொழி</em></span></label><select id="lang">${[["English","English"],["Tamil","தமிழ் (Tamil)"]].map(([v,t])=>`<option value="${v}" ${v===s.lang?"selected":""}>${t}</option>`).join("")}</select></div></div>\n    '
             '<label class="f" for="heard"><span>How did you hear about us?<em>optional</em></span></label><select id="heard">${HEARD.map(h=>`<option ${h===s.heard?"selected":""}>${h}</option>`).join("")}</select>\n    '
             '<label class="f" for="notes"><span>Anything else we should know?', s, "heard select")
    s = rep1('else if(t.id==="file"){addPhotos(t.files); t.value="";}',
             'else if(t.id==="heard"){S.heard=t.value;}\n  else if(t.id==="contact"){S.contact=t.value;}\n  else if(t.id==="lang"){S.lang=t.value;}\n  else if(t.id==="file"){addPhotos(t.files); t.value="";}', s, "heard change")
    s = rep1('"Notes":S.notes||""',
             '"Notes":["Contact: "+S.contact,"Language: "+S.lang,window.leadSourceText?leadSourceText():"",(S.heard&&S.heard!==HEARD[0])?"Heard: "+S.heard:"",S.notes||""].filter(Boolean).join(" | ")',
             s, "notes value")
    s = sub1(r'(`Price confirmation: \$\{\(CONFIRM\.find\(x=>x\.id===S\.confirm\)\|\|CONFIRM\[0\]\)\.short\}`,)',
             lambda m: m.group(1) + '`Contact by: ${S.contact} · Language: ${S.lang}`,`Heard about us: ${(S.heard&&S.heard!==HEARD[0])?S.heard:"not given"}`,', s, label="summary heard")
    s = rep1("Keep your reference number handy. If you do not hear from us within a day, text us the summary below.",
             "Keep your reference number handy. We usually reply within an hour between 8am and 8pm. If you have not heard from us by then, text us the summary below.",
             s, "done screen reply time")
    s = rep1('if(res.some(Boolean)||photoState==="sent") S.sent.delivered=true; else S.sent.failed=true;',
             'if(res.some(Boolean)||photoState==="sent"){ S.sent.delivered=true; if(window.track6) track6("Lead",{value:c.low,currency:"CAD",content_name:svc.t}); } else S.sent.failed=true;',
             s, "lead event")
    return s


def faq_jsonld(s):
    i = s.index("const FAQ = [")
    j = s.index("];", i)
    faq = json.loads(s[i + len("const FAQ = "):j + 1])
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


def guide_section(eyebrow, title, links, intro=""):
    a = "".join(f'<a href="{f}">{t}</a>' for f, t in links)
    p = f"<p>{intro}</p>" if intro else ""
    return f'<section class="sec"><div class="head"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2>{p}</div><div class="guide">{a}</div></section>'


def main():
    for page in PAGES:
        s = shared(base(page), page)
        if page == "index":
            s = index_page(s)
            s = estimator_extras(s)
        else:
            s = wrap_phero(s)
        if page == "about":
            s = rep1("We keep the process simple: a clear price first, careful work, and a swept finish.",
                     "We keep the process simple: a clear price first, careful work, and a swept finish. We speak English and Tamil.", s, "about lead")
            s = rep1("</head>", faq_jsonld(s) + "</head>", s, "about head")
        if page == "areas":
            s = rep1("</head>", ld_tag(biz_ld(AREAS_ALL)) + "</head>", s, "areas head")
        if page == "services":
            loads = re.findall(r'\{id:"[^"]+",\s*t:"([^"]+)",\s*frac:[.\d]+,\s*price:(\d+)', s)
            if len(loads) != 7:
                sys.exit("could not read LOADS on services")
            svc = dict(biz_ld(AREAS_ALL), hasOfferCatalog={"@type": "OfferCatalog", "name": "Junk removal prices by truck space (no tax added)",
                       "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Junk removal: " + t.lower().replace("trucks", "loads")},
                                            "price": p, "priceCurrency": "CAD"} for t, p in loads]})
            s = rep1("</head>", ld_tag(svc) + "</head>", s, "services head")
        if page == "realtors-landlords":
            s = rep1("</head>", ld_tag({"@context": "https://schema.org", "@type": "Service",
                                        "name": "Move-out and unit turnover junk removal for realtors, landlords and property managers",
                                        "serviceType": "Junk removal", "areaServed": "Greater Toronto Area",
                                        "audience": {"@type": "BusinessAudience", "audienceType": "Realtors, landlords and property managers"},
                                        "provider": biz_ld(AREAS_ALL)}) + "</head>", s, "realtors head")
        if page == "areas":
            s = rep1("</main>", guide_section("City guides", "Junk removal near you.", [(f, "Junk removal in " + c) for f, c in CITY_PAGES],
                                              "Local prices, neighbourhoods and city pickup rules for the places we work most.") + "</main>", s, "areas main")
        if page == "services":
            s = rep1("</main>", '<section class="sec"><div class="head">' + LAUNCH_LIGHT + '<p class="eyebrow">Ways to save</p><h2>Keep the price down.</h2></div>'
                     + SAVE_HTML + "</section>" + guide_section("Popular jobs", "Guides for the jobs we do most.", ITEM_PAGES) + "</main>", s, "services main")
        s = price_visuals(s)
        s = s.replace('The estimate tool above adds those for your address.</p>',
                      f'The estimate tool above adds those for your address.</p><a class="costlink" href="{COST_PAGE[0]}">See the full cost guide, with worked examples →</a>')
        if page == "index":
            s = rep1('<section id="giveback"', owners_html() + '<section id="giveback"', s, "owners home")
        if page == "about":
            s = rep1('</section></div>', '</section></div>' + owners_html(OWNERS_ABOUT_EXTRA), s, "owners about")
        if 'id="pricetable"' in s:
            s = sub1(r'(<table id="pricetable">.*?</table></div>)', lambda m: m.group(1) + (INCLUDED_HTML if page == "index" else FITS_ONLY_HTML), s, flags=re.S, label="included box")
        if page == "index":
            take = ('<section id="take" class="sec"><div class="head"><p class="eyebrow">What we take</p><h2>Almost anything that is not hazardous.</h2>'
                    '<p>Tap an item to price it. Prices are for the item on its own, before travel. In a bigger load, most items add little or nothing.</p></div>'
                    + take_tiles(s, "") + notake_html() + '</section>')
            s = rep1('<section id="pricing" class="sec">', take + '<section id="pricing" class="sec">', s, "take section")
        if page == "services":
            s = rep1('<h2>Most household and light renovation items.</h2></div>',
                     '<h2>Most household and light renovation items.</h2><p>Tap an item to price it in the estimator.</p></div>' + take_tiles(s, "index.html")
                     + '<div style="height:18px"></div>', s, "services tiles")
            links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}<small>{a}</small></a>' for n, u, a in DEPOTS)
            s = rep1("Your city has a household hazardous waste drop-off.</p>",
                     'Your city or region takes them at its own drop-off depots, most of them free for residents:</p><div class="depots">' + links + "</div>",
                     s, "services depots")
        if page == "areas":
            s = map_page(s)
        s = social_tags(s)
        (ROOT / f"{page}.html").write_text(s, encoding="utf-8", newline="\n")
        print("patched", page)


if __name__ == "__main__":
    main()
