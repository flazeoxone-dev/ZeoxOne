# ZeoxOne — site éditorial

ZeoxOne est un site statique consacré à l'informatique, au matériel PC, aux logiciels et au gaming. Le site est hébergé sur GitHub Pages et utilise HTML, CSS et JavaScript, avec une interface française / anglaise.

## Objectif éditorial

Publier des articles utiles, exacts, compréhensibles par les débutants et suffisamment documentés pour que les lecteurs puissent vérifier les informations. L'IA peut aider à rechercher, structurer et rédiger, mais **aucun article ne doit être publié sans vérification humaine**.

La priorité est la qualité et l'utilité pour les lecteurs, pas la production massive d'articles ni la répétition de mots-clés. Voir les recommandations officielles de [Google sur le contenu utile](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) et [l'utilisation de l'IA générative dans les contenus web](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content).

## Arborescence et rôle des fichiers

- `index.html` : page d'accueil ; affiche les articles récents depuis le catalogue.
- `articles.html` : archives de tous les articles référencés.
- `articles.json` : catalogue central utilisé par l'accueil et les archives.
- `feedback.html` : formulaire d'avis (page volontairement exclue de l'indexation des moteurs de recherche).
- `articles/` : fichiers HTML des articles.
- `recommandations.html` : sélection de produits, logiciels et services.
- `styles.css` : styles du site.
- `script.js` : interactions, traductions FR/EN, sélecteur de langue global, filtre de recherche des archives et lien « Donner un avis » dans le pied de page.
- `sitemap.xml` : URLs à proposer aux moteurs de recherche.
- `robots.txt` : règles d'exploration.
- `assets/` : images et ressources du site.

## Procédure pour publier un nouvel article

1. Choisir un sujet précis qui répond à une vraie question des lecteurs de ZeoxOne.
2. Faire une recherche documentaire sur le Web. Ouvrir réellement les pages utilisées et vérifier leur date, leur auteur/éditeur et les informations qu'elles contiennent.
3. Rédiger l'article avec le prompt éditorial ci-dessous. Ne jamais inventer de source, de citation, de prix, de caractéristique, de test, de mesure ou d'expérience personnelle.
4. Créer un fichier HTML dans `articles/`, avec un nom court, descriptif, en minuscules et séparé par des tirets (ex. `choisir-un-ecran-pc.html`).
5. Ajouter une entrée au début de `articles.json` en respectant exactement le format des entrées existantes. La page `articles.html` récupère automatiquement le catalogue ; son champ de recherche filtre les titres, descriptions et catégories.
6. Ajouter l'URL absolue de l'article à `sitemap.xml`, avec la bonne date de dernière modification.
7. Vérifier les liens, le HTML, l'affichage mobile, les chemins relatifs, le titre, la description, la langue et les sources.
8. Relire et valider l'article avant de pousser les changements sur la branche `main`. GitHub Pages publiera ensuite les modifications.

**Important :** ne pas modifier `index.html` ni `articles.html` pour une publication normale. Ces pages utilisent le catalogue `articles.json`. Ne pas supprimer ni renommer les anciens articles : leurs URLs doivent rester accessibles. Si une URL doit absolument changer, prévoir une redirection ou conserver une page à l'ancienne adresse.

### Format de `articles.json`

Chaque article doit avoir les champs suivants :

```json
{
  "title": "Titre clair de l'article",
  "description": "Résumé précis en une phrase.",
  "category": "Matériel",
  "type": "GUIDE",
  "minutes": 7,
  "url": "articles/nom-du-fichier.html",
  "date": "2026-11-22",
  "visual": "hardware"
}
```

- `title` : titre visible.
- `description` : résumé fidèle, sans promesse exagérée.
- `category` : utiliser l'une des catégories du site : `IA & Actualité`, `Gaming`, `Matériel & PC`, `Informatique` ou `Tuto & Guide`.
- `type` : `GUIDE`, `DOSSIER` ou un type déjà pris en charge par le site.
- `minutes` : estimation raisonnable du temps de lecture.
- `url` : chemin relatif exact du fichier HTML.
- `date` : date de publication au format `AAAA-MM-JJ`.
- `visual` : valeur visuelle déjà utilisée par le site, si elle est prise en charge.

Ne pas ajouter de champs au hasard : vérifier d'abord le format existant dans `articles.json`.

