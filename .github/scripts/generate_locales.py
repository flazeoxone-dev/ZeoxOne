#!/usr/bin/env python3
"""Génère les versions FR/EN/ES/DE de ZeoxOne avec DeepL API Free.

Les sources françaises restent la référence éditoriale. Les traductions sont
créées avant publication, conservées dans des répertoires statiques et contrôlées
par le workflow qualité. Aucune clé API n'est intégrée au site public.
"""
from __future__ import annotations
import copy
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from html import escape as html_escape, unescape as html_unescape
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://flazeoxone-dev.github.io/ZeoxOne"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"
LOCALES = {
    "en": {"target": "EN-GB", "hreflang": "en-GB", "market": "Market note: prices and availability mentioned in this guide refer to France unless stated otherwise. Check official local retailers before buying."},
    "es": {"target": "ES", "hreflang": "es-ES", "market": "Nota de mercado: salvo que se indique lo contrario, los precios y la disponibilidad de esta guía corresponden a Francia. Comprueba las tiendas oficiales de tu país antes de comprar."},
    "de": {"target": "DE", "hreflang": "de-DE", "market": "Markthinweis: Sofern nicht anders angegeben, beziehen sich Preise und Verfügbarkeit in diesem Ratgeber auf Frankreich. Prüfe vor dem Kauf die offiziellen Händler in deinem Land."},
}
FR_MARKET = "Note de marché : les prix et disponibilités mentionnés dans ce guide correspondent au marché français, sauf indication contraire."
SKIP = {"404.html", "google9787bf245aba8089.html"}
HTML_FILES = [
    "index.html", "articles.html", "recommandations.html", "a-propos.html",
    "feedback.html", "mentions-legales.html", "politique-confidentialite.html",
    "methodologie-editoriale.html",
    "articles/choisir-composants-pc.html",
    "articles/gta-6-quelle-console-ps5-ps5-pro-xbox.html",
    "articles/outils-windows.html",
    "articles/performances-jeux-pc.html",
]
LOCALE_TEXT = {
    "fr": {"language":"Langue","suggest":"La langue de ton navigateur semble différente. Souhaites-tu consulter cette page dans cette langue ?","market_legal":"Cette traduction est fournie à titre informatif. En cas de différence, la version française fait foi jusqu'à une relecture juridique locale.","market":FR_MARKET,"fallback":"Certaines parties restent en français, car leur traduction automatique n'a pas pu être vérifiée.","close":"Fermer"},
    "en": {"language":"Language","suggest":"Your browser language seems to be different. Would you like to view this page in that language?","market_legal":"This translation is provided for information. If anything differs, the French version remains authoritative until a local legal review.","market":LOCALES["en"]["market"],"fallback":"Some sections remain in French because their automatic translation could not be verified.","close":"Close"},
    "es": {"language":"Idioma","suggest":"El idioma de tu navegador parece ser diferente. ¿Quieres consultar esta página en ese idioma?","market_legal":"Esta traducción se ofrece a título informativo. Si existe alguna diferencia, prevalece la versión francesa hasta que se realice una revisión jurídica local.","market":LOCALES["es"]["market"],"fallback":"Algunas secciones permanecen en francés porque no se pudo verificar su traducción automática.","close":"Cerrar"},
    "de": {"language":"Sprache","suggest":"Die Sprache deines Browsers scheint eine andere zu sein. Möchtest du diese Seite in dieser Sprache ansehen?","market_legal":"Diese Übersetzung dient nur zu Informationszwecken. Bei Abweichungen ist bis zu einer lokalen rechtlichen Prüfung die französische Fassung maßgeblich.","market":LOCALES["de"]["market"],"fallback":"Einige Abschnitte bleiben auf Französisch, da ihre automatische Übersetzung nicht überprüft werden konnte.","close":"Schließen"},
}

