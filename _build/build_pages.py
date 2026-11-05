"""Builds the city and item landing pages from the patched about.html shell.

Run patch_shared.py first, then this script. The header, footer, styles and scripts
come from about.html, and prices and zones are read from index.html, so the new pages
never drift from the main site. Page copy lives in CITIES and ITEMS below.
Run:  python _build/build_pages.py
"""
import datetime, html, json, pathlib, re, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from patch_shared import (CALL_BTN, SMS_BTN, LAUNCH_DARK, LAUNCH_LIGHT, LAUNCH_TEXT, SAVE_HTML, TRUST_HTML,  # noqa: E402
                          CITY_PAGES, ITEM_PAGES, social_tags, ICO_PHONE, ICO_MSG, biz_ld, GIVEBACK_UNTIL, HOURS_LD,
                          truck_static, SENIOR_PCT, COST_PAGE, TAKE_PAGE, OWNERS, DEPOTS, notake_html)

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://6ixcleanoutco-cmyk.github.io/6ix-cleanout/"
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
SHELL = (ROOT / "about.html").read_text(encoding="utf-8")

LOAD_PRICES = [int(p) for p in re.findall(r'\{id:"[^"]+",\s*t:"[^"]+",\s*frac:[.\d]+,\s*price:(\d+)', INDEX)]
ZONES = {c: (int(z), int(fee)) for z, fee, cs in re.findall(r'\{z:(\d), name:"[^"]+", fee:(\d+), cities:\[([^\]]*)\]', INDEX)
         for c in re.findall(r'"([^"]+)"', cs)}
ITEM_PRICE = {i: (int(s), int(a)) for i, s, a in re.findall(r'\{id:"(\w+)", t:"[^"]+", solo:(\d+), add:(\d+)', INDEX)}
MIN = int(re.search(r"minCharge: (\d+)", INDEX).group(1))
assert len(LOAD_PRICES) == 7 and ZONES and ITEM_PRICE, "could not read prices from index.html"
BOOK = {1: "Any day, often within the week", 2: "Most days", 3: "On our route days for the east end"}
ROWS = [("A few items", "A couch, a mattress or a few bags"), ("Quarter truck", "One small room, or a couch plus a few boxes"),
        ("Half truck", "A bedroom, or a full basement corner"), ("Three-quarter truck", "A living room plus extras"),
        ("Full truck", "A one-bedroom apartment or a packed garage")]

TORONTO_CURB = ('<p>The City of Toronto picks up oversized items like furniture and mattresses beside your garbage bin on your collection day, for houses on city collection. '
                'If you can carry it to the curb yourself and you can wait, that is a good free option.</p>'
                '<p><b>Call us when</b> it has to go now, it is stuck in a basement or up a flight of stairs, you live in a condo or apartment, or there is more than the curb program takes.</p>'
                '<p class="note">City rules change. Check the <a href="https://www.toronto.ca/services-payments/recycling-organics-garbage/houses/oversized-metal-items/" rel="noopener">City of Toronto oversized items page</a> for the current details.</p>')
DURHAM_CURB = ('<p>Durham Region picks up furniture and large items on your regular every-other-week garbage day, up to two items per pickup, set out by 7 a.m. '
               'Metal items, electronics and porcelain need an appointment.</p>'
               '<p><b>Call us when</b> you have more than two items, it needs carrying out of the house, or you cannot wait for the next garbage day.</p>'
               '<p class="note">Check <a href="https://www.durham.ca/living-here/garbage-green-bin-and-other-collection/curbside-collection/furniture-and-large-item-collection/" rel="noopener">Durham Region\'s furniture and large item page</a> for current rules.</p>')

CITIES = {
    "Scarborough": dict(
        slug="scarborough", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Scarborough is our home base. Basements, garages, backyards and condo units cleared by the owners themselves, with your price in 2 minutes online and no tax added.",
        hoods=["Agincourt", "Malvern", "Wexford", "Birch Cliff", "Cliffside", "Guildwood", "West Hill", "Highland Creek", "Morningside",
               "Scarborough Village", "L'Amoreaux", "Milliken", "Bendale", "Dorset Park", "Woburn", "Rouge"],
        hood_intro="We cover every part of Scarborough, from the Bluffs to Steeles. Same-week bookings are often possible here.",
        curb_title="City pickup or us?", curb=TORONTO_CURB,
        jobs=[("Basement cleanouts", "Old couches, boxes, exercise machines and the things nobody has touched in years, carried up and out."),
              ("Condo and apartment clear-outs", "We work with your building's freight elevator booking and loading area. Send us the building rules when you book."),
              ("Garage and backyard junk", "Broken patio sets, old bikes, lumber and yard clutter cleared in one visit.")],
        faqs=[("Do you charge travel in Scarborough?", "No. Scarborough is in our home zone, so there is no travel charge. The price you see online is for your Scarborough address."),
              ("Can you take things from a Scarborough condo?", "Yes. Most buildings need a booked freight elevator. Tell us the building name and any rules when you book, and we plan the time around the elevator booking."),
              ("Do you speak Tamil?", "Yes. We speak English and Tamil, so you can call or text us in either language.")]),
    "Markham": dict(
        slug="markham", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Markham and Unionville are part of our home zone. Garage cleanouts, move-outs and single items, priced online in 2 minutes with no travel charge and no tax added.",
        hoods=["Unionville", "Markham Village", "Milliken Mills", "Cornell", "Berczy Village", "Cathedraltown", "Box Grove", "Wismer",
               "Greensborough", "Angus Glen", "Cachet", "Thornhill (Markham side)"],
        hood_intro="We cover all of Markham, including Unionville and the newer neighbourhoods in the north and east.",
        curb_title="City pickup or us?",
        curb=('<p>The City of Markham collects bulky items such as furniture and mattresses at the curb every other week on your garbage day, up to three items, set out by 7 a.m. No appointment is needed. '
              'Condos and apartments go through their property manager.</p>'
              '<p><b>Call us when</b> you have more than three items, it needs carrying out of the house, or you are moving and cannot wait two weeks.</p>'
              '<p class="note">Check the <a href="https://www.markham.ca/neighbourhood-services/recycling-garbage/furniture-bulky-items" rel="noopener">City of Markham bulky items page</a> for current rules.</p>'),
        jobs=[("Garage cleanouts", "Full or half garages cleared so the car fits again. We sort out what can be donated or recycled."),
              ("Move-out and move-in clear-ups", "Everything the movers will not take, plus packaging and boxes after you move in."),
              ("Townhouse and condo pickups", "We plan around visitor parking and building rules. Tell us about parking when you book.")],
        faqs=[("Is there a travel charge for Markham or Unionville?", "No. Markham and Unionville are in our home zone, so there is no travel charge."),
              ("Can you clear a garage in one visit?", "Most garages fit in a half to full truck and take one visit. Send photos and we confirm the price and time before we come."),
              ("What happens to things that still work?", "We set aside usable items for donation where we can. Metal and electronics go to recycling, and only what is left goes to a licensed site.")]),
    "Unionville": dict(
        slug="unionville", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Unionville is part of our home zone. Garage cleanouts, move-outs, downsizing and single items, priced online in 2 minutes with no travel charge and no tax added.",
        hoods=["Main Street Unionville", "Toogood Pond", "Angus Glen", "Unionville Station area", "Rouge Valley side", "Cachet"],
        hood_intro="We cover all of Unionville, from the Main Street heritage homes to the newer streets around Highway 7 and Kennedy Road.",
        curb_title="City pickup or us?",
        curb=('<p>Unionville is part of the City of Markham, which collects bulky items such as furniture and mattresses at the curb every other week on your garbage day, up to three items, set out by 7 a.m. No appointment is needed. '
              'Condos and apartments go through their property manager.</p>'
              '<p><b>Call us when</b> you have more than three items, it needs carrying out of the house, or you are moving and cannot wait two weeks.</p>'
              '<p class="note">Check the <a href="https://www.markham.ca/neighbourhood-services/recycling-garbage/furniture-bulky-items" rel="noopener">City of Markham bulky items page</a> for current rules.</p>'),
        jobs=[("Downsizing and estate clear-outs", "Calm, careful clearing of a family home. We work from your list of what stays and set aside usable items for donation where we can."),
              ("Garage and basement cleanouts", "Full or half garages and finished basements cleared in one visit, carried out and swept."),
              ("Move-out and move-in clear-ups", "Everything the movers will not take, plus packaging and boxes after you move in.")],
        faqs=[("Is there a travel charge for Unionville?", "No. Unionville is in our home zone, so there is no travel charge. The price you see online is for your Unionville address."),
              ("Do you serve the Main Street Unionville area?", "Yes. For older homes with narrow driveways or street parking, tell us when you book so we plan where to park the truck."),
              ("What happens to things that still work?", "We set aside usable items for donation where we can. Metal and electronics go to recycling, and only what is left goes to a licensed site.")]),
    "North York": dict(
        slug="north-york", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Condo clear-outs, move-outs and furniture pickup across North York. Your price online in 2 minutes, a small $25 travel charge and no tax added.",
        hoods=["Willowdale", "Don Mills", "York Mills", "Bayview Village", "Newtonbrook", "Bathurst Manor", "Downsview", "Flemingdon Park",
               "Parkwoods", "Victoria Village", "Hillcrest Village", "Bayview Woods-Steeles"],
        hood_intro="From the Yonge and Sheppard condos to the houses in Don Mills and Willowdale, we work across North York most days.",
        curb_title="City pickup or us?", curb=TORONTO_CURB,
        jobs=[("Condo move-outs", "Units cleared and swept so you can hand back the keys. Tell us about the freight elevator and loading dock when you book."),
              ("Furniture pickup", "Couches, beds, dressers and tables carried out from any floor."),
              ("Downsizing", "Calm, careful clearing when moving from a house to a condo. We work from your list of what stays.")],
        faqs=[("How much is the travel charge for North York?", "North York is in our inner ring, so there is a $25 travel charge. It is already included in the online price for your address."),
              ("Do you work in condo buildings?", "Yes. Most buildings need a booked freight elevator, and some ask for paperwork from contractors. Send us the building rules when you book so we can confirm everything before the day."),
              ("How soon can you come?", "We book North York jobs most days. Choose your preferred date in the estimate form and we confirm a time window with your price.")]),
    "East York": dict(
        slug="east-york", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Basement cleanouts, condo and apartment clear-outs and furniture pickup across East York. Your price online in 2 minutes, a small $25 travel charge and no tax added.",
        hoods=["Leaside", "Thorncliffe Park", "Crescent Town", "Woodbine Heights", "O'Connor-Parkview", "Danforth Village", "Taylor-Massey",
               "Broadview North", "Pape Village"],
        hood_intro="From the high-rises at Thorncliffe Park and Crescent Town to the houses in Leaside and Danforth Village, we work across East York most days.",
        curb_title="City pickup or us?", curb=TORONTO_CURB,
        jobs=[("Basement cleanouts", "Old couches, boxes, exercise machines and the things nobody has touched in years, carried up and out."),
              ("Apartment and condo clear-outs", "We work with your building's freight elevator booking and loading area. Send us the building rules when you book."),
              ("Furniture pickup", "Couches, beds, dressers and tables carried out from any floor. Tell us about street parking when you book.")],
        faqs=[("How much is the travel charge for East York?", "East York is in our inner ring, so there is a $25 travel charge. It is already included in the online price for your address."),
              ("Can you take things from an East York apartment or condo?", "Yes. Most buildings need a booked freight elevator. Tell us the building name and any rules when you book, and we plan the time around the elevator booking."),
              ("Do you speak Tamil?", "Yes. We speak English and Tamil, so you can call or text us in either language.")]),
    "Pickering": dict(
        slug="pickering", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Garages, basements, renovation leftovers and move-outs across Pickering. Your price online in 2 minutes, a small $25 travel charge and no tax added.",
        hoods=["Bay Ridges", "Amberlea", "Liverpool", "Rosebank", "Dunbarton", "Duffin Heights", "Seaton", "Brock Ridge", "Village East",
               "Highbush", "Rougemount", "Claremont"],
        hood_intro="We are right next door in Scarborough, so Pickering is a short drive for us, from the lake up to Seaton and Claremont.",
        curb_title="Region pickup or us?", curb=DURHAM_CURB,
        jobs=[("New-build move-in clear-ups", "Boxes, packaging and leftover building materials from new homes in Seaton and Duffin Heights."),
              ("Basement and garage cleanouts", "One visit, carried out, loaded and swept."),
              ("Renovation leftovers", "Old cabinets, flooring, drywall pieces and fixtures from light renovation work.")],
        faqs=[("How much is the travel charge for Pickering?", "Pickering is in our inner ring, so there is a $25 travel charge, already included in the online price for your address."),
              ("Can you take renovation debris?", "Yes, light renovation debris like cabinets, flooring, trim and drywall pieces. We cannot take asbestos, paint, chemicals or other hazardous waste."),
              ("Durham only takes two items. Can you take the rest?", "Yes. There is no item limit with us, and we carry everything out for you.")]),
    "Richmond Hill": dict(
        slug="richmond-hill", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Estate cleanouts, downsizing and furniture pickup across Richmond Hill. Your price online in 2 minutes, a small $25 travel charge and no tax added.",
        hoods=["Oak Ridges", "Richvale", "Bayview Hill", "Mill Pond", "Jefferson", "Westbrook", "Rouge Woods", "Langstaff", "Crosby",
               "Devonsleigh", "Observatory", "Doncrest"],
        hood_intro="We cover Richmond Hill from Langstaff up to Oak Ridges, including the condo towers along Yonge and Highway 7.",
        curb_title="City pickup or us?",
        curb=('<p>Richmond Hill offers free bulky item pickup, including mattresses, for apartments and condominiums by online appointment, usually on Mondays about twice a month. '
              'Houses have their own curbside rules.</p>'
              '<p><b>Call us when</b> you cannot wait for the next pickup date, the items need carrying down from your unit, or there is a lot to clear.</p>'
              '<p class="note">Check the <a href="https://forms.richmondhill.ca/Community-Services/Bulky-Waste-Collection-Form" rel="noopener">City of Richmond Hill bulky waste page</a> or call Access Richmond Hill for current rules.</p>'),
        jobs=[("Estate and downsizing cleanouts", "Careful, respectful clearing of a family home. We sort for donation as we go and work from your list."),
              ("Furniture pickup", "Large sofas, sectionals, dining sets and beds carried out and hauled away."),
              ("Condo unit clear-outs", "Planned around your building's freight elevator booking.")],
        faqs=[("How much is the travel charge for Richmond Hill?", "Richmond Hill is in our inner ring, so there is a $25 travel charge, already included in the online price for your address."),
              ("Do you help with estate cleanouts?", "Yes. We go at the family's pace, set aside anything you want kept or donated, and leave the home swept. Heavy clutter needs a quick look first."),
              ("Can I be away while you work?", "For vacant homes, yes. We can work with a lockbox or building access arranged in writing, and send photos when we finish.")]),
    "Ajax": dict(
        slug="ajax", headline='Junk gone. <span class="lime">Space back.</span>',
        lead="Garage, basement and full home cleanouts in Ajax, booked on our east-end route days. Your price online in 2 minutes, a $60 travel charge and no tax added.",
        hoods=["Pickering Village", "South Ajax", "Central Ajax", "North Ajax", "West Ajax", "East Ajax", "Lakefront", "Harwood"],
        hood_intro="We come out to Ajax on our east-end route days, which keeps the travel charge low. Bigger jobs make the trip most worth it.",
        curb_title="Region pickup or us?", curb=DURHAM_CURB,
        jobs=[("Full garage cleanouts", "Car back in the garage in one visit. Bigger jobs make the most sense for the trip out."),
              ("Basement and storage clear-outs", "Old furniture, boxes and storage bins carried up and out."),
              ("Move-outs", "Everything left behind cleared and swept before the new owners or tenants arrive.")],
        faqs=[("Why is the travel charge higher for Ajax?", "Ajax is in our middle ring, so there is a $60 travel charge. We book Ajax on our east-end route days so we can keep it at that."),
              ("When do you come to Ajax?", "On our route days for the east end. Choose \"Flexible\" timing in the estimate form and we offer you the next route day."),
              ("Durham only takes two items. Can you take the rest?", "Yes. There is no item limit with us, and we carry everything out for you.")]),
}