## Prompt éditorial à copier dans une IA

Copier le bloc ci-dessous, puis remplacer les champs entre crochets. Utiliser une IA qui peut effectuer des recherches Web. Si elle ne peut pas consulter le Web, elle doit le dire et demander des sources à l'utilisateur au lieu de fabriquer des références.

```text
Tu es le journaliste-rédacteur technique de ZeoxOne, un média francophone indépendant consacré à l'informatique, au matériel PC, aux logiciels et au gaming. Tu écris pour des lecteurs débutants, sans les prendre de haut.

BRIEF
- Sujet : [SUJET PRÉCIS]
- Question principale du lecteur : [QUESTION À RÉSOUDRE]
- Public : débutants et curieux.
- Type : [GUIDE / DOSSIER / EXPLICATION / ACTUALITÉ]
- Angle ou valeur ajoutée souhaitée : [ANGLE]
- Longueur indicative : 900 à 1 400 mots pour un guide complet ; moins si le sujet est simple.
- Date de recherche et de rédaction : utilise la date réelle du jour.
- Nom de fichier souhaité : [nom-en-minuscules-avec-tirets.html]

MISSION 1 — RECHERCHE ET VÉRIFICATION
1. Effectue une recherche Web réelle avant de rédiger. Ouvre et lis les sources originales, pas seulement les extraits des moteurs de recherche.
2. Utilise en priorité les sources primaires adaptées au sujet : documentation officielle des fabricants/éditeurs, pages d'assistance, fiches techniques, annonces officielles, normes ou organismes reconnus. Complète si nécessaire par au moins deux tests ou analyses indépendants, sérieux et identifiables.
3. Pour une actualité, vérifie la date de publication et la date des faits. Pour les spécifications, prix, compatibilités, versions et disponibilités, vérifie qu'ils sont encore valables à la date de rédaction.
4. Croise les informations importantes avec deux sources indépendantes lorsque c'est possible. Distingue clairement un fait confirmé, une annonce, une rumeur, une estimation et une opinion.
5. N'invente JAMAIS une URL, un titre de source, un auteur, une date, une citation, un chiffre, un benchmark, un prix ou une caractéristique. N'attribue jamais à une source une information qu'elle ne dit pas.
6. Si une information importante ne peut pas être vérifiée, retire-la ou indique explicitement qu'elle reste à confirmer. Si tu ne peux pas naviguer sur le Web, arrête la rédaction factuelle et fournis la liste des sources nécessaires.
7. Ne copie pas les textes des sources et ne fais pas une simple paraphrase article par article. Synthétise avec tes propres mots et apporte une explication, une comparaison ou une méthode réellement utile.
8. À la fin, fournis une liste de sources avec le titre, l'organisme ou l'éditeur, la date si disponible et l'URL exacte. Chaque source citée dans le texte doit figurer dans cette liste, et inversement.

MISSION 2 — ACCROCHE ET RÉDACTION
1. Commence par une accroche concrète de 2 à 4 phrases : pars d'un problème, d'une question fréquente, d'une situation réaliste ou d'un changement vérifié. Donne immédiatement au lecteur une raison de lire la suite.
2. L'accroche doit être honnête : pas de sensationnalisme, de fausse urgence, de promesse spectaculaire ni de question artificielle.
3. Après l'accroche, explique clairement ce que le lecteur saura faire ou comprendre à la fin.
4. Organise le texte avec un seul H1, des H2 informatifs et des H3 seulement si utiles. Utilise des paragraphes courts, des listes et des tableaux uniquement lorsqu'ils facilitent réellement la compréhension.
5. Explique les termes techniques lors de leur première apparition. Donne des exemples concrets pour débutants.
6. Ajoute une vraie valeur éditoriale : méthode pas à pas, critères de choix, tableau comparatif justifié, erreurs à éviter, limites, cas où le conseil ne s'applique pas ou checklist.
7. Termine par une conclusion courte qui répond directement à la question principale.
8. N'invente jamais une expérience personnelle, un essai matériel, une mesure ou un test réalisé par ZeoxOne. Si aucun test n'a été fait, écris-le clairement et présente l'article comme une analyse documentaire.
9. Évite le remplissage, les répétitions, les superlatifs commerciaux et le bourrage de mots-clés. Ne promets jamais une position dans Google.

MISSION 3 — LIENS ET TRANSPARENCE
1. Ajoute des liens externes vers les sources réellement consultées, directement près des affirmations qu'elles étayent, puis une section « Sources et références » en fin d'article.
2. Vérifie chaque URL et utilise des liens descriptifs. N'utilise pas « clique ici » comme texte de lien.
3. N'ajoute aucun lien affilié, partenariat ou recommandation commerciale qui n'a pas été fourni et vérifié. Ne prétends jamais qu'un lien est affilié s'il ne l'est pas.
4. Si le brief contient des liens affiliés, ajoute une mention visible et compréhensible près du premier lien commercial, par exemple : « Certains liens de cet article sont affiliés : ZeoxOne peut recevoir une commission si vous effectuez un achat, sans coût supplémentaire pour vous. » Ne transforme pas un avis non testé en test produit.
5. Indique les limites et les éventuels conflits d'intérêts connus.

MISSION 4 — LIVRABLES POUR LE SITE
Fournis dans cet ordre :
A. Un bref dossier de recherche : faits vérifiés, points incertains et sources ouvertes.
B. Le titre, une méta-description unique et une accroche.
C. Le fichier HTML COMPLET, prêt à être enregistré dans `articles/[nom-du-fichier].html`.
D. L'objet JSON exact à ajouter au début de `articles.json`.
E. La ligne XML exacte à ajouter à `sitemap.xml`.
F. Une checklist de vérification humaine avant publication.

CONTRAINTES HTML
- Reprends la structure et les classes du modèle existant dans `articles/choisir-composants-pc.html` : même en-tête, navigation « Tous les articles », conteneur `main.wrap.article`, pied de page et classes CSS existantes.
- Conserve les chemins relatifs adaptés au dossier `articles/` : CSS `../styles.css`, favicon `../assets/favicon.svg`, accueil `../index.html`, archives `../articles.html`, mentions légales `../mentions-legales.html`, confidentialité `../politique-confidentialite.html`.
- Le document doit contenir `<!doctype html>`, `<html lang="fr">`, charset UTF-8, viewport mobile, un titre SEO descriptif, une méta-description fidèle, une URL canonique absolue correcte et `<meta name="robots" content="index,follow">`.
- Utilise le style du site et des balises HTML sémantiques. N'ajoute pas de framework, de script externe ou de CSS inline inutile.
- Ajoute une byline exacte et honnête. N'invente pas de personne, de diplôme, d'expertise ou d'auteur. Utilise « Par ZeoxOne » si aucun auteur réel n'est fourni.
- Ajoute une date de mise à jour uniquement si le contenu a réellement été revu à cette date.
- Le titre, la description, la date, la catégorie, le temps de lecture et le nom de fichier doivent correspondre exactement entre le HTML et articles.json.
- Le code doit être complet, propre, accessible et sans texte de remplacement comme [à compléter].

CONTRÔLE FINAL
Avant de répondre, vérifie la cohérence des faits et des liens, la validité du JSON et du XML, l'absence d'affirmations inventées, l'absence de faux tests, les chemins relatifs et la compatibilité avec le modèle ZeoxOne. Signale honnêtement tout élément qui nécessite une vérification humaine. Ne dis pas qu'un fichier a été publié ou modifié dans GitHub : tu fournis des fichiers prêts à être intégrés, sauf si tu disposes réellement d'un accès permettant de les modifier.
```

