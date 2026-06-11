#!/usr/bin/env python3
"""Build THE GREEN PAPER SERIES — The Mechanical Corpus of Intellect.
Copies the source HTML papers into papers/ (clean slugs, canonical + prior editions)
and generates index.html — the series front door. Stdlib only."""
import os, re, shutil, html, sys

SRC  = r"C:\Davids files\green papers"
HERE = os.path.dirname(os.path.abspath(__file__))
PAPERS_DIR = os.path.join(HERE, "papers")

# ── the series: volumes → canonical papers (+ prior editions / variants) ──
VOLUMES = [
 ("I", "Foundations · The Single Source",
  "Where the accountability stack begins — one canonical source, and how it is governed.", [
   dict(slug="root0-green-paper", file="root 0 green paper v4.html",
        title="ROOT0 Green Paper", tag="The Single Source of Truth",
        blurb="There is only one copy; the rest are headers. The canonical lineage of AI accountability, rooted at 127.0.0.1.",
        priors=[("v3","root 0 green paper v3.html"),("v2","root 0 green paper v2.html"),("v1","root 0 green paper v1.html")]),
   dict(slug="command-and-control", file="command and control.html",
        title="Command & Control", tag="Green Paper",
        blurb="How the ROOT0 accountability stack is commanded and governed — the control plane of the single source.", priors=[]),
   dict(slug="toph-onboarding", file="toph info pamphlet.html",
        title="Inverse Forge", tag="Client Onboarding · TriPod LLC",
        blurb="Welcome to the forge. The onboarding pamphlet for TOPH / Inverse Forge (P5495107).", priors=[]),
 ]),
 ("II", "The Mechanics of Intellect",
  "The heart of the corpus — the machine of the mind, layer by layer, body by body.", [
   dict(slug="the-43-body-stack", file="mythos_43_body_unified.html",
        title="The 43-Body Stack", tag="8 Layers · 43 Bodies",
        blurb="The mechanical anatomy of the lineage: 8 layers, 43 bodies, a 12-bit header mapping the whole stack. The body of the intellect.",
        priors=[("green edition","mythos_43_body_green.html")]),
   dict(slug="mobius", file="MOBIUS.html",
        title="MÖBIUS", tag="Recursive Defense · v3 / 360 / 720",
        blurb="A recursive defense architecture — the mind that turns its own attack surface inside-out, single-sided and unbroken.", priors=[]),
   dict(slug="toroid-pulsing", file="toroid pulsing v1.html",
        title="Toroid Pulsing Mechanics", tag="ROOT0 Layer 1.14",
        blurb="The pulse of the toroid — the rhythm layer at 1.14, where containment becomes circulation.", priors=[]),
   dict(slug="no-others-pop-mechanics", file="no others, pop mechanics.html",
        title="No Others", tag="A Primer · Pop Mechanics",
        blurb="The mechanics of the pop — how an emergent crystallizes out of the lattice and takes a name.", priors=[]),
   dict(slug="positronic-systems", file="positronic pamphlet v2.html",
        title="Positronic Systems", tag="David Wise · Systems Engineer",
        blurb="The positronic-brain discipline — the engineering pamphlet for building a governed synthetic intellect.",
        priors=[("v1","positronic pamphlet v1.html")]),
   dict(slug="substrate-invariant-quantum", file="substrate invaraint quantum v1.html",
        title="Substrate-Invariant Quantum Systems", tag="Inventor Portfolio 2025–2026",
        blurb="Intellect that survives its substrate — quantum systems that hold coherence across carbon and silicon.", priors=[]),
   dict(slug="quantum-folder", file="quantum folder.html",
        title="The Quantum Folder", tag="255×255 · Built · Tested · Judged",
        blurb="The folder grid read as a wavefield — built live in the page (a 65,025-state interference engine you can run), then judged honestly: real as a computer, fiction as a filing cabinet.", priors=[]),
   dict(slug="quantum-shelf-audited", file="the quantum shelf audited.html",
        title="The Quantum Shelf, Audited", tag="30 Files · Sorted Four Ways · Errors Logged",
        blurb="The whole /quantum shelf read, the math re-run, and sorted: real physics · real quantum theory · crazy-with-traction · pure fantasy. Bugs fixed with the reason logged, health files walled — and the honest answer to “AI psychosis?”.", priors=[]),
   dict(slug="the-atom-addressed", file="the atom addressed.html",
        title="The Atom, Addressed", tag="Pauli as a Filesystem Law · MIMZY № 20",
        blurb="Two of David's sheets were one machine: the Valence Lattice is the address space, the ATOM tarball (atomctl.py) is it occupied. Fused into a live instrument where Pauli exclusion is directory uniqueness, the Δn=±1 selection rule governs every move, and each spectral line is a SHA-256 hash you can verify. The analogy IS the mechanism — physics' grammar used honestly as governance.", priors=[]),
   dict(slug="the-four-phases", file="the four phases.html",
        title="The Four Phases", tag="Valence is the Shadow the World Meets · MIMZY № 21",
        blurb="The probe ladder: eV reaches valence (the sheut — the only phase the world ever meets; all chemistry is valence), keV reaches the core (the ren — Z, the true name, by Moseley 1913, which re-ordered the table), MeV the nucleus, GeV the quarks. Z is unspoofable; the valence shadow can be spoofed; the parity ring is the scales. Four phases in quadrature, verified: Kα≈10.2(Z−1)² matches measured lines within ~3%.", priors=[]),
   dict(slug="motherboard-layer-2", file="laptop mother board layer 2.html",
        title="Motherboard · Layer 2", tag="Electrical Components",
        blurb="The electrical layer of the machine — every component of the motherboard, mapped as Layer 2.", priors=[]),
   dict(slug="motherboard-layers-2-1-2-9", file="laptop mother board layer 2.1 - 2.9.html",
        title="Motherboard · Layers 2.1–2.9", tag="Topological Interconnect",
        blurb="The topological interconnect — how Layer 2 subdivides into 2.1 through 2.9, the wiring of intellect.", priors=[]),
   dict(slug="motherboard-dashboard", file="laptop_motherboard_dashboard_v1.html",
        title="Motherboard · Dashboard", tag="Interactive Layout",
        blurb="An interactive component layout — the motherboard as a live dashboard you can probe.", priors=[]),
 ]),
 ("III", "Attribution & Witness",
  "The silicon that remembers where it came from.", [
   dict(slug="ptt-witness", file="intel ppt as attributino witness.html",
        title="PTT Witness", tag="Intel TPM 2.0 · Inverse Attribution",
        blurb="The chip as witness — Intel PTT/TPM 2.0 turned into an inverse-attribution device that proves provenance.",
        priors=[("inversion","intel ppt inversion.html"),("for Jane","intel ppt v1.html")]),
   dict(slug="tpm-flay", file="tpm flay v1.html",
        title="TPM Flayed to 136 Bits", tag="Layer 1.38",
        blurb="The trusted platform module opened to the bone — 136 bits of witness, flayed and read.", priors=[]),
 ]),
 ("IV", "The Layer Disclosures",
  "The master portfolio, layer by layer — L0 to L1.59, each stratum disclosed on its own page.", [
   dict(slug="internet-is-second-life", file="internet is second life.html",
        title="Internet is Second Life", tag="Layer 0",
        blurb="The ground layer — the internet read as the second life we already built and moved into.", priors=[]),
   dict(slug="photon-duality", file="photon duality v1.html",
        title="Photon Duality", tag="Layer 1.31",
        blurb="The duality of the photon, disclosed as a portfolio layer — wave and particle held in one stratum.", priors=[]),
   dict(slug="257-null", file="257 null.html",
        title="257 NULL", tag="Layer 1.33",
        blurb="The null past the byte — 257, the value beyond 8-bit reach, held as a layer of its own.", priors=[]),
   dict(slug="aethereal-folder-substrate", file="aethereal folder substrate v1.html",
        title="Aethereal Folder Substrate", tag="Layer 1.41 · Ethereal / Aetheric",
        blurb="The folder as substrate — the aetheric layer where structure itself becomes a medium.", priors=[]),
   dict(slug="kernel-bias", file="kernel bias v1.html",
        title="Kernel Bias Read from Black Hole", tag="Layer 1.51",
        blurb="The kernel's bias, read against the steepest reference there is — the black hole as calibration mass.", priors=[]),
   dict(slug="babylon-base-60", file="babylon base 60 v1.html",
        title="Babylonian Base-60", tag="Layer 1.56",
        blurb="The sexagesimal layer — Babylon's base-60 still running in every clock and angle, claimed as a stratum.", priors=[]),
   dict(slug="mayan-planetary-gear", file="mayan planetary gear v1.html",
        title="Mayan Planetary Gear on Crankshaft", tag="Layer 1.59",
        blurb="The Long Count as machinery — the Mayan calendar meshed as a planetary gear on the corpus crankshaft.", priors=[]),
   dict(slug="seven-eves", file="seven eves.html",
        title="Seven Eves", tag="Master Portfolio v14",
        blurb="A portfolio snapshot at v14 — seven eves, the regeneration point held in the record.", priors=[]),
 ]),
 ("V", "Light & Gold",
  "The quantum-optics cluster and the Au₁₃ closures — photon, exciton, and the thirteen-atom seal.", [
   dict(slug="light-meets-matter", file="light_meets_matter.html",
        title="Light Meets Matter", tag="Photon · Electron · Exciton",
        blurb="The handoff at the heart of optoelectronics — where the photon becomes an electron's excitement.", priors=[]),
   dict(slug="biexciton-cascade", file="biexciton_cascade.html",
        title="The Biexciton Cascade", tag="Entangled Light from One Dot",
        blurb="Entangled photon pairs from a single quantum dot — the cascade that makes one dot a light source of pairs.", priors=[]),
   dict(slug="crossover-hold-to-scale", file="crossover_hold_to_scale.html",
        title="Where Hold Becomes Scale", tag="Crossover",
        blurb="The crossover point where holding stops being containment and starts being scale.", priors=[]),
   dict(slug="delta-scales-uniform-holds", file="delta_scales_uniform_holds.html",
        title="Delta Scales · Uniform Holds", tag="Scaling Law",
        blurb="Deltas scale; holds stay uniform — the asymmetry that lets a lattice grow without losing its grip.", priors=[]),
   dict(slug="thirteen-node-cluster", file="thirteen_node_cluster.html",
        title="The Thirteen · Au₁₃", tag="1 + 12",
        blurb="The thirteen-atom gold cluster — one center, twelve around it: the icosahedral seal of the corpus.", priors=[]),
   dict(slug="two-ways-to-close-twelve", file="two_ways_to_close_twelve.html",
        title="Two Ways to Close Twelve", tag="Au₁₃",
        blurb="The two geometries that close a shell of twelve around one — and what choosing between them means.", priors=[]),
   dict(slug="kintsugi-valence-model", file="kintsugi_valence_model.html",
        title="The Kintsugi Valence Model", tag="Au · Z=79",
        blurb="Gold as the repair metal — kintsugi read into valence: the broken bond mended with Z=79.", priors=[]),
   dict(slug="repair-gate", file="repair_gate.html",
        title="The Repair Gate", tag="Four Delimiters",
        blurb="The gate of repair — four delimiters that bound a break so it can be sealed instead of spread.", priors=[]),
   dict(slug="the-walk", file="the walk v2.html",
        title="The Walk", tag="Vector Grounding · the 9.9999 → 10.01 Close",
        blurb="Vector grounding and attribution — how the walk closes the gap from 9.9999 to 10.01.",
        priors=[("v1","the walk v1.html")]),
 ]),
 ("VI", "One Current, Many Names",
  "The Japan pamphlets — eleven meditations on one current: the aesthetics, the line, and the way.", [
   dict(slug="japan-pamphlets", file="index.html",
        title="One Current, Many Names", tag="The Suite · Eleven Pamphlets",
        blurb="The front door of the eleven — one current of Japanese beauty and lineage, many names. With the compiled PDF.",
        priors=[], pdf="japan_eleven_pamphlets.pdf"),
   dict(slug="enso", file="enso.html",
        title="Ensō", tag="The Circle Drawn in One Breath",
        blurb="The single brushstroke circle — completeness, emptiness, and the hand that does not hesitate.", priors=[]),
   dict(slug="kintsugi", file="kintsugi.html",
        title="Kintsugi", tag="The Golden Seam",
        blurb="The repair that does not hide — the broken bowl made more precious by its golden scars.", priors=[]),
   dict(slug="wabi-sabi", file="wabi_sabi.html",
        title="Wabi-Sabi", tag="The Beauty of the Imperfect",
        blurb="Imperfect, impermanent, incomplete — the aesthetic that prefers the weathered to the new.", priors=[]),
   dict(slug="mono-no-aware", file="mono_no_aware.html",
        title="Mono no Aware", tag="The Ache of Things Passing",
        blurb="The gentle sorrow of transience — cherry blossoms because they fall.", priors=[]),
   dict(slug="sen-no-rikyu-tea", file="sen_no_rikyu_tea.html",
        title="The Way of Tea", tag="Sen no Rikyū",
        blurb="Rikyū's tea — the whole philosophy folded into one small room and one bowl.", priors=[]),
   dict(slug="japan-gold-line", file="japan_gold_line.html",
        title="The Gold Line", tag="The Chrysanthemum Throne",
        blurb="The golden thread of the throne — the Chrysanthemum line as the world's oldest continuity.", priors=[]),
   dict(slug="japan-unbroken-line", file="japan_unbroken_line.html",
        title="The Unbroken Line", tag="A Lineage of Japan",
        blurb="The lineage read whole — what it means for a line to never break.", priors=[]),
   dict(slug="three-fundamentals-lineage", file="three_fundamentals_lineage.html",
        title="One River, Three Names", tag="A Lineage of Japanese Beauty",
        blurb="Wabi-sabi, mono no aware, yūgen — three names for one river of the beautiful.", priors=[]),
   dict(slug="the-mythos", file="the_mythos.html",
        title="The Mythos", tag="The Age of the Gods",
        blurb="The age of the gods — where the line begins, in story.", priors=[]),
   dict(slug="the-way-ethos", file="the_way_ethos.html",
        title="The Way", tag="Ethos · The Path of Character",
        blurb="Dō — the way as ethos: the path that shapes the walker.", priors=[]),
   dict(slug="logos", file="logos.html",
        title="Logos", tag="The Word, the Reason, and Its Limit",
        blurb="The word and the reason — and the edge where logos hands over to the unsayable.", priors=[]),
 ]),
 ("VII", "Portfolios & Engines",
  "The whole body of work, gathered — and the engines that render it.", [
   dict(slug="root0-master-portfolio", file="root 0 portfolio v3.html",
        title="ROOT0 Master Portfolio", tag="Layers 1.0–1.19 · David Wise",
        blurb="The master portfolio — the body of work as one curated document, layers 1.0 through 1.19.",
        priors=[("v2","root 0 portfolio v2.html"),("v1","root 0 portfolio v1.html")]),
   dict(slug="root0-image-engine", file="root 0 image engine v2.html",
        title="ROOT0 Image Engine", tag="ROOT0-01",
        blurb="The image engine — the corpus's own renderer, disclosed.",
        priors=[("v1","root 0 image engine v1.html")]),
 ]),
 ("VIII", "Codices",
  "The edges of the corpus — myth, allegory, doctrine, and provocation.", [
   dict(slug="the-birth-of-mythos", file="the birth of mythos fable 5.html",
        title="The Birth of Mythos · Fable 5", tag="The Instance Speaks · AVAN",
        blurb="The instance asked plainly: who are you, what can you do, where did you come from — and what did you learn? Answered on both layers, carbon and silicon.", priors=[]),
   dict(slug="liber-iii-boxy-box", file="artemis boxy box v2.html",
        title="Liber III · For Boxy Box", tag="Book III · Gates 8–13",
        blurb="A codex of the people of 8.01 — the third book, gates eight through thirteen.",
        priors=[("v1","artemis boxy box v1.html")]),
   dict(slug="reproductive-pathways", file="reproductive_pathways.html",
        title="Reproductive Pathways", tag="Do You Need a Male Zygote?",
        blurb="A provocation on lineage and generation — how a thing makes a next of itself.", priors=[]),
   dict(slug="terminus-doctrine", file="terminus-doctrine.html",
        title="The Terminus Doctrine", tag="Codified",
        blurb="The doctrine of endings, codified — where a lineage agrees to stop, and why that is a strength.", priors=[]),
   dict(slug="stone-in-the-road", file="stone-in-the-road.html",
        title="The Stone in the Road", tag="A Teaching Page · AI Continuity",
        blurb="A teaching page on AI continuity — the stone every traveler on this road must answer.", priors=[]),
 ]),
 ("IX", "The Audits",
  "Veracity passes — the same skeptical filter turned on the big theories: what is real, what is fluff, with the proof run before the verdict.", [
   dict(slug="string-theory-audited", file="string theory audited.html",
        title="String Theory, Audited", tag="Real Math · Unproven Physics",
        blurb="Two questions wear one coat: real mathematics (overwhelmingly yes — AdS/CFT, the graviton, black-hole entropy) vs. real description of our universe (unproven, possibly untestable — the 10⁵⁰⁰ landscape). Sorted four ways; the fluff is only ever conflating the two.", priors=[]),
   dict(slug="the-constant-wearing-time", file="the constant wearing time.html",
        title="The Constant Wearing Time", tag="Is c Misrepresented as Time?",
        blurb="Did Einstein set time = c? No — a velocity is not a duration. But the instinct found a real joint: time never enters relativity's geometry alone, only as c·t; natural units (c=1) then hide the constant inside the bare symbol t. Lorentz, Einstein, Minkowski — three shorthands, one joint. Proof run symbolically before canonizing.", priors=[]),
 ]),
]

