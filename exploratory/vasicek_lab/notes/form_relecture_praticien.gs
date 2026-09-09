/**
 * FORMULAIRE 2 sur 3 : la relecture de praticien.
 * Mémoire d'actuariat, ENSAE Paris / Institut des Actuaires. Version 3.0 du 9 septembre 2026.
 *
 * Destinataires : praticiens du secteur, tuteur entreprise, tutrice académique. La liste
 * nominative de juillet a été retirée : elle était périmée (un collaborateur a quitté le
 * projet le 27 juillet) et n'a pas à figurer dans un fichier destiné à circuler.
 * Remplace le kit papier : tout passe désormais par le formulaire.
 *
 * =======================================================================================
 * NE RELANCEZ PAS creerFormulaire SUR UN FORMULAIRE DÉJÀ DIFFUSÉ. LIRE CE BLOC D'ABORD.
 *
 *   creerFormulaire() crée À CHAQUE EXÉCUTION un formulaire NEUF et une feuille de réponses
 *   NEUVE, tous deux portant le même titre que les précédents. Au 9 septembre 2026 le Drive
 *   du projet contenait SEPT couples formulaire/feuille identiques de nom, créés les 3 août
 *   (trois fois), 12 août, 2 septembre, 8 septembre et 9 septembre.
 *
 *   Conséquence observée, et elle a coûté une demi-journée : la seule réponse reçue vivait
 *   dans la feuille du 8 septembre pendant qu'on regardait celle du 9, vide. Une feuille
 *   vide ne prouve donc RIEN sur le fait qu'un praticien ait répondu ou non.
 *
 *   Conséquence plus grave, à vérifier avant toute relance : si deux praticiens détiennent
 *   des liens générés à des dates différentes, leurs réponses partent dans DEUX feuilles
 *   différentes. Avant de relancer qui que ce soit, s'assurer que tout le monde a le MÊME
 *   lien, celui du formulaire en cours de diffusion.
 *
 *   POUR AJOUTER DES QUESTIONS À UN FORMULAIRE DÉJÀ DIFFUSÉ, utiliser
 *   ajouterQuestionsDiscriminantes() en bas de ce fichier, qui greffe les questions sur le
 *   formulaire existant et conserve les réponses déjà reçues dans la même feuille.
 * =======================================================================================
 *
 * =======================================================================================
 * ÉCART CONSTATÉ LE 9 SEPTEMBRE ENTRE CE FICHIER ET LE FORMULAIRE EN LIGNE.
 *   La feuille de réponses du formulaire diffusé ne porte NI la question de consentement
 *   obligatoire, NI la question de forme de citation graduée, NI la demande de relecture,
 *   toutes trois ajoutées ici le 13 août. Elle porte en revanche l'ancienne question
 *   « Acceptez-vous d'être cité par votre nom ? », retirée ici le 17 août.
 *   Le projet Apps Script en ligne est donc une version ANTÉRIEURE de ce fichier : le
 *   dépôt a été corrigé, le formulaire déployé non. Recoller ce fichier dans le projet
 *   Apps Script avant toute nouvelle diffusion.
 * =======================================================================================
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
 *
 * CE QUE LA PREMIÈRE RÉPONSE A APPRIS, ET POURQUOI LA VERSION 3.0 EXISTE
 *   La première praticienne à répondre n'a contredit AUCUNE des sept phrases : deux accords
 *   pleins, cinq accords avec nuance. Un instrument qui ne recueille que des accords ne
 *   discrimine rien, et trois réponses de ce type ne vaudront pas mieux qu'une.
 *
 *   Deux défauts précis, tous deux dans les phrases et non chez la répondante :
 *
 *   a. LA PHRASE 3 EMPAQUETTE DEUX AFFIRMATIONS, que la gouvernance dégrade les autres
 *      domaines ET que l'inverse ne se produit pas. La répondante a nuancé la première et
 *      n'a rien dit de la seconde, qui est pourtant celle qui fait de P1 une source pure.
 *      On a donc perdu l'information qui compte. La phrase 8 isole cette seconde moitié.
 *
 *   b. LA PHRASE 2 NE DISCRIMINE PAS ce qu'elle prétend discriminer. Elle oppose la
 *      contagion à la cause commune, mais l'exemple donné en accord (une recette
 *      insuffisante avant mise en production, donc plus d'incidents) est PARFAITEMENT
 *      COMPATIBLE avec une cause commune : une direction informatique sous-dotée teste mal
 *      et gère mal, sans que l'un cause l'autre. La phrase 9 pose la question en choix
 *      forcé, avec une modalité « je ne peux pas trancher » qui est celle qui intéresse le
 *      plus : un praticien qui la choisit corrobore sur le terrain la frontière
 *      d'identifiabilité du chapitre 09, ce qui vaut davantage qu'un accord sur la matrice.
 *
 *   La phrase 10 transforme en item mesurable la nuance la plus utile de la première
 *   réponse : la répondante distingue l'OCCURRENCE d'un incident chez un prestataire, qu'une
 *   bonne gouvernance ne change pas, et la MAÎTRISE de ses conséquences, qu'elle change.
 *   Traduite dans le modèle, cette distinction dit que l'arc P1 vers P4 vivrait dans le
 *   canal de détection plutôt que dans la matrice de propagation. La phrase 10 demande aux
 *   répondants suivants de trancher.
 */

