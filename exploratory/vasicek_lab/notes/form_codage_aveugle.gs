/**
 * FORMULAIRE 1 sur 2 : le codage en aveugle (fiabilité inter-juges, chapitre 9).
 * Mémoire d'actuariat, ENSAE / Nexialog Consulting.
 *
 * MODE D'EMPLOI
 *   1. script.google.com, nouveau projet.
 *   2. Coller ce fichier entier à la place du contenu par défaut.
 *   3. Exécuter la fonction creerFormulaire, autoriser l'accès.
 *   4. Ctrl+Entrée pour lire le journal : URL de diffusion, URL d'édition, feuille de réponses.
 *   5. HABILLAGE NEXIALOG : voir le bloc BRANDING ci-dessous, à faire à la main dans Forms.
 *
 * ---------------------------------------------------------------------------------------
 * BRANDING, LES TROIS CLICS QUE CE SCRIPT NE PEUT PAS FAIRE
 *
 *   L'API Apps Script n'expose ni l'image d'en-tête ni la couleur du thème. Ces réglages
 *   se font uniquement dans l'interface, en trois clics, une fois le formulaire créé :
 *
 *   Ouvrir le formulaire en édition, cliquer sur la palette en haut à droite
 *   (« Personnaliser le thème »), puis :
 *     a. EN-TÊTE : « Choisir une image », onglet « Importer », déposer le logo Nexialog.
 *        Format conseillé 1600 x 400 px, fond blanc ou transparent, logo centré à gauche.
 *        Google recadre en bandeau : ne pas envoyer un logo carré, il sera tronqué.
 *     b. COULEUR : cliquer sur « + » pour une couleur personnalisée et saisir le
 *        hexadécimal de la charte Nexialog. Si le sélecteur ne propose que la palette,
 *        prendre le bleu le plus proche.
 *     c. POLICE : « Formel ». C'est la plus proche d'un document professionnel.
 *
 *   Faire exactement les mêmes réglages sur le formulaire 2 (relecture praticien) pour que
 *   les deux instruments se ressemblent.
 * ---------------------------------------------------------------------------------------
 *
 * CE QUE LE SCRIPT CONSTRUIT
 *   Une page d'introduction (les cinq domaines, la règle de réponse), puis sept pages, une
 *   par incident : le récit, puis une grille de dix lignes (les dix paires de piliers) et
 *   cinq colonnes (les cinq réponses possibles). Enfin une page de commentaire libre.
 *   Soixante-dix cases, identiques au gabarit CSV, pour que les deux codeurs traitent
 *   exactement le même corpus.
 *
 * UN CHOIX ASSUMÉ : aucune question n'est obligatoire. Une case laissée vide est une
 * information (le codeur n'a pas su trancher), et forcer une réponse fabriquerait du signal.
 */

// ---------------------------------------------------------------- identité

var ORGANISATION = "Nexialog Consulting";
var AUTEUR = "Kélian Kaddouri";
var CONTACT = "kkaddouri@nexialog.com";
var CADRE = "Mémoire d'actuariat, ENSAE / " + ORGANISATION;

// ---------------------------------------------------------------- protocole

var PAIRES = [
  "1. Gouvernance / Incidents",
  "2. Gouvernance / Tests",
  "3. Gouvernance / Prestataires",
  "4. Gouvernance / Partage d'infos",
  "5. Incidents / Tests",
  "6. Incidents / Prestataires",
  "7. Incidents / Partage d'infos",
  "8. Tests / Prestataires",
  "9. Tests / Partage d'infos",
  "10. Prestataires / Partage d'infos"
];

var OPTIONS = [
  "le 1er a entraîné le 2e",
  "le 2e a entraîné le 1er",
  "en même temps",
  "non concerné",
  "je ne sais pas"
];

var CONSIGNE_GRILLE =
  "Chaque ligne est une paire de domaines. Le 1er est celui écrit à gauche du slash, "
  + "le 2e celui de droite. Laissez vide si vous préférez ne pas répondre.";

