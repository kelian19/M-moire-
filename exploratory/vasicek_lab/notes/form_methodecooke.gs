/**
 * FORMULAIRE 3 sur 3 : l'élicitation de W par la méthode de Cooke.
 * Mémoire d'actuariat, ENSAE / Nexialog Consulting. Version 1.0 du 13 août 2026.
 *
 * MODE D'EMPLOI
 *   1. script.google.com, nouveau projet (SÉPARÉ des deux autres formulaires).
 *   2. Coller ce fichier entier, exécuter creerFormulaire, autoriser l'accès.
 *   3. Ctrl+Entrée pour lire les URL dans le journal.
 *   4. HABILLAGE : mêmes trois réglages que les formulaires 1 et 2, voir ci-dessous.
 *
 * ---------------------------------------------------------------------------------------
 * BRANDING, LES TROIS CLICS QUE CE SCRIPT NE PEUT PAS FAIRE
 *   Apps Script n'expose ni l'image d'en-tête ni la couleur du thème. Dans le formulaire en
 *   édition, palette en haut à droite (« Personnaliser le thème ») :
 *     a. EN-TÊTE : importer le MÊME bandeau logo que les formulaires 1 et 2 (1600 x 400 px).
 *     b. COULEUR : la MÊME couleur de charte.
 *     c. POLICE : « Formel ».
 * ---------------------------------------------------------------------------------------
 *
 * DEUX DÉFAUTS DE LA VERSION PAPIER DE JUILLET SONT CORRIGÉS ICI, ET IL FAUT LE SAVOIR AVANT
 * DE MODIFIER QUOI QUE CE SOIT.
 *
 *   1. UNE GRAINE ÉTAIT FAUSSE. La liste comptait « indice de queue de sévérité xi », valeur
 *      vraie 0,90. Or 0,90 est la valeur POSÉE du scénario de pire cas ; la calibration figée
 *      du mémoire donne 0,5954. Dans la méthode de Cooke une graine fausse ne dégrade pas le
 *      résultat à la marge, elle INVERSE les poids : le répondant qui vise juste est pénalisé.
 *      La question est RETIRÉE et non corrigée, parce que xi est une estimation d'intervalle
 *      [0,30 ; 0,83], plus large que la valeur elle-même. Une graine doit être une grandeur
 *      RÉALISÉE. Il reste neuf graines, toutes reproductibles par une sortie versionnée.
 *   2. LA CONVENTION DE DIRECTION ÉTAIT INVERSÉE. Le formulaire papier notait les liens
 *      « de k vers j » quand le mémoire écrit W_jk avec j la SOURCE (la ligne émet, la colonne
 *      reçoit). Une saisie fidèle aurait TRANSPOSÉ W, donc inversé toutes les conclusions de
 *      direction. Ici, partout, la PREMIÈRE lettre est le pilier qui défaille en premier.
 *
 * CE QUE LE FORMULAIRE APPORTE QUE LE PAPIER NE PEUT PAS
 *   L'ordre de saisie est IMPOSÉ : haute, puis basse, puis médiane. Sur papier on ne peut que
 *   le conseiller, et le conseil n'est pas suivi. Demander la médiane en premier ancre les deux
 *   autres autour d'elle et resserre artificiellement les intervalles, ce qui est exactement le
 *   biais que la pondération de Cooke sanctionne. Le formulaire rend l'ordre contraignant, et
 *   c'est la raison principale de préférer ce canal au PDF.
 *
 * UN CHOIX ASSUMÉ : aucune question n'est obligatoire, sauf le consentement. Une case vide est
 * une information (le répondant n'a pas voulu se prononcer) ; forcer une réponse fabriquerait
 * du signal. La méthode tolère les non-réponses, elle ne tolère pas les réponses inventées.
 */

// ---------------------------------------------------------------- identité

var ORGANISATION = "Nexialog Consulting";
var AUTEUR = "Kélian Kaddouri";
var CONTACT = "kkaddouri@nexialog.com";
var CADRE = "Mémoire d'actuariat, ENSAE Paris / Institut des Actuaires, promotion 2026";
var VERSION = "version 1.0 du 13 août 2026";

// ---------------------------------------------------------------- les neuf graines
// Chacune est une grandeur MESURÉE, reproductible par la sortie de script indiquée. C'est ce
// qui rend défendable de NOTER un répondant contre elle.

