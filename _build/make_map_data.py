"""Builds areas-map.json (city outlines for the Areas page map) and the postal-code table.

Sources, saved in _build/geo_src so the build never needs the internet:
  - fine_<key>.json: city and former-city boundaries from OpenStreetMap (Nominatim, simplified),
    (c) OpenStreetMap contributors, ODbL. The map credits OpenStreetMap.
  - fsa_M.json / fsa_L.json: the first 3 characters of postal codes (FSA) and their area,
    from Wikipedia's lists of postal codes of Canada (M and L).
Run:  python _build/make_map_data.py   (then patch_shared.py, which reads fsa_table())
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "geo_src"
ROOT = HERE.parent

# key: (label on the map, estimator city)
AREAS = {
    "scarborough": ("Scarborough", "Scarborough"),
    "markham": ("Markham and Unionville", "Markham"),
    "northyork": ("North York", "North York"),
    "eastyork": ("East York", "East York"),
    "oldtoronto": ("Toronto: downtown, east and west end", "Downtown Toronto"),
    "york": ("York (Toronto)", "Downtown Toronto"),
    "richmondhill": ("Richmond Hill", "Richmond Hill"),
    "pickering": ("Pickering", "Pickering"),
    "vaughan": ("Vaughan", "Vaughan"),
    "etobicoke": ("Etobicoke", "Etobicoke"),
    "ajax": ("Ajax", "Ajax"),
    "whitby": ("Whitby", "Whitby"),
    "stouffville": ("Whitchurch-Stouffville", "Stouffville"),
    "mississauga": ("Mississauga", "Mississauga"),
    "brampton": ("Brampton", "Brampton"),
    "oshawa": ("Oshawa", "Oshawa"),
    "oakville": ("Oakville", "Oakville"),
}

# postal-code area name (from the FSA lists) -> (estimator city, label shown to the customer)
TORONTO = {"Scarborough": ("Scarborough", "Scarborough"), "North York": ("North York", "North York"), "East York": ("East York", "East York"),
           "Etobicoke": ("Etobicoke", "Etobicoke"), "Downtown Toronto": ("Downtown Toronto", "downtown Toronto"),
           "Central Toronto": ("Downtown Toronto", "midtown Toronto"), "East Toronto": ("Downtown Toronto", "the east end of Toronto"),
           "West Toronto": ("Downtown Toronto", "the west end of Toronto"), "York": ("Downtown Toronto", "York, Toronto"), "Mississauga": ("Mississauga", "Mississauga")}
L_AREAS = {"Markham": ("Markham", "Markham"), "Richmond Hill": ("Richmond Hill", "Richmond Hill"), "Vaughan": ("Vaughan", "Vaughan"),
           "Concord": ("Vaughan", "Concord, Vaughan"), "Woodbridge": ("Vaughan", "Woodbridge, Vaughan"), "Stouffville": ("Stouffville", "Stouffville"),
           "Pickering": ("Pickering", "Pickering"), "Ajax": ("Ajax", "Ajax"), "Whitby": ("Whitby", "Whitby"), "Oshawa": ("Oshawa", "Oshawa"),
           "Mississauga": ("Mississauga", "Mississauga"), "Brampton": ("Brampton", "Brampton"), "Oakville": ("Oakville", "Oakville")}
# Thornhill is split: L3T is the Markham side, L4J the Vaughan side
SPECIAL = {"L3T": ("Markham", "Thornhill, Markham"), "L4J": ("Vaughan", "Thornhill, Vaughan")}


def fsa_table():
    m = json.loads((SRC / "fsa_M.json").read_text(encoding="utf-8"))
    l = json.loads((SRC / "fsa_L.json").read_text(encoding="utf-8"))
    out = {}
    for code, area in m.items():
        if area in TORONTO:
            out[code] = list(TORONTO[area])
        elif "Queen's Park" in area:
            out[code] = ["Downtown Toronto", "downtown Toronto"]
    for code, area in l.items():
        if code in SPECIAL:
            out[code] = list(SPECIAL[code])
        elif area in L_AREAS:
            out[code] = list(L_AREAS[area])
    return dict(sorted(out.items()))


def rings(geo):
    polys = [geo["coordinates"]] if geo["type"] == "Polygon" else geo["coordinates"]
    return [[[[round(lat, 4), round(lon, 4)] for lon, lat in ring] for ring in poly] for poly in polys]


def main():
    areas = []
    for key, (label, city) in AREAS.items():
        d = json.loads((SRC / f"fine_{key}.json").read_text(encoding="utf-8"))
        if not d or d[0].get("geojson", {}).get("type") not in ("Polygon", "MultiPolygon"):
            sys.exit("no outline for " + key)
        areas.append({"key": key, "label": label, "city": city, "polys": rings(d[0]["geojson"])})
    out = {"credit": "City outlines (c) OpenStreetMap contributors, ODbL", "areas": areas}
    (ROOT / "areas-map.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8", newline="\n")
    print("areas-map.json:", len(areas), "areas,", (ROOT / "areas-map.json").stat().st_size // 1024, "KB;", len(fsa_table()), "postal-code areas")


if __name__ == "__main__":
    main()