// ---------------------------------------------------------------- identité

var ORGANISATION = "Nexialog Consulting";
var AUTEUR = "Kélian Kaddouri";
var CONTACT = "kkaddouri@nexialog.com";
var CADRE = "Mémoire d'actuariat, ENSAE Paris / Institut des Actuaires, promotion 2026";
var VERSION = "version 3.0 du 9 septembre 2026";

// IDENTIFIANT DU FORMULAIRE EN COURS DE DIFFUSION, à renseigner avant d'utiliser
// ajouterQuestionsDiscriminantes(). C'est la longue chaîne entre /d/ et /edit dans l'URL
// d'édition du formulaire. Au 9 septembre 2026, le formulaire diffusé est celui du 8
// septembre, dont la feuille de réponses porte déjà une réponse : ne pas en créer un autre.
var FORM_ID_EN_DIFFUSION = "1uBKaP_3dj6blEsHqVHgJQp-Rf7rViu2PwYjxI8uIpyY";

// MENTIONS ET CONSENTEMENT, AJOUTÉS LE 13 AOÛT 2026, ET ICI L'ENJEU EST PLUS LOURD QUE POUR LE
// FORMULAIRE 1. Celui-ci annonce en toutes lettres que « vos réponses seront citées dans mon
// mémoire », ce qui est le bon choix éditorial : un désaccord de praticien vaut d'être publié.
// Mais la version de juillet l'annonçait sans recueillir le moindre accord, sans dire sous
// quelle forme la citation apparaîtrait, et sans offrir de relecture. Citer un praticien
// identifiable sur un avis technique, sans trace de son consentement, n'est pas défendable
// devant un jury. Le consentement est désormais explicite ET gradué : chacun choisit la forme
// sous laquelle il accepte d'être cité.
var MENTIONS =
  "USAGE. Vos réponses servent uniquement à ce mémoire d'actuariat. Aucune transmission à un "
  + "tiers, aucun autre traitement.\n\n"
  + "CITATION, ET C'EST LE POINT À LIRE. Contrairement à un questionnaire ordinaire, vos "
  + "réponses ont vocation à être CITÉES dans le mémoire, désaccords en premier : c'est tout "
  + "l'intérêt de vous solliciter. Vous choisissez ci-dessous la forme sous laquelle vous "
  + "acceptez de l'être, et ce choix est respecté sans discussion. Par défaut, si vous ne "
  + "répondez pas à cette question, la citation est anonyme.\n\n"
  + "RELECTURE. Vous pouvez demander à relire vos propos tels qu'ils sont cités avant toute "
  + "diffusion, et faire retirer ou reformuler ce que vous voulez.\n\n"
  + "RETRAIT. Vous pouvez demander le retrait complet de vos réponses jusqu'à la remise du "
  + "mémoire, sans avoir à le motiver.\n\n"
  + "CONSERVATION. Jusqu'à la soutenance, puis destruction.\n\n"
  + "CONTACT. " + AUTEUR + " · " + CONTACT;