var GRAINES = [
  { code: "A1", texte: "Part des sinistres financiers portés par une cause commune, "
                     + "c'est-à-dire imputables à un même prestataire tiers",
    unite: "en %", source: "08g" },
  { code: "A2", texte: "Délai médian entre la survenance d'un incident et sa déclaration",
    unite: "en jours", source: "08e" },
  { code: "A3", texte: "Part des incidents déclarés plus d'un mois après leur survenance",
    unite: "en %", source: "08e" },
  { code: "A4", texte: "Durée médiane de containment, de la brèche à sa fermeture",
    unite: "en jours", source: "08f" },
  { code: "A5", texte: "Nombre d'incidents TIC matériels par an, pour une entité financière "
                     + "de GRANDE TAILLE (au moins dix incidents sur la période)",
    unite: "nombre par an", source: "08b" },
  { code: "A6", texte: "Délai médian de déclaration pour les seuls incidents de type piratage",
    unite: "en jours", source: "08e" },
  { code: "A7", texte: "Indice de Gini de la concentration des sinistres sur les jours de "
                     + "l'année (0 = un même nombre chaque jour ; 1 = tout un seul jour)",
    unite: "entre 0 et 1", source: "08g" },
  { code: "A8", texte: "Nombre maximal d'entités victimes d'une même cause commune en une "
                     + "seule journée",
    unite: "un nombre d'entités", source: "08g" },
  { code: "A9", texte: "Part des jours de l'année qui portent une cause commune",
    unite: "en %", source: "08g" }
];

// ---------------------------------------------------------------- les six liens dirigés
// PREMIÈRE lettre = pilier qui défaille en PREMIER. Ne pas intervertir : cela transposerait W.

var LIENS = [
  { code: "B1", texte: "P1 → P2 : une défaillance de GOUVERNANCE entraîne un incident mal géré" },
  { code: "B2", texte: "P2 → P1 : LE SENS INVERSE DU PRÉCÉDENT — un incident mal géré entraîne "
                     + "une défaillance de gouvernance" },
  { code: "B3", texte: "P4 → P2 : la défaillance d'un PRESTATAIRE TIERS entraîne un incident "
                     + "mal géré" },
  { code: "B4", texte: "P1 → P4 : une défaillance de GOUVERNANCE entraîne une défaillance côté "
                     + "prestataires" },
  { code: "B5", texte: "P3 → P1 : un défaut de TESTS ET DE DÉTECTION entraîne une défaillance "
                     + "de gouvernance" },
  { code: "B6", texte: "P5 → P2 : un défaut de PARTAGE D'INFORMATION entraîne un incident "
                     + "mal géré" }
];

// ---------------------------------------------------------------- textes

var DESCRIPTION =
  CADRE + " · " + VERSION + "\n\n"
  + "Ce questionnaire porte sur la propagation d'une défaillance entre les cinq domaines de "
  + "résilience informatique définis par le règlement DORA. Il ne demande aucune donnée sur "
  + "votre organisation : uniquement votre jugement.\n\n"
  + "Comptez trente minutes. Pour chaque quantité, vous donnerez TROIS nombres plutôt qu'un "
  + "seul : une valeur haute, une valeur basse et une valeur médiane. On mesure ainsi non "
  + "seulement votre estimation, mais aussi l'incertitude que vous lui attachez, et c'est cette "
  + "seconde information qui fait la valeur de la méthode.\n\n"
  + "Il n'y a pas de réponse attendue et la première partie n'est pas un test de "
  + "connaissances : elle sert à pondérer les répondants entre eux.\n\n"
  + AUTEUR + " · " + CONTACT;

var COMMENT_REPONDRE =
  "POUR CHAQUE QUANTITÉ, TROIS NOMBRES, ET DANS CET ORDRE.\n\n"
  + "1. LA HAUTE d'abord : une valeur assez élevée pour que vous soyez surpris, disons une "
  + "chance sur vingt, que la vraie valeur soit AU-DESSUS.\n\n"
  + "2. LA BASSE ensuite : de même, une chance sur vingt qu'elle soit EN DESSOUS.\n\n"
  + "3. LA MÉDIANE en dernier : une valeur telle que la vraie ait autant de chances d'être "
  + "au-dessus qu'en dessous.\n\n"
  + "POURQUOI CET ORDRE, QUI PEUT SURPRENDRE. Commencer par la médiane ancre les deux autres "
  + "autour d'elle et produit des intervalles trop étroits. Or l'excès de confiance est le seul "
  + "défaut que la méthode sanctionne réellement. Partir des extrêmes élargit les intervalles, "
  + "et c'est précisément le but.\n\n"
  + "RÉPONDEZ MÊME TRÈS INCERTAIN. Un intervalle large est une réponse honnête et parfaitement "
  + "exploitable ; une case vide ne l'est pas. Aucune question n'est obligatoire, mais chaque "
  + "case vide retire de l'information.\n\n"
  + "EXEMPLE, SUR UNE QUESTION SANS RAPPORT AVEC LE SUJET. Quelle est la hauteur de la tour "
  + "Montparnasse, en mètres ? Haute = 260, basse = 150, médiane = 200. L'intervalle est large, "
  + "et c'est bien ainsi : il annonce franchement ce que l'on ignore.";