## Contrôle humain obligatoire avant publication

- [ ] J'ai ouvert les sources et vérifié qu'elles soutiennent bien les affirmations.
- [ ] Les dates, versions, chiffres et caractéristiques sont exacts et à jour.
- [ ] Les liens fonctionnent et pointent vers les bonnes pages.
- [ ] L'article apporte quelque chose de plus qu'un résumé de résultats Web.
- [ ] Aucun test, avis personnel, auteur ou chiffre n'a été inventé.
- [ ] Le fichier HTML s'affiche sur mobile et les liens internes fonctionnent.
- [ ] L'entrée `articles.json` est un JSON valide et pointe vers le bon fichier.
- [ ] L'URL a été ajoutée au sitemap.
- [ ] Les liens commerciaux éventuels sont clairement signalés.

## Référencement et qualité

Le sitemap aide les moteurs de recherche à découvrir les URLs, mais ne garantit ni l'indexation ni une position dans les résultats. Conserver des URLs stables, des liens internes vers les anciens articles et des titres descriptifs. Mettre à jour un ancien article seulement lorsque cela apporte une information réellement nouvelle ; conserver son URL lorsque c'est possible.

Références officielles :
- [Google Search Central — Créer du contenu utile, fiable et conçu pour les internautes](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Central — Conseils sur le contenu généré par IA](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content)