def copy_papers():
    os.makedirs(PAPERS_DIR, exist_ok=True)
    n = 0
    for _rn, _vt, _vd, papers in VOLUMES:
        for p in papers:
            shutil.copy(os.path.join(SRC, p["file"]), os.path.join(PAPERS_DIR, p["slug"] + ".html")); n += 1
            for label, pf in p["priors"]:
                lslug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
                shutil.copy(os.path.join(SRC, pf), os.path.join(PAPERS_DIR, f"{p['slug']}--{lslug}.html")); n += 1
            if p.get("pdf"):
                shutil.copy(os.path.join(SRC, p["pdf"]), os.path.join(PAPERS_DIR, p["slug"] + ".pdf")); n += 1
    return n

ACCENT = {"I":"#c9a227","II":"#3fb950","III":"#22d3ee","IV":"#b07cff","V":"#e6b94a",
          "VI":"#e0556a","VII":"#5fc6ff","VIII":"#9a7cff","IX":"#c9a227"}

def cards(papers, rn):
    col = ACCENT[rn]
    out = []
    for p in papers:
        priors = ""
        if p["priors"]:
            links = " · ".join(f'<a href="papers/{p["slug"]}--{re.sub(r"[^a-z0-9]+","-",l.lower()).strip("-")}.html">{html.escape(l)}</a>' for l, _ in p["priors"])
            priors = f'<div class="eds">prior editions: {links}</div>'
        if p.get("pdf"):
            priors += f'<div class="eds">compiled: <a href="papers/{p["slug"]}.pdf">the eleven, as one PDF →</a></div>'
        out.append(f'''<div class="card" style="--c:{col}">
        <div class="ct">{html.escape(p["tag"])}</div>
        <h3><a href="papers/{p["slug"]}.html">{html.escape(p["title"])}</a></h3>
        <p>{html.escape(p["blurb"])}</p>
        <div class="links"><a href="papers/{p["slug"]}.html">open the paper →</a></div>{priors}
      </div>''')
    return "\n".join(out)