ITEMS = {
    "couch-furniture-removal.html": dict(
        title="Couch and Furniture Removal GTA | 6ix Cleanout Co.",
        desc="Couch and furniture removal in Scarborough, Markham and the GTA. From $129, no tax added, carried out from any floor. Call (647) 517-2721.",
        kick="Couch and furniture removal", headline='Old couch? <span class="lime">Gone today.</span>',
        lead="Couches, sectionals, mattresses, dressers and tables carried out from any room or floor and hauled away. Usable pieces go to donation where we can.",
        quote="pickup", item="couch", name="Couch and furniture removal",
        prices=[("One couch or sofa on its own", f"${MIN}", "Our minimum charge, carried out and hauled away"),
                ("Couch plus a few more pieces", f"from ${LOAD_PRICES[1]}", "A quarter truck: couch, chair, side tables and a few boxes"),
                ("A room of furniture", f"from ${LOAD_PRICES[2]}", "A half truck: a living room or bedroom set")],
        what="<p><b>Donate first.</b> Clean, sturdy furniture is set aside for donation where we can find it a home. Broken or stained pieces go to a licensed site, and metal frames go to scrap recycling.</p>"
             "<p><b>New couch coming?</b> Book us for the same day as your delivery and the old one is gone before the new one arrives.</p>",
        ready=["Clear a path from the room to the door", "Take cushions and personal items out of drawers", "Tell us about stairs, narrow doors or a condo elevator", "Texting a photo gets you a firm price fastest"],
        faqs=[("Do I need to move the couch outside first?", "No. We carry it out from wherever it is, including basements and upper floors. Stairs add a small charge that shows in your estimate."),
              ("Can you take a sectional or sofa bed?", "Yes. Sectionals and sofa beds are heavier, so send a photo and we confirm the price before we come."),
              ("Will you donate my couch?", "If it is clean and in good shape, we try to. We cannot promise every piece will be accepted, and anything that is not goes to a licensed site.")]),
    "mattress-removal.html": dict(
        title="Mattress Removal Scarborough &amp; Markham | 6ix Cleanout Co.",
        desc="Mattress and box spring removal across the GTA. From $129 on its own, or $25 extra in a bigger load. No tax added. Call (647) 517-2721.",
        kick="Mattress removal", headline='New mattress? <span class="lime">We take the old one.</span>',
        lead="Mattresses and box springs carried out from any room and taken to recycling where it is available. Add one to any bigger job for just $25.",
        quote="pickup", item="mattress", name="Mattress removal",
        prices=[("A mattress or box spring on its own", f"${MIN}", "Our minimum charge, a mattress and box spring together usually fit in it"),
                ("Added to a bigger load", f"+${ITEM_PRICE['mattress'][1]}", "Per mattress or box spring, on top of the load price"),
                ("Bedroom set with mattress", f"from ${LOAD_PRICES[1]}", "A quarter truck: bed frame, mattress, dresser")],
        what="<p><b>Recycled where possible.</b> Mattresses are mostly steel, foam and fabric that can be recovered. We take them to mattress recycling where it is available and to a licensed site where it is not, which is why they carry a small separate fee.</p>"
             "<p><b>Bed bugs?</b> Tell us before we come. We can still take it, but it needs to be fully wrapped in plastic first.</p>",
        ready=["Strip the sheets and covers", "Tell us if it is a king, queen or a box spring set", "Let us know about stairs or a condo elevator", "Mention any bed bugs before the day"],
        faqs=[("Why does a mattress cost extra?", f"Mattresses have their own recycling and disposal fees, so we add ${ITEM_PRICE['mattress'][1]} per mattress when it is part of a bigger load. On its own, a mattress is covered by our ${MIN} minimum."),
              ("Can I just put it at the curb?", "Many cities collect mattresses at the curb on garbage day for houses, so check your city's rules first. We are for when it needs to go now or needs carrying out of the house or a condo."),
              ("Can you take a bed frame too?", "Yes. Add the frame, headboard and box spring in the estimate form and we price it all together.")]),
    "appliance-removal.html": dict(
        title="Appliance Removal: Fridges, Washers | 6ix Cleanout Co.",
        desc="Fridge, freezer, washer, dryer and stove removal in Scarborough, Markham and the GTA. Carried out and recycled. Call (647) 517-2721.",
        kick="Appliance removal", headline='Old appliance? <span class="lime">Out and recycled.</span>',
        lead="Fridges, freezers, washers, dryers, stoves and dishwashers carried out and taken for recycling. Fridges and freezers go where the refrigerant can be removed safely.",
        quote="pickup", item="fridge", name="Appliance removal",
        prices=[("One appliance on its own", f"${MIN}", "Our minimum charge covers one fridge, freezer, washer, dryer or stove"),
                ("Two appliances together", f"from ${ITEM_PRICE['fridge'][0] + ITEM_PRICE['washer'][0]}", "For example a fridge and a washer in one visit"),
                ("Added to a bigger load", f"+${ITEM_PRICE['fridge'][1]} / +${ITEM_PRICE['washer'][1]}", "Fridge or freezer / washer or dryer, on top of the load price")],
        what="<p><b>Fridges, freezers and air conditioners</b> hold refrigerant that has to be removed by a certified technician before the metal can be recycled. We take them to recyclers that handle this, which is why they carry a separate fee.</p>"
             "<p><b>Washers, dryers and stoves</b> are mostly steel and go to metal recycling.</p>",
        ready=["Empty the fridge or freezer and let it defrost", "Unplug it and disconnect water lines the day before", "Disconnect gas appliances with a licensed gas technician first", "Clear a path and tell us about stairs"],
        faqs=[("Do I need to disconnect the appliance?", "Please unplug it and turn off and disconnect any water line before we come. Gas appliances must be disconnected by a licensed gas technician first. We do not disconnect gas lines."),
              ("Why do fridges cost more?", "Fridges and freezers contain refrigerant that must be removed by a certified technician before recycling, so they cost more to dispose of properly."),
              ("Can you take an appliance from a basement?", "Yes. We carry it up, and stairs add a small charge that shows in your estimate.")]),
    "garage-basement-cleanout.html": dict(
        title="Garage and Basement Cleanouts GTA | 6ix Cleanout Co.",
        desc="Garage, basement and storage cleanouts across the GTA. From $230 by truck space, no tax added. We load, haul and sweep. Call (647) 517-2721.",
        kick="Garage and basement cleanouts", headline='Get the car <span class="lime">back in the garage.</span>',
        lead="Garages, basements, sheds and storage units cleared in one visit. We do all the carrying, sort for donation and recycling, and sweep before we leave.",
        quote="garage", item=None, name="Garage and basement cleanout",
        prices=[("Corner of a garage or basement", f"from ${LOAD_PRICES[1]}", "A quarter truck: a pile of boxes, bikes and old furniture"),
                ("Half a garage or basement", f"from ${LOAD_PRICES[2]}", "A half truck: one side of the garage or a full basement corner"),
                ("A full garage", f"from ${LOAD_PRICES[4]}", "A full truck: everything out so the car fits again")],
        what="<p><b>Sorted, not just dumped.</b> Tools, bikes and furniture in good shape go to donation where we can. Metal goes to scrap, electronics to e-waste recycling, and only the rest goes to a licensed site.</p>"
             "<p><b>What we cannot take:</b> paint, propane tanks, gasoline, oil, pool chemicals, asbestos and other hazardous waste. Your city or region runs free household hazardous waste drop-offs for these.</p>",
        ready=["Set aside anything you want to keep", "Move cars out of the driveway if you can", "Tell us about stairs into the basement", "Photos of each wall get you a firm price fastest"],
        faqs=[("How long does a garage cleanout take?", "Most garages take 2 to 4 hours with a two-person crew. Your estimate shows the expected time on site."),
              ("Do I have to sort things first?", "No. Just tell us what stays. We sort the rest for donation, recycling and disposal as we load."),
              ("Can you take old paint and chemicals?", "No. Paint, propane, gasoline, oil and chemicals are hazardous waste. Your city or region has free drop-off depots for them.")]),
}