// ---------------------------------------------------------------- les sept récits

var RECITS = [
  {
    titre: "Incident 1 sur 7 : fournisseur de messagerie d'entreprise, 2023",
    source: "Rapport d'une commission d'enquête publique américaine.",
    faits: [
      "Le rapport juge que l'entreprise ne mettait pas assez la sécurité au premier plan, et recommande que la direction générale et le conseil s'en saisissent eux-mêmes.",
      "Le renouvellement des clés de sécurité, fait à la main et rarement, a été arrêté en 2021 après une panne, sans être remplacé par un système automatique.",
      "Aucune alerte ne signalait qu'une clé devenait trop ancienne.",
      "Une clé créée en 2016, censée ne plus servir, a été utilisée par les attaquants.",
      "L'entreprise n'a pas découvert l'attaque elle-même : c'est un client qui l'a prévenue.",
      "Ses communications publiques donnaient une explication de l'origine de la fuite ; elles ont été corrigées six mois plus tard pour dire que l'origine restait inconnue.",
      "Le rapport relève des failles dans la façon dont l'entreprise sécurise les sociétés qu'elle rachète : les accès d'un ingénieur venu d'une société rachetée ont servi à entrer."
    ]
  },
  {
    titre: "Incident 2 sur 7 : banque britannique, migration informatique de 2018",
    source: "Enquête indépendante commandée par la banque, sanctions des deux autorités de contrôle britanniques, sanction personnelle de l'ancien directeur informatique.",
    faits: [
      "Cinq millions de clients ont été basculés sur une nouvelle plateforme. Beaucoup se sont retrouvés sans accès à leur compte, certains ont vu des montants disparaître, d'autres ont eu accès aux comptes d'autres clients.",
      "Les autorités ont sanctionné des manquements dans le pilotage du projet et dans la surveillance des sous-traitants.",
      "Le chantier a mobilisé plus de 70 fournisseurs et plus de 1 400 personnes ; l'enquête juge la surveillance de ces fournisseurs insuffisante.",
      "Deux centres de données n'ont pas été testés avant la mise en service, l'un étant réservé à l'exploitation : l'ensemble n'a donc jamais été testé en charge réelle.",
      "Sur 5 359 défauts recensés, 4 424 étaient encore ouverts le jour du démarrage.",
      "L'ancien directeur informatique a été sanctionné à titre personnel pour n'avoir pas veillé à ce que la banque encadre convenablement son contrat de sous-traitance.",
      "La gestion de la crise et l'information des clients ont été critiquées ; le coût dépasse 300 millions de livres."
    ]
  },
  {
    titre: "Incident 3 sur 7 : société américaine de renseignement financier, 2017",
    source: "Rapports d'un organisme d'audit public et d'une commission parlementaire.",
    faits: [
      "En mars 2017, une alerte publique demande de corriger sans délai un logiciel très répandu. L'entreprise diffuse l'alerte en interne, mais la liste de diffusion n'était plus à jour et les personnes concernées ne l'ont jamais reçue.",
      "Un contrôle automatique passé la semaine suivante n'a pas repéré la faille.",
      "Un certificat de surveillance avait expiré en janvier 2017 : sans lui, les outils de surveillance ne voyaient plus rien. Personne ne s'en est aperçu pendant plus de six mois. Plus de 300 certificats étaient expirés, dont 79 sur des systèmes critiques.",
      "Le certificat a été renouvelé fin juillet 2017 : les outils ont immédiatement signalé une activité suspecte. Les intrus étaient là depuis environ 76 jours.",
      "L'audit relève qu'il n'y avait pas de responsabilités claires ni de ligne hiérarchique nette dans l'organisation informatique, et un écart entre les règles écrites et leur application réelle, qui a aussi freiné d'autres chantiers de sécurité.",
      "L'annonce publique a eu lieu en septembre 2017."
    ]
  },
  {
    titre: "Incident 4 sur 7 : société de courtage américaine, 1er août 2012",
    source: "Décision du régulateur boursier américain.",
    faits: [
      "Une mise à jour logicielle n'a pas été installée correctement sur tous les serveurs ; l'un d'eux a continué à faire tourner un ancien programme resté actif.",
      "Le régulateur constate l'absence de contrôles et de procédures convenables pour installer et vérifier ces mises à jour.",
      "Il constate aussi l'absence de procédures écrites suffisantes pour guider les employés quand un incident technique grave survient.",
      "L'épisode a duré environ 45 minutes et coûté de l'ordre de 440 millions de dollars."
    ]
  },
  {
    titre: "Incident 5 sur 7 : banque américaine, 2019",
    source: "Décisions de deux autorités de contrôle bancaires américaines.",
    faits: [
      "L'autorité sanctionne l'absence d'une véritable évaluation des risques AVANT de basculer des activités importantes chez un hébergeur extérieur.",
      "Elle relève aussi que les insuffisances constatées n'ont pas été corrigées dans un délai raisonnable.",
      "Un équipement de protection mal configuré a permis d'accéder aux données hébergées.",
      "La banque a appris l'intrusion par un signalement venu de l'extérieur.",
      "La seconde décision porte sur le pilotage et la surveillance par le conseil d'administration."
    ]
  },
  {
    titre: "Incident 6 sur 7 : éditeur de logiciels pour les marchés financiers, janvier 2023",
    source: "Communications de l'entreprise et réactions des autorités européennes et britanniques.",
    faits: [
      "Un rançongiciel a frappé une division de cet éditeur, dont les logiciels sont utilisés par de nombreux acteurs des marchés.",
      "Beaucoup de ses clients ont dû revenir à des traitements manuels.",
      "Des déclarations réglementaires ont été retardées dans tout le secteur."
    ]
  },
  {
    titre: "Incident 7 sur 7 : logiciel de transfert de fichiers, mai et juin 2023",
    source: "Listes de victimes publiques.",
    faits: [
      "Une faille d'un logiciel de transfert de fichiers vendu par un éditeur extérieur a été exploitée massivement.",
      "Des centaines d'organisations, dont des banques et des assureurs, ont été touchées en même temps et ont dû gérer puis déclarer un incident."
    ]
  }
];

