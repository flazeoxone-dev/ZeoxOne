const translations = {
fr: {
topline:"LE FUTUR DU NUMÉRIQUE, DÉCRYPTÉ.",navNews:"Actualités",navGuides:"Guides",navReviews:"Comparatifs",navAbout:"À propos",navFollow:"Nous suivre",
heroEyebrow:"TECHNOLOGIE · INFORMATIQUE · GAMING",heroTitle:'Comprendre la tech.<br><span>Voir plus loin.</span>',heroText:"L'actualité, les guides et les analyses qui t'aident à mieux comprendre le monde numérique et à faire les bons choix.",heroButton:"Explorer le média",heroSecondary:"Découvrir ZEOX1ONE",heroMeta:"INDÉPENDANT. CURIEUX. TOURNÉ VERS DEMAIN.",visualLabel:"EXPLORER L'INNOVATION",
latestEyebrow:"À LA UNE",latestTitle:'Le radar <span>ZEOX1ONE.</span>',viewAll:"Tous les articles ↗",categoryHardware:"MATÉRIEL",categorySoftware:"LOGICIELS",categoryGaming:"CULTURE GAMING",
article1Title:"Comment choisir les composants de son premier PC ?",article1Text:"Processeur, carte graphique, mémoire vive : les bases pour construire une configuration cohérente.",article2Title:"Les outils gratuits à connaître sur Windows",article2Text:"Une sélection d'utilitaires pratiques pour améliorer son environnement de travail.",article3Title:"Comment évoluent les performances des jeux PC ?",article3Text:"FPS, résolution et technologies d'upscaling : comprendre ce qui change vraiment l'expérience.",readArticle:"Lire l'article",demoNote:"Exemples de rubriques : remplace ces articles de démonstration par tes propres contenus vérifiés avant publication.",
topicsEyebrow:"NOS UNIVERS",topicsTitle:'La tech, sous <span>tous ses angles.</span>',topic1:"Informatique",topic1Text:"PC, composants, systèmes et logiciels.",topic2:"Gaming",topic2Text:"Jeux, tendances, industrie et culture.",topic3:"Matériel",topic3Text:"Périphériques, tests et comparatifs.",topic4:"Innovation",topic4Text:"IA, nouvelles technologies et demain.",
reviewsEyebrow:"FAIRE LE BON CHOIX",reviewsTitle:'Moins de bruit.<br><span>Plus de clarté.</span>',reviewsText:"Acheter du matériel ou choisir un logiciel ne devrait pas être compliqué. Notre ambition : expliquer les critères importants, comparer avec méthode et rendre la technologie plus accessible.",reviewsButton:"Suivre nos prochains guides ↗",newsletterEyebrow:"RESTER CONNECTÉ",newsletterTitle:'Le signal, pas le <span>bruit.</span>',newsletterText:"Une sélection des prochains contenus ZEOX1ONE, directement dans ta boîte mail. La newsletter sera activée ultérieurement.",newsletterButton:"Être informé",footerLine:"Explorer. Comprendre. Avancer.",contact:"Contact",legal:"Mentions légales",rights:"Tous droits réservés."
},
en: {
topline:"THE FUTURE OF DIGITAL, DECODED.",navNews:"News",navGuides:"Guides",navReviews:"Reviews",navAbout:"About",navFollow:"Follow us",
heroEyebrow:"TECHNOLOGY · COMPUTING · GAMING",heroTitle:'Understand tech.<br><span>Look further.</span>',heroText:"News, guides and insights to help you understand the digital world and make smarter choices.",heroButton:"Explore the media",heroSecondary:"Discover ZEOX1ONE",heroMeta:"INDEPENDENT. CURIOUS. FUTURE-FOCUSED.",visualLabel:"EXPLORE INNOVATION",
latestEyebrow:"FEATURED",latestTitle:'The <span>ZEOX1ONE</span> radar.',viewAll:"All articles ↗",categoryHardware:"HARDWARE",categorySoftware:"SOFTWARE",categoryGaming:"GAMING CULTURE",
article1Title:"How to choose components for your first PC",article1Text:"CPU, graphics card, memory: the basics for building a balanced setup.",article2Title:"Free Windows tools worth knowing",article2Text:"A selection of useful utilities to improve your everyday workflow.",article3Title:"How are PC gaming performances evolving?",article3Text:"FPS, resolution and upscaling: understand what really changes the experience.",readArticle:"Read article",demoNote:"Sample sections: replace these demo articles with your own verified content before publishing.",
topicsEyebrow:"OUR UNIVERSES",topicsTitle:'Technology, from <span>every angle.</span>',topic1:"Computing",topic1Text:"PCs, components, systems and software.",topic2:"Gaming",topic2Text:"Games, trends, industry and culture.",topic3:"Hardware",topic3Text:"Peripherals, tests and comparisons.",topic4:"Innovation",topic4Text:"AI, emerging technology and tomorrow.",
reviewsEyebrow:"MAKE THE RIGHT CHOICE",reviewsTitle:'Less noise.<br><span>More clarity.</span>',reviewsText:"Buying hardware or choosing software shouldn't be complicated. Our goal: explain what matters, compare with care and make technology more accessible.",reviewsButton:"Explore upcoming guides ↗",newsletterEyebrow:"STAY CONNECTED",newsletterTitle:'The signal, not the <span>noise.</span>',newsletterText:"A selection of upcoming ZEOX1ONE stories, delivered to your inbox. The newsletter will be enabled later.",newsletterButton:"Keep me updated",footerLine:"Explore. Understand. Move forward.",contact:"Contact",legal:"Legal notice",rights:"All rights reserved."
}};
let currentLang = "fr";
const langButton = document.getElementById("langSwitch");
function setLanguage(lang){
  currentLang = lang;
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    const key=el.dataset.i18n;
    if(translations[lang][key]) el.textContent=translations[lang][key];
  });
  document.querySelectorAll("[data-i18n-html]").forEach(el=>{
    const key=el.dataset.i18nHtml;
    if(translations[lang][key]) el.innerHTML=translations[lang][key];
  });
  langButton.textContent = lang === "fr" ? "EN" : "FR";
  document.title = lang === "fr" ? "ZEOX1ONE — Tech, Gaming & Innovation" : "ZEOX1ONE — Tech, Gaming & Innovation";
}
langButton.addEventListener("click",()=>setLanguage(currentLang==="fr"?"en":"fr"));
const menuToggle=document.getElementById("menuToggle");
const nav=document.getElementById("mainNav");
menuToggle.addEventListener("click",()=>{
  const open=nav.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded",String(open));
});
nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>nav.classList.remove("open")));
document.getElementById("year").textContent=new Date().getFullYear();