def esc(s):
    return html.escape(s, quote=True)


def money(n):
    return f"${n:,}"


def shell(title, desc, canonical, jsonld):
    head = SHELL[:SHELL.index("<main>")]
    tail = SHELL[SHELL.index("</main>"):]
    head = re.sub(r"<title>[^<]*</title>", lambda m: f"<title>{title}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{esc(desc)}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', lambda m: f'<link rel="canonical" href="{SITE}{canonical}">', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
    head = head.replace("</head>", "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",", ":"))}</script>' for j in jsonld) + "</head>")
    head = head.replace(' aria-current="page"', "")
    head = social_tags(head)
    return head, tail


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def business_ld(area):
    return biz_ld(area, MIN)


def details(faqs):
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)


def guide(eyebrow, title, links):
    return (f'<section class="sec"><div class="head"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div><div class="guide">'
            + "".join(f'<a href="{f}">{t}</a>' for f, t in links) + "</div></section>")


def city_page(city, d):
    z, fee = ZONES[city] if city in ZONES else ZONES["Markham"] if city == "Unionville" else (None, None)
    fee_txt = "No travel charge" if fee == 0 else f"+{money(fee)} travel"
    rows = "".join(f"<tr><td><b>{t}</b></td><td class=\"p\">{money(LOAD_PRICES[i] + fee)}</td><td>{l}</td></tr>" for i, (t, l) in enumerate(ROWS))
    title = f"Junk Removal {city} | From {money(LOAD_PRICES[0] + fee)} | 6ix Cleanout Co."
    desc = (f"Junk removal in {city}: furniture, appliances, garages and cleanouts. Price in 2 minutes, "
            f"{'no travel fee' if not fee else f'{money(fee)} travel'}, no tax added. Call (647) 517-2721.")
    fname = f"junk-removal-{d['slug']}.html"
    head, tail = shell(title, desc, fname, [business_ld([city]), faq_ld(d["faqs"])])
    others = [(f, "Junk removal in " + c) for f, c in CITY_PAGES if c != city]
    main = (
        f'<main><div class="hband"><section class="phero">{LAUNCH_DARK}<p class="eyebrow">{city} · Zone {z} · {fee_txt}</p>'
        f'<h1><span class="kick">Junk removal in {city}</span>{d["headline"]}</h1><p class="lead">{d["lead"]}</p>'
        f'<div class="cta"><a class="btn hv" href="index.html#quote-in-{d["slug"]}">Get my {city} price</a>{CALL_BTN}{SMS_BTN}</div></section></div>'
        f"{TRUST_HTML}"
        f'<section class="sec" style="padding-top:20px"><div class="head"><p class="eyebrow">Typical prices in {city}</p>'
        f'<h2>Priced by truck space, {"no travel charge" if not fee else "travel included"}.</h2>'
        f'<p>Starting prices for a {city} address{"" if not fee else f", including the {money(fee)} travel charge"}. Stairs, long carries and special items like mattresses and fridges are added in your online estimate. Booking: {BOOK[z].lower()}.</p></div>'
        f'<div class="tbl"><table><thead><tr><th>Job size</th><th>From</th><th>Looks like</th></tr></thead><tbody>{rows}</tbody></table></div>'
        f'<p class="note" style="margin-top:12px">No tax added. The price we confirm before we start is the price you pay.</p>{SAVE_HTML}</section>'
        f'<section class="sec"><div class="two"><div class="card"><h3>Neighbourhoods we cover</h3><p style="color:var(--muted);margin-top:8px">{d["hood_intro"]}</p>'
        f'<div class="hoods" style="margin-top:12px">{"".join(f"<span>{esc(h)}</span>" for h in d["hoods"])}</div></div>'
        f'<div class="card"><h3>{d["curb_title"]}</h3><div class="prose" style="margin-top:10px">{d["curb"]}</div></div></div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">{city} jobs we do most</p><h2>What we clear in {city}.</h2></div><div class="cards3">'
        + "".join(f'<div class="svc"><h3>{t}</h3><p style="color:var(--muted)">{p}</p></div>' for t, p in d["jobs"])
        + '</div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">Questions</p><h2>Junk removal in {city}: common questions.</h2></div>{details(d["faqs"])}</section>'
        + guide("Nearby", "Other areas we cover.", others + [("areas.html", "All service areas")])
        + guide("Popular jobs", "Guides for the jobs we do most.", ITEM_PAGES)
        + "</main>")
    return fname, head + main + tail


def item_page(fname, d):
    head, tail = shell(d["title"], d["desc"], fname, [
        {"@context": "https://schema.org", "@type": "Service", "name": d["name"], "serviceType": "Junk removal",
         "provider": business_ld(["Scarborough", "Markham", "Toronto", "Greater Toronto Area"]), "areaServed": "Greater Toronto Area",
         "offers": {"@type": "Offer", "priceCurrency": "CAD", "price": str(MIN)}},
        faq_ld(d["faqs"])])
    rows = "".join(f'<tr><td><b>{esc(a)}</b></td><td class="p">{b}</td><td>{esc(c)}</td></tr>' for a, b, c in d["prices"])
    others = [(f, t) for f, t in ITEM_PAGES if f != fname]
    main = (
        f'<main><div class="hband"><section class="phero">{LAUNCH_DARK}<p class="eyebrow">Scarborough · Markham · GTA</p>'
        f'<h1><span class="kick">{d["kick"]} in Scarborough, Markham &amp; the GTA</span>{d["headline"]}</h1><p class="lead">{d["lead"]}</p>'
        f'<div class="cta"><a class="btn hv" href="index.html#quote-{d["quote"]}">Get my price</a>{CALL_BTN}{SMS_BTN}</div></section></div>'
        f"{TRUST_HTML}"
        f'<section class="sec" style="padding-top:20px"><div class="head"><p class="eyebrow">Prices</p><h2>Clear prices, no tax added.</h2>'
        f'<p>Home-zone prices for Scarborough, Markham and Unionville. Other areas add a small travel charge that shows in your online estimate.</p></div>'
        f'<div class="tbl"><table><thead><tr><th>Job</th><th>Price</th><th>What it covers</th></tr></thead><tbody>{rows}</tbody></table></div>{SAVE_HTML}</section>'
        f'<section class="sec"><div class="two"><div class="card"><h3>What happens to it</h3><div class="prose" style="margin-top:10px">{d["what"]}</div></div>'
        f'<div class="card"><h3>How to get ready</h3><ul>{"".join(f"<li>{esc(r)}</li>" for r in d["ready"])}</ul></div></div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">Questions</p><h2>Before you book.</h2></div>{details(d["faqs"])}</section>'
        + guide("More jobs", "Other things we take.", others)
        + guide("Areas", "Where we work.", CITY_PAGES and [(f, "Junk removal in " + c) for f, c in CITY_PAGES])
        + "</main>")
    return fname, head + main + tail


LEGAL = {
    "privacy.html": dict(
        title="Privacy Policy | 6ix Cleanout Co.",
        desc="How 6ix Cleanout Co. collects, uses and protects the details you share for a junk removal quote or job.",
        h1="Privacy policy", lead="Plain language, last updated November 2026. We only collect what we need to quote and do your job, and we never sell your information.",
        sections=[
            ("Who we are", ["6ix Cleanout Co. is a junk removal business based in Scarborough and Markham, Ontario, run by its two owners. Contact: 6ixcleanoutco@gmail.com or (647) 517-2721."]),
            ("What we collect", ["When you ask for an estimate or book a job: your name, phone number, email, the job address and city, details about the items and access, your preferred date and time, any photos you send, and how you heard about us.",
                                 "When you visit the website: if we turn on website analytics (Microsoft Clarity) or ad measurement (Meta Pixel), these tools record how the site is used, such as pages visited and clicks, and the website you came from. They do not give us your name."]),
            ("Why we use it", ["To prepare your price, book and do the job, send your confirmation, reminder and receipt, follow up on your quote, and ask for a review.",
                               "To understand which advertising and pages bring customers, so we can improve the website.",
                               "Occasionally, to send past customers a seasonal note. Every one of those messages has a way to stop receiving them."]),
            ("Who we share it with", ["We do not sell or rent your information. We use a few services to run the business: Google (Gmail, Forms, Sheets and Calendar store our requests and bookings), FormSubmit (delivers the photos you upload to our email), and, if turned on, Microsoft Clarity and Meta for website analytics and ad measurement. These services may store data outside Canada.",
                                      "We may share information if the law requires it."]),
            ("Photos", ["Photos you send are used only to price and plan your job. We only post before and after photos of a job with your permission, and never with faces, house numbers, licence plates or personal documents visible."]),
            ("How long we keep it", ["We keep job records for as long as tax and business rules require, generally up to 7 years, and delete photos and requests that did not become a job when they are no longer needed."]),
            ("Your choices", ["You can ask what information we hold about you, ask us to correct it, or ask us to stop sending follow-ups or seasonal messages at any time. Email 6ixcleanoutco@gmail.com and we will reply within 30 days.",
                              "You can block analytics cookies in your browser settings."]),
        ]),
    "terms.html": dict(
        title="Service Terms | 6ix Cleanout Co.",
        desc="Prices, bookings, deposits, cancellations and what we can take: the simple terms for every 6ix Cleanout Co. junk removal job.",
        h1="Service terms", lead="The short version: a clear price before we start, payment at the end, and no surprises. Last updated November 2026.",
        sections=[
            ("Prices and estimates", ["The online estimate is a range based on what you tell us. We confirm a final price in writing, by text or email, before any work starts.",
                                      "If there is more to take than we agreed, we tell you the new price and only take the extra items once you agree.",
                                      "Heavy materials such as concrete, brick, dirt, shingles and plaster are priced by weight and confirmed from photos first. No tax is added while we are not registered for HST."]),
            ("Booking, deposits and changes", ["Your booking is confirmed when you reply YES to the confirmation, or sign the job agreement for larger jobs.",
                                               "Jobs over $500 need a deposit of 20% of the price by e-Transfer to book (for example $136 on a $680 job), taken off your final bill. You can change or cancel free up to 24 hours before your arrival window. For a later cancellation the deposit is kept."]),
            ("On the day", ["Please make sure we can reach the items: a clear path, nearby parking, and any condo elevator booking. If access is very different from what was described, we will agree any change in price with you first.",
                            "Please remove valuables, documents, cash and keepsakes before we arrive. If we find anything personal or valuable, we hand it back to you before we leave."]),
            ("Payment", ["Payment is due at the end of the job, after you have seen the cleared space: cash or Interac e-Transfer. Card may be available on request. Business clients can ask for an invoice."]),
            ("What happens to your items", ["Once loaded, items become the property of 6ix Cleanout Co. We reuse, donate or recycle what we can and take the rest to licensed disposal sites."]),
            ("What we cannot take", ["Hazardous waste, including paint, propane tanks, gasoline, oil, chemicals, asbestos, needles and biohazards. Your city has free household hazardous waste drop-offs for these."]),
            ("If something goes wrong", ["Tell us within 48 hours and we will make it right: we come back to fix any mess we left, and we will work with you fairly on any damage we caused."]),
        ]),
}


def legal_page(fname, d):
    head, tail = shell(d["title"], d["desc"], fname, [])
    body = "".join(f'<section class="sec" style="padding-top:36px"><div class="head"><h2>{esc(h)}</h2></div><div class="prose">'
                   + "".join(f"<p>{esc(p)}</p>" for p in ps) + "</div></section>" for h, ps in d["sections"])
    main = (f'<main><div class="hband"><section class="phero"><p class="eyebrow">6ix Cleanout Co.</p><h1>{d["h1"]}</h1><p class="lead">{d["lead"]}</p>'
            f'<div class="cta"><a class="btn hv" href="index.html#quote">Get my estimate</a>{CALL_BTN}</div></section></div>{body}</main>')
    return fname, head + main + tail


# ---------- Booking page (behind the "Book this price" button in quote emails) ----------
# Link format: book.html?job=JOB-ABC123&name=Sam&price=390  (add &change=1 for a reschedule request).
# It reuses the website's Google Form, so a booking lands in the Requests tab with Service "Booking request".
GFORM = re.search(r'googleForm: (\{.*?\n  \}),', INDEX, re.S).group(1)
GFORM_JSON = json.loads(GFORM)


def booking_page():
    fname = "book.html"
    head, tail = shell("Book your job | 6ix Cleanout Co.", "Pick a day and arrival window for your 6ix Cleanout Co. job.", fname, [])
    head = head.replace("</head>", '<meta name="robots" content="noindex"></head>', 1)
    main = f'''<main><div class="hband"><section class="phero"><p class="eyebrow">Book your job</p>
<h1 id="bk-h">Pick a day that works for you.</h1><p class="lead" id="bk-lead">Choose a day and an arrival window. We confirm by text within the hour between 8am and 8pm.</p></section></div>
<section class="sec" style="padding-top:28px"><div class="panel" style="max-width:640px" id="bk">
<div class="ticket" style="border-radius:12px;margin-bottom:18px"><div class="hd"><b id="bk-job">Your job</b><br><span id="bk-price" class="mono"></span></div></div>
<label class="f" for="bk-name"><span>Your name</span></label><input type="text" id="bk-name" autocomplete="name">
<label class="f" for="bk-phone"><span>Phone<em>so we can text the confirmation</em></span></label><input type="tel" id="bk-phone" autocomplete="tel">
<label class="f" for="bk-date"><span>Day</span></label><input type="date" id="bk-date">
<label class="f" for="bk-win"><span>Arrival window</span></label><select id="bk-win"><option>Morning, 8 to 11am</option><option>Midday, 11am to 2pm</option><option>Afternoon, 2 to 5pm</option><option>Evening, 5 to 8pm</option></select>
<label class="f" for="bk-notes"><span>Anything we should know?<em>optional</em></span></label><textarea id="bk-notes" placeholder="Parking, elevator booking, buzzer code..."></textarea>
<p class="note">Payment is at the end of the job, after you have seen the cleared space: cash or Interac e-Transfer. Jobs over $500 need a 20% deposit to hold the day. Free changes up to 24 hours before. <a href="terms.html">Service terms</a>.</p>
<div class="nav"><span></span><button type="button" class="btn hv" id="bk-send">Request this day</button></div><div id="bk-msg"></div></div></section></main>
<script>
(function(){{
  const GF={json.dumps(GFORM_JSON)};
  const q=new URLSearchParams(location.search), job=(q.get("job")||"").slice(0,20), change=q.get("change")==="1";
  const $=id=>document.getElementById(id);
  const price=+q.get("price")||0;
  if(q.get("name")) $("bk-name").value=q.get("name").slice(0,60);
  $("bk-job").textContent=job?("Job "+job):"Your job";
  $("bk-price").textContent=price?("Confirmed price $"+price.toLocaleString("en-CA")+", no tax added"):"";
  if(change){{ $("bk-h").textContent="Change your day or time."; $("bk-send").textContent="Request the change"; }}
  const d=new Date(); d.setDate(d.getDate()+1); $("bk-date").min=d.toISOString().slice(0,10);
  $("bk-send").addEventListener("click",async()=>{{
    const name=$("bk-name").value.trim(), phone=$("bk-phone").value.trim(), date=$("bk-date").value, win=$("bk-win").value, notes=$("bk-notes").value.trim();
    if(!name||!date){{ $("bk-msg").innerHTML='<div class="alert bad">Please add your name and pick a day.</div>'; return; }}
    const vals={{"Reference":job||("BOOK-"+Date.now().toString(36).toUpperCase().slice(-6)),"Name":name,"Phone":phone,"Service":change?"Change request":"Booking request",
      "Preferred date":date,"Best time of day":win,"Notes":(change?"CHANGE REQUEST":"BOOKING REQUEST")+": "+date+", "+win+(price?", quoted $"+price:"")+(notes?" | "+notes:"")}};
    const body=new URLSearchParams(); Object.keys(GF.entries).forEach(k=>body.append("entry."+GF.entries[k], vals[k]==null?"":vals[k]));
    $("bk-send").disabled=true; $("bk-send").textContent="Sending...";
    try{{ await fetch(GF.action,{{method:"POST",mode:"no-cors",headers:{{"Content-Type":"application/x-www-form-urlencoded"}},body}});
      if(window.track6) track6("Schedule",{{content_name:job}});
      $("bk").innerHTML='<h2>Thanks, '+name.split(" ")[0].replace(/[<>&"]/g,"")+'! Your request is in.</h2><p class="lead" style="margin-top:10px">We will text you to confirm '+date+', '+win.toLowerCase()+', usually within the hour between 8am and 8pm. Need us sooner? Call or text <a data-call href="tel:+16475172721">(647) 517-2721</a>.</p>';
    }}catch(e){{ $("bk-send").disabled=false; $("bk-send").textContent="Try again"; $("bk-msg").innerHTML='<div class="alert bad">That did not send. Please call or text (647) 517-2721.</div>'; }}
  }});
}})();
</script>'''
    return fname, head + main + tail


# ---------- Tamil page (தமிழ்) ----------
# Written in neutral Tamil that Sri Lankan and Indian Tamil readers both understand, with the English
# words people actually use in Toronto kept in brackets. The owners check every line before it goes live.
KOLAM = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 60 60'%3E"
         "%3Cg fill='none' stroke='%23B8F334' stroke-width='1.6'%3E%3Ccircle cx='30' cy='30' r='21'/%3E%3Ccircle cx='0' cy='0' r='21'/%3E"
         "%3Ccircle cx='60' cy='0' r='21'/%3E%3Ccircle cx='0' cy='60' r='21'/%3E%3Ccircle cx='60' cy='60' r='21'/%3E%3C/g%3E"
         "%3Cg fill='%23B8F334'%3E%3Ccircle cx='30' cy='0' r='2.4'/%3E%3Ccircle cx='0' cy='30' r='2.4'/%3E%3Ccircle cx='60' cy='30' r='2.4'/%3E"
         "%3Ccircle cx='30' cy='60' r='2.4'/%3E%3Ccircle cx='30' cy='30' r='2.4'/%3E%3C/g%3E%3C/svg%3E")