var FORMES_CITATION = [
  "Anonyme : « un praticien du secteur »",
  "Par fonction seulement : « un directeur des risques », sans nom ni employeur",
  "Nom et fonction",
  "Je préfère ne pas être cité du tout"
];

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

// ------------------------------------------------- les trois questions qui discriminent
//
// AJOUT DU 9 SEPTEMBRE 2026. Elles ne remplacent aucune des sept phrases : les remplacer
// rendrait la première réponse reçue incomparable aux suivantes. Elles s'ajoutent à la fin,
// et chacune propose des modalités PROPRES, différentes de l'échelle d'accord, parce qu'une
// échelle d'accord ne peut pas trancher entre deux explications concurrentes.

var QUESTIONS_ORDRE = [
  {
    titre: "Phrase 8 : un incident majeur, un test raté ou la défaillance d'un prestataire "
         + "peuvent-ils DÉGRADER la gouvernance elle-même, c'est-à-dire la façon dont "
         + "l'entreprise décide, attribue les responsabilités et alloue les moyens à la "
         + "sécurité ?",
    aide: "C'est la moitié de la phrase 3 sur laquelle mon modèle repose le plus, et celle "
        + "sur laquelle j'ai le moins d'avis. Une réponse « au contraire » m'intéresse autant "
        + "qu'un « oui ».",
    choix: [
      "Non, jamais",
      "Non, au contraire : ces événements la font progresser",
      "Oui, ils la dégradent temporairement",
      "Oui, ils la dégradent durablement",
      "Sans avis"
    ]
  },
  {
    titre: "Phrase 9 : repensez à un cas précis où vous avez vu, chez le même acteur, deux "
         + "domaines défaillants en même temps. D'après ce que vous avez observé, qu'est-ce "
         + "qui s'est réellement passé ?",
    aide: "C'est la question la plus utile de tout le formulaire. La modalité « je ne peux pas "
        + "trancher » est une réponse pleine et entière, pas un aveu : mon mémoire démontre "
        + "précisément que cette distinction n'est pas identifiable sur les données "
        + "disponibles, et savoir qu'elle ne l'est pas non plus sur le terrain est un "
        + "résultat.",
    choix: [
      "L'un a entraîné l'autre, et je pourrais dire lequel",
      "Les deux venaient d'une même cause en amont (moyens, priorités, organisation), sans "
        + "que l'un cause l'autre",
      "Les deux à la fois : une cause commune, et un enchaînement par-dessus",
      "Je ne peux pas trancher entre les deux",
      "Je n'ai pas de cas précis en tête"
    ]
  },
  {
    titre: "Phrase 10 : une gouvernance solide change-t-elle la PROBABILITÉ qu'un prestataire "
         + "critique tombe, ou seulement votre capacité à en LIMITER LES CONSÉQUENCES ?",
    aide: "Cette distinction m'a été signalée par une première relecture et je n'y avais pas "
        + "pensé. Elle décide de l'endroit où ce lien vit dans mon modèle, et les deux "
        + "endroits ne donnent pas le même chiffre.",
    choix: [
      "Elle change la probabilité que cela arrive",
      "Elle ne change que la capacité à en limiter les conséquences",
      "Les deux, à parts comparables",
      "Sans avis"
    ]
  }
];

