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
              ("junk-removal-north-york.html", "North York"), ("junk-removal-pickering.html", "Pickering"),
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
.launch.on-light{background:var(--night);border-color:var(--night)}
.launch .dot{width:8px;height:8px;border-radius:50%;background:var(--lime);animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(184,243,52,.6)}70%{box-shadow:0 0 0 8px rgba(184,243,52,0)}100%{box-shadow:0 0 0 0 rgba(184,243,52,0)}}
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
.save{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:18px}
@media (max-width:820px){.save{grid-template-columns:1fr}}
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

LAUNCH_DARK = '<p class="launch" data-launch hidden><span class="dot"></span>Launch pricing · <b data-spots>25 of 25</b> spots left</p>'
LAUNCH_LIGHT = '<p class="launch on-light" data-launch hidden><span class="dot"></span>Launch pricing · <b data-spots>25 of 25</b> spots left</p>'

SAVE_HTML = ('<div class="save">'
             '<div><b>Single items on route days</b><p>Choose "Flexible" timing and we add you to our next route day. That is how we keep single pickups at <span data-min>$129</span>.</p></div>'
             '<div><b>Neighbour bundle: $20 off each</b><p>Book with a neighbour on the same street for the same day and you both save $20.</p></div>'
             '<div><b>Refer a friend: $25 off</b><p>Get $25 off your next job for every friend who books with us.</p></div></div>')

TRUST_HTML = ('<div class="trust" aria-label="What you get with every job"><span>No tax added</span><span>Price confirmed before we start</span>'
              f'<span>Loaded, hauled and swept</span><span>Donate and recycle first</span><span>{TAMIL}&nbsp;· English and Tamil</span></div>')

TITLES = {
    "index": ("Junk Removal Scarborough &amp; Markham | 6ix Cleanout Co.",
              "Junk removal in Scarborough, Markham and the GTA. Your price in 2 minutes, no tax added. Furniture, appliances, garages, cleanouts. Call (647) 517-2721."),
    "services": ("Junk Removal Services and Prices | 6ix Cleanout Co.",
                 "Junk removal across the GTA: home cleanouts, move-outs, single items, estates, garages and reno debris. Prices from $129, no tax added."),
    "realtors-landlords": ("Move-Out Junk Removal for Realtors &amp; Landlords | 6ix Cleanout", None),
    "areas": ("Junk Removal Service Areas Across the GTA | 6ix Cleanout Co.", None),
    "about": ("About Us and FAQ | 6ix Cleanout Co. Junk Removal", None),
}

SITE_URL = "https://6ixcleanoutco-cmyk.github.io/6ix-cleanout/"
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
    items = "".join(f'<a href="{f}">{t}</a>' for f, t in ITEM_PAGES)
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
           '<section id="reviews" class="sec" data-reviews hidden><div class="head"><p class="eyebrow">Reviews</p><h2>What customers say.</h2></div><div class="revs"></div></section>')
    s = rep1('</section><section id="pricing" class="sec">', '</section>' + why + '<section id="pricing" class="sec">', s, "why section")
    s = rep1('<div class="head"><p class="eyebrow">Typical prices</p>', '<div class="head">' + LAUNCH_LIGHT + '<p class="eyebrow">Typical prices</p>', s, "pricing launch")
    s = sub1(r'(<p class="note" id="addons"[^>]*>.*?</p>)', lambda m: m.group(1) + SAVE_HTML, s, flags=re.S, label="addons note")
    # JSON-LD fixes
    s = rep1('"priceRange":"$130 to $1,250 CAD"', '"priceRange":"$129 to $1,250 CAD"', s, "priceRange")
    s = rep1('"paymentAccepted":"Credit card, Interac e-Transfer"', '"paymentAccepted":"Cash, Interac e-Transfer","knowsLanguage":["en","ta"]', s, "payment")
    s = s.replace('content="6ix Cleanout Co. | Junk removal and property clean outs, Toronto and the GTA"',
                  'content="6ix Cleanout Co. | Junk removal in Scarborough, Markham and the GTA"')
    # lead source: "how did you hear" question, saved into the Notes column of the tracker
    s = rep1('const TOD = ["Any time","Morning","Afternoon","Evening"];',
             'const TOD = ["Any time","Morning","Afternoon","Evening"];\n'
             'const HEARD = ["Choose one","Google search or Maps","Facebook or Instagram","TikTok","Facebook Marketplace","Flyer or door hanger","Friend, family or neighbour","Realtor or property manager","Other"];',
             s, "TOD")
    s = rep1('confirm:"photos", notes:"",', 'confirm:"photos", notes:"", heard:"",', s, "DEFAULT heard")
    s = rep1('<label class="f" for="notes"><span>Anything else we should know?',
             '<label class="f" for="heard"><span>How did you hear about us?<em>optional</em></span></label><select id="heard">${HEARD.map(h=>`<option ${h===s.heard?"selected":""}>${h}</option>`).join("")}</select>\n    '
             '<label class="f" for="notes"><span>Anything else we should know?', s, "heard select")
    s = rep1('else if(t.id==="file"){addPhotos(t.files); t.value="";}',
             'else if(t.id==="heard"){S.heard=t.value;}\n  else if(t.id==="file"){addPhotos(t.files); t.value="";}', s, "heard change")
    s = rep1('"Notes":S.notes||""',
             '"Notes":[window.leadSourceText?leadSourceText():"",(S.heard&&S.heard!==HEARD[0])?"Heard: "+S.heard:"",S.notes||""].filter(Boolean).join(" | ")',
             s, "notes value")
    s = sub1(r'(`Price confirmation: \$\{\(CONFIRM\.find\(x=>x\.id===S\.confirm\)\|\|CONFIRM\[0\]\)\.short\}`,)',
             lambda m: m.group(1) + '`Heard about us: ${(S.heard&&S.heard!==HEARD[0])?S.heard:"not given"}`,', s, label="summary heard")
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
        else:
            s = wrap_phero(s)
        if page == "about":
            s = rep1("We keep the process simple: a clear price first, careful work, and a swept finish.",
                     "We keep the process simple: a clear price first, careful work, and a swept finish. We speak English and Tamil.", s, "about lead")
            s = rep1("</head>", faq_jsonld(s) + "</head>", s, "about head")
        if page == "areas":
            s = rep1("</main>", guide_section("City guides", "Junk removal near you.", [(f, "Junk removal in " + c) for f, c in CITY_PAGES],
                                              "Local prices, neighbourhoods and city pickup rules for the places we work most.") + "</main>", s, "areas main")
        if page == "services":
            s = rep1("</main>", '<section class="sec"><div class="head">' + LAUNCH_LIGHT + '<p class="eyebrow">Ways to save</p><h2>Keep the price down.</h2></div>'
                     + SAVE_HTML + "</section>" + guide_section("Popular jobs", "Guides for the jobs we do most.", ITEM_PAGES) + "</main>", s, "services main")
        s = social_tags(s)
        (ROOT / f"{page}.html").write_text(s, encoding="utf-8", newline="\n")
        print("patched", page)


if __name__ == "__main__":
    main()
