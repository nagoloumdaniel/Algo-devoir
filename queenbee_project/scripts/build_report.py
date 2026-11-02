"""Génère le compte rendu PDF unique du binôme (HTML -> PDF via Playwright/Chromium).

    python scripts/build_report.py

Sorties : docs/Compte_Rendu_QueenBee_Dijkstra.pdf (+ docs/rapport.html)
"""

import base64
import html
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from markdown_it import MarkdownIt
from playwright.sync_api import sync_playwright
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_PDF = DOCS / "Compte_Rendu_QueenBee_Dijkstra.pdf"
FONTS = ROOT / "assets" / "fonts"


def font_face(family, weight, file, fmt):
    data = base64.b64encode((FONTS / file).read_bytes()).decode()
    return (f"@font-face {{ font-family: '{family}'; font-weight: {weight}; "
            f"src: url(data:font/{fmt};base64,{data}) format('{fmt}'); }}\n")


FONT_CSS = (font_face("Inter", 400, "Inter-400.woff2", "woff2") + font_face("Inter", 600, "Inter-600.woff2", "woff2")
            + font_face("Inter", 700, "Inter-700.woff2", "woff2") + font_face("Poppins", 500, "Poppins-Medium.ttf", "truetype")
            + font_face("Poppins", 700, "Poppins-Bold.ttf", "truetype"))

MEMBERS = [("Daniel Nagoloum TALLA", "Tests E2E, captures, rapport PDF, dépôt GitHub"),
           ("Wissam AIT EL HADI", "Algorithme, tas binaire, API, tests unitaires, benchmark")]
GITHUB = "https://github.com/nagoloumdaniel/Algo-devoir"


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def code_block(path, title):
    src = (ROOT / path).read_text(encoding="utf-8")
    body = highlight(src, PythonLexer(), HtmlFormatter(linenos="inline", cssclass="hl"))
    return (f"<h3>{html.escape(title)} <small><code>{path}</code> "
            f"({src.count(chr(10)) + 1} lignes)</small></h3>{body}")


def img(path, caption, width="100%"):
    data = base64.b64encode((ROOT / path).read_bytes()).decode()
    return (f'<figure><img src="data:image/png;base64,{data}" style="width:{width}">'
            f"<figcaption>{html.escape(caption)}</figcaption></figure>")


def analysis_html():
    md = (DOCS / "analyse_complexite.md").read_text(encoding="utf-8")
    md = md.split("\n", 1)[1]  # le titre est repris dans la page
    md = re.sub(r"!\[([^\]]*)\]\((benchmark/[^)]+)\)", lambda m: "@@IMG:" + m.group(2) + "|" + m.group(1) + "@@", md)
    out = MarkdownIt("commonmark").enable("table").render(md)

    def repl(m):
        p, cap = m.group(1).split("|", 1)
        return img("docs/" + p, "Figure : " + cap, "92%")

    out = re.sub(r"<p>@@IMG:(.*?)@@</p>", repl, out)
    return out.replace("<h2>", "<h3>").replace("</h2>", "</h3>")


CAPTURES = [
    ("docs/captures/01_swagger_documentation_endpoint.png", "Documentation OpenAPI : endpoint POST /api/v1/routing/emergency-path exposé dans Swagger UI."),
    ("docs/captures/02_swagger_requete_nominale_200_succes.png", "Requête nominale C01 vers H07 : HTTP 200, coût 17,5 min, chemin BASE_NORD, J1, J2, J3, J4, H07, temps de calcul en ms."),
    ("docs/captures/03_swagger_ruche_inexistante_404.png", "Ruche inexistante H99 : HTTP 404."),
    ("docs/captures/04_swagger_identifiant_invalide_422.png", "Identifiant mal formé « ZZZ » : validation Pydantic, HTTP 422."),
    ("docs/captures/05_swagger_ruche_isolee_aucun_itineraire.png", "Ruche isolée H13 (graphe non connexe) : HTTP 200, status « error », chemin vide, coût null."),
    ("docs/captures/06_swagger_schemas_pydantic.png", "Schémas Pydantic d'entrée et de sortie documentés."),
    ("docs/captures/07_openapi_json_contrat_api.png", "Contrat OpenAPI brut (/openapi.json)."),
]

