"""Build notebook.pdf (the printed team notebook). Run from anywhere:
    python3 notebook/build_pdf.py
Needs pandoc (for the .md pages) and Node Playwright + Chromium (for HTML -> PDF).
Self-test blocks (everything after `if __name__ == "__main__":`) are left out of the print.
"""
import html
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = [
    ("Index: constraints, keywords, traps", "index.md"),
    ("Template", "template.py"),
    ("Python standard library", "python_stdlib.md"),
    ("Greedy + techniques", "techniques.py"),
    ("Data structures", "data_structures.py"),
    ("Math", "math_nt.py"),
    ("Geometry", "geometry.py"),
    ("Graphs", "graphs.py"),
    ("DP", "dp.py"),
    ("Strings", "strings.py"),
]

CSS = """
@page { size: Letter landscape; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 8pt; line-height: 1.22;
       columns: 2; column-gap: 0.3in; column-rule: 0.5pt solid #bbb; color: #000; }
h1 { column-span: all; font-size: 13pt; margin: 0 0 4pt; }
h2.page { font-size: 10.5pt; background: #222; color: #fff; padding: 2pt 5pt; margin: 8pt 0 4pt;
          break-after: avoid; }
h1, h2, h3 { break-after: avoid; }
h2:not(.page), h3 { font-size: 9pt; margin: 6pt 0 2pt; }
pre, code { font-family: 'DejaVu Sans Mono', 'Courier New', monospace; font-size: 7pt; }
pre { white-space: pre-wrap; margin: 2pt 0; line-height: 1.2; }
pre.src { border-left: 2pt solid #222; padding-left: 4pt; }
table { border-collapse: collapse; font-size: 7.6pt; margin: 3pt 0; width: 100%; }
td, th { border: 0.5pt solid #999; padding: 1pt 3pt; vertical-align: top; text-align: left; }
p, ul, ol { margin: 2pt 0; } ul, ol { padding-left: 14pt; }
.toc { column-span: all; font-size: 8.4pt; margin-bottom: 4pt; }
"""


def code_page(path):
    src = open(path).read()
    cut = src.find('\nif __name__ == "__main__":')
    if cut >= 0:
        src = src[:cut].rstrip() + "\n"
    return '<pre class="src">' + html.escape(src) + "</pre>"


def md_page(path):
    out = subprocess.run(["pandoc", "-f", "gfm", "-t", "html", path],
                         capture_output=True, text=True, check=True).stdout
    import re
    return re.sub(r"<h1[^>]*>.*?</h1>", "", out, count=1, flags=re.S)   # page header replaces it


def build():
    parts = ["<h1>Team notebook: Tyler / Hugo / Edwin</h1>",
             '<div class="toc">' + " &middot; ".join(f"{i+1}. {t}" for i, (t, _) in enumerate(PAGES)) + "</div>"]
    for i, (title, f) in enumerate(PAGES):
        p = os.path.join(HERE, f)
        parts.append(f'<h2 class="page">{i+1}. {html.escape(title)} <small>({f})</small></h2>')
        parts.append(md_page(p) if f.endswith(".md") else code_page(p))
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"
    out_html = os.path.join(HERE, "notebook.html")
    open(out_html, "w").write(doc)
    # HTML -> PDF with Node Playwright (works with the preinstalled Chromium)
    js = """
const { chromium } = require('playwright');
(async () => {
  let b; try { b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); }
  catch (e) { b = await chromium.launch(); }
  const p = await b.newPage();
  await p.goto('file://' + process.argv[1]);
  await p.pdf({ path: process.argv[2], format: 'Letter', landscape: true, printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: "<div style='font-size:7pt;width:100%;text-align:center'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
    margin: { top: '0.4in', bottom: '0.45in', left: '0.4in', right: '0.4in' } });
  await b.close();
})();
"""
    env = dict(os.environ)
    if not env.get("NODE_PATH"):
        env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", "-e", js, out_html, os.path.join(HERE, "notebook.pdf")], check=True, env=env)
    print("wrote notebook.pdf")


if __name__ == "__main__":
    build()