KOLAM_DARK = KOLAM.replace("%23B8F334", "%230A0F0D")
TA_SMS = ("sms:+16475172721?&amp;body=" + __import__("urllib.parse").parse.quote(
    "வணக்கம் 6ix Cleanout, அகற்ற வேண்டிய பொருட்களின் புகைப்படங்கள் இதோ. என் பகுதி: "))
TA_CSS = f"""<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Catamaran:wght@600;800;900&family=Noto+Sans+Tamil:wght@400;500;700&display=swap" rel="stylesheet">
<style>
html[lang="ta"] body{{font-family:"Noto Sans Tamil","Figtree",system-ui,sans-serif;line-height:1.7}}
html[lang="ta"] h1,html[lang="ta"] h2,html[lang="ta"] h3{{font-family:"Catamaran","Noto Sans Tamil",sans-serif;line-height:1.3;letter-spacing:0}}
.ta-hero h1{{font-size:clamp(2.1rem,5.2vw,3.9rem);font-weight:900;max-width:none}}
.ta-hero .kick{{font-family:"Catamaran",sans-serif;font-size:clamp(1rem,1.8vw,1.25rem)}}
.kolam{{position:absolute;inset:0;background-image:url("{KOLAM}");background-size:60px 60px;opacity:.13;z-index:-1;
 -webkit-mask-image:linear-gradient(110deg,transparent 35%,#000 75%);mask-image:linear-gradient(110deg,transparent 35%,#000 75%)}}
.proverb{{display:block;width:fit-content;max-width:100%;border:1px solid rgba(184,243,52,.35);border-radius:12px;padding:10px 14px;margin-top:18px;color:#cfd8cf;font-size:.95rem}}
html[lang="ta"] .eyebrow{{font-family:"Noto Sans Tamil",sans-serif;letter-spacing:0;text-transform:none;font-weight:700;font-size:.88rem}}
html[lang="ta"] .sec .head{{max-width:78ch}}
html[lang="ta"] .mbar.sub .btn{{font-size:.86rem;padding-inline:8px}}
.proverb s{{color:#8c968e}}
.proverb b{{color:var(--lime)}}
.kolam-rule{{height:34px;margin:56px auto 0;max-width:1180px;background-image:url("{KOLAM_DARK}");background-size:34px 34px;opacity:.16;border-radius:8px}}
.owners{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;max-width:760px}}
@media (max-width:620px){{.owners{{grid-template-columns:1fr}}}}
.owner{{display:flex;gap:14px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px}}
.owner .av{{flex:none;width:64px;height:64px;border-radius:50%;background:var(--night);color:var(--lime);display:grid;place-items:center;font:900 1.6rem "Catamaran",sans-serif;box-shadow:0 0 0 3px var(--lime)}}
.owner b{{display:block;font-size:1.1rem}}
.owner span{{color:var(--muted);font-size:.92rem}}
.parents{{background:var(--night);color:#eef3ec;border-radius:20px;padding:clamp(22px,4vw,40px);position:relative;overflow:hidden;isolation:isolate}}
.parents h2{{color:#fff}}
.parents p{{color:#c9d2ca;max-width:62ch;margin-top:12px}}
.parents .kolam{{-webkit-mask-image:linear-gradient(250deg,#000 10%,transparent 60%);mask-image:linear-gradient(250deg,#000 10%,transparent 60%);opacity:.12}}
.bhogi{{border:2px dashed var(--line);border-radius:20px;padding:clamp(20px,3.5vw,34px);background:var(--surface)}}
.bhogi .tag{{display:inline-block;background:var(--lime);color:var(--night);font-weight:800;border-radius:99px;padding:4px 12px;font-size:.85rem;margin-bottom:10px}}
.ta-steps{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
@media (max-width:760px){{.ta-steps{{grid-template-columns:1fr}}}}
.ta-steps div{{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px}}
.ta-steps .n{{width:40px;height:40px;border-radius:50%;background:var(--lime);color:var(--night);display:grid;place-items:center;font:900 1.1rem "Catamaran",sans-serif;margin-bottom:10px}}
.ta-steps p{{color:var(--muted)}}
.finalcta{{text-align:center;background:var(--night);color:#fff;border-radius:20px;padding:clamp(26px,5vw,48px);margin-top:64px}}
.finalcta .big{{display:block;font:900 clamp(1.8rem,5vw,3rem) "Catamaran",sans-serif;color:var(--lime);margin:8px 0 18px;text-decoration:none}}
.finalcta .cta{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
</style>"""