TASKS_W = [
    ("T-W1, T-W2", "Dijkstra avec tas binaire (BinaryHeap codé de zéro : heapify, insert, extract_min, redimensionnement)", "src/min_heap.py, src/dijkstra.py"),
    ("T-W3, T-W4", "Reconstitution du chemin optimal, coût cumulé, format « X min Y sec »", "src/dijkstra.py"),
    ("T-W5 à T-W7", "Endpoint REST, schémas Pydantic d'entrée et de sortie, graphe du site, service de routage", "src/api.py, src/routing_service.py, src/site_graph.py"),
    ("T-W9, T-W10", "Tests pytest : cas normaux et cas limites (55 tests)", "tests/"),
    ("T-W11 à T-W14", "Version naïve O(|V|²), benchmark, note de complexité", "src/benchmark.py, docs/analyse_complexite.md"),
]
TASKS_D = [
    ("T-D1 à T-D4", "Architecture API : endpoint, modèles, validation des identifiants, routage URL", "Relue et validée ; chaque comportement est vérifié de bout en bout (E2E, section 4)."),
    ("T-D5 à T-D7", "Intégration de Dijkstra, gestion des erreurs, format JSON", "Vérifiées par les tests E2E : 200, 404, 422, 405, ruche isolée (status « error »)."),
    ("T-D8 (API)", "Documentation OpenAPI", "Vérifiée dans Swagger UI par Playwright, captures nommées (section 4)."),
    ("T-D8 à T-D11", "Benchmarks, graphiques, note de complexité, analyse des résultats", "Données, graphiques et note relus et intégrés au rapport (section 5)."),
    ("T-D12, T-D13", "Mise en page du PDF unique, taille < 5 Mo", "Rapport généré par scripts/build_report.py (taille vérifiée à chaque génération)."),
    ("T-D15", "Traçabilité noms et prénoms", "Page de garde avec les noms des deux membres du binôme."),
    ("T-D14", "Dépôt sur Pronote", "À faire par chaque étudiant avant le 05/11/2026 (action manuelle)."),
]

CSS = """
* { box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1f2430; }
h1, h2, h3, th, .cover .sub { font-family: 'Poppins', 'Inter', sans-serif; }
h1 { font-weight: 700; font-size: 21pt; color: #7a4b00; border-bottom: 3px solid #f2a900; padding-bottom: 5px; margin-top: 0; }
h2 { font-size: 15pt; color: #7a4b00; margin-top: 18px; }
h3 { font-size: 12pt; color: #333; margin-top: 16px; }
h3 small { font-weight: normal; color: #666; font-size: 9pt; }
section.page { break-before: page; }
code, pre { font-family: Consolas, 'Courier New', monospace; }
code { background: #f4efe3; padding: 0 3px; border-radius: 3px; font-size: 9pt; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9pt; break-inside: avoid; }
th { background: #f2a900; color: #fff; text-align: left; padding: 4px 6px; }
td { border-bottom: 1px solid #e3dccb; padding: 3px 6px; vertical-align: top; }
.hl { background: #fbfaf6; border: 1px solid #e3dccb; border-radius: 4px; padding: 6px; font-size: 7.4pt; line-height: 1.3; }
.hl pre { margin: 0; white-space: pre-wrap; word-break: break-word; }
.hl .linenos { color: #aaa; padding-right: 8px; user-select: none; }
pre.out { background: #1e2230; color: #d6e2ff; padding: 8px; border-radius: 4px; font-size: 6.9pt; line-height: 1.25; white-space: pre-wrap; }
figure { margin: 10px 0; text-align: center; break-inside: avoid; }
figure img { border: 1px solid #ccc; border-radius: 4px; }
figcaption { font-size: 8.5pt; color: #555; font-style: italic; margin-top: 3px; }
.cover { text-align: center; padding-top: 60px; }
.cover h1 { border: none; font-size: 28pt; margin-bottom: 4px; }
.cover .sub { font-size: 14pt; color: #444; margin-bottom: 40px; }
.cover .box { display: inline-block; text-align: left; border: 2px solid #f2a900; border-radius: 8px; padding: 14px 30px; margin: 10px 0; }
.cover .meta { margin-top: 40px; color: #555; font-size: 10pt; }
.ok { color: #1b7f3b; font-weight: bold; }
"""


