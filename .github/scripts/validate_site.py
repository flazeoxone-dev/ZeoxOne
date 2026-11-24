#!/usr/bin/env python3
"""Contrôles statiques de publication pour ZeoxOne (sans dépendance externe)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://flazeoxone-dev.github.io/ZeoxOne"
errors = []

def fail(message):
    errors.append(message)

class PageInspector(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.lang = None
        self.title_open = False
        self.title_text = ""
        self.has_description = False
        self.ids = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "title":
            self.title_open = True
        if tag == "meta" and attrs.get("name", "").lower() == "description":
            self.has_description = bool(attrs.get("content", "").strip())
        if attrs.get("id"):
            ident = attrs["id"]
            if ident in self.ids:
                fail(f"{self.path}: identifiant HTML dupliqué: {ident}")
            self.ids.add(ident)
        for attr in ("href", "src"):
            value = attrs.get(attr, "").strip()
            if value:
                self.links.append(value)
    def handle_endtag(self, tag):
        if tag == "title":
            self.title_open = False
    def handle_data(self, data):
        if self.title_open:
            self.title_text += data

def check_local_target(page, raw):
    if raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return
    parsed = urlparse(raw)
    if parsed.scheme or parsed.netloc:
        if parsed.netloc and parsed.netloc != "flazeoxone-dev.github.io":
            return
        raw_path = parsed.path
        prefix = "/ZeoxOne/"
        if not raw_path.startswith(prefix):
            return
        target = (ROOT / raw_path[len(prefix):]).resolve()
    elif parsed.path.startswith("/ZeoxOne/"):
        target = (ROOT / parsed.path[len("/ZeoxOne/"):]).resolve()
    elif parsed.path.startswith("/"):
        return
    else:
        target = (page.parent / parsed.path).resolve()
    if not parsed.path:
        return
    try:
        target.relative_to(ROOT)
    except ValueError:
        fail(f"{page.relative_to(ROOT)}: chemin sortant du site: {raw}")
        return
    if target.is_dir():
        target = target / "index.html"
    if not target.exists():
        fail(f"{page.relative_to(ROOT)}: lien ou ressource introuvable: {raw}")

# JSON catalogue
catalogue_path = ROOT / "articles.json"
try:
    articles = json.loads(catalogue_path.read_text(encoding="utf-8"))
    if not isinstance(articles, list):
        fail("articles.json doit contenir une liste.")
    for article in articles:
        for key in ("title", "description", "category", "url", "date"):
            if not article.get(key):
                fail(f"articles.json: champ obligatoire absent ({key}) dans {article.get('title', 'article sans titre')}.")
        if article.get("url") and not (ROOT / article["url"]).is_file():
            fail(f"articles.json: fichier d'article introuvable: {article['url']}")
except Exception as exc:
    articles = []
    fail(f"articles.json invalide: {exc}")

# Sitemap XML
try:
    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {node.text for node in sitemap.findall("sm:url/sm:loc", ns)}
    for article in articles:
        expected = BASE + "/" + article.get("url", "").lstrip("/")
        if expected not in sitemap_urls:
            fail(f"sitemap.xml: URL d'article absente: {expected}")
except Exception as exc:
    fail(f"sitemap.xml invalide: {exc}")

# HTML structure minimale + liens locaux
for page in ROOT.rglob("*.html"):
    if any(part.startswith(".") for part in page.relative_to(ROOT).parts):
        continue
    try:
        parser = PageInspector(page)
        parser.feed(page.read_text(encoding="utf-8"))
        # Pages techniques d'authentification et page 404 : contrôles SEO adaptés.
        technical = page.name in {"404.html", "google9787bf245aba8089.html"}
        if not technical and not parser.lang:
            fail(f"{page.relative_to(ROOT)}: attribut lang manquant sur <html>.")
        if not technical and not parser.title_text.strip():
            fail(f"{page.relative_to(ROOT)}: titre <title> absent ou vide.")
        if not technical and not parser.has_description:
            fail(f"{page.relative_to(ROOT)}: méta-description absente ou vide.")
        for link in parser.links:
            check_local_target(page, link)
    except Exception as exc:
        fail(f"{page.relative_to(ROOT)}: erreur de lecture HTML: {exc}")

if errors:
    print("ÉCHEC DES CONTRÔLES ZEOXONE")
    for error in errors:
        print(" - " + error)
    sys.exit(1)

print(f"Contrôles réussis : {len(articles)} articles référencés et pages HTML vérifiées.")