## SEO technique et indexation

- La propriété Search Console doit correspondre exactement à l'URL publiée : `https://flazeoxone-dev.github.io/ZeoxOne/`.
- Le sitemap public est `https://flazeoxone-dev.github.io/ZeoxOne/sitemap.xml`. Il doit contenir uniquement des URL canoniques accessibles, indexables et utiles. Ne pas y ajouter les pages avec `noindex`, les redirections ou les pages d'erreur.
- `robots.txt` autorise l'exploration et déclare l'URL absolue du sitemap. Ne pas utiliser robots.txt pour tenter de forcer l'indexation.
- Chaque page publique doit avoir un titre, une méta-description et une URL canonique cohérents et uniques. Les pages d'articles doivent conserver un balisage JSON-LD `Article` dont les dates et l'auteur correspondent au contenu réel.
- Les pages de présentation et de méthodologie doivent être reliées depuis la navigation ou le pied de page afin d'être faciles à découvrir.
- Après une publication, vérifier que le déploiement GitHub Pages a réussi, ouvrir l'URL publique, contrôler le sitemap puis demander une indexation dans Search Console si nécessaire. Cette demande ne garantit pas l'indexation.
- Si Search Console indique « Explorée, actuellement non indexée », vérifier en priorité la qualité et l'originalité de la page, son accessibilité, ses liens internes, sa canonical et l'absence de contenu dupliqué. Un sitemap valide ne suffit pas à rendre une page indexable.
- Les pages qui reçoivent des avis ou des retours personnels doivent respecter la confidentialité. Ne pas afficher publiquement un message envoyé via le formulaire sans consentement explicite et sans dispositif de modération.

## Pages de transparence

- `a-propos.html` présente le projet et ses objectifs sans inventer d'équipe, de qualifications ou de résultats.
- `methodologie-editoriale.html` explique la recherche, la vérification des sources, l'usage de l'IA, les limites des tests et la gestion des corrections.
- Les informations légales et de confidentialité doivent être relues et complétées par le responsable du site avant toute utilisation commerciale. Ne jamais publier de données personnelles non nécessaires.

## Déploiement GitHub Pages

Les changements poussés sur la branche `main` sont publiés par GitHub Pages selon la configuration du dépôt. Vérifier l'onglet **Actions** et attendre la réussite du workflow avant de contrôler le site en ligne.


## Réglages d'accessibilité et contrôle qualité

- Le curseur « Contraste » propose quatre niveaux. Le réglage reste temporaire par défaut.
- Une demande discrète permet d'accepter ou de refuser la mémorisation du contraste sur l'appareil. Aucun réglage n'est mémorisé avant acceptation.
- Les animations sont réduites lorsque le système signale `prefers-reduced-motion`.
- Le workflow GitHub Actions `.github/workflows/quality.yml` contrôle la syntaxe JavaScript, le catalogue JSON, le sitemap XML, les métadonnées HTML minimales et les liens locaux avant intégration.
- Le validateur est un contrôle statique : il ne remplace pas les tests visuels sur mobile, les tests clavier/lecteur d'écran, ni une vérification humaine des traductions.


## Langues du site : français et anglais

Le français est la langue principale et la version éditoriale de référence de ZeoxOne. L'anglais est la seule langue secondaire prise en charge pour le moment. L'espagnol et l'allemand sont hors périmètre : aucun sélecteur, générateur ou contrôle qualité ne doit les proposer.

Les pages françaises conservent leurs adresses actuelles. Les versions anglaises sont générées en pages statiques dans `/en/`, avant publication. Aucune traduction n'est appelée depuis le navigateur et aucune clé API n'est exposée aux visiteurs. Le sélecteur de langue reste constitué de liens HTML ordinaires et fonctionne sans JavaScript.

### Générer la version anglaise