var CONSIGNE_CAS =
  "Décrivez le cas en deux lignes, sans nommer l'entreprise. Un exemple précis vaut mieux "
  + "qu'une appréciation générale.";

// ---------------------------------------------------------------- textes

// AJOUT DU 17 AOUT 2026 : voir la note identique du formulaire 1. Les destinataires n'ont
// aucun contexte sur ce travail.
var DESCRIPTION =
  CADRE + " · " + VERSION + "\n\n"
  + AUTEUR + ", élève actuaire à l'ENSAE Paris, mémoire réalisé chez " + ORGANISATION
  + ". Sujet : le capital réglementaire qu'un assureur devrait immobiliser au titre d'une "
  + "mauvaise application du règlement européen DORA sur la résilience informatique.\n\n"
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
  + "À CELLES-LÀ, ET AUX PHRASES 8 À 10.";

var INTRO_DISCRIMINANTES =
  "Les sept phrases ci-dessus demandent si vous êtes d'accord. Les trois qui suivent "
  + "demandent autre chose : elles vous font choisir entre des explications concurrentes.\n\n"
  + "Elles existent parce qu'une première relecture n'a contredit aucune des sept phrases, "
  + "tout en donnant un exemple qui admettait deux lectures opposées. Une échelle d'accord ne "
  + "pouvait pas trancher : ces trois questions le peuvent.\n\n"
  + "Comptez cinq minutes de plus.";

var CONSIGNE_COMMENTAIRE =
  "Le commentaire est la partie qui m'intéresse vraiment : un exemple précis vaut mieux "
  + "qu'une appréciation générale.";

var CONFIRMATION =
  "Merci du temps que vous y avez passé.\n\n"
  + "Vos réponses seront citées dans mon mémoire sous la forme que vous avez choisie, et les "
  + "désaccords en premier. Si vous avez contredit la phrase 3 ou la 4, je corrige le modèle : "
  + "c'est précisément pour cela que je vous ai écrit.\n\n"
  + "Si vous avez demandé à relire vos propos, je vous les envoie avant toute diffusion.\n\n"
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
  form.setCollectEmail(false);          // l'anonymat par défaut doit être vrai techniquement
  form.addSectionHeaderItem()
      .setTitle("Usage, citation et conservation")
      .setHelpText(MENTIONS);
  form.addMultipleChoiceItem()
      .setTitle("Consentement")
      .setChoiceValues(["J'accepte que mes réponses soient utilisées dans le cadre décrit "
                        + "ci-dessus."])
      .setRequired(true);              // la SEULE question obligatoire du formulaire
  form.addMultipleChoiceItem()
      .setTitle("Sous quelle forme acceptez-vous d'être cité ?")
      .setHelpText("Sans réponse, la citation est anonyme.")
      .setChoiceValues(FORMES_CITATION)
      .setRequired(false);
  form.addMultipleChoiceItem()
      .setTitle("Souhaitez-vous relire vos propos tels qu'ils seront cités, avant diffusion ?")
      .setChoiceValues(["Oui", "Non"])
      .setRequired(false);
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

  // les trois questions qui discriminent
  poserQuestionsDiscriminantes(form);

  // page finale
  // LA QUESTION DE CITATION N'EST PAS REPOSEE ICI, ET C'EST UNE CORRECTION DU 17 AOUT 2026.
  // Cette page en portait une seconde (« Acceptez-vous d'etre cite par votre nom ? », trois
  // choix) alors que la page d'introduction pose deja la meme question avec quatre choix
  // gradues. Deux questions de consentement au meme formulaire, aux options differentes,
  // autorisent des reponses CONTRADICTOIRES sur le seul point ou le repondant doit etre
  // protege : impossible de savoir laquelle fait foi, et impossible de citer sans arbitrer a
  // sa place. La question d'introduction est conservee, celle-ci est retiree. Le role, le
  // secteur et l'anciennete restent demandes : ils decrivent le panel et servent a la
  // citation « par fonction ».
  form.addPageBreakItem()
      .setTitle("La question la plus précieuse, pour finir")
      .setHelpText("Puis trois éléments sur vous, pour décrire le panel dans le mémoire. La "
                   + "forme sous laquelle vous acceptez d'être cité est celle que vous avez "
                   + "choisie au début, elle n'est pas redemandée.");
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

  // feuille de réponses
  var ss = SpreadsheetApp.create("Relecture praticien · réponses");
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log("Formulaire à diffuser : " + form.getPublishedUrl());
  Logger.log("Formulaire à éditer   : " + form.getEditUrl());
  Logger.log("Réponses              : " + ss.getUrl());
  Logger.log("");
  Logger.log("RESTE À FAIRE À LA MAIN : même en-tête, même couleur et même police que le");
  Logger.log("  formulaire du codage en aveugle.");
  Logger.log("ET METTRE À JOUR FORM_ID_EN_DIFFUSION en tête de ce fichier avec l'identifiant");
  Logger.log("  du formulaire qui vient d'être créé, sans quoi la prochaine greffe de");
  Logger.log("  questions ira sur l'ancien.");
}