var INTRO_GRAINES =
  "Neuf quantités effectivement mesurées dans les données de l'étude, sur une base publique "
  + "d'incidents du secteur financier. Leur valeur est connue de l'analyste et n'est pas "
  + "affichée ; chacune est reproductible par un calcul versionné, de sorte qu'aucune notation "
  + "ne repose sur un chiffre invérifiable.\n\n"
  + "CES QUESTIONS SERVENT À PONDÉRER, PAS À PIÉGER. Personne n'est censé connaître ces valeurs "
  + "de mémoire. Ce que l'on mesure est la justesse de vos intervalles, pas votre érudition.";

var INTRO_LIENS =
  "On vous demande la FORCE D'UN LIEN DIRIGÉ entre deux domaines, entre 0 et 1.\n\n"
  + "LECTURE DE L'ÉCHELLE. 0 signifie qu'une défaillance du premier domaine n'entraîne JAMAIS "
  + "celle du second ; 1 qu'elle l'entraîne QUASI CERTAINEMENT dans la foulée.\n\n"
  + "L'ORDRE DES DEUX DOMAINES EST CE QUI COMPTE. Le domaine cité EN PREMIER est celui qui "
  + "défaille en premier ; le second est celui qui est entraîné.\n\n"
  + "LES DEUX SENS D'UNE MÊME PAIRE SONT POSÉS SÉPARÉMENT ET N'ONT AUCUNE RAISON D'ÊTRE ÉGAUX. "
  + "C'est précisément cette asymétrie que l'étude cherche à mesurer : ne cherchez pas à faire "
  + "correspondre les deux réponses.\n\n"
  + "LES CINQ DOMAINES. P1 gouvernance et gestion du risque informatique · P2 gestion des "
  + "incidents et réponse · P3 tests de résilience et détection · P4 risque lié aux "
  + "prestataires tiers · P5 partage d'information.";

var MENTIONS =
  "USAGE. Vos réponses servent uniquement à ce mémoire d'actuariat, décrit en tête de "
  + "formulaire. Elles ne font l'objet d'aucun autre traitement et ne sont transmises à aucun "
  + "tiers.\n\n"
  + "ANONYMAT. Vos réponses sont enregistrées sous un identifiant anonyme. Ni votre nom ni "
  + "celui de votre organisation n'apparaissent dans le mémoire, dans les fichiers de travail "
  + "versionnés, ni dans aucune restitution. Seuls les intervalles agrégés sont publiés, et les "
  + "poids individuels le sont sous cet identifiant.\n\n"
  + "DONNÉES COLLECTÉES. Votre fonction, et rien d'autre. Le champ de contact est facultatif et "
  + "sert uniquement à vous renvoyer les résultats si vous le demandez.\n\n"
  + "RETRAIT. Vous pouvez demander le retrait de vos réponses jusqu'à la remise du mémoire, "
  + "sans avoir à le motiver : elles seront détruites et exclues de l'agrégation.\n\n"
  + "CONSERVATION. Jusqu'à la soutenance, puis destruction.\n\n"
  + "CONTACT. " + AUTEUR + " · " + CONTACT;

var CONFIRMATION =
  "Merci. Vos réponses sont enregistrées.\n\n"
  + "Si vous avez demandé la synthèse, je vous l'envoie une fois l'agrégation faite.\n\n"
  + AUTEUR + " · " + CONTACT;

// ---------------------------------------------------------------- construction

/** Trois champs numériques pour une quantité, dans l'ordre anti-ancrage. */
function troisQuantiles(form, code, libelle, aide, borneMin, borneMax) {
  var ordre = [
    { q: "HAUTE (95 %)", note: "une chance sur vingt que la vraie valeur soit au-dessus" },
    { q: "BASSE (5 %)", note: "une chance sur vingt qu'elle soit en dessous" },
    { q: "MÉDIANE (50 %)", note: "autant de chances au-dessus qu'en dessous" }
  ];
  form.addSectionHeaderItem().setTitle(code + ". " + libelle).setHelpText(aide);
  for (var i = 0; i < ordre.length; i++) {
    var item = form.addTextItem()
        .setTitle(code + " — " + ordre[i].q)
        .setHelpText(ordre[i].note)
        .setRequired(false);
    // ATTENTION : requireNumber() N'EXISTE PAS dans TextValidationBuilder, contrairement à ce
    // qu'on suppose. Les seules méthodes numériques sont requireNumberBetween et les
    // comparaisons. Toutes les quantités élicitées ici sont positives ou nulles, d'où le
    // repli sur requireNumberGreaterThanOrEqualTo(0) quand aucune borne haute n'a de sens.
    var v;
    if (borneMin !== null && borneMax !== null) {
      v = FormApp.createTextValidation().requireNumberBetween(borneMin, borneMax);
    } else {
      v = FormApp.createTextValidation().requireNumberGreaterThanOrEqualTo(0);
    }
    item.setValidation(v.build());
  }
}