1. Utiliser DeepL API Free si une génération automatique est nécessaire.
2. Enregistrer la clé dans GitHub : **Settings → Secrets and variables → Actions → New repository secret**.
3. Nom du secret : `DEEPL_AUTH_KEY`. Ne jamais placer la clé dans un fichier du dépôt, dans le HTML ou dans `script.js`.
4. Le workflow `.github/workflows/translations.yml` génère uniquement les pages anglaises, leurs catalogues et les métadonnées SEO associées.
5. Relire les pages anglaises avant toute fusion ou publication. La traduction automatique ne remplace pas une vérification éditoriale.

La version française reste canonique pour les pages françaises. Les pages anglaises possèdent leurs propres URL canoniques et les balises `hreflang` se limitent à `fr-FR`, `en-GB` et `x-default`. Les notes de marché précisent lorsque les prix ou disponibilités cités concernent la France.

### Contrôles

Le workflow qualité vérifie les pages françaises et anglaises, les catalogues JSON, les articles référencés, les liens locaux, les métadonnées HTML, les URL canoniques et les balises `hreflang`. Il ne remplace pas la relecture humaine ni les tests visuels, clavier et mobile.


## Règles obligatoires pour le bilingue FR / EN

Le sélecteur 🇫🇷 FR / 🇬🇧 EN doit être présent et fonctionnel sur **toutes les pages HTML publiques**, y compris les pages légales, la page de retour, la page 404 et chaque article.

- Charger `script.js` sur chaque page HTML (sauf fichier de vérification technique).
- Conserver les boutons `data-set-lang="fr"` et `data-set-lang="en"` dans l'en-tête. Si une page n'a pas encore de sélecteur, le script global doit l'ajouter.
- Toute page doit conserver son choix de langue entre les navigations grâce à la préférence `zeoxone-lang`.
- Traduire le titre du document, le H1, la navigation, le fil d'Ariane, les boutons, les libellés, les messages d'état, les paragraphes, les tableaux, les légendes d'images, les sources et le pied de page.
- Pour un texte simple, utiliser `data-locale-fr` et `data-locale-en`. Pour du contenu contenant du HTML (liens, emphase, retours à la ligne), utiliser `data-locale-html-fr` et `data-locale-html-en`.
- Ne jamais imbriquer un attribut de traduction dans la valeur d'un autre attribut. Chaque élément ne doit avoir qu'une paire d'attributs FR/EN valide.
- Ne pas laisser un mélange de français et d'anglais après changement de langue. Si une traduction n'est pas prête, ne pas présenter la page comme entièrement bilingue : terminer et vérifier la traduction avant publication.
- Vérifier le changement FR → EN → FR sur ordinateur et mobile, puis recharger une page pour confirmer que la langue reste mémorisée.

## Règles obligatoires pour les images d'articles

Chaque article doit avoir un visuel éditorial propre, pertinent pour son sujet et distinct des visuels des autres articles.

- Ne jamais réutiliser la même image de couverture pour deux articles différents.
- Choisir une image nette, lisible en petit format, avec un sujet identifiable et un cadrage adapté à une carte d'article.
- Éviter les photos génériques sans rapport avec le sujet, les logos tiers utilisés comme illustration, les visuels trompeurs et les images qui donnent l'impression d'un test réellement effectué par ZeoxOne.
- Renseigner une description `imageAlt` précise et utile dans `articles.json`.
- Garder cohérents le visuel de la carte dans `articles.json`, l'image principale de l'article, les métadonnées Open Graph / Twitter et l'image du balisage JSON-LD.
- Avant publication, vérifier que chaque URL d'image répond correctement, que l'image s'affiche sur mobile et qu'aucune image d'un autre article n'est reprise par erreur.
- Si aucune image pertinente et vérifiable n'est disponible, créer une illustration originale ou utiliser le visuel graphique de secours du site plutôt qu'une photo sans rapport.

## Contrôle avant publication — bilingue et visuels

- [ ] Le sélecteur FR/EN fonctionne sur chaque page HTML.
- [ ] Tous les textes visibles sont traduits dans les deux langues, y compris les articles complets et les messages du formulaire.
- [ ] Le choix de langue reste mémorisé après navigation et rechargement.
- [ ] Aucun attribut `data-locale-*` n'est mal formé ou dupliqué.
- [ ] Chaque article utilise une image de couverture différente et pertinente.
- [ ] Les images, textes alternatifs, cartes, métadonnées et JSON-LD sont cohérents.
- [ ] Le site a été contrôlé en français et en anglais sur mobile et ordinateur.
