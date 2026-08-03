/**
 * FORMULAIRE 2 sur 2 : la relecture de praticien.
 * Mémoire d'actuariat, ENSAE / Nexialog Consulting.
 *
 * Destinataires : Hugo, Mehdi à son retour, Nathanaël, Franck, le superviseur.
 * Remplace le kit papier : tout passe désormais par le formulaire.
 *
 * MODE D'EMPLOI
 *   1. script.google.com, nouveau projet (SÉPARÉ de celui du formulaire 1).
 *   2. Coller ce fichier entier, exécuter creerFormulaire, autoriser.
 *   3. Ctrl+Entrée pour lire les URL dans le journal.
 *   4. HABILLAGE : mêmes trois réglages que le formulaire 1, voir ci-dessous.
 *
 * ---------------------------------------------------------------------------------------
 * BRANDING, LES TROIS CLICS QUE CE SCRIPT NE PEUT PAS FAIRE
 *   Apps Script n'expose ni l'image d'en-tête ni la couleur du thème. Dans le formulaire en
 *   édition, palette en haut à droite (« Personnaliser le thème ») :
 *     a. EN-TÊTE : importer le MÊME bandeau logo que le formulaire 1 (1600 x 400 px).
 *     b. COULEUR : la MÊME couleur de charte.
 *     c. POLICE : « Formel ».
 *   Les deux formulaires doivent être visuellement identiques : ils sont envoyés aux mêmes
 *   personnes, un écart de style se lit comme un défaut de sérieux.
 * ---------------------------------------------------------------------------------------
 *
 * PARTI PRIS
 *   Les sept phrases tiennent sur UNE page, volontairement. Le message dit qu'en cas de
 *   manque de temps il faut répondre aux phrases 3 et 4 : il faut donc pouvoir les
 *   atteindre en faisant défiler, sans traverser six pages.
 *   Aucune question n'est obligatoire, sauf rien du tout. Un praticien qui ne répond qu'à
 *   deux phrases sur sept a déjà rendu le service demandé.
 */

// ---------------------------------------------------------------- identité

var ORGANISATION = "Nexialog Consulting";
var AUTEUR = "Kélian Kaddouri";
var CONTACT = "kkaddouri@nexialog.com";
var CADRE = "Mémoire d'actuariat, ENSAE / " + ORGANISATION;

var AVIS = [
  "D'accord",
  "D'accord, mais avec une nuance",
  "Pas d'accord",
  "Sans avis"
];

// ---------------------------------------------------------------- les sept phrases

var PHRASES = [
  {
    num: "Phrase 1",
    texte: "Ces cinq domaines suffisent à décrire la solidité informatique d'un acteur "
         + "financier. Il n'en manque pas un, et ils ne se chevauchent pas au point de gêner.",
    relance: ""
  },
  {
    num: "Phrase 2",
    texte: "Quand plusieurs domaines flanchent chez un même acteur, c'est souvent parce que "
         + "l'un a entraîné l'autre, et pas seulement parce qu'une cause extérieure commune "
         + "les a touchés tous les deux.",
    relance: ""
  },
  {
    num: "Phrase 3 (la plus importante)",
    texte: "Une gouvernance défaillante dégrade les autres domaines, mais l'inverse ne se "
         + "produit pas : un incident, un test raté ou un prestataire qui tombe ne dégradent "
         + "pas la gouvernance elle-même.",
    relance: "C'est la phrase que j'aimerais le plus vous voir contredire. Avez-vous déjà vu "
           + "un incident faire empirer la gouvernance ?"
  },
  {
    num: "Phrase 4 (la plus importante)",
    texte: "Les problèmes des autres domaines finissent par se voir dans la gestion des "
         + "incidents, mais une mauvaise gestion des incidents ne dégrade pas en retour les "
         + "tests, les prestataires ou la circulation de l'information.",
    relance: "Même remarque que pour la phrase 3 : c'est ici que votre expérience vaut plus "
           + "que mes calculs."
  },
  {
    num: "Phrase 5",
    texte: "Un prestataire partagé qui tombe abîme plusieurs domaines EN MÊME TEMPS, au lieu "
         + "de faire tomber les choses les unes après les autres. C'est différent des autres "
         + "domaines, et je le traite différemment.",
    relance: ""
  },
  {
    num: "Phrase 6",
    texte: "Ces trois indicateurs sont ceux qu'une direction des risques suit vraiment, ou "
         + "pourrait produire sans grand chantier : le délai pour déclarer un incident, le "
         + "temps qu'il faut pour le circonscrire, et le degré de concentration des "
         + "prestataires.",
    relance: ""
  },
  {
    num: "Phrase 7",
    texte: "Il serait réaliste de demander aux acteurs financiers un registre d'incidents qui "
         + "note la date où l'incident A EU LIEU (et non celle où il a été déclaré), qui range "
         + "chaque incident par domaine plutôt que par type d'attaque, et qui compte un "
         + "problème touchant vingt acteurs comme UN événement à vingt victimes.",
    relance: ""
  }
];

// ---------------------------------------------------------------- textes

var DESCRIPTION =
  CADRE + "\n\n"
  + "Ce qu'on vous demande, et surtout ce qu'on ne vous demande pas : PAS de lire mon "
  + "mémoire. Je vous soumets sept phrases sur lesquelles ce que vous avez vu chez des "
  + "clients vaut mieux que n'importe quel calcul, et je vous demande d'essayer de les "
  + "CONTREDIRE.\n\n"
  + "Un désaccord argumenté m'est plus utile qu'un accord, et il sera cité comme tel. "
  + "Comptez une demi-heure.\n\n"
  + AUTEUR + " · " + CONTACT;