def build_html():
    unit = run([sys.executable, "-m", "pytest", "tests", "--ignore=tests/e2e", "-v", "--no-header", "-p", "no:warnings"])
    e2e = run([sys.executable, "-m", "pytest", "tests/e2e", "-v", "--no-header", "-p", "no:warnings"])
    unit_sum = unit.strip().splitlines()[-1].strip("= ")
    e2e_sum = e2e.strip().splitlines()[-1].strip("= ")
    clean = lambda s: html.escape("\n".join(l for l in s.splitlines() if l.strip()))
    hl_css = HtmlFormatter(style="friendly", cssclass="hl").get_style_defs(".hl")
    members_li = "".join(f"<li><b>{n}</b> : {r}</li>" for n, r in MEMBERS)
    rows_w = "".join(f"<tr><td>{a}</td><td>{b}</td><td><code>{c}</code></td></tr>" for a, b, c in TASKS_W)
    rows_d = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in TASKS_D)
    names_li = "".join(f'<li style="font-size:14pt">{n}</li>' for n, _ in MEMBERS)

    p = [f"<html><head><meta charset='utf-8'><style>{FONT_CSS}{CSS}{hl_css}</style></head><body>"]

    p.append(f"""
<section class="cover">
  <h1>Projet QueenBee : Algorithme de Dijkstra</h1>
  <div class="sub">Plus court chemin à source unique, interventions d'urgence (UC-C01)</div>
  <div class="box"><b>Membres du groupe (binôme)</b><ul>{names_li}</ul></div>
  <div class="meta">
    <p><b>Spécialité :</b> Développement / DevOps<br>
    <b>Formation :</b> Mastère 1 INGETIS / ITIS, application fil rouge QueenBee<br>
    <b>Évaluation :</b> Algorithmique (sujet B : Dijkstra, file de priorité / tas binaire)<br>
    <b>Date de rendu :</b> 05/11/2026 (Pronote), document généré le {date.today().strftime('%d/%m/%Y')}<br>
    <b>Dépôt :</b> {GITHUB}</p>
  </div>
</section>""")

    p.append(f"""
<section class="page"><h1>Compte rendu</h1>
<h2>1. Contexte et objectif</h2>
<p>Le projet QueenBee déploie un réseau apicole connecté (8 sites, 3 pays, 400 ruches). Quand une ruche déclenche
une alerte critique, le coordinateur régional doit la rejoindre au plus vite. Nous avons implémenté Dijkstra
<b>sans aucune bibliothèque de graphes</b>, avec un <b>tas binaire (min-heap)</b> codé à la main, puis nous l'avons exposé
dans le backend sous la forme de l'endpoint <code>POST /api/v1/routing/emergency-path</code>.</p>
<h2>2. Membres du groupe et répartition</h2><ul>{members_li}</ul>
<h3>Tâches réalisées par Wissam AIT EL HADI</h3>
<table><tr><th>Tâches</th><th>Contenu</th><th>Fichiers</th></tr>{rows_w}</table>
<h3>Tâches réalisées par Daniel Nagoloum TALLA</h3>
<table><tr><th>Tâches</th><th>Contenu</th><th>Réalisation</th></tr>{rows_d}</table>
<p>Daniel a de plus ajouté les <b>tests E2E Playwright</b> (8 tests, 7 captures d'écran) et corrigé le <code>.gitignore</code>
(encodage cassé, fichiers <code>__pycache__</code> suivis par git).</p>
<h2>3. Checklist du sujet</h2>
<table><tr><th>Exigence</th><th>Statut</th><th>Preuve</th></tr>
<tr><td>Dijkstra avec min-heap (sans bibliothèque de graphes)</td><td class="ok">Fait</td><td>src/min_heap.py, src/dijkstra.py</td></tr>
<tr><td>Reconstitution du chemin, coût cumulé</td><td class="ok">Fait</td><td>reconstruct_path, path_cost, format_duration</td></tr>
<tr><td>Cas limites (non connexe, cycles, source = cible, vide, un seul nœud)</td><td class="ok">Fait</td><td>tests/test_dijkstra.py</td></tr>
<tr><td>Endpoint REST, sortie JSON (coût, chemin, temps de calcul)</td><td class="ok">Fait</td><td>src/api.py, captures E2E</td></tr>
<tr><td>Version naïve O(|V|²) et benchmark comparatif</td><td class="ok">Fait</td><td>src/benchmark.py, section 5</td></tr>
<tr><td>Complexité formalisée O((|V|+|E|) log |V|)</td><td class="ok">Fait</td><td>section 5</td></tr>
<tr><td>Tests unitaires et E2E passants</td><td class="ok">Fait</td><td>{html.escape(unit_sum)} ; {html.escape(e2e_sum)}</td></tr>
<tr><td>PDF unique &lt; 5 Mo</td><td class="ok">Fait</td><td>ce document</td></tr>
<tr><td>Dépôt Pronote par les deux étudiants</td><td>À faire</td><td>avant le 05/11/2026</td></tr></table>
</section>""")

    p.append("<section class=\"page\"><h1>3. Implémentation de l'algorithme (code source)</h1>"
             "<p>Code complet et commenté. Aucune bibliothèque de graphes n'est utilisée : seule la bibliothèque standard "
             "Python est employée pour l'algorithme ; FastAPI et Pydantic servent uniquement à la couche REST.</p>")
    p.append(code_block("src/min_heap.py", "Structure de données : tas binaire (min-heap)"))
    p.append(code_block("src/dijkstra.py", "Dijkstra avec tas, version naïve, reconstitution du chemin"))
    p.append(code_block("src/site_graph.py", "Graphe de démonstration du site (pistes et accès)"))
    p.append(code_block("src/routing_service.py", "Service de routage d'urgence"))
    p.append(code_block("src/api.py", "API REST FastAPI"))
    p.append("</section>")

    p.append("<section class=\"page\"><h1>4. Jeux de tests et résultats</h1><h2>4.1 Tests unitaires (pytest)</h2>"
             f'<p>Résultat : <span class="ok">{html.escape(unit_sum)}</span>. Cas normaux, cas limites (graphe non connexe, '
             "cycles, source = cible, graphe vide, graphe à un seul nœud), reconstitution du chemin, coût total, "
             "cohérence tas / version naïve, tas binaire, service et API.</p>")
    p.append(f'<pre class="out">{clean(unit)}</pre>')
    for path, t in [("tests/test_dijkstra.py", "Tests de Dijkstra"), ("tests/test_min_heap.py", "Tests du tas binaire"),
                    ("tests/test_routing_service.py", "Tests du service de routage"), ("tests/test_api.py", "Tests de l'API")]:
        p.append(code_block(path, t))
    p.append("<h2>4.2 Tests E2E (Playwright)</h2>"
             "<p>Un vrai serveur uvicorn est lancé et un navigateur Chromium pilote Swagger UI. Résultat : "
             f'<span class="ok">{html.escape(e2e_sum)}</span>. Chaque test vérifie le code HTTP et le contenu de la réponse, '
             "puis enregistre une capture nommée.</p>")
    p.append(f'<pre class="out">{clean(e2e)}</pre>')
    p.append(code_block("tests/e2e/test_e2e_playwright.py", "Code des tests E2E"))
    p.append("<h2>4.3 Captures d'écran des tests E2E</h2>")
    for path, c in CAPTURES:
        p.append(img(path, f"{Path(path).name} : {c}", "88%"))
    p.append("</section>")

    p.append("<section class=\"page\"><h1>5. Note d'analyse de complexité</h1>" + analysis_html() + "</section>")
    p.append("</body></html>")
    return "\n".join(p)


def main():
    html_text = build_html()
    (DOCS / "rapport.html").write_text(html_text, encoding="utf-8")
    footer = ("<div style='font-family:Inter,sans-serif;font-size:8px;width:100%;text-align:center;color:#777'>"
              "QueenBee | Dijkstra | Daniel Nagoloum TALLA &amp; Wissam AIT EL HADI | page "
              "<span class='pageNumber'></span>/<span class='totalPages'></span></div>")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.set_content(html_text, wait_until="load")
        page.pdf(path=str(OUT_PDF), format="A4", print_background=True, display_header_footer=True,
                 header_template="<span></span>", footer_template=footer,
                 margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
        browser.close()
    size = OUT_PDF.stat().st_size / 1e6
    print(f"{OUT_PDF} : {size:.2f} Mo")
    assert size < 5, "PDF > 5 Mo"


if __name__ == "__main__":
    main()