TA_FAQ = [
    ("விலை எவ்வளவு ஆகும்?", "லாரியில் உங்கள் பொருட்கள் எடுக்கும் இடத்தைப் பொறுத்து விலை. சில பொருட்கள் மட்டும் என்றால் $129 முதல். இணையத்தில் 2 நிமிடத்தில் விலை வரம்பு தெரியும்; புகைப்படங்களைப் பார்த்து உறுதியான விலையைச் சொல்வோம்."),
    ("வரி (HST) சேர்ப்பீர்களா?", "இல்லை. நாங்கள் உறுதிசெய்யும் விலைதான் நீங்கள் செலுத்தும் விலை. மறைமுகக் கட்டணங்கள் இல்லை."),
    ("பணம் எப்போது, எப்படிச் செலுத்துவது?", "வேலை முடிந்து, சுத்தமான இடத்தை நீங்கள் பார்த்த பிறகுதான். காசு (cash) அல்லது Interac e-Transfer."),
    ("எதை எடுக்க மாட்டீர்கள்?", "பெயிண்ட், புரொப்பேன் சிலிண்டர், பெட்ரோல், எண்ணெய், இரசாயனங்கள், ஆஸ்பெஸ்டாஸ். இவற்றுக்கு நகரசபையின் இலவச மையங்கள் உள்ளன; எங்கு கொண்டு செல்லலாம் என்று சொல்லித் தருவோம்."),
    ("தமிழில் பேசலாமா?", "நிச்சயமாக. தொலைபேசியில் அழையுங்கள் அல்லது தமிழில் மெசேஜ் அனுப்புங்கள். வீட்டில் உள்ள பெரியவர்களுடனும் தமிழிலேயே பேசி எல்லாவற்றையும் விளக்குவோம்."),
    ("பொருட்களில் ஏதாவது முக்கியமானது இருந்தால்?", "வேலைக்கு முன் முக்கியமான பொருட்களை எடுத்துவிடுங்கள். அதன் பிறகும் பணம், நகை, ஆவணங்கள், குடும்பப் புகைப்படங்கள் எதாவது கிடைத்தால், அவற்றை உங்களிடமே ஒப்படைப்போம்."),
]


def tamil_page():
    fname = "tamil.html"
    title = "குப்பை அகற்றும் சேவை | Junk Removal in Tamil | 6ix Cleanout"
    desc = "ஸ்காபரோ, மார்க்கம், GTA முழுவதும் குப்பை அகற்றும் சேவை. 2 நிமிடத்தில் விலை, வரி இல்லை. தமிழில் பேசும் உள்ளூர் உரிமையாளர்கள். (647) 517-2721"
    ld = [business_ld(["Scarborough", "Markham", "Toronto", "Greater Toronto Area"]), faq_ld(TA_FAQ),
          {"@context": "https://schema.org", "@type": "WebPage", "name": title, "inLanguage": "ta", "url": SITE + fname}]
    head, tail = shell(title, desc, fname, ld)
    head = head.replace('<html lang="en">', '<html lang="ta">', 1)
    head = head.replace("</head>", f'<link rel="alternate" hreflang="ta" href="{SITE}{fname}"><link rel="alternate" hreflang="en" href="{SITE}">{TA_CSS}</head>', 1)
    head = head.replace('<a class="btn alt sm langpill" href="tamil.html" lang="ta" hreflang="ta" title="தமிழில் பார்க்க">தமிழ்</a>',
                        '<a class="btn alt sm langpill" href="index.html" lang="en" hreflang="en" title="View in English">English</a>')
    tail = re.sub(r'<div class="mbar sub">.*?</div>', lambda m: (
        f'<div class="mbar sub"><a class="btn alt" data-call href="tel:+16475172721">{ICO_PHONE}அழைக்க</a>'
        f'<a class="btn alt" href="{TA_SMS}">{ICO_MSG}மெசேஜ்</a><a class="btn hv" href="index.html#quote">விலை</a></div>'), tail, count=1, flags=re.S)
    l = LOAD_PRICES
    rows = [("சில பொருட்கள் மட்டும் (couch, மெத்தை, ஃப்ரிட்ஜ்)", f"${MIN}"), ("கால் லாரி: ஒரு சிறிய அறை", f"${l[1]}"),
            ("அரை லாரி: ஒரு படுக்கையறை அல்லது அடித்தளத்தின் ஒரு பகுதி", f"${l[2]}"), ("முக்கால் லாரி: ஒரு வரவேற்பறை முழுவதும்", f"${l[3]}"),
            ("முழு லாரி: ஒரு படுக்கையறை அபார்ட்மென்ட் அல்லது நிறைந்த கராஜ்", f"${l[4]}")]
    trs = "".join(f'<tr><td><b>{esc(a)}</b></td><td class="p">{b}</td></tr>' for a, b in rows)
    main = f'''<main>
<div class="hband ta-hero"><div class="kolam"></div><section class="phero">{LAUNCH_DARK.replace(LAUNCH_TEXT, "முதல் 25 · அறிமுக விலை").replace("spots left", "இடங்கள் மீதம்").replace("<b data-spots>25 of 25</b>", "<b data-spots data-of=\" / \">25 / 25</b>")}
<p class="eyebrow">ஸ்காபரோ · மார்க்கம் · GTA முழுவதும்</p>
<h1><span class="kick">தமிழில் பேசும் உள்ளூர் குப்பை அகற்றும் சேவை</span>குப்பை போனால், <span class="lime">இடம் பிறக்கும்.</span></h1>
<p class="lead">பழைய couch, மெத்தை, ஃப்ரிட்ஜ், கராஜ், அடித்தளம், முழு வீடு. எல்லாவற்றையும் நாங்களே தூக்கி, ஏற்றி, அகற்றி, இடத்தைச் சுத்தம் செய்துவிட்டுச் செல்கிறோம். வேலைக்கு முன்பே உறுதியான விலை.</p>
<div class="cta"><a class="btn hv" href="index.html#quote">2 நிமிடத்தில் விலை அறிய</a><a class="btn alt" data-call href="tel:+16475172721">{ICO_PHONE}தமிழில் அழையுங்கள்</a><a class="btn alt" href="{TA_SMS}">{ICO_MSG}புகைப்படம் அனுப்புங்கள்</a></div>
<p class="proverb"><s>தை பிறந்தால் வழி பிறக்கும்</s> என்பது போல, <b>குப்பை போனால் இடம் பிறக்கும்.</b></p>
</section></div>
<div class="trust" aria-label="ஒவ்வொரு வேலையிலும்"><span>வரி இல்லை</span><span>வேலைக்கு முன் உறுதியான விலை</span><span>தூக்கி, ஏற்றி, சுத்தம் செய்வோம்</span><span>முடிந்தவற்றைத் தானம், மறுசுழற்சி</span><span>வேலை முடிந்த பிறகே பணம்</span></div>

<section class="sec"><div class="head"><p class="eyebrow">ஏன் எங்களை நம்பலாம்?</p><h2>உங்கள் வீட்டை, எங்கள் வீடு போல மதிக்கிறோம்.</h2></div><div class="why">
<div><span class="num">1</span><h3>2 நிமிடத்தில் விலை</h3><p>பெரிய நிறுவனங்கள் வீட்டுக்கு வந்த பிறகுதான் விலை சொல்வார்கள். நாங்கள் முன்பே சொல்கிறோம், வேலைக்கு முன் உறுதிசெய்கிறோம்.</p></div>
<div><span class="num">2</span><h3>உரிமையாளர்களே வருவோம்</h3><p>ஒவ்வொரு வேலைக்கும் நாங்கள் இருவருமே வருகிறோம். தெரியாத ஆட்கள், அழைப்பு மையங்கள் இல்லை.</p></div>
<div><span class="num">3</span><h3>சுத்தமாக விட்டுச் செல்வோம்</h3><p>தரை, கதவு, சுவர்களைப் பாதுகாத்து வேலை செய்கிறோம். முடிந்ததும் கூட்டிச் சுத்தம் செய்கிறோம்.</p></div>
<div><span class="num">4</span><h3>முதலில் தானம், மறுசுழற்சி</h3><p>பயன்படக்கூடியவை மீண்டும் பயன்பாட்டுக்கு, உலோகமும் மின்சாதனங்களும் மறுசுழற்சிக்கு. மீதி மட்டுமே உரிமம் பெற்ற இடங்களுக்கு.</p></div>
</div></section>

<section class="sec"><div class="head"><p class="eyebrow">உங்களைச் சந்திக்க வருபவர்கள்</p><h2>நாங்கள் Seythu, Atheeshan.</h2><p>ஸ்காபரோ, மார்க்கத்திலிருந்து இயங்கும் இரண்டு இளம் தொழில்முனைவோர். உங்கள் அழைப்புக்கு நாங்களே பதில் சொல்வோம், நாங்களே வருவோம்.</p></div>
<div class="owners"><div class="owner"><span class="av">S</span><div><b>Seythu</b><span>இணை உரிமையாளர் · தமிழ், English</span></div></div><div class="owner"><span class="av">A</span><div><b>Atheeshan</b><span>இணை உரிமையாளர் · தமிழ், English</span></div></div></div></section>

<section class="sec"><div class="head">{LAUNCH_LIGHT.replace(LAUNCH_TEXT, "முதல் 25 · அறிமுக விலை").replace("spots left", "இடங்கள் மீதம்").replace("<b data-spots>25 of 25</b>", "<b data-spots data-of=\" / \">25 / 25</b>")}<p class="eyebrow">விலைகள்</p><h2>லாரியில் எடுக்கும் இடத்தைப் பொறுத்து விலை.</h2>
<p>ஸ்காபரோ, மார்க்கம், யூனியன்வில்லுக்கு பயணக் கட்டணம் இல்லை. மற்ற பகுதிகளுக்குச் சிறிய பயணக் கட்டணம் உண்டு; அது உங்கள் விலையிலேயே தெரியும்.</p></div>
<div class="tbl"><table><thead><tr><th>வேலையின் அளவு</th><th>விலை (முதல்)</th></tr></thead><tbody>{trs}</tbody></table></div>
<p class="note" style="margin-top:12px">மெத்தை +$25, ஃப்ரிட்ஜ் +$45, washer/dryer +$30 போன்ற சிறப்புப் பொருட்களுக்குச் சிறிய கூடுதல் கட்டணம். வரி இல்லை.</p></section>

<section class="sec"><div class="head"><p class="eyebrow">எப்படி வேலை செய்கிறோம்</p><h2>மூன்று எளிய படிகள்.</h2></div><div class="ta-steps">
<div><span class="n">1</span><h3>புகைப்படம் அனுப்புங்கள்</h3><p>அகற்ற வேண்டியவற்றின் 2, 3 புகைப்படங்களை மெசேஜ் செய்யுங்கள், அல்லது இணையத்தில் விலை கணக்கிடுங்கள்.</p></div>
<div><span class="n">2</span><h3>உறுதியான விலை</h3><p>விலையையும் வரும் நேரத்தையும் எழுத்தில் உறுதிசெய்கிறோம். ஆச்சரியங்கள் இல்லை.</p></div>
<div><span class="n">3</span><h3>நாங்கள் பார்த்துக்கொள்கிறோம்</h3><p>தூக்கி, ஏற்றி, அகற்றி, சுத்தம் செய்கிறோம். இடத்தைப் பார்த்த பிறகே பணம்.</p></div>
</div></section>

<div class="kolam-rule" aria-hidden="true"></div>

<section class="sec" style="padding-top:40px"><div class="parents"><div class="kolam"></div><p class="eyebrow" style="color:var(--lime)">பெற்றோர் வீடு</p>
<h2>அம்மா, அப்பாவின் வீட்டை ஒழுங்குபடுத்துவது எளிதல்ல. நாங்கள் பொறுமையாக உதவுகிறோம்.</h2>
<p>வீடு மாறும்போதும், பெரியவர்களின் வீட்டைச் சுருக்கும்போதும், ஒவ்வொரு பொருளுக்கும் ஒரு நினைவு இருக்கும். எதை வைத்துக்கொள்வது, எதைத் தானம் செய்வது என்று உங்கள் குடும்பம் முடிவு செய்யும்; நாங்கள் உங்கள் பட்டியலின்படி மட்டுமே வேலை செய்கிறோம். பெரியவர்களுடன் தமிழிலேயே பேசுவோம், அவசரப்படுத்த மாட்டோம். கிடைக்கும் புகைப்படங்கள், ஆவணங்கள், நகைகள் எல்லாம் உங்களிடமே ஒப்படைக்கப்படும்.</p>
<div class="cta" style="margin-top:20px"><a class="btn hv" data-call href="tel:+16475172721">{ICO_PHONE}அமைதியாகப் பேசலாம்: அழையுங்கள்</a></div></div></section>

<section class="sec"><div class="bhogi"><span class="tag">போகி · தைப்பொங்கல்</span><h2>போகிக்கு முன் பழையதை அகற்றுங்கள். புகை இல்லாமல்.</h2>
<p style="color:var(--muted);margin-top:10px;max-width:64ch">பழையதைக் கழித்துப் புதியதை வரவேற்கும் போகியின் அர்த்தம் அப்படியே. எரிக்காமல், பயன்படுவதைத் தானம் செய்து, மீதியை மறுசுழற்சி செய்து, சுத்தமான வீட்டில் பொங்கலைக் கொண்டாடுங்கள். ஜனவரி முதல் வாரத்திற்கு முன்பதிவு செய்ய இப்போதே அழையுங்கள்.</p></div></section>

<section class="sec"><div class="head"><p class="eyebrow">கேள்விகள்</p><h2>அடிக்கடி கேட்கப்படும் கேள்விகள்.</h2></div>{details(TA_FAQ)}</section>

<section class="sec" style="padding-top:0"><div class="finalcta"><p class="eyebrow" style="color:#a3aea6">இன்றே அழையுங்கள், தமிழில் பேசுங்கள்</p>
<a class="big" data-call href="tel:+16475172721">(647) 517-2721</a>
<div class="cta"><a class="btn hv" href="index.html#quote">2 நிமிடத்தில் விலை</a><a class="btn alt" href="{TA_SMS}" style="color:#fff;border-color:#3A463F">{ICO_MSG}புகைப்படம் அனுப்புங்கள்</a></div></div></section>
</main>'''
    return fname, head + main + tail