// ------------------------------------------------------------ greffe sur un formulaire vivant

/**
 * Ajoute les trois questions discriminantes à un formulaire DÉJÀ DIFFUSÉ, sans en créer un
 * nouveau et sans toucher aux réponses déjà reçues, qui restent dans la même feuille.
 *
 * À utiliser plutôt que creerFormulaire dès qu'un lien a circulé. Renseigner d'abord
 * FORM_ID_EN_DIFFUSION en tête de fichier.
 *
 * Les questions sont ajoutées EN FIN de formulaire, donc après les questions de profil. Ce
 * n'est pas l'ordre idéal, mais c'est le prix à payer pour ne pas casser la comparabilité
 * avec les réponses déjà reçues : réordonner les items décale les colonnes de la feuille.
 */
function ajouterQuestionsDiscriminantes() {
  if (!FORM_ID_EN_DIFFUSION) {
    throw new Error("Renseigner FORM_ID_EN_DIFFUSION en tête de fichier avant d'exécuter.");
  }
  var form = FormApp.openById(FORM_ID_EN_DIFFUSION);

  // garde-fou : ne pas greffer deux fois les mêmes questions.
  var items = form.getItems();
  for (var i = 0; i < items.length; i++) {
    if (items[i].getTitle().indexOf("Phrase 8") === 0) {
      Logger.log("DÉJÀ FAIT : ce formulaire porte déjà la phrase 8. Rien n'a été ajouté.");
      return;
    }
  }

  poserQuestionsDiscriminantes(form);

  Logger.log("Trois questions ajoutées au formulaire : " + form.getTitle());
  Logger.log("Formulaire à diffuser : " + form.getPublishedUrl());
  Logger.log("");
  Logger.log("PRÉVENIR LES PERSONNES QUI ONT DÉJÀ RÉPONDU : leurs colonnes des phrases 8 à 10");
  Logger.log("  resteront vides. Trois questions, cinq minutes, et le panel redevient");
  Logger.log("  comparable.");
}

/** Corps commun aux deux fonctions ci-dessus. */
function poserQuestionsDiscriminantes(form) {
  form.addPageBreakItem()
      .setTitle("Trois questions qui tranchent")
      .setHelpText(INTRO_DISCRIMINANTES);

  for (var i = 0; i < QUESTIONS_ORDRE.length; i++) {
    var q = QUESTIONS_ORDRE[i];
    form.addMultipleChoiceItem()
        .setTitle(q.titre)
        .setHelpText(q.aide)
        .setChoiceValues(q.choix)
        .setRequired(false);
    form.addParagraphTextItem()
        .setTitle(q.titre.split(" :")[0] + " : le cas que vous avez en tête")
        .setHelpText(CONSIGNE_CAS)
        .setRequired(false);
  }
}