// ---------------------------------------------------------------- textes

var DESCRIPTION =
  CADRE + "\n\n"
  + "Vous allez lire sept récits d'incidents réels, tirés de rapports d'enquête publics. "
  + "Pour chacun, on vous demande simplement, entre deux domaines qui ont tous les deux "
  + "flanché, lequel a flanché en premier et a entraîné l'autre. C'est tout.\n\n"
  + "Comptez trois quarts d'heure. Aucune connaissance technique n'est nécessaire : les "
  + "faits vous sont donnés, vous n'avez qu'à les ordonner.\n\n"
  + "Il n'y a pas de réponse attendue. Vos réponses seront comparées aux miennes, que je ne "
  + "vous montre pas avant que vous ayez rendu les vôtres, pour ne pas vous influencer.\n\n"
  + AUTEUR + " · " + CONTACT;

var DOMAINES =
  "Toute la grille porte sur ces cinq domaines. Retenez les noms, ils suffisent.\n\n"
  + "GOUVERNANCE : qui décide, qui est responsable de quoi, quelle importance la direction "
  + "accorde à la sécurité, quels moyens elle y met.\n\n"
  + "INCIDENTS : repérer qu'un incident a lieu, l'escalader, y répondre, en informer les "
  + "clients et les autorités.\n\n"
  + "TESTS : tester avant de mettre en service, vérifier régulièrement, appliquer les "
  + "correctifs, renouveler les certificats et les clés.\n\n"
  + "PRESTATAIRES : les fournisseurs et sous-traitants, et la dépendance à un outil ou un "
  + "service extérieur.\n\n"
  + "PARTAGE D'INFOS : recevoir et faire circuler les alertes sur les menaces, en interne "
  + "comme avec l'extérieur.";