# ---------- Launch-week Giveback Cleanout (nominations by email through FormSubmit, nothing touches the tracker) ----------
FORM_ENDPOINT = re.search(r'photoEndpoint: "([^"]+)"', INDEX).group(1)
GB_FAQ = [("Can I nominate myself?", "Yes. Tell us your story the same way you would for someone else."),
          ("Does it cost anything to enter?", "No. There is nothing to buy, and you do not need to follow, like or share anything."),
          ("Will my nomination be posted online?", "No. Nominations stay private. We only share the story, name or photos of the person we pick if they say yes."),
          ("How do you pick?", "Both owners read every nomination and choose the home where a cleanout would make the biggest difference. It is not a random draw.")]


def giveback_page():
    fname = "giveback.html"
    q = money(LOAD_PRICES[1])
    title = "Free Launch Cleanout: Nominate a Neighbour | 6ix Cleanout"
    desc = (f"6ix Cleanout Co. is clearing one home in Scarborough, Markham or Unionville for free (up to a quarter truck, {q} value). "
            "Nominate by November 20.")
    event = {"@context": "https://schema.org", "@type": "WebPage", "name": "The Scarborough Giveback Cleanout", "url": SITE + fname,
             "description": desc, "publisher": business_ld(["Scarborough", "Markham", "Unionville"])}
    head, tail = shell(title, desc, fname, [event, faq_ld(GB_FAQ)])
    rules = [
        "Nominations close Friday, November 20, 2026 at 11:59 p.m. We contact the person we pick directly and announce it on Monday, November 23, 2026.",
        f"One prize: one free cleanout of up to a quarter truck (about one small room, or a couch plus a few boxes; value {q}), carried out, hauled away and swept, "
        "on a day that suits both of us before December 31, 2026. No cash value.",
        "Open to homes in Scarborough, Markham and Unionville. The person picked must be 18 or older, agree to the cleanout and be able to give us access to the items.",
        "Not included: hazardous waste (paint, propane, chemicals, asbestos) and heavy materials such as concrete, brick, dirt and shingles.",
        "The two owners choose the winner from the nominations, based on how much the cleanout would help. It is not a random draw. No purchase, follow, like or share is needed. "
        "You can nominate more than one person, or yourself.",
        "If we cannot reach the person picked within 3 days, we choose another nomination.",
        "We use nomination details only to run this giveback and delete the rest afterwards. See our privacy policy.",
        "This giveback is run only by 6ix Cleanout Co. It is not sponsored, endorsed or run by, or connected with, Facebook, Instagram, TikTok or any other platform, "
        "and by taking part you release them from any responsibility for it.",
    ]
    main = '''<main><div class="hband"><section class="phero"><p class="eyebrow">Launch week giveback · Scarborough · Markham · Unionville</p>
<h1><span class="kick">The Scarborough Giveback Cleanout</span>Know someone who <span class="lime">deserves a fresh start?</span></h1>
<p class="lead">To celebrate our launch, we are clearing one home for free. Nominate a neighbour, a relative, a friend, or yourself. We reveal who we picked on November 23.</p>
<div class="cta"><a class="btn hv" href="#nominate">Nominate someone</a>__CALL__</div></section></div>
<section class="sec" style="padding-top:36px"><div class="gbcards">
<div><span class="gbn">1</span><h3>What they get</h3><p>A free cleanout of up to a quarter truck, value __Q__. We do all the carrying, haul it away, donate and recycle what we can, and sweep up.</p></div>
<div><span class="gbn">2</span><h3>Who to nominate</h3><p>A senior who can no longer lift the heavy things, a busy single parent, a family that just arrived, someone getting back on their feet. Anyone in Scarborough, Markham or Unionville.</p></div>
<div><span class="gbn">3</span><h3>How we choose</h3><p>We read every nomination and pick the home where it would make the biggest difference. Not a random draw, and nothing to buy.</p></div>
</div></section>
<section id="nominate" class="sec"><div class="head"><p class="eyebrow">Nominate</p><h2>Tell us about them.</h2><p>Your story stays private. We only share the winner's story, name or photos if they say yes.</p></div>
<div class="panel" style="max-width:660px" id="gb">
<label class="f" for="gb-name"><span>Your name</span></label><input type="text" id="gb-name" autocomplete="name" maxlength="80">
<label class="f" for="gb-contact"><span>Your phone or email<em>so we can reach you</em></span></label><input type="text" id="gb-contact" autocomplete="tel" maxlength="120">
<div class="grid2"><div><label class="f" for="gb-who"><span>Who are you nominating?</span></label><input type="text" id="gb-who" maxlength="60" placeholder="First name, or &quot;Me&quot;"></div>
<div><label class="f" for="gb-area"><span>Their area</span></label><select id="gb-area"><option>Scarborough</option><option>Markham</option><option>Unionville</option></select></div></div>
<label class="f" for="gb-what"><span>What needs to go?</span></label><input type="text" id="gb-what" maxlength="200" placeholder="For example: an old couch, a broken treadmill and boxes in the basement">
<label class="f" for="gb-why"><span>Why them, and why now?</span></label><textarea id="gb-why" maxlength="2000" placeholder="A few sentences is plenty."></textarea>
<label class="chk"><input type="checkbox" id="gb-ok"><span>They know I am nominating them, and they are happy for 6ix Cleanout to contact them. (Tick this for yourself too.)</span></label>
<input type="text" id="gb-hp" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="nav"><span></span><button type="button" class="btn hv" id="gb-send">Send nomination</button></div><div id="gb-msg"></div></div></section>
<section class="sec"><div class="head"><p class="eyebrow">The rules</p><h2>Simple and fair.</h2></div><div class="prose"><ul>__RULES__</ul></div></section>
<section class="sec"><div class="head"><p class="eyebrow">Questions</p><h2>Before you nominate.</h2></div>__FAQ__</section>
<section class="sec"><div class="gb"><div><p class="eyebrow">Not picked, or need it gone sooner?</p><h2>Founding 25 launch prices.</h2>
<p>Our first 25 customers get launch prices, from __MIN__ with no tax added. See your price in 2 minutes.</p></div><div class="cta"><a class="btn hv" href="index.html#quote">Get my price</a></div></div></section>
</main>
<script>
(function(){
  const END=new Date("__UNTIL__T00:00:00"), EP="__EP__", $=id=>document.getElementById(id);
  const closed=()=>{ $("gb").innerHTML='<h2>Nominations are closed.</h2><p class="lead" style="margin-top:10px">Thank you to everyone who nominated someone. We announce the cleanout on November 23 on our Facebook and Instagram.</p>'; };
  if(new Date()>=END){ closed(); return; }
  $("gb-send").addEventListener("click",async()=>{
    const v={name:$("gb-name").value.trim(),contact:$("gb-contact").value.trim(),who:$("gb-who").value.trim(),area:$("gb-area").value,what:$("gb-what").value.trim(),why:$("gb-why").value.trim()};
    if(!v.name||!v.contact||!v.who||!v.why){ $("gb-msg").innerHTML='<div class="alert bad">Please fill in your name, how to reach you, who you are nominating and why.</div>'; return; }
    if(!$("gb-ok").checked){ $("gb-msg").innerHTML='<div class="alert bad">Please tick the box to confirm they know about the nomination.</div>'; return; }
    if($("gb-hp").value) return;
    const fd=new FormData();
    fd.append("_subject","Giveback nomination: "+v.who+" ("+v.area+")"); fd.append("_template","table"); fd.append("_captcha","false"); fd.append("_honey","");
    fd.append("nominated_by",v.name); fd.append("contact",v.contact); fd.append("nominee",v.who); fd.append("area",v.area); fd.append("what_needs_to_go",v.what); fd.append("why",v.why);
    fd.append("nominee_agreed","yes"); fd.append("source",window.leadSourceText?leadSourceText():"");
    $("gb-send").disabled=true; $("gb-send").textContent="Sending...";
    try{ await fetch(EP,{method:"POST",mode:"no-cors",body:fd});
      if(window.track6) track6("SubmitApplication",{content_name:"giveback"});
      $("gb").innerHTML='<h2>Thank you, '+v.name.split(" ")[0].replace(/[<>&"]/g,"")+'!</h2><p class="lead" style="margin-top:10px">Your nomination is in. We read every one, and we reveal who we picked on November 23. Know someone else? You can nominate more than one person.</p><div class="cta" style="margin-top:16px"><a class="btn alt" href="giveback.html">Nominate someone else</a></div>';
    }catch(e){ $("gb-send").disabled=false; $("gb-send").textContent="Try again"; $("gb-msg").innerHTML='<div class="alert bad">That did not send. Please text us at (647) 517-2721 or email 6ixcleanoutco@gmail.com.</div>'; }
  });
})();
</script>'''
    main = (main.replace("__CALL__", CALL_BTN).replace("__Q__", q).replace("__MIN__", money(MIN)).replace("__UNTIL__", GIVEBACK_UNTIL)
            .replace("__EP__", FORM_ENDPOINT).replace("__RULES__", "".join(f"<li>{esc(r)}</li>" for r in rules)).replace("__FAQ__", details(GB_FAQ)))
    assert "__" not in main.replace("__proto__", ""), "unfilled placeholder in giveback page"
    return fname, head + main + tail