var CONTEXTE =
  "Je cherche à chiffrer ce que coûte, en capital réglementaire, le fait de mal appliquer "
  + "le règlement européen sur la résilience informatique des acteurs financiers.\n\n"
  + "Mon modèle suppose qu'un problème sur un domaine EN ENTRAÎNE un autre, dans un certain "
  + "ordre, plutôt que les problèmes ne surviennent chacun de leur côté. Cet ordre, je n'ai "
  + "pas pu le mesurer sur des bases de données : je l'ai déduit de rapports d'enquête "
  + "publics, et c'est exactement là que votre avis compte.";

var DOMAINES =
  "GOUVERNANCE : qui décide, qui est responsable, quels moyens la direction met sur la "
  + "sécurité.\n\n"
  + "INCIDENTS : repérer un incident, l'escalader, y répondre, le déclarer.\n\n"
  + "TESTS : tester avant de mettre en service, vérifier, appliquer les correctifs.\n\n"
  + "PRESTATAIRES : les fournisseurs et la dépendance à un service extérieur.\n\n"
  + "PARTAGE D'INFOS : recevoir et faire circuler les alertes sur les menaces.";

var AVERTISSEMENT =
  "Les phrases 3 et 4 portent sur l'ordre dans lequel les choses lâchent, et je les ai "
  + "déduites de rapports d'enquête officiels.\n\n"
  + "Or une enquête officielle cherche toujours un responsable, et finit très souvent par "
  + "conclure que la direction n'encadrait pas assez. Il se peut donc que l'ordre que j'ai "
  + "trouvé reflète la façon dont ces rapports sont écrits, plutôt que ce qui se passe "
  + "vraiment dans une entreprise.\n\n"
  + "Votre réponse à ces deux phrases, fondée sur ce que vous avez vu et non sur des "
  + "rapports, est le seul moyen de faire la différence. SI VOUS MANQUEZ DE TEMPS, RÉPONDEZ "
  + "À CELLES-LÀ.";

var CONSIGNE_COMMENTAIRE =
  "Le commentaire est la partie qui m'intéresse vraiment : un exemple précis vaut mieux "
  + "qu'une appréciation générale.";

var CONFIRMATION =
  "Merci du temps que vous y avez passé.\n\n"
  + "Vos réponses seront citées dans mon mémoire, et les désaccords en premier. Si vous avez "
  + "contredit la phrase 3 ou la 4, je corrige le modèle : c'est précisément pour cela que "
  + "je vous ai écrit.\n\n"
  + AUTEUR + " · " + CONTACT;

// ---------------------------------------------------------------- construction

function creerFormulaire() {
  var form = FormApp.create("Sept phrases à contredire");
  form.setTitle("Sept phrases à contredire");
  form.setDescription(DESCRIPTION);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(CONFIRMATION);

  // page d'introduction
  form.addSectionHeaderItem()
      .setTitle("De quoi il s'agit, en trois phrases")
      .setHelpText(CONTEXTE);
  form.addSectionHeaderItem()
      .setTitle("Les cinq domaines dont je parle")
      .setHelpText(DOMAINES);
  form.addSectionHeaderItem()
      .setTitle("À lire avant de répondre aux phrases 3 et 4")
      .setHelpText(AVERTISSEMENT);

  // les sept phrases, sur une seule page
  form.addPageBreakItem()
      .setTitle("Les sept phrases")
      .setHelpText("Pour chacune : votre avis, puis un commentaire si vous en avez un. "
                   + "Rien n'est obligatoire. Répondre à deux phrases sur sept rend déjà le "
                   + "service demandé.");

  for (var i = 0; i < PHRASES.length; i++) {
    var p = PHRASES[i];
    var aide = p.relance ? p.relance : "";
    form.addMultipleChoiceItem()
        .setTitle(p.num + " : " + p.texte)
        .setHelpText(aide)
        .setChoiceValues(AVIS)
        .setRequired(false);
    form.addParagraphTextItem()
        .setTitle(p.num + " : commentaire, exemple vécu")
        .setHelpText(CONSIGNE_COMMENTAIRE)
        .setRequired(false);
  }

  // page finale
  form.addPageBreakItem()
      .setTitle("La question la plus précieuse, pour finir")
      .setHelpText("Puis quelques éléments sur vous, pour savoir comment vous citer.");
  form.addParagraphTextItem()
      .setTitle("Qu'est-ce qui manque ? Quelle phrase aurait dû figurer dans cette liste, ou "
                + "quel enchaînement voyez-vous régulièrement sur le terrain et dont je ne "
                + "parle nulle part ?")
      .setRequired(false);
  form.addTextItem()
      .setTitle("Votre rôle")
      .setRequired(false);
  form.addTextItem()
      .setTitle("Votre secteur")
      .setRequired(false);
  form.addTextItem()
      .setTitle("Depuis combien de temps exercez-vous ?")
      .setRequired(false);
  form.addMultipleChoiceItem()
      .setTitle("Acceptez-vous d'être cité par votre nom ?")
      .setChoiceValues([
        "Oui, citez-moi par mon nom",
        "Non, citez-moi de façon anonyme (rôle et secteur seulement)",
        "Ne me citez pas du tout"
      ])
      .setRequired(false);

  // feuille de réponses
  var ss = SpreadsheetApp.create("Relecture praticien · réponses");
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log("Formulaire à diffuser : " + form.getPublishedUrl());
  Logger.log("Formulaire à éditer   : " + form.getEditUrl());
  Logger.log("Réponses              : " + ss.getUrl());
  Logger.log("");
  Logger.log("RESTE À FAIRE À LA MAIN : même en-tête, même couleur et même police que le");
  Logger.log("  formulaire du codage en aveugle.");
}