var CONSIGNE =
  "Pour chaque paire de domaines, choisissez l'une des cinq réponses.\n\n"
  + "LE 1ER A ENTRAÎNÉ LE 2E, ou LE 2E A ENTRAÎNÉ LE 1ER : si le récit montre que l'un a "
  + "lâché en premier ET a entraîné l'autre.\n\n"
  + "EN MÊME TEMPS : les deux ont lâché, mais rien ne dit lequel a entraîné l'autre.\n\n"
  + "NON CONCERNÉ : au moins un des deux domaines n'apparaît pas dans ce récit.\n\n"
  + "JE NE SAIS PAS : vous hésitez, ou le récit ne permet pas de trancher.\n\n"
  + "LA RÈGLE À TENIR, ET LA SEULE. Ne choisissez un sens que si le récit MONTRE qu'un "
  + "domaine a entraîné l'autre. Si les deux problèmes sont juste racontés l'un à côté de "
  + "l'autre, répondez EN MÊME TEMPS. Dans le doute, JE NE SAIS PAS est une bonne réponse. "
  + "Si vous répondez souvent EN MÊME TEMPS ce n'est pas un problème : c'est même une "
  + "information.";

var CONFIRMATION =
  "Merci. Vos réponses sont enregistrées.\n\n"
  + "Je vous envoie les miennes dès réception : l'écart entre les deux est justement ce qui "
  + "m'intéresse.\n\n"
  + AUTEUR + " · " + CONTACT;

// ---------------------------------------------------------------- construction

function creerFormulaire() {
  var form = FormApp.create("Sept incidents, une question simple");
  form.setTitle("Sept incidents, une question simple");
  form.setDescription(DESCRIPTION);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(CONFIRMATION);

  // page d'introduction
  form.addSectionHeaderItem()
      .setTitle("Les cinq domaines")
      .setHelpText(DOMAINES);
  form.addSectionHeaderItem()
      .setTitle("Comment répondre")
      .setHelpText(CONSIGNE);

  // une page par incident
  for (var i = 0; i < RECITS.length; i++) {
    var r = RECITS[i];
    var corps = r.source + "\n\n";
    for (var k = 0; k < r.faits.length; k++) {
      corps += "• " + r.faits[k] + "\n\n";
    }
    form.addPageBreakItem().setTitle(r.titre).setHelpText(corps);
    form.addGridItem()
        .setTitle("Dans cet incident, qu'est-ce qui a lâché en premier ?")
        .setHelpText(CONSIGNE_GRILLE)
        .setRows(PAIRES)
        .setColumns(OPTIONS)
        .setRequired(false);
  }

  // page finale
  form.addPageBreakItem()
      .setTitle("Une dernière question, la plus utile")
      .setHelpText("Deux champs facultatifs, mais le premier vaut souvent plus que la grille.");
  form.addParagraphTextItem()
      .setTitle("Y a-t-il une case où vous avez vraiment hésité, ou un enchaînement que vous "
                + "avez vu sur le terrain et qui ne ressemble à aucun de ces sept récits ?")
      .setRequired(false);
  form.addTextItem()
      .setTitle("Votre prénom (facultatif, seulement pour que je puisse vous remercier)")
      .setRequired(false);

  // feuille de réponses
  var ss = SpreadsheetApp.create("Codage en aveugle · réponses");
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log("Formulaire à diffuser : " + form.getPublishedUrl());
  Logger.log("Formulaire à éditer   : " + form.getEditUrl());
  Logger.log("Réponses              : " + ss.getUrl());
  Logger.log("");
  Logger.log("RESTE À FAIRE À LA MAIN : palette en haut à droite du formulaire en édition,");
  Logger.log("  en-tête = logo Nexialog (1600 x 400 px), couleur = charte, police = Formel.");
}