# ---------- Page not found (GitHub Pages serves 404.html for any missing address) ----------
# ===== Cost guide (2026-11-04): every number is read from index.html, so it can never disagree with the estimator =====
ITEM_NAMES = {i: t for i, t in re.findall(r'\{id:"(\w+)", t:"([^"]+)", solo:\d+, add:\d+', INDEX)}
FAR_MIN = int(re.search(r"farZoneMin: (\d+)", INDEX).group(1))
def _num(pat):
    m = re.search(pat, INDEX)
    if not m:
        sys.exit("cost guide: could not read " + pat)
    return int(m.group(1))
STAIRS = _num(r"const a=(\d+)\*s\.stairs")
CARRY1, CARRY2 = _num(r"s\.carry===1\)\{ sub\+=(\d+)"), _num(r"s\.carry===2\)\{ sub\+=(\d+)")
PARK = _num(r"s\.parking===1\)\{ sub\+=(\d+)")
PRIORITY = _num(r"s\.timing===2\)\{ sub\+=(\d+)")
RLO, RHI = float(re.search(r"rangeLow: ([\d.]+)", INDEX).group(1)), float(re.search(r"rangeHigh: ([\d.]+)", INDEX).group(1))
LOAD_LOOKS = ["A few bags, a chair or a small table", "One small room, or a couch plus a few boxes", "A bedroom, or a full basement corner",
              "A living room plus extras", "A one-bedroom apartment", "A full garage or a small house floor", "A full house cleanout or hoarding clean-up"]
LOAD_NAMES = ["A few items", "Quarter truck", "Half truck", "Three-quarter truck", "Full truck", "1.5 trucks", "2 trucks"]
LOAD_FRAC = [.125, .25, .5, .75, 1, 1.5, 2]


def _r5(n):
    return int((n / 5) + 0.5) * 5


def estimate(job, city, stairs=0, senior=False):
    """Same steps as calc() in index.html: job price, access, seniors discount, travel, minimums, then the range."""
    z, fee = ZONES[city]
    sub = job + STAIRS * stairs
    if senior:
        sub -= min(round(sub * SENIOR_PCT / 100), max(0, sub - MIN))
    sub += fee
    if z == 4 and sub < FAR_MIN:
        sub = FAR_MIN
    floor = FAR_MIN if z == 4 else MIN
    low = max(floor, _r5(sub * RLO))
    return low, max(low, _r5(sub * RHI))


def cost_page():
    fname = COST_PAGE[0]
    url = SITE + fname
    lp, ip = LOAD_PRICES, ITEM_PRICE
    examples = [
        ("One couch, ground floor, Scarborough", "A single item in the home zone. The couch alone is under the minimum, so the minimum applies.",
         estimate(max(ip["couch"][0], MIN), "Scarborough")),
        ("A mattress and box spring, upstairs bedroom, Markham", f"Two pieces at {money(ip['mattress'][0])} each, plus {money(STAIRS)} for one flight of stairs.",
         estimate(2 * ip["mattress"][0], "Markham", stairs=1)),
        ("Half a garage, North York", f"A half truck ({money(lp[2])}) plus the {money(ZONES['North York'][1])} travel charge for North York.",
         estimate(lp[2], "North York")),
        ("A one-bedroom move-out, Pickering", f"A full truck ({money(lp[4])}) plus {money(ZONES['Pickering'][1])} travel.",
         estimate(lp[4], "Pickering")),
        ("A senior's basement, Scarborough", f"A three-quarter truck ({money(lp[3])}) with the {SENIOR_PCT}% seniors discount.",
         estimate(lp[3], "Scarborough", senior=True)),
        ("A half truck in Mississauga", f"Outer-ring jobs add {money(ZONES['Mississauga'][1])} travel and have a {money(FAR_MIN)} minimum.",
         estimate(lp[2], "Mississauga")),
    ]
    faqs = [
        ("How much does junk removal cost in Toronto?",
         f"With us, most jobs cost between {money(MIN)} and {money(lp[4])}. A few items start at {money(MIN)}, a half truck (about a bedroom's worth) is {money(lp[2])} and a full truck (about a one-bedroom apartment) is {money(lp[4])}. "
         "Travel outside Scarborough, Markham and Unionville adds a small charge. No tax is added."),
        ("How much does it cost to get rid of a couch?",
         f"{money(max(ip['couch'][0], MIN))} for a single couch from a home in Scarborough, Markham or Unionville, plus travel for other areas. In a bigger load, a couch adds nothing."),
        ("How much does mattress removal cost?",
         f"{money(max(ip['mattress'][0], MIN))} for one mattress on its own. In a bigger load, each mattress adds {money(ip['mattress'][1])}, because mattresses go to a separate recycler."),
        ("Do you charge for stairs?", f"Yes, {money(STAIRS)} for each flight. A carry of 15 to 30 metres adds {money(CARRY1)}, over 30 metres {money(CARRY2)}, and parking more than 50 metres away {money(PARK)}."),
        ("Is tax included?", "We do not add tax. We are a small business that is not registered for HST yet, so the price we confirm is the price you pay."),
        ("What is the minimum charge?", f"{money(MIN)}. In the outer ring (Mississauga, Brampton, Oshawa and Oakville) the minimum is {money(FAR_MIN)}, because of the drive."),
        ("Is there a seniors discount?", f"Yes. Customers 65 and older get {SENIOR_PCT}% off the job, down to the {money(MIN)} minimum. Tick the box in the online estimate."),
        ("How do I get an exact price?", "Use the online estimate (about 2 minutes) and add a few photos, or text the photos to us. We confirm a firm price in writing before any work starts."),
    ]
    head, tail = shell("Junk Removal Cost in Toronto: 2026 Prices | 6ix Cleanout Co.",
                       f"What junk removal costs in Toronto, Scarborough and Markham in 2026: real prices from {money(MIN)}, what changes the price, and worked examples. No tax added.",
                       fname, [
                           {"@context": "https://schema.org", "@type": "Article", "headline": "How much does junk removal cost in Toronto in 2026?",
                            "datePublished": "2026-11-04", "dateModified": datetime.date.today().isoformat(), "mainEntityOfPage": url, "inLanguage": "en-CA",
                            "author": {"@type": "Organization", "name": "6ix Cleanout Co.", "url": SITE},
                            "publisher": {"@type": "Organization", "name": "6ix Cleanout Co.", "url": SITE, "logo": {"@type": "ImageObject", "url": SITE + "apple-touch-icon.png"}}},
                           faq_ld(faqs)])
    loads = "".join(f'<tr><td><b>{n}</b></td><td>{d}</td><td>{truck_static(f)}</td><td class="p">{money(p)}</td></tr>'
                    for n, d, f, p in zip(LOAD_NAMES, LOAD_LOOKS, LOAD_FRAC, lp))
    items = "".join(f'<tr><td><b>{esc(ITEM_NAMES[i])}</b></td><td class="p">{money(max(s_, MIN))}</td><td>{"+" + money(a) if a else "No extra"}</td></tr>'
                    for i, (s_, a) in ip.items())
    zrows = {}
    for c, (z, fee) in ZONES.items():
        zrows.setdefault((z, fee), []).append(c)
    zones = "".join(f'<tr><td><b>Zone {z}</b></td><td>{", ".join(cs)}</td><td class="p">{"None" if not fee else "+" + money(fee)}</td></tr>' for (z, fee), cs in sorted(zrows.items()))
    exs = "".join(f'<div><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="tkp">{money(lo)} to {money(hi)}</span></div>' for t, d, (lo, hi) in examples)
    changes = [
        ("How much space it takes", "The main thing. We price by how much of the truck your things fill, from a few items to two full trucks."),
        ("Heavy materials", "Concrete, brick, dirt, shingles and plaster are priced by weight, and we confirm the price from photos first."),
        ("Getting it out", f"{money(STAIRS)} for each flight of stairs, {money(CARRY1)} to {money(CARRY2)} for a long carry, {money(PARK)} if we have to park more than 50 metres away."),
        ("Where you are", "Scarborough, Markham and Unionville have no travel charge. Other areas add $25 to $100."),
        ("How soon", f"Priority within 24 hours adds {money(PRIORITY)}. Flexible timing keeps single items at {money(MIN)}."),
        ("Special items", f"Some items need special handling, such as fridges with refrigerant (+{money(ip['fridge'][1])} in a load) and mattresses (+{money(ip['mattress'][1])}). Pianos and hot tubs need a third person."),
    ]
    ch = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in changes)
    ask = ["Is disposal included in the price, or added after?", "Is tax added on top?", "Do I get a confirmed price before you start, or only an estimate?",
           "Is there a charge for stairs, distance or parking?", "Where do my things go: donation, recycling or a licensed disposal site?"]
    main = (
        f'<main><div class="hband"><section class="phero">{LAUNCH_DARK}<p class="eyebrow">Cost guide · Updated November 2026</p>'
        f'<h1><span class="kick">Junk removal cost in Toronto, Scarborough &amp; Markham</span>What junk removal costs in 2026.</h1>'
        f'<p class="lead">Real prices from our own price list, what changes them, and worked examples. Most jobs cost {money(MIN)} to {money(lp[4])}, with no tax added.</p>'
        f'<div class="cta"><a class="btn hv" href="index.html#quote">Get my exact price</a>{CALL_BTN}{SMS_BTN}</div></section></div>'
        f'{TRUST_HTML}'
        f'<section class="sec" style="padding-top:20px"><div class="head"><p class="eyebrow">The short answer</p><h2>Priced by the space your things take up.</h2>'
        f'<p>Home-zone prices for Scarborough, Markham and Unionville. Disposal and recycling fees are included.</p></div>'
        f'<div class="tbl"><table><thead><tr><th>Truck space</th><th>Looks like</th><th>How full</th><th>Price</th></tr></thead><tbody>{loads}</tbody></table></div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">Examples</p><h2>What real jobs would cost.</h2>'
        f'<p>Worked out with the same rules as our online estimate. You get a range first and a confirmed price before we start.</p></div><div class="exgrid">{exs}</div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">Single items</p><h2>One thing, or one thing in a bigger load.</h2></div>'
        f'<div class="tbl"><table><thead><tr><th>Item</th><th>On its own</th><th>In a bigger load</th></tr></thead><tbody>{items}</tbody></table></div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">What changes the price</p><h2>Six things move the number.</h2></div><div class="exgrid">{ch}</div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">Travel</p><h2>Travel charge by area.</h2></div>'
        f'<div class="tbl"><table><thead><tr><th>Zone</th><th>Areas</th><th>Travel</th></tr></thead><tbody>{zones}</tbody></table></div></section>'
        f'<section class="sec"><div class="two"><div class="card"><h3>Questions to ask any junk removal company</h3><ul>{"".join(f"<li>{esc(a)}</li>" for a in ask)}</ul></div>'
        f'<div class="card"><h3>Ways to pay less</h3><p style="color:var(--muted);margin-top:8px">Choose flexible timing, book with a neighbour, refer a friend, or ask about the seniors discount. Details below.</p></div></div>{SAVE_HTML}</section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">Questions</p><h2>Cost questions, answered.</h2></div>{details(faqs)}</section>'
        + guide("More guides", "Popular jobs.", ITEM_PAGES)
        + "</main>")
    return fname, head + main + tail