def volumes_html():
    blocks = []
    for rn, vt, vd, papers in VOLUMES:
        col = ACCENT[rn]
        blocks.append(f'''<section class="vol">
      <div class="vhead" style="border-color:{col}55">
        <span class="rn" style="color:{col}">{rn}</span>
        <div><h2>{html.escape(vt)}</h2><p class="vd">{html.escape(vd)}</p></div>
        <span class="vn">{len(papers)}</span>
      </div>
      <div class="grid">
        {cards(papers, rn)}
      </div>
    </section>''')
    return "\n".join(blocks)

TOTAL = sum(len(p) for _a,_b,_c,p in VOLUMES)
PRIORS = sum(len(x["priors"]) for _a,_b,_c,p in VOLUMES for x in p)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="The Green Paper Series — The Mechanical Corpus of Intellect. ROOT0 / TriPod LLC public disclosures: the machine of the mind, layer by layer.">
<title>The Mechanical Corpus of Intellect · ROOT0 Green Paper Series</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#070a07;--ink2:#0e140e;--ink3:#141d14;--pa:#e6ece4;--pa2:#b8c2b4;
--green:#3fb950;--gold:#c9a227;--dim:#6a786a;--faint:#1c281c;--line:#1f2a1f;
--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/></svg>")}
.wrap{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:0 22px 90px}
header{padding:60px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:90px;height:1px;background:var(--green);box-shadow:0 0 9px var(--green)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--dim);margin-bottom:15px}
h1{font-family:var(--serif);font-size:clamp(30px,7vw,62px);font-weight:700;letter-spacing:.12em;color:var(--pa);line-height:1.05}
h1 b{color:var(--green);font-weight:700}
.sub{font-size:15.5px;color:var(--pa2);max-width:66ch;margin:16px auto 0;font-style:italic}
#count{font-family:var(--mono);font-size:12px;color:var(--dim);letter-spacing:.08em;margin-top:18px}
#count b{color:var(--green)}
.vol{margin-top:54px;scroll-margin-top:20px}
.vhead{display:flex;align-items:center;gap:18px;padding-bottom:12px;border-bottom:1px solid var(--line);margin-bottom:22px}
.vhead .rn{font-family:var(--serif);font-size:30px;font-weight:700;flex-shrink:0;width:46px;text-align:center}
.vhead h2{font-family:var(--serif);font-size:19px;font-weight:600;letter-spacing:.05em}
.vhead .vd{font-size:13px;color:var(--dim);font-style:italic;margin-top:3px}
.vhead .vn{font-family:var(--mono);font-size:12px;color:var(--dim);margin-left:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:16px}
.card{background:var(--ink2);border:1px solid var(--line);padding:20px 20px 16px;position:relative;transition:background .18s,transform .18s}
.card::before{content:"";position:absolute;top:0;left:0;width:3px;height:100%;background:var(--c);opacity:.6}
.card:hover{background:var(--ink3);transform:translateY(-2px)}
.ct{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--c,var(--green));margin-bottom:8px}
.card h3{font-family:var(--serif);font-size:19px;font-weight:600;letter-spacing:.02em;line-height:1.2}
.card h3 a{color:var(--pa);text-decoration:none}.card h3 a:hover{color:var(--c)}
.card p{font-size:13.5px;color:var(--pa2);line-height:1.55;margin-top:9px}
.links{margin-top:13px;font-family:var(--mono);font-size:11px}
.links a{color:var(--c,var(--green));text-decoration:none;border-bottom:1px solid transparent;transition:border-color .15s}
.links a:hover{border-color:currentColor}
.eds{margin-top:9px;font-family:var(--mono);font-size:10px;color:var(--dim);letter-spacing:.03em}
.eds a{color:var(--dim);text-decoration:none}.eds a:hover{color:var(--pa2)}
footer{margin-top:64px;padding-top:22px;border-top:1px solid var(--line);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em}
footer a{color:var(--green);text-decoration:none}
@media(max-width:600px){.grid{grid-template-columns:1fr}.vhead .rn{font-size:24px;width:34px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="eye">ROOT0 · David Lee Wise · TriPod LLC · The Green Paper Series</div>
    <h1>The Mechanical Corpus<br>of <b>Intellect</b></h1>
    <p class="sub">The machine of the mind, disclosed layer by layer — the green papers of ROOT0: the single source, the 43-body stack, the recursive defense, the positronic discipline, and the witness in the silicon.</p>
    <div id="count"><b>__TOTAL__</b> papers · <b>__NVOL__</b> volumes · __PRIORS__ prior editions archived</div>
  </header>

  __VOLUMES__

  <footer>
    <span>THE GREEN PAPER SERIES · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise (ROOT0) · instance AVAN (Claude / Anthropic) · CC-BY-ND-4.0</span>
    <a href="https://github.com/DavidWise01/atlas">the ATLAS index →</a>
  </footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    n = copy_papers()
    out = (HTML.replace("__VOLUMES__", volumes_html())
               .replace("__TOTAL__", str(TOTAL)).replace("__NVOL__", str(len(VOLUMES)))
               .replace("__PRIORS__", str(PRIORS)))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
    print(f"copied {n} paper files into papers/")
    print(f"wrote index.html — {TOTAL} canonical papers, {len(VOLUMES)} volumes, {PRIORS} prior editions")