def deepl_translate(text: str, target: str, key: str) -> str:
    payload = urllib.parse.urlencode({
        "text": text,
        "source_lang": "FR",
        "target_lang": target,
        "tag_handling": "html",
        "ignore_tags": "script,style,code,pre,svg",
        "preserve_formatting": "1",
        "outline_detection": "0",
    }).encode("utf-8")
    request = urllib.request.Request(
        DEEPL_URL, data=payload,
        headers={"Authorization": "DeepL-Auth-Key " + key,
                 "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["translations"][0]["text"]

def page_rel(path: str) -> str:
    return path

def add_hreflang(html: str, source_path: str) -> str:
    canonical = BASE + ("/" if source_path == "index.html" else "/" + source_path)
    localized = lambda code: BASE + "/" + code + ("/" if source_path == "index.html" else "/" + source_path)
    tags = [
        f'<link rel="alternate" hreflang="fr-FR" href="{canonical}">',
        *[f'<link rel="alternate" hreflang="{v["hreflang"]}" href="{localized(k)}">' for k,v in LOCALES.items()],
        f'<link rel="alternate" hreflang="x-default" href="{canonical}">',
    ]
    block = "\n  " + "\n  ".join(tags) + "\n"
    if re.search(r'rel=["\']alternate["\']\s+hreflang=', html, re.I):
        html = re.sub(r'\s*<link rel=["\']alternate["\']\s+hreflang=["\'][^>]+>\s*', "\n", html, flags=re.I)
    return re.sub(r"</head>", block + "</head>", html, count=1, flags=re.I)

def rewrite_local_paths(html: str, locale: str, nested: bool) -> str:
    depth = "../../" if nested else "../"
    # Shared assets and scripts live at the repository root.
    for attr in ("href", "src"):
        html = re.sub(rf'({attr}=["\'])assets/', rf'\g<1>{depth}assets/', html)
        html = re.sub(rf'({attr}=["\'])\.\./assets/', rf'\g<1>{depth}assets/', html)
        html = re.sub(rf'({attr}=["\'])styles\.css', rf'\g<1>{depth}styles.css', html)
        html = re.sub(rf'({attr}=["\'])\.\./styles\.css', rf'\g<1>{depth}styles.css', html)
        html = re.sub(rf'({attr}=["\'])script\.js', rf'\g<1>{depth}script.js', html)
        html = re.sub(rf'({attr}=["\'])\.\./script\.js', rf'\g<1>{depth}script.js', html)
    # Site-absolute internal links are routed into the selected language.
    html = html.replace(BASE + "/", BASE + "/" + locale + "/")
    html = html.replace('href="/ZeoxOne/', f'href="/ZeoxOne/{locale}/')
    html = html.replace('src="/ZeoxOne/', f'src="/ZeoxOne/{locale}/')
    return html

def language_switcher(locale: str, source_path: str) -> str:
    links = []
    for code, label in (("fr","FR"),("en","EN"),("es","ES"),("de","DE")):
        suffix = "" if source_path == "index.html" else source_path
        href = f"/ZeoxOne/{code}/" + suffix
        current = ' aria-current="page"' if code == locale else ""
        links.append(f'<a href="{href}" lang="{LOCALE_TEXT[code].get("hreflang", code)}"{current}>{label}</a>')
    return '<nav class="locale-switcher" aria-label="' + LOCALE_TEXT[locale]["language"] + '">' + "".join(links) + "</nav>"

def clean_language_ui(html: str) -> str:
    html = re.sub(r'<nav class=["\']locale-switcher["\'][^>]*>.*?</nav>', "", html, flags=re.I|re.S)
    html = re.sub(r'<!-- ZEOXONE_LANGUAGE_SUGGESTION_START -->.*?<!-- ZEOXONE_LANGUAGE_SUGGESTION_END -->', "", html, flags=re.I|re.S)
    html = re.sub(r'\s*<link rel=["\']alternate["\']\s+hreflang=["\'][^>]+>', "", html, flags=re.I)
    return html

def inject_language_ui(html: str, locale: str, source_path: str) -> str:
    switch = language_switcher(locale, source_path)
    # Replace the old two-state switch or an existing selector.
    html, count = re.subn(r'<nav class=["\']locale-switcher["\'][^>]*>.*?</nav>', switch, html, count=1, flags=re.I|re.S)
    if not count:
        html, count = re.subn(r'<button[^>]*id=["\']langSwitch["\'][^>]*>.*?</button>', switch, html, count=1, flags=re.I|re.S)
    if not count:
        html = re.sub(r"</header>", switch + "</header>", html, count=1, flags=re.I)
    suggestion = f'''
  <aside class="language-suggestion" id="languageSuggestion" hidden aria-live="polite">
    <span>{LOCALE_TEXT[locale]["suggest"]}</span>
    <span id="languageSuggestionLinks"></span>
    <button type="button" id="dismissLanguageSuggestion" aria-label="{LOCALE_TEXT[locale]["close"]}">×</button>
  </aside>
  <script>
  (function(){{
    var supported=["fr","en","es","de"], current="{locale}";
    var browser=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||""]).map(function(x){{return (x||"").slice(0,2).toLowerCase()}});
    var stored=null;
    try{{if(localStorage.getItem("zeoxone-preferences-consent")==="yes")stored=localStorage.getItem("zeoxone-lang")}}catch(e){{}}
    var wanted=(stored&&supported.indexOf(stored)>=0)?stored:browser.find(function(x){{return supported.indexOf(x)>=0}});
    if(wanted&&wanted!==current){{
      var box=document.getElementById("languageSuggestion"),slot=document.getElementById("languageSuggestionLinks");
      var a=document.createElement("a");a.href="/ZeoxOne/"+wanted+"/{source_path}";a.textContent=wanted.toUpperCase();a.className="language-suggestion-link";
      slot.appendChild(a);box.hidden=false;
      document.getElementById("dismissLanguageSuggestion").addEventListener("click",function(){{box.hidden=true}});
    }}
  }})();
  </script>
'''
    suggestion = "<!-- ZEOXONE_LANGUAGE_SUGGESTION_START -->" + suggestion + "<!-- ZEOXONE_LANGUAGE_SUGGESTION_END -->"
    html = re.sub(r"</body>", suggestion + "\n</body>", html, count=1, flags=re.I)
    return html

class DirectChildSplitter(HTMLParser):
    """Découpe le contenu d'un main en éléments HTML de premier niveau."""
    VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.current = ""
        self.chunks = []
    def _append(self, value):
        if self.stack:
            self.current += value
        elif value.strip():
            self.chunks.append(value)
    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        if not self.stack:
            self.current = raw
        else:
            self.current += raw
        if tag not in self.VOID:
            self.stack.append(tag)
        elif not self.stack:
            self.chunks.append(self.current)
            self.current = ""
    def handle_startendtag(self, tag, attrs):
        raw = self.get_starttag_text()
        if self.stack:
            self.current += raw
        else:
            self.chunks.append(raw)
    def handle_endtag(self, tag):
        if self.stack:
            self.current += f"</{tag}>"
            if tag in self.stack:
                index = len(self.stack) - 1 - self.stack[::-1].index(tag)
                self.stack = self.stack[:index]
                if not self.stack:
                    self.chunks.append(self.current)
                    self.current = ""
    def handle_data(self, data):
        self._append(data)
    def handle_entityref(self, name):
        self._append(f"&{name};")
    def handle_charref(self, name):
        self._append(f"&#{name};")
    def handle_comment(self, data):
        self._append(f"<!--{data}-->")
    def handle_decl(self, decl):
        self._append(f"<!{decl}>")

def translate_main_sections(inner: str, target: str, key: str, locale: str):
    splitter = DirectChildSplitter()
    splitter.feed(inner)
    if splitter.stack and splitter.current:
        splitter.chunks.append(splitter.current)
    chunks = splitter.chunks or [inner]
    groups, current = [], []
    for chunk in chunks:
        is_boundary = bool(re.match(r"\s*<(?:section|h2)\b", chunk, re.I))
        if is_boundary and current:
            groups.append("".join(current))
            current = []
        current.append(chunk)
    if current:
        groups.append("".join(current))
    translated, fallback_count = [], 0
    for group in groups:
        try:
            translated.append(deepl_translate(group, target, key))
            time.sleep(0.12)
        except HTTPError as exc:
            if exc.code in (401, 403, 456):
                raise
            fallback_count += 1
            translated.append('<div class="translation-fallback" lang="fr">' + group + "</div>")
        except (URLError, TimeoutError):
            fallback_count += 1
            translated.append('<div class="translation-fallback" lang="fr">' + group + "</div>")
    if fallback_count:
        notice = LOCALE_TEXT[locale]["fallback"]
        translated.insert(0, '<p class="translation-fallback-notice" role="note">' + notice + "</p>")
    return "".join(translated), fallback_count

def translate_document(source: str, target: str, key: str, locale: str):
    match = re.search(r"(<main\b[^>]*>)([\s\S]*?)(</main>)", source, re.I)
    if not match:
        return deepl_translate(source, target, key), 0
    main_open, main_inner, main_close = match.groups()
    placeholder = '<span id="ZEOXONE_MAIN_PLACEHOLDER" translate="no">ZEOXONE_MAIN_PLACEHOLDER</span>'
    outer = source[:match.start()] + main_open + placeholder + main_close + source[match.end():]
    translated_outer = deepl_translate(outer, target, key)
    translated_main, fallback_count = translate_main_sections(main_inner, target, key, locale)
    translated_outer, count = re.subn(
        r"<span[^>]*id=['\"]ZEOXONE_MAIN_PLACEHOLDER['\"][^>]*>.*?</span>",
        lambda _: translated_main, translated_outer, count=1, flags=re.I|re.S
    )
    if not count:
        raise RuntimeError("Le repère de traduction du contenu principal a été perdu.")
    return translated_outer, fallback_count

def translate_meta_attributes(source: str, translated: str, target: str, key: str) -> str:
    """Traduit explicitement les champs SEO qui sont des attributs HTML."""
    for attr, value in (("name", "description"), ("property", "og:title"), ("property", "og:description")):
        selector = re.compile(r"<meta\\b(?=[^>]*\\b" + attr + r"=['\\\"]" + re.escape(value) + r"['\\\"])[^>]*>", re.I)
        source_match = selector.search(source)
        target_match = selector.search(translated)
        if not source_match or not target_match:
            continue
        content = re.search(r"content=(['\\\"])(.*?)\\1", source_match.group(0), re.I)
        if not content:
            continue
        translated_value = deepl_translate(html_unescape(content.group(2)), target, key)
        new_tag = re.sub(
            r"content=(['\\\"]).*?\\1",
            lambda m: "content=" + m.group(1) + html_escape(translated_value, quote=True) + m.group(1),
            target_match.group(0), count=1, flags=re.I|re.S
        )
        translated = translated[:target_match.start()] + new_tag + translated[target_match.end():]
    return translated

def prepare_page(source: str, source_path: str, locale: str, key: str | None) -> str:
    html = clean_language_ui(source)
    if locale != "fr":
        if not key:
            raise RuntimeError("La variable DEEPL_AUTH_KEY est absente.")
        html, fallback_count = translate_document(html, LOCALES[locale]["target"], key, locale)
        html = translate_meta_attributes(source, html, LOCALES[locale]["target"], key)
        if fallback_count:
            print(f"Fallback français : {fallback_count} bloc(s) dans {locale}/{source_path}")
        time.sleep(0.15)
        # The French legal copy remains the authoritative reference pending local review.
        if source_path in {"mentions-legales.html", "politique-confidentialite.html"}:
            note = LOCALE_TEXT[locale]["market_legal"]
            html = re.sub(r"(<main\b[^>]*>)", r'\1<p class="translation-notice">' + note + "</p>", html, count=1, flags=re.I)
        if source_path.startswith("articles/"):
            note = LOCALE_TEXT[locale]["market"]
            html = re.sub(r"(<main\b[^>]*>)", r'\1<p class="market-notice">' + note + "</p>", html, count=1, flags=re.I)
    html = re.sub(r'<html\b([^>]*)\blang=["\'][^"\']*["\']', rf'<html\1lang="{locale}"', html, count=1, flags=re.I)
    html = re.sub(r'\sdata-i18n(?:-html)?=["\'][^"\']*["\']', "", html, flags=re.I)
    html = re.sub(r'<meta\s+name=["\']google-site-verification["\'][^>]*>', "", html, flags=re.I)
    html = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>', "", html, flags=re.I)
    if source_path == "index.html":
        canonical = BASE + ("/" if locale == "fr" else f"/{locale}/")
    else:
        canonical = BASE + ("/" if locale == "fr" else f"/{locale}/") + source_path
    html = rewrite_local_paths(html, locale, source_path.startswith("articles/"))
    html = re.sub(r"</head>", f'<link rel="canonical" href="{canonical}"></head>', html, count=1, flags=re.I)
    html = add_hreflang(html, source_path)
    html = inject_language_ui(html, locale, source_path)
    return html

def build_catalogue(locale: str, key: str | None):
    data = json.loads((ROOT / "articles.json").read_text(encoding="utf-8"))
    if locale != "fr":
        for article in data:
            for field in ("title", "description", "imageAlt", "type"):
                if article.get(field):
                    article[field] = deepl_translate(article[field], LOCALES[locale]["target"], key)
                    time.sleep(0.12)
    out = ROOT / locale / "articles.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def build_sitemap():
    sitemap_files = [path for path in HTML_FILES if path != "feedback.html"]
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xhtml = "http://www.w3.org/1999/xhtml"
    ET.register_namespace("", ns)
    ET.register_namespace("xhtml", xhtml)
    root = ET.Element(f"{{{ns}}}urlset")
    for path in sitemap_files:
        if path in SKIP:
            continue
        loc = BASE + ("/" if path == "index.html" else "/" + path)
        entry = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(entry, f"{{{ns}}}loc").text = loc
        for locale, info in [("fr", {"hreflang":"fr-FR"}), *LOCALES.items()]:
            href = loc if locale == "fr" else BASE + "/" + locale + ("/" if path == "index.html" else "/" + path)
            alt = ET.SubElement(entry, f"{{{xhtml}}}link", {"rel":"alternate","hreflang":info["hreflang"],"href":href})
        ET.SubElement(entry, f"{{{xhtml}}}link", {"rel":"alternate","hreflang":"x-default","href":loc})
    ET.indent(root, space="  ")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")

def main():
    key = os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        print("ERREUR : ajoute DEEPL_AUTH_KEY dans les secrets GitHub avant de lancer la génération.", file=sys.stderr)
        return 2
    for path in HTML_FILES:
        source_path = ROOT / path
        if not source_path.is_file():
            raise FileNotFoundError(f"Page source manquante : {path}")
        source = source_path.read_text(encoding="utf-8")
        for locale in ("fr", *LOCALES.keys()):
            target = ROOT / locale / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(prepare_page(source, path, locale, key), encoding="utf-8")
        print("Pages traduites :", path)
    # Les pages françaises historiques restent accessibles et deviennent la référence
    # canonique. Elles proposent aussi des liens directs vers les versions localisées.
    for path in HTML_FILES:
        source_path = ROOT / path
        source = clean_language_ui(source_path.read_text(encoding="utf-8"))
        source = add_hreflang(source, path)
        source = inject_language_ui(source, "fr", path)
        source_path.write_text(source, encoding="utf-8")
    for locale in ("fr", *LOCALES.keys()):
        build_catalogue(locale, key)
    build_sitemap()
    print("Génération terminée : FR / EN / ES / DE.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