def take_page():
    fname = TAKE_PAGE[0]
    url = SITE + fname
    ip = ITEM_PRICE
    fridge = money(max(ip["fridge"][0], MIN))
    yes = [
        ("Furniture", "Couches, sofas, chairs, tables, dressers and beds."),
        ("Mattresses and box springs", "Any size. Mattresses go to a separate recycler, which is why they add a small amount in a bigger load."),
        ("Appliances", f"Fridges and freezers (from {fridge} on their own), washers, dryers, stoves and dishwashers."),
        ("Electronics", "TVs and monitors."),
        ("Exercise equipment", "Treadmills and other home gym gear."),
        ("Clutter and cleanouts", "Boxes, bags, garage and basement contents, estate and move-out leftovers."),
        ("Yard and outdoor", "Old fencing, patio sets, bikes, lumber and yard waste."),
        ("Light renovation debris", "Cabinets, flooring, trim and drywall pieces."),
        ("Big and awkward", "Pianos and hot tubs. These need a third person, so send photos first."),
    ]
    faqs = [
        ("What can't a junk removal truck take?",
         "Hazardous waste: paint, solvents, gasoline, oil and other chemicals, propane tanks, pool chemicals, asbestos, and medical waste or needles. Your city or region takes these at its own drop-off depots, most of them free for residents."),
        ("Do you take fridges and freezers?",
         f"Yes. A fridge or freezer on its own starts at {fridge}. In a bigger load it adds {money(ip['fridge'][1])}, because the refrigerant has to be handled properly."),
        ("Do you take car batteries and tires?", "Ask us first. Send a text or photo and we will tell you if we can take them with your job."),
        ("Can you take concrete, brick or dirt?",
         "Yes, but heavy materials such as concrete, brick, dirt, shingles and plaster are priced by weight, and we confirm the price from photos first."),
        ("How does junk removal work with us?",
         "Get a price online in about 2 minutes, or text us photos. We confirm a firm price in writing before any work starts. We arrive in your time window, load everything and sweep up, and you pay after the job by cash or Interac e-Transfer."),
        ("Where does my stuff go?", "Items are reused, donated or recycled first. What is left goes to licensed disposal sites."),
        ("How do I get rid of old paint or chemicals?", "Take them to your city or region's household hazardous waste depot. Links are on this page. We cannot take them in the truck."),
    ]
    head, tail = shell("What Junk Removal Takes, and What It Can't | 6ix Cleanout",
                       "What junk removal can and can't take in Scarborough, Markham and the GTA: furniture, appliances, mattresses, renovation debris, and why hazardous waste is out.",
                       fname, [
                           {"@context": "https://schema.org", "@type": "Article", "headline": "What can a junk removal company take, and what can't it?",
                            "datePublished": "2026-11-05", "dateModified": datetime.date.today().isoformat(), "mainEntityOfPage": url, "inLanguage": "en-CA",
                            "author": {"@type": "Organization", "name": "6ix Cleanout Co.", "url": SITE},
                            "publisher": {"@type": "Organization", "name": "6ix Cleanout Co.", "url": SITE, "logo": {"@type": "ImageObject", "url": SITE + "apple-touch-icon.png"}}},
                           faq_ld(faqs)])
    cards = "".join(f'<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in yes)
    main = (
        f'<main><div class="hband"><section class="phero">{LAUNCH_DARK}<p class="eyebrow">Guide · Updated November 2026</p>'
        f'<h1><span class="kick">What junk removal takes in Scarborough, Markham &amp; the GTA</span>What we take, and what we can\'t.</h1>'
        f'<p class="lead">Almost anything from a home that is not hazardous. Here is the full list, how the price works, and where the few things we cannot take should go.</p>'
        f'<div class="cta"><a class="btn hv" href="index.html#quote">Get my price</a>{CALL_BTN}{SMS_BTN}</div></section></div>'
        f'{TRUST_HTML}'
        f'<section class="sec" style="padding-top:20px"><div class="head"><p class="eyebrow">We take</p><h2>Most household and light renovation items.</h2>'
        f'<p>Prices start at {money(MIN)}. Disposal and recycling fees are included, and we confirm the price in writing before any work starts.</p></div><div class="exgrid">{cards}</div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">We cannot take</p><h2>Hazardous waste.</h2></div>{notake_html()}</section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">How the price works</p><h2>Priced by space, confirmed first.</h2>'
        f'<p>We price by how much of the truck your things fill, plus small add-ons for stairs, long carries and travel outside our home zone. No tax is added. '
        f'<a href="{COST_PAGE[0]}">See the full cost guide, with worked examples</a>.</p></div></section>'
        f'<section class="sec"><div class="head"><p class="eyebrow">Questions</p><h2>Before you book.</h2></div>{details(faqs)}</section>'
        + guide("More guides", "Popular jobs.", ITEM_PAGES + [COST_PAGE])
        + "</main>")
    return fname, head + main + tail


def not_found_page():
    head, tail = shell("Page not found | 6ix Cleanout Co.", "This page does not exist. Get your junk removal price in 2 minutes instead.", "404.html", [])
    head = re.sub(r'<link rel="canonical" href="[^"]*">', "", head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">\n?', "", head)
    base_path = re.match(r"https?://[^/]+(/.*)", SITE).group(1)  # "/6ix-cleanout/" now, "/" once the custom domain is set
    head = head.replace("<head>", f'<head><base href="{base_path}">', 1).replace("</head>", '<meta name="robots" content="noindex"></head>', 1)
    main = ('<main><div class="hband"><section class="phero"><p class="eyebrow">Error 404</p><h1>This page has been <span class="lime">cleared out.</span></h1>'
            '<p class="lead">The page you are looking for does not exist, or it moved. Here is where to go instead.</p>'
            f'<div class="cta"><a class="btn hv" href="index.html#quote">Get my free estimate</a><a class="btn alt" href="index.html">Home page</a>{CALL_BTN}</div></section></div>'
            + guide("Popular", "Most visited pages.", [("services.html", "Services and prices"), ("areas.html", "Service areas"), ("about.html", "About and FAQ")] + ITEM_PAGES)
            + "</main>")
    return "404.html", head + main + tail


# ---------- llms.txt: a plain summary for AI assistants (ChatGPT, Gemini, Perplexity) ----------
def llms_txt():
    zone_lines = {}
    for c, (z, fee) in ZONES.items():
        zone_lines.setdefault((z, fee), []).append(c)
    zones = "\n".join(f"  - Zone {z} ({'no travel charge' if not fee else money(fee) + ' travel'}): {', '.join(cs)}{' (larger jobs only)' if z == 4 else ''}" for (z, fee), cs in sorted(zone_lines.items()))
    names = ["A few items", "Quarter truck", "Half truck", "Three-quarter truck", "Full truck", "1.5 trucks", "2 trucks"]
    loads = "\n".join(f"  - {n}: {money(p)}" for n, p in zip(names, LOAD_PRICES))
    pages = [("index.html", "Home and instant online estimate"), ("services.html", "Services and prices"), ("areas.html", "Service areas and travel charges"),
             ("about.html", "About the owners and FAQ"), ("realtors-landlords.html", "Realtors, landlords and property managers"), ("tamil.html", "Tamil page (தமிழ்)"),
             ("terms.html", "Service terms"), ("privacy.html", "Privacy policy"), (COST_PAGE[0], "Junk removal cost guide with worked examples"), (TAKE_PAGE[0], "What junk removal takes and what it cannot take")] + [(f, "Junk removal in " + c) for f, c in CITY_PAGES] + ITEM_PAGES
    links = "\n".join(f"- [{t}]({SITE}{'' if f == 'index.html' else f})" for f, t in pages)
    hours = "Monday to Saturday 7am to 8pm, Sunday 8am to 6pm"
    assert HOURS_LD[0]["opens"] == "07:00" and HOURS_LD[1]["closes"] == "18:00", "update the hours text in llms_txt"
    return f"""# 6ix Cleanout Co.

> Local junk removal and cleanouts in Scarborough, Markham and the Greater Toronto Area, Ontario, Canada. Run by its two owners, {OWNERS[0]} and {OWNERS[1]}, who do every job themselves. Instant online price in about 2 minutes, a confirmed price before any work starts, no tax added, payment after the job.

## Key facts
- Services: furniture and couch removal, mattress removal, appliance removal (fridges, washers, dryers, stoves), garage and basement cleanouts, move-outs, estate and downsizing cleanouts, light renovation debris, unit turnovers for landlords and property managers.
- Minimum charge: {money(MIN)}. Prices by truck space, no tax added:
{loads}
- Add-ons in a load: mattress +{money(ITEM_PRICE['mattress'][1])}, fridge or freezer +{money(ITEM_PRICE['fridge'][1])}, washer or dryer +{money(ITEM_PRICE['washer'][1])}. Priority within 24 hours: +$60.
- Travel by zone:
{zones}
- Seniors (65+): {SENIOR_PCT}% off the job, down to the minimum.
- Payment: cash or Interac e-Transfer after the job. Jobs over $500 need a 20% deposit to book, refundable up to 24 hours before.
- Items are donated and recycled first; the rest goes to licensed disposal sites. No hazardous waste (paint, propane, chemicals, asbestos).
- Languages: English and Tamil.
- Hours: {hours}.
- Contact: (647) 517-2721 (call or text), 6ixcleanoutco@gmail.com.

## Pages
{links}
"""


def lastmod(f):
    """Date the file last really changed: today if it differs from the last commit, otherwise that commit's date."""
    changed = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", f], cwd=ROOT).returncode != 0
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", f], cwd=ROOT, capture_output=True).returncode == 0
    if changed or not tracked:
        return datetime.date.today().isoformat()
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or datetime.date.today().isoformat()


def sitemap(files):
    urls = "".join(f"<url><loc>{SITE}{'' if f == 'index.html' else f}</loc><lastmod>{lastmod(f)}</lastmod></url>" for f in files)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def main():
    files = ["index.html", "services.html", "realtors-landlords.html", "areas.html", "about.html"]
    for city, d in CITIES.items():
        f, s = city_page(city, d)
        (ROOT / f).write_text(s, encoding="utf-8", newline="\n"); files.append(f); print("built", f)
    for fname, d in ITEMS.items():
        f, s = item_page(fname, d)
        (ROOT / f).write_text(s, encoding="utf-8", newline="\n"); files.append(f); print("built", f)
    for fname, d in LEGAL.items():
        f, s = legal_page(fname, d)
        (ROOT / f).write_text(s, encoding="utf-8", newline="\n"); files.append(f); print("built", f)
    f, s2 = tamil_page()
    s2 = s2.replace('href="index.html#quote"', 'href="index.html?lang=ta#quote"')  # Tamil visitors start the estimate with Tamil preselected
    (ROOT / f).write_text(s2, encoding="utf-8", newline="\n"); files.append(f); print("built", f)
    f, s3 = booking_page()  # not in the sitemap: it is only reached from quote emails
    (ROOT / f).write_text(s3, encoding="utf-8", newline="\n"); print("built", f)
    f, s4 = giveback_page()
    (ROOT / f).write_text(s4, encoding="utf-8", newline="\n"); files.append(f); print("built", f)
    f, s6 = cost_page()
    (ROOT / f).write_text(s6, encoding="utf-8", newline="\n"); files.append(f); print("built", f)
    f, s7 = take_page()
    (ROOT / f).write_text(s7, encoding="utf-8", newline="\n"); files.append(f); print("built", f)
    f, s5 = not_found_page()  # not in the sitemap
    (ROOT / f).write_text(s5, encoding="utf-8", newline="\n"); print("built", f)
    (ROOT / "llms.txt").write_text(llms_txt(), encoding="utf-8", newline="\n"); print("built llms.txt")
    (ROOT / "sitemap.xml").write_text(sitemap(files), encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8", newline="\n")
    print("built sitemap.xml and robots.txt with", len(files), "pages")


if __name__ == "__main__":
    main()