function creerFormulaire() {
  var titre = "Propagation entre domaines de résilience — questionnaire d'expert";
  var form = FormApp.create(titre);
  form.setTitle(titre);
  form.setDescription(DESCRIPTION);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(CONFIRMATION);
  form.setCollectEmail(false);          // l'anonymat annoncé doit être vrai techniquement

  // ---- page 1 : consentement et mode d'emploi
  form.addSectionHeaderItem()
      .setTitle("Usage, anonymat et conservation")
      .setHelpText(MENTIONS);
  form.addMultipleChoiceItem()
      .setTitle("Consentement")
      .setChoiceValues(["J'accepte que mes réponses soient utilisées, sous identifiant "
                        + "anonyme, dans le cadre décrit ci-dessus."])
      .setRequired(true);              // la SEULE question obligatoire du formulaire
  form.addTextItem()
      .setTitle("Votre fonction")
      .setHelpText("Par exemple : actuaire, risk manager, RSSI, auditeur. Sert à décrire la "
                   + "composition du panel, jamais à vous identifier.")
      .setRequired(false);
  form.addSectionHeaderItem()
      .setTitle("Comment répondre")
      .setHelpText(COMMENT_REPONDRE);

  // ---- page 2 : les graines
  form.addPageBreakItem()
      .setTitle("Partie A — questions d'étalonnage")
      .setHelpText(INTRO_GRAINES);
  for (var i = 0; i < GRAINES.length; i++) {
    var g = GRAINES[i];
    var borneMin = null, borneMax = null;
    if (g.unite === "en %") { borneMin = 0; borneMax = 100; }
    if (g.unite === "entre 0 et 1") { borneMin = 0; borneMax = 1; }
    troisQuantiles(form, g.code, g.texte, "Répondez " + g.unite + ".", borneMin, borneMax);
  }

  // ---- page 3 : les liens dirigés
  form.addPageBreakItem()
      .setTitle("Partie B — liens dirigés entre domaines")
      .setHelpText(INTRO_LIENS);
  for (var j = 0; j < LIENS.length; j++) {
    troisQuantiles(form, LIENS[j].code, LIENS[j].texte,
                   "Une force entre 0 et 1. Le domaine cité en PREMIER est celui qui défaille "
                   + "en premier.", 0, 1);
  }

  // ---- page 4 : retours
  form.addPageBreakItem()
      .setTitle("Deux questions facultatives, et la première vaut souvent le reste")
      .setHelpText("");
  form.addParagraphTextItem()
      .setTitle("Y a-t-il un lien que vous auriez voulu renseigner et qui ne figure pas ici, "
                + "ou un enchaînement vu sur le terrain qui contredirait ces six ?")
      .setRequired(false);
  form.addMultipleChoiceItem()
      .setTitle("Souhaitez-vous recevoir la synthèse des résultats agrégés ?")
      .setChoiceValues(["Oui", "Non"])
      .setRequired(false);
  form.addTextItem()
      .setTitle("Si oui, une adresse de contact (facultatif)")
      .setHelpText("Conservée séparément des réponses et détruite après l'envoi de la synthèse.")
      .setRequired(false);

  // ---- feuille de réponses
  var ss = SpreadsheetApp.create("Élicitation Cooke · réponses");
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log("Formulaire à diffuser : " + form.getPublishedUrl());
  Logger.log("Formulaire à éditer   : " + form.getEditUrl());
  Logger.log("Réponses              : " + ss.getUrl());
  Logger.log("");
  Logger.log("RESTE À FAIRE À LA MAIN : palette en haut à droite du formulaire en édition,");
  Logger.log("  en-tête = logo Nexialog (1600 x 400 px), couleur = charte, police = Formel.");
  Logger.log("");
  Logger.log("APRÈS COLLECTE : exporter la feuille, une ligne par répondant, puis alimenter");
  Logger.log("  26b_elicitation_reelle.py. Les valeurs vraies des neuf graines sont dans");
  Logger.log("  26_elicitation_cooke.py, avec le script source de chacune.");
}
