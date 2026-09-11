#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_soutenance_ppt.py : fabrique le support de soutenance devant l'Institut.

POURQUOI UN SCRIPT ET PAS UN FICHIER FAIT A LA MAIN. Le projet publie chaque
nombre depuis un script versionne, et un support de soutenance est le document ou
un chiffre perime coute le plus cher : le jury « essaie de retrouver dans le texte
du memoire ce que l'etudiant presente a l'oral ». Un support genere se regenere,
se relit et se met sous harnais ; un support fait a la main derive.

ET C'EST CE QUI A RENDU LE CHANGEMENT DE CHARTE BON MARCHE. Le 11 septembre 2026,
Kelian a fourni le gabarit de presentation Nexialog et demande « le style exacte
que je veux ». Le contenu n'a pas bouge d'une ligne : seules les primitives de
mise en page ci-dessous ont ete reecrites. Un support fait a la main aurait exige
de refaire vingt-sept diapositives une par une.

LA CHARTE EST MESUREE, PAS DEVINEE. Les couleurs, les polices et leurs corps sont
releves dans le gabarit lui-meme, aplat par aplat et span par span. Le detail et
la provenance des visuels sont dans charte_nexialog/README.md.

REGLES TENUES, toutes issues du CLAUDE.md ou du GUIDE_REDACTION du depot :
  - aucun chiffre qui ne soit pas deja publie dans le memoire ou une sortie de
    script. Le fichier controle_soutenance.md les liste un par un ;
  - jamais « le SCR DORA de telle entite » mais « besoin de capital ORSA au titre
    de DORA » ;
  - jamais l'addition des quatre canaux, ni celle des deux interactions ;
  - le niveau absolu est annonce ILLUSTRATIF, le rapport est le resultat ;
  - pas de tiret cadratin. Le gabarit ecrit « Message cle — » ; le support ecrit
    « Message cle » en gras suivi du texte, ce qui rend la meme lecture.

Sortie : soutenance_memoire_DORA.pptx.
"""

import os
import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
except ImportError:
    sys.exit("python-pptx absent. Installer avec : .venv\\Scripts\\python.exe -m pip install python-pptx")

ICI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ICI, "..", "vasicek_lab", "figures")
CHARTE = os.path.join(ICI, "charte_nexialog")
SORTIE = os.path.join(ICI, "soutenance_memoire_DORA.pptx")

# ---------------------------------------------------------------------------
# PALETTE DU GABARIT NEXIALOG. Relevee dans le PDF du gabarit, ponderee par la
# surface des aplats et par le nombre de caracteres pour les textes.
#
# ATTENTION : ce n'est PAS la palette de style_nexialog.py, qui reste la source
# unique des couleurs des FIGURES. Les deux familles se ressemblent sans se
# confondre. Une figure du memoire garde ses couleurs de figure.
# ---------------------------------------------------------------------------
ARDOISE = RGBColor(0x22, 0x3E, 0x55)    # bleu de marque : titres et aplats
PROFOND = RGBColor(0x19, 0x2E, 0x3F)    # la meme, plus sombre : intercalaires
ACIER = RGBColor(0x43, 0x5B, 0x6E)      # la meme, eclaircie : second aplat
ENCRE = RGBColor(0x12, 0x27, 0x38)      # texte courant
GRIS = RGBColor(0x59, 0x59, 0x59)       # texte secondaire et legendes
ACCENT = RGBColor(0xB1, 0x00, 0x31)     # rouge de marque : accents et alertes
CLAIR = RGBColor(0xF2, 0xF2, 0xF2)      # aplat clair, bandeau de message
FILET = RGBColor(0xD9, 0xD9, 0xD9)      # filets
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
PIED = RGBColor(0xA5, 0xA5, 0xA5)       # pagination et pied de page

TITRAGE = "Georgia"                     # titres, comme le gabarit
POLICE = "Segoe UI"                     # corps, comme le gabarit

L, H = Inches(13.333), Inches(7.5)      # 16:9
MARGE = Inches(0.82)                    # gouttiere du gabarit
LARG = L - 2 * MARGE
Y_CORPS = Inches(1.52)                  # haut de la zone de contenu
Y_BANDE = Inches(6.33)                  # haut du bandeau « Message cle »
H_BANDE = Inches(0.60)
Y_PIED = Inches(7.03)
MILIEU = MARGE + LARG / 2               # axe du filet vertical a deux colonnes

_numero = {"n": 0}                      # pagination, remise a zero par construire()


# ---------------------------------------------------------------------------
# MESURE DU TEXTE. On ouvre les fichiers de police et l'on mesure, au lieu
# d'estimer une largeur moyenne de caractere.
#
# POURQUOI. Le gabarit fourni porte deux titres tronques et un titre qui
# chevauche son sous-titre : ce sont des defauts de mise en page que personne ne
# voit en relisant la source, et qui sautent aux yeux sur la diapositive rendue.
# La regle du projet est de regarder la sortie ; mesurer avant de poser evite
# d'avoir a corriger apres avoir regarde.
# ---------------------------------------------------------------------------
_FICHIERS = {(TITRAGE, True): "georgiab.ttf", (TITRAGE, False): "georgia.ttf",
             (POLICE, True): "segoeuib.ttf", (POLICE, False): "segoeui.ttf"}
_ECHELLE = 8                            # mesurer en grand puis diviser : moins de bruit d'arrondi
_cache = {}


def _fonte(police, gras, taille):
    cle = (police, gras, taille)
    if cle not in _cache:
        from PIL import ImageFont
        chemin = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts",
                              _FICHIERS[(police, gras)])
        _cache[cle] = ImageFont.truetype(chemin, int(taille * _ECHELLE))
    return _cache[cle]


def largeur_pt(texte, police=POLICE, gras=False, taille=14):
    return _fonte(police, gras, taille).getlength(texte) / _ECHELLE


def nb_lignes(texte, largeur_emu, police=POLICE, gras=False, taille=14):
    """Nombre de lignes qu'occupera un paragraphe, par coupure aux espaces."""
    dispo = Emu(int(largeur_emu)).pt
    n, courante = 1, ""
    for mot in texte.split():
        essai = (courante + " " + mot).strip()
        if largeur_pt(essai, police, gras, taille) <= dispo or not courante:
            courante = essai
        else:
            n += 1
            courante = mot
    return n


def taille_qui_tient(texte, largeur_emu, police=TITRAGE, gras=True,
                     maxi=26, mini=20):
    """Le plus grand corps entre mini et maxi qui tient sur UNE ligne."""
    dispo = Emu(int(largeur_emu)).pt
    for t in range(maxi, mini - 1, -1):
        if largeur_pt(texte, police, gras, t) <= dispo:
            return t
    return mini


# ---------------------------------------------------------------------------
# Primitives de charte
# ---------------------------------------------------------------------------
def _rect(s, x, y, l, h, couleur, bord=None, epaisseur=1.0):
    f = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(x), int(y), int(l), int(h))
    if couleur is None:
        f.fill.background()
    else:
        f.fill.solid()
        f.fill.fore_color.rgb = couleur
    if bord is None:
        f.line.fill.background()
    else:
        f.line.color.rgb = bord
        f.line.width = Pt(epaisseur)
    f.shadow.inherit = False
    return f


def _triangle(s, points, couleur):
    """Triangle plein defini par trois sommets en EMU.

    POURQUOI UNE FORME LIBRE ET PAS MSO_SHAPE.RIGHT_TRIANGLE. Le gabarit coupe
    ses photographies en diagonale dans les deux sens ; une autoforme imposerait
    de jouer sur la rotation et l'effet miroir, ce qui deplace aussi le cadre.
    Trois points sont plus courts et exacts.
    """
    ff = s.shapes.build_freeform(int(points[0][0]), int(points[0][1]))
    ff.add_line_segments([(int(x), int(y)) for x, y in points[1:]], close=True)
    f = ff.convert_to_shape()
    f.fill.solid()
    f.fill.fore_color.rgb = couleur
    f.line.fill.background()
    f.shadow.inherit = False
    return f


def _photo_couvrante(s, chemin, x, y, l, h):
    """Pose une photographie en la RECADRANT, jamais en l'etirant ni en la
    laissant deborder.

    Premiere version : on agrandissait l'image jusqu'a couvrir le cadre et le
    debord etait cense se perdre hors diapositive. Il ne s'y perdait pas : sur la
    couverture et sur le sommaire, la photographie sortait par la gauche et par la
    droite de sa zone et passait sous le texte. Le recadrage par `crop_*` fait
    exactement ce que fait le gabarit, et le cadre reste celui qu'on demande.
    """
    from PIL import Image
    lp, hp = Image.open(chemin).size
    pic = s.shapes.add_picture(chemin, int(x), int(y), int(l), int(h))
    r_cadre, r_image = l / h, lp / hp
    if r_image > r_cadre:                       # image trop large : rogner les cotes
        f = (1 - r_cadre / r_image) / 2
        pic.crop_left = pic.crop_right = f
    else:                                       # image trop haute : rogner haut et bas
        f = (1 - r_image / r_cadre) / 2
        pic.crop_top = pic.crop_bottom = f
    return pic


def zone(s, x, y, l, h):
    tb = s.shapes.add_textbox(int(x), int(y), int(l), int(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    return tf


def para(tf, texte, taille, couleur=ENCRE, gras=False, italique=False,
         espace_avant=0, aligne=PP_ALIGN.LEFT, premier=False, police=POLICE):
    p = tf.paragraphs[0] if premier else tf.add_paragraph()
    p.alignment = aligne
    p.space_before = Pt(espace_avant)
    r = p.add_run()
    r.text = texte
    r.font.size = Pt(taille)
    r.font.bold = gras
    r.font.italic = italique
    r.font.color.rgb = couleur
    r.font.name = police
    return p


def morceaux(tf, bouts, taille, espace_avant=0, aligne=PP_ALIGN.LEFT, premier=False):
    """Un paragraphe compose de plusieurs styles, pour « Message cle » et les
    tetes de bloc numerotees."""
    p = tf.paragraphs[0] if premier else tf.add_paragraph()
    p.alignment = aligne
    p.space_before = Pt(espace_avant)
    for texte, couleur, gras, police in bouts:
        r = p.add_run()
        r.text = texte
        r.font.size = Pt(taille)
        r.font.bold = gras
        r.font.italic = False
        r.font.color.rgb = couleur
        r.font.name = police
    return p


def nouvelle(prs, pagine=True, coin=True, logo=True):
    """Une diapositive de contenu au gabarit : fond blanc, coin rouge, logo,
    pagination."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fond = _rect(s, 0, 0, L, H, BLANC)
    s.shapes._spTree.remove(fond._element)
    s.shapes._spTree.insert(2, fond._element)
    if coin:
        _triangle(s, [(0, 0), (Inches(0.62), 0), (0, Inches(0.92))], ACCENT)
        _triangle(s, [(Inches(0.30), 0), (Inches(0.62), 0), (0, Inches(0.92)),
                      (0, Inches(0.48))], ACCENT)
    if logo:
        s.shapes.add_picture(os.path.join(CHARTE, "nexialog.png"),
                             int(L - Inches(0.55) - Inches(1.62)), int(Inches(0.20)),
                             int(Inches(1.62)), int(Inches(0.59)))
    if pagine:
        _numero["n"] += 1
        tf = zone(s, L - Inches(1.10), Y_PIED, Inches(0.55), Inches(0.28))
        para(tf, str(_numero["n"]), 10, PIED, premier=True, aligne=PP_ALIGN.RIGHT)
    return s


def titre(s, texte, sous_titre=None):
    """Titre navy en Georgia gras, sous-titre rouge en dessous.

    Le titre porte une AFFIRMATION, pas une etiquette ; le sous-titre situe.

    LE CORPS EST CHOISI PAR MESURE, ENTRE 26 ET 20 POINTS. Un titre pose a 26 pt
    et qui passe a la ligne recouvre son propre sous-titre : le gabarit fourni
    porte ce defaut deux fois, et la premiere version de ce support l'a reproduit
    sur six diapositives. La regle qui l'empeche est simple : le titre tient sur
    UNE ligne, et c'est le corps qui cede, pas la mise en page. L'ecart de corps
    d'une diapositive a l'autre ne se voit pas ; un titre chevauche, si.
    """
    dispo = LARG - Inches(1.90)
    tf = zone(s, MARGE, Inches(0.32), dispo, Inches(0.58))
    para(tf, texte, taille_qui_tient(texte, dispo), ARDOISE, gras=True,
         premier=True, police=TITRAGE)
    if sous_titre:
        tf2 = zone(s, MARGE, Inches(0.88), dispo, Inches(0.42))
        para(tf2, sous_titre, taille_qui_tient(sous_titre, dispo, maxi=18, mini=14),
             ACCENT, gras=True, premier=True, police=TITRAGE)


def separation_colonnes(s, haut=None, bas=None):
    """Le filet vertical pointille qui separe les deux colonnes du gabarit."""
    haut = haut if haut is not None else Y_CORPS - Inches(0.06)
    bas = bas if bas is not None else Y_BANDE - Inches(0.18)
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, int(MILIEU), int(haut),
                               int(MILIEU), int(bas))
    c.line.color.rgb = RGBColor(0x9D, 0xC3, 0xC8)
    c.line.width = Pt(1.25)
    c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return c


def tete(s, x, y, l, numero, texte):
    """Tete de bloc : numero cercle rouge puis libelle navy, comme le gabarit."""
    tf = zone(s, x, y, l, Inches(0.34))
    cercles = "①②③④⑤⑥"
    morceaux(tf, [(cercles[numero - 1] + " ", ACCENT, True, POLICE),
                  (texte, ARDOISE, True, POLICE)], 15, premier=True)
    return y + Inches(0.36)


def _retrait(p, marge=Inches(0.24)):
    """Retrait negatif de premiere ligne, pour qu'une puce longue s'aligne sous
    son texte et non sous sa puce."""
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(int(marge)))
    pPr.set("indent", str(-int(marge)))


def lignes(s, x, y, l, items, taille=14, interligne=8, h=None):
    """Corps de colonne. Un tuple (texte, style) par ligne.

    style : "puce" pour une puce, "texte" pour un paragraphe, "fort" pour du gras
    navy, "alerte" pour du gras rouge, "note" pour du gris.

    Rend la hauteur CONSOMMEE, pour que l'appelant pose le bloc suivant dessous
    au lieu de la deviner. Deux blocs se chevauchaient dans la premiere version
    pour cette seule raison.
    """
    h = h if h is not None else Y_BANDE - y - Inches(0.15)
    tf = zone(s, x, y, l, h)
    prise = 0
    for i, (t, st) in enumerate(items):
        avant = 0 if i == 0 else interligne
        corps = taille - 1 if st == "note" else taille
        if st == "puce":
            p = morceaux(tf, [("•   ", GRIS, False, POLICE), (t, ENCRE, False, POLICE)],
                         taille, espace_avant=avant, premier=(i == 0))
            _retrait(p)
            nl = nb_lignes("•   " + t, l - Inches(0.24), POLICE, False, taille)
        elif st == "fort":
            para(tf, t, taille, ARDOISE, gras=True, espace_avant=avant, premier=(i == 0))
            nl = nb_lignes(t, l, POLICE, True, taille)
        elif st == "alerte":
            para(tf, t, taille, ACCENT, gras=True, espace_avant=avant, premier=(i == 0))
            nl = nb_lignes(t, l, POLICE, True, taille)
        elif st == "note":
            para(tf, t, corps, GRIS, espace_avant=avant, premier=(i == 0))
            nl = nb_lignes(t, l, POLICE, False, corps)
        else:
            para(tf, t, taille, ENCRE, espace_avant=avant, premier=(i == 0))
            nl = nb_lignes(t, l, POLICE, False, taille)
        prise += Pt(avant) + Pt(nl * corps * 1.22)
    return prise


def message(s, texte):
    """Le bandeau de bas de diapositive du gabarit.

    Le gabarit ecrit « Message cle — ». Le tiret cadratin est proscrit dans les
    livrables du projet : le gras du libelle rend la meme separation.
    """
    _rect(s, MARGE - Inches(0.20), Y_BANDE, LARG + Inches(0.40), H_BANDE, CLAIR)
    _rect(s, MARGE - Inches(0.20), Y_BANDE, Pt(6), H_BANDE, ACCENT)
    tf = zone(s, MARGE + Inches(0.06), Y_BANDE + Inches(0.13),
              LARG + Inches(0.10), H_BANDE - Inches(0.16))
    morceaux(tf, [("Message clé   ", ACCENT, True, POLICE),
                  (texte, GRIS, False, POLICE)], 14, premier=True)


def source(s, texte):
    """Mention de source. L'Institut exige la tracabilite, et le projet exige en
    plus que chaque diapositive dise de quel script elle tient ses nombres."""
    tf = zone(s, MARGE - Inches(0.20), Y_PIED, LARG - Inches(0.70), Inches(0.28))
    para(tf, texte, 9, PIED, italique=True, premier=True)


def figure(s, nom, haut=None, bas=None, largeur=None):
    """Insere une figure du depot, centree et mise a l'echelle sans deformation.

    Les figures ne sont PAS redessinees : ce sont celles du memoire, produites par
    les scripts et deja relues. Les recadrer ou les recolorier romprait la
    correspondance entre l'oral et le document, que le jury verifie.
    """
    chemin = os.path.join(FIG, nom)
    if not os.path.exists(chemin):
        raise SystemExit(f"figure absente : {chemin}")
    from PIL import Image
    lp, hp = Image.open(chemin).size
    haut = haut if haut is not None else Y_CORPS
    bas = bas if bas is not None else H - Y_BANDE + Inches(0.12)
    dispo_l = largeur if largeur is not None else LARG
    dispo_h = H - haut - bas
    ech = min(dispo_l / lp, dispo_h / hp)
    ll, hh = int(lp * ech), int(hp * ech)
    s.shapes.add_picture(chemin, int((L - ll) / 2), int(haut + (dispo_h - hh) / 2), ll, hh)


def figure_gauche(s, nom, largeur=None, haut=None, bas=None):
    """Figure haute placee a GAUCHE, le texte occupant la colonne de droite.

    POURQUOI CE SECOND GABARIT. Trois figures du memoire sont presque carrees,
    voire hautes : posees pleine largeur elles se dimensionnent sur la HAUTEUR
    disponible et n'occupent alors qu'un tiers de la diapositive, etiquettes
    illisibles. C'est la meme regle que dans le memoire, ou une figure portrait
    prend une page entiere et jamais un debord en largeur.
    """
    chemin = os.path.join(FIG, nom)
    if not os.path.exists(chemin):
        raise SystemExit(f"figure absente : {chemin}")
    from PIL import Image
    lp, hp = Image.open(chemin).size
    largeur = largeur if largeur is not None else MILIEU - MARGE - Inches(0.24)
    haut = haut if haut is not None else Y_CORPS
    bas = bas if bas is not None else H - Y_BANDE + Inches(0.12)
    dispo_h = H - haut - bas
    ech = min(largeur / lp, dispo_h / hp)
    ll, hh = int(lp * ech), int(hp * ech)
    s.shapes.add_picture(chemin, int(MARGE + (largeur - ll) / 2),
                         int(haut + (dispo_h - hh) / 2), ll, hh)
    separation_colonnes(s)
    return MILIEU + Inches(0.28)


def carte(s, x, y, l, h, entete, contenu, teinte=ARDOISE, taille=13):
    """Bloc a bandeau colore : entete pleine, corps sur fond clair.

    C'est la forme que le gabarit emploie pour ses chaines de traitement et ses
    comparaisons terme a terme.
    """
    he = Inches(0.34)
    b = _rect(s, x, y, l, he, teinte)
    tfb = b.text_frame
    tfb.word_wrap = True
    tfb.margin_left = tfb.margin_right = Inches(0.04)
    tfb.margin_top = tfb.margin_bottom = 0
    tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(tfb, entete, taille + 1, BLANC, gras=True, premier=True, aligne=PP_ALIGN.CENTER)
    if h > he:
        c = _rect(s, x, y + he, l, h - he, CLAIR, bord=FILET, epaisseur=0.75)
        tfc = c.text_frame
        tfc.word_wrap = True
        tfc.margin_left = tfc.margin_right = Inches(0.08)
        tfc.margin_top = Inches(0.08)
        tfc.vertical_anchor = MSO_ANCHOR.MIDDLE
        for i, t in enumerate(contenu):
            para(tfc, t, taille, ENCRE, espace_avant=0 if i == 0 else 5,
                 premier=(i == 0), aligne=PP_ALIGN.CENTER)
    return b


def chevron(s, x, y, l, h, texte, teinte, taille=13, couleur_texte=BLANC):
    """Etape de chaine, en chevron, comme la bande « Bale / Solvabilite / DORA »
    du gabarit."""
    f = s.shapes.add_shape(MSO_SHAPE.PENTAGON, int(x), int(y), int(l), int(h))
    f.fill.solid()
    f.fill.fore_color.rgb = teinte
    f.line.fill.background()
    f.shadow.inherit = False
    tf = f.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(tf, texte, taille, couleur_texte, gras=True, premier=True, aligne=PP_ALIGN.CENTER)
    return f


def fleche_bas(s, x, y, l, h=Inches(0.30)):
    a = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, int(x), int(y), int(l), int(h))
    a.fill.solid()
    a.fill.fore_color.rgb = ACIER
    a.line.fill.background()
    a.shadow.inherit = False


def notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte.strip()


# ---------------------------------------------------------------------------
# Diapositives de gabarit : couverture, sommaire, intercalaire, cloture
# ---------------------------------------------------------------------------
def couverture(prs):
    """La couverture du gabarit : photographie coupee en diagonale a droite,
    logos en haut, titre navy, bandeau rouge, mentions en Georgia italique."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _rect(s, 0, 0, L, H, BLANC)
    # La photographie occupe la droite ; la diagonale blanche la coupe. Le champ
    # blanc s'elargit vers le bas, ce qui est exactement ce dont le bloc de titre
    # a besoin : il est pose la ou il y a de la place, pas la ou il gene.
    x0, x1 = Inches(6.40), Inches(9.05)
    _photo_couvrante(s, os.path.join(CHARTE, "photo_couverture.jpg"), x0, 0, L - x0, H)
    _triangle(s, [(x0, 0), (x0, H), (x1, H)], BLANC)
    _triangle(s, [(0, 0), (Inches(0.66), 0), (0, Inches(0.98))], ACCENT)

    s.shapes.add_picture(os.path.join(CHARTE, "institut_actuaires.png"),
                         int(Inches(2.35)), int(Inches(0.18)),
                         int(Inches(1.45)), int(Inches(0.62)))
    s.shapes.add_picture(os.path.join(CHARTE, "nexialog.png"),
                         int(Inches(0.35)), int(Inches(0.88)),
                         int(Inches(1.95)), int(Inches(0.71)))
    s.shapes.add_picture(os.path.join(CHARTE, "ensae.png"),
                         int(Inches(4.60)), int(Inches(0.42)),
                         int(Inches(1.10)), int(Inches(1.30)))

    # Meme regle que pour les titres de contenu : les deux lignes du titre sont
    # POSEES, et c'est le corps qui cede pour qu'aucune ne passe a la ligne.
    lt = Inches(7.00)
    ct = min(taille_qui_tient("Quantification du SCR lié à la non-conformité", lt,
                              maxi=26, mini=15),
             taille_qui_tient("au règlement DORA (UE 2022/2554)", lt, maxi=26, mini=15))
    tf = zone(s, Inches(0.42), Inches(3.05), lt, Inches(1.15))
    for t in ("Quantification du SCR lié à la non-conformité",
              "au règlement DORA (UE 2022/2554)"):
        para(tf, t, ct, ARDOISE, gras=True, premier=(t.startswith("Quanti")),
             police=TITRAGE)

    bd = _rect(s, Inches(0.95), Inches(4.38), Inches(5.70), Inches(0.46), ACCENT)
    tfb = bd.text_frame
    tfb.word_wrap = True
    tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(tfb, "Une cascade dirigée entre les cinq piliers", 15, BLANC, gras=True,
         premier=True, aligne=PP_ALIGN.CENTER)

    tf = zone(s, Inches(0.42), Inches(5.12), Inches(6.55), Inches(0.90))
    para(tf, "Présenté par :  Kélian KADDOURI", 16, ARDOISE, italique=True,
         premier=True, aligne=PP_ALIGN.CENTER, police=TITRAGE)
    para(tf, "ENSAE Paris, filière Actuariat  ·  Nexialog Consulting", 14, ARDOISE,
         italique=True, espace_avant=8, aligne=PP_ALIGN.CENTER, police=TITRAGE)
    # La date reste ouverte tant qu'elle n'est pas fixee, et elle s'imprime entre
    # crochets : meme dispositif que la page de garde du memoire, ou un depot
    # avec une date fausse doit etre impossible par inadvertance.
    para(tf, "[jj / mm / 2026]", 14, ACCENT, gras=True, italique=True,
         espace_avant=10, aligne=PP_ALIGN.CENTER, police=TITRAGE)

    tf = zone(s, Inches(0.42), Inches(6.35), Inches(2.90), Inches(0.80))
    para(tf, "Sous la supervision de :", 13, ARDOISE, italique=True, premier=True,
         police=TITRAGE)
    para(tf, "M. Hugo RAPIOR", 14, ARDOISE, gras=True, italique=True,
         espace_avant=6, police=TITRAGE)
    tf = zone(s, Inches(3.95), Inches(6.35), Inches(3.05), Inches(0.80))
    para(tf, "Tutrice académique :", 13, ARDOISE, italique=True, premier=True,
         aligne=PP_ALIGN.RIGHT, police=TITRAGE)
    para(tf, "Caroline HILLAIRET", 14, ARDOISE, gras=True, italique=True,
         espace_avant=6, aligne=PP_ALIGN.RIGHT, police=TITRAGE)

    s.shapes.add_picture(os.path.join(CHARTE, "think_smart.png"),
                         int(Inches(2.30)), int(Inches(7.05)),
                         int(Inches(2.55)), int(Inches(0.34)))
    _numero["n"] += 1                    # la couverture compte, mais ne s'imprime pas
    notes(s, """
[0:20] Ne pas lire la slide. Se presenter, annoncer la duree, et poser la
question tout de suite : combien coute en capital de ne pas se conformer a DORA,
et jusqu'ou ce chiffre peut-il etre affirme.
La date entre crochets est a renseigner avant la soutenance.
""")
    return s


def sommaire(prs, entrees):
    """Le sommaire du gabarit : photographie coupee en haut a gauche, titre
    « SOMMAIRE » en Georgia rouge, carte blanche et barre rouge."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _rect(s, 0, 0, L, H, BLANC)
    _photo_couvrante(s, os.path.join(CHARTE, "photo_section.jpg"), 0, 0,
                     Inches(4.30), H)
    _triangle(s, [(Inches(2.05), 0), (Inches(4.30), 0), (Inches(4.30), Inches(1.60))], BLANC)
    _triangle(s, [(Inches(4.30), Inches(3.55)), (Inches(4.30), H), (Inches(1.15), H)], BLANC)
    s.shapes.add_picture(os.path.join(CHARTE, "nexialog.png"),
                         int(L - Inches(0.55) - Inches(1.62)), int(Inches(0.20)),
                         int(Inches(1.62)), int(Inches(0.59)))

    tf = zone(s, Inches(5.20), Inches(0.80), Inches(7.40), Inches(0.80))
    para(tf, "SOMMAIRE", 40, ACCENT, premier=True, aligne=PP_ALIGN.CENTER,
         police=TITRAGE)

    _rect(s, Inches(1.60), Inches(2.15), Inches(11.15), Inches(2.95), BLANC,
          bord=FILET, epaisseur=0.75)
    _rect(s, Inches(1.60), Inches(5.10), Inches(11.15), Inches(0.12), ACCENT)

    for i, t in enumerate(entrees):
        col, rang = i % 3, i // 3
        x = Inches(1.95) + col * Inches(3.62)
        y = Inches(2.55) + rang * Inches(1.15)
        tf = zone(s, x, y, Inches(3.30), Inches(0.90))
        para(tf, "%02d" % (i + 1), 20, ACCENT, gras=True, premier=True, police=TITRAGE)
        para(tf, t, 14, ARDOISE, gras=True, espace_avant=2)

    _numero["n"] += 1
    tf = zone(s, L - Inches(1.10), Y_PIED, Inches(0.55), Inches(0.28))
    para(tf, str(_numero["n"]), 10, PIED, premier=True, aligne=PP_ALIGN.RIGHT)
    notes(s, """
[0:25] Annoncer le plan en six temps et la duree de chacun, puis passer. Ne pas
commenter les entrees une par une : le jury les relira sur le support.
""")
    return s


def intercalaire(prs, texte):
    """L'intercalaire du gabarit : photographie pleine page, champ blanc en
    chevron borde d'un filet navy, coin navy en haut a droite, signature et titre.

    La geometrie est faite de DEUX polygones superposes, le navy legerement plus
    large que le blanc : leur difference est la bande diagonale. Trois triangles
    empiles, essayes d'abord, laissaient passer la photographie entre eux.
    """
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _rect(s, 0, 0, L, H, BLANC)
    _photo_couvrante(s, os.path.join(CHARTE, "photo_section.jpg"), 0, 0, L, H)
    _triangle(s, [(0, 0), (Inches(3.45), 0), (Inches(8.40), H), (0, H)], PROFOND)
    _triangle(s, [(0, 0), (Inches(3.05), 0), (Inches(8.00), H), (0, H)], BLANC)
    _triangle(s, [(L, 0), (L, Inches(1.70)), (Inches(10.60), 0)], ARDOISE)
    _triangle(s, [(0, 0), (Inches(0.66), 0), (0, Inches(0.98))], ACCENT)
    s.shapes.add_picture(os.path.join(CHARTE, "nexialog_blanc.png"),
                         int(L - Inches(0.45) - Inches(1.55)), int(Inches(0.18)),
                         int(Inches(1.55)), int(Inches(0.56)))

    _rect(s, Inches(1.15), Inches(1.95), Inches(4.55), Inches(0.66), BLANC)
    s.shapes.add_picture(os.path.join(CHARTE, "think_smart.png"),
                         int(Inches(1.75)), int(Inches(2.09)),
                         int(Inches(3.30)), int(Inches(0.40)))

    _rect(s, Inches(0.60), Inches(3.95), Inches(2.60), Pt(5), FILET)
    tf = zone(s, Inches(0.55), Inches(4.45), Inches(5.20), Inches(0.90))
    para(tf, texte, 34, ACCENT, premier=True, police=TITRAGE)

    tf = zone(s, MARGE - Inches(0.35), Y_PIED, Inches(3.0), Inches(0.28))
    para(tf, "www.nexialog.com", 9, PIED, premier=True)
    _numero["n"] += 1
    tf = zone(s, L - Inches(1.10), Y_PIED, Inches(0.55), Inches(0.28))
    para(tf, str(_numero["n"]), 10, PIED, premier=True, aligne=PP_ALIGN.RIGHT)
    return s


def cloture(prs):
    """La diapositive de fin du gabarit."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _rect(s, 0, 0, L, H, BLANC)
    _photo_couvrante(s, os.path.join(CHARTE, "photo_couverture.jpg"),
                     Inches(6.90), 0, L - Inches(6.90), H)
    _triangle(s, [(Inches(6.90), 0), (Inches(6.90), H), (Inches(9.20), H)], BLANC)
    _triangle(s, [(0, 0), (Inches(0.66), 0), (0, Inches(0.98))], ACCENT)
    s.shapes.add_picture(os.path.join(CHARTE, "nexialog.png"),
                         int(Inches(0.55)), int(Inches(0.60)),
                         int(Inches(2.20)), int(Inches(0.80)))

    tf = zone(s, Inches(0.55), Inches(2.85), Inches(6.10), Inches(1.60))
    para(tf, "Merci pour votre attention", 32, ARDOISE, gras=True, premier=True,
         police=TITRAGE)
    para(tf, "Des questions ?", 28, ACCENT, gras=True, espace_avant=16,
         police=TITRAGE)
    _rect(s, Inches(0.55), Inches(4.90), Inches(2.60), Pt(5), ACCENT)
    tf = zone(s, Inches(0.55), Inches(5.20), Inches(6.10), Inches(1.10))
    para(tf, "Dix diapositives de sauvegarde suivent : sources, paramètres, "
             "sévérité, cascade, identifiabilité, bande, canaux, tiers, limites, "
             "glossaire.", 13, GRIS, premier=True)
    s.shapes.add_picture(os.path.join(CHARTE, "think_smart.png"),
                         int(Inches(0.55)), int(Inches(6.80)),
                         int(Inches(2.55)), int(Inches(0.34)))
    _numero["n"] += 1
    tf = zone(s, L - Inches(1.10), Y_PIED, Inches(0.55), Inches(0.28))
    para(tf, str(_numero["n"]), 10, PIED, premier=True, aligne=PP_ALIGN.RIGHT)
    notes(s, """
Slide sobre. Garder l'ecran dessus pendant les questions.
Les dix slides de sauvegarde suivent, et elles s'appellent a la voix.
""")
    return s


def annexe(prs, rang, texte, sous_titre=None):
    """Une diapositive de sauvegarde : meme gabarit, plus un cartouche
    « ANNEXE N » au-dessus du titre."""
    s = nouvelle(prs, pagine=False)
    tf = zone(s, MARGE, Inches(0.22), Inches(3.0), Inches(0.26))
    para(tf, "ANNEXE %d" % rang, 11, ACCENT, gras=True, premier=True)
    dispo = LARG - Inches(1.90)
    tf = zone(s, MARGE, Inches(0.52), dispo, Inches(0.56))
    para(tf, texte, taille_qui_tient(texte, dispo, maxi=24, mini=17), ARDOISE,
         gras=True, premier=True, police=TITRAGE)
    if sous_titre:
        tf2 = zone(s, MARGE, Inches(1.04), dispo, Inches(0.38))
        para(tf2, sous_titre, taille_qui_tient(sous_titre, dispo, maxi=16, mini=13),
             ACCENT, gras=True, premier=True, police=TITRAGE)
    tf = zone(s, L - Inches(1.30), Y_PIED, Inches(0.75), Inches(0.28))
    para(tf, "A%d" % rang, 10, PIED, premier=True, aligne=PP_ALIGN.RIGHT)
    return s


# ---------------------------------------------------------------------------
# Le support
# ---------------------------------------------------------------------------
def construire():
    prs = Presentation()
    prs.slide_width, prs.slide_height = L, H
    _numero["n"] = 0

    couverture(prs)
    sommaire(prs, ["Le vide prudentiel",
                   "La donnée et sa frontière",
                   "La cascade dirigée",
                   "Borner plutôt que poser",
                   "Quatre canaux et le capital",
                   "Décision, limites et suites"])

    # ---- 1. Le probleme metier -------------------------------------------
    s = nouvelle(prs)
    titre(s, "DORA impose une maîtrise, aucun dispositif n'en fait du capital",
          "Règlement (UE) 2022/2554, applicable depuis janvier 2025")
    separation_colonnes(s)
    lg = MILIEU - MARGE - Inches(0.30)
    xd = MILIEU + Inches(0.28)
    ld = L - MARGE - xd

    y = tete(s, MARGE, Y_CORPS, lg, 1, "Un déplacement du centre de gravité prudentiel")
    y += lignes(s, MARGE, y, lg, [
        ("Bâle, puis Solvabilité II, puis DORA : de la couverture financière du "
         "risque vers la continuité opérationnelle", "puce"),
        ("DORA ne remplace pas l'exigence de capital, il en révèle l'angle mort : "
         "la dynamique propre des défaillances technologiques", "puce"),
    ], h=Inches(1.40)) + Inches(0.30)
    y = tete(s, MARGE, y, lg, 2, "L'espace laissé libre par Solvabilité II")
    lignes(s, MARGE, y, lg, [
        ("Dans la Formule Standard, la charge opérationnelle est forfaitaire : "
         "elle n'exprime rien de l'état de conformité de l'entité", "puce"),
        ("Un score qualitatif de conformité ne dit rien du capital qu'une "
         "direction des risques doit immobiliser", "puce"),
        ("Le secteur conserve en revanche le choix méthodologique, et c'est cet "
         "espace que le mémoire occupe", "puce"),
    ])

    # La chaine est VERTICALE, et ce n'est pas un choix de gout : posee en cinq
    # colonnes dans une demi-diapositive, chaque etape n'avait qu'un pouce de
    # large et coupait ses mots au milieu.
    y = tete(s, xd, Y_CORPS, ld, 3, "Le maillon manquant, étape par étape")
    lp = Inches(1.72)
    for i, (t, d) in enumerate([("Non-conformité", "à un ou plusieurs des cinq piliers"),
                                ("Incident TIC", "défaillance, puis propagation"),
                                ("Perte", "opérationnelle et cyber"),
                                ("Capital", "exigence de couverture"),
                                ("Décision", "remédier, détenir ou transférer")]):
        yy = y + i * Inches(0.46)
        b = _rect(s, xd, yy, lp, Inches(0.38), ACCENT if i == 3 else ARDOISE)
        b.text_frame.word_wrap = True
        b.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        para(b.text_frame, t, 12, BLANC, gras=True, premier=True, aligne=PP_ALIGN.CENTER)
        tfd = zone(s, xd + lp + Inches(0.16), yy + Inches(0.09),
                   ld - lp - Inches(0.16), Inches(0.30))
        para(tfd, d, 13, GRIS, premier=True)
    y += Inches(2.30)
    fleche_bas(s, xd + lp / 2 - Inches(0.14), y, Inches(0.28), Inches(0.26))
    bd = _rect(s, xd, y + Inches(0.38), ld, Inches(0.46), ACCENT)
    bd.text_frame.word_wrap = True
    bd.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(bd.text_frame, "Besoin de capital ORSA au titre de DORA", 14, BLANC,
         gras=True, premier=True, aligne=PP_ALIGN.CENTER)
    lignes(s, xd, y + Inches(1.02), ld, [
        ("La Formule Standard donne le même chiffre à une entité exemplaire et à "
         "une entité défaillante : c'est la définition d'un angle mort.", "note"),
    ])
    message(s, "une exigence de maîtrise sans traduction prudentielle, et c'est le vide que ce travail comble.")
    source(s, "Sources : mémoire, chapitres 1 et 2.")
    notes(s, """
[1:30] Le point a faire passer est le MAILLON MANQUANT, pas le reglement. DORA
impose la maitrise de cinq domaines depuis janvier 2025. Aucun module prudentiel
ne traduit ce niveau de maitrise en capital : la Formule Standard charge le
risque operationnel par un pourcentage de primes ou de provisions, donc elle donne
le meme chiffre a une entite exemplaire et a une entite defaillante.
Dire « besoin de capital ORSA au titre de DORA », jamais « le SCR DORA ».
Transition : « la question de ce memoire est donc celle du maillon du milieu. »
""")

    # ---- 2. Question et contribution -------------------------------------
    s = nouvelle(prs)
    titre(s, "Une question en deux temps, et trois apports",
          "Ce qui se chiffre, et ce qui peut être affirmé")
    bd = _rect(s, MARGE, Y_CORPS, LARG, Inches(0.72), CLAIR)
    _rect(s, MARGE, Y_CORPS, Pt(6), Inches(0.72), ACCENT)
    bd.text_frame.word_wrap = True
    bd.text_frame.margin_left = Inches(0.20)
    bd.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(bd.text_frame, "Combien coûte en capital de ne pas se conformer à DORA, "
                        "et jusqu'où ce chiffre peut-il être affirmé ?", 19, ARDOISE,
         gras=True, premier=True, police=TITRAGE)
    lb = (LARG - Inches(0.60)) / 3
    for i, (t, ls, c) in enumerate([
            ("Méthodologique", ["Une cascade dirigée entre domaines",
                                "de contrôle, trois propriétés",
                                "démontrées"], ARDOISE),
            ("Empirique", ["Une frontière d'identifiabilité :",
                           "ce que la donnée ne dit pas,",
                           "et ce qu'elle ne dira jamais"], ACCENT),
            ("Opérationnelle", ["La donnée manquante devient",
                                "une exigence de reporting,",
                                "hiérarchisée par son apport"], ARDOISE)]):
        carte(s, MARGE + i * (lb + Inches(0.30)), Inches(2.80), lb, Inches(2.05),
              t, ls, c, taille=13)
    lignes(s, MARGE, Inches(5.35), LARG, [
        ("La seconde moitié de la question fait le travail : elle interdit de "
         "publier une précision que la donnée ne porte pas.", "fort"),
    ], taille=16)
    message(s, "répondre à la première moitié sans la seconde produirait un chiffre indéfendable.")
    source(s, "Sources : mémoire, chapitre 1, section contribution et plan.")
    notes(s, """
[1:20] Insister sur la SECONDE moitie de la question. Beaucoup de memoires
repondent a la premiere. Celui-ci mesure aussi ce qu'il ne peut pas affirmer, et
c'est ce qui produit la contribution.
""")

    # ---- 3. Les cinq piliers ---------------------------------------------
    s = nouvelle(prs)
    titre(s, "Cinq domaines de contrôle, pas cinq cases à cocher",
          "Et la défaillance de l'un dégrade la tenue des autres")
    piliers = [("P1", ["Gouvernance", "du risque TIC"]),
               ("P2", ["Incidents", "gestion, notification"]),
               ("P3", ["Tests", "de résilience"]),
               ("P4", ["Tiers", "prestataires TIC"]),
               ("P5", ["Partage", "sur les cybermenaces"])]
    lb = (LARG - Inches(0.80)) / 5
    for i, (code, ls) in enumerate(piliers):
        carte(s, MARGE + i * (lb + Inches(0.20)), Y_CORPS + Inches(0.35), lb,
              Inches(2.05), code, ls, ACCENT if code in ("P1", "P4") else ARDOISE,
              taille=14)
    lignes(s, MARGE, Inches(4.55), LARG, [
        ("Une gouvernance défaillante retarde la détection des incidents ; une "
         "dépendance non maîtrisée ouvre une porte que les tests n'ont pas "
         "explorée ; un partage d'information absent prive des trois autres.", "texte"),
        ("En rouge, les deux piliers qui émettent le plus dans la matrice calibrée.",
         "alerte"),
    ], taille=16, interligne=14)
    message(s, "la non-conformité ne reste pas dans son pilier, elle se propage, et c'est ce que le modèle doit porter.")
    source(s, "Sources : mémoire, chapitres 1 et 2 ; matrice de propagation, chapitre 6.")
    notes(s, """
[1:00] Ne PAS reciter le reglement. Le seul point : ce sont des domaines de
CONTROLE, et ils interagissent. Les deux piliers en rouge, gouvernance et tiers,
sont ceux qui emettent le plus dans la matrice calibree. Si on demande pourquoi,
la reponse est au chapitre 6 et la figure est en sauvegarde.
""")

    # ---- 4. Donnee : observable et non observable ------------------------
    s = nouvelle(prs)
    titre(s, "La donnée montre la co-occurrence, jamais la direction",
          "Sept sources, et chacune avec son statut de preuve déclaré")
    separation_colonnes(s)
    lg = MILIEU - MARGE - Inches(0.30)
    xd = MILIEU + Inches(0.28)
    ld = L - MARGE - xd
    carte(s, MARGE, Y_CORPS, lg, Inches(0.34), "Observable", [], ARDOISE, taille=14)
    lignes(s, MARGE, Y_CORPS + Inches(0.52), lg, [
        ("Fréquence des incidents, par année et par entité", "puce"),
        ("Sévérité des pertes, en euros, au-delà d'un seuil", "puce"),
        ("Co-occurrence entre piliers dans un même sinistre", "puce"),
        ("Structure du risque par vecteur d'attaque", "puce"),
    ], taille=15, interligne=13, h=Inches(2.10))
    carte(s, xd, Y_CORPS, ld, Inches(0.34), "Non identifiable", [], ACCENT, taille=14)
    lignes(s, xd, Y_CORPS + Inches(0.52), ld, [
        ("La DIRECTION de la contagion", "puce"),
        ("Quel pilier entraîne l'autre", "puce"),
        ("Une matrice et sa transposée sont indistinguables", "puce"),
        ("Et elles donnent pourtant un capital différent", "puce"),
    ], taille=15, interligne=13, h=Inches(2.10))
    lignes(s, MARGE, Inches(4.40), LARG, [
        ("Deux statuts de preuve sont distingués dans tout le document : la donnée "
         "versionnée et rejouable, et la citation externe non recalculable.", "texte"),
        ("Cette limite n'est pas un manque de données à combler par plus de données "
         "du même type : elle est structurelle, et elle commande la suite.", "alerte"),
    ], taille=15, interligne=13)
    message(s, "la frontière est dans la nature de l'observable, pas dans la taille de l'échantillon.")
    source(s, "Sources : mémoire, chapitre 4 (sources et statuts de preuve) et chapitre 8.")
    notes(s, """
[1:30] C'est la slide qui PREPARE le coeur. Annoncer les deux colonnes, et
surtout dire que la colonne de droite n'est pas un manque de donnees a combler
par plus de donnees du meme type : elle est structurelle. La demonstration
arrive deux slides plus loin.
""")

    # ---- 5. Architecture --------------------------------------------------
    s = nouvelle(prs)
    titre(s, "D'un état de conformité à une décision, en quatre étages",
          "Deux canaux calibrables, deux canaux bornés")
    lb = (LARG - Inches(0.72)) / 4
    etages = [("État de conformité", ["par pilier,", "chaîne de Markov"], ARDOISE),
              ("Quatre canaux", ["fréquence, détection,", "propagation, accumulation"], ACCENT),
              ("Perte annuelle", ["fréquence et sévérité,", "cascade entre piliers"], ARDOISE),
              ("Capital et décision", ["quantile à 99,5 %,", "remédier ou transférer"], ARDOISE)]
    for i, (t, ls, c) in enumerate(etages):
        chevron(s, MARGE + i * (lb + Inches(0.24)), Y_CORPS + Inches(0.22), lb,
                Inches(0.50), t, c, taille=13)
        lignes(s, MARGE + i * (lb + Inches(0.24)), Y_CORPS + Inches(0.84), lb,
               [(x, "note") for x in ls], taille=12, interligne=3, h=Inches(0.70))
    separation_colonnes(s, haut=Inches(3.55), bas=Inches(5.85))
    lg = MILIEU - MARGE - Inches(0.30)
    xd = MILIEU + Inches(0.28)
    ld = L - MARGE - xd
    y = tete(s, MARGE, Inches(3.55), lg, 1, "Calibrés sur données")
    lignes(s, MARGE, y, lg, [
        ("Fréquence des incidents", "puce"),
        ("Taux de détection des pertes", "puce"),
        ("Ces deux canaux portent un intervalle estimé.", "note"),
    ], taille=15, interligne=11, h=Inches(2.0))
    y = tete(s, xd, Inches(3.55), ld, 2, "Bornés, non calibrés")
    lignes(s, xd, y, ld, [
        ("Gain de propagation entre piliers", "puce"),
        ("Accumulation par prestataire commun", "puce"),
        ("Ces deux canaux portent un scénario borné, et leur part n'est pas un "
         "budget de remédiation.", "note"),
    ], taille=15, interligne=11, h=Inches(2.0))
    message(s, "le modèle est partiellement calibré et partiellement borné, et le document dit lequel est lequel.")
    source(s, "Sources : mémoire, chapitres 5 à 10.")
    notes(s, """
[1:30] Donner la chaine complete en une fois, sans notation. Le point a ne pas
rater : deux canaux CALIBRABLES, deux canaux BORNES. C'est la distinction qui
revient a la fin sur les limites, et c'est elle qui interdit d'additionner les
quatre leviers pour chiffrer une remediation partielle.
""")

    # ---- 6. Pourquoi une cascade dirigee ---------------------------------
    s = nouvelle(prs)
    titre(s, "L'ordre de propagation change la criticité",
          "Ce qu'une structure de dépendance symétrique ne peut pas voir")
    figure(s, "H1_reseau_W.png")
    message(s, "une copule capture la co-occurrence des pertes, mais symétriquement : elle ne distingue pas ce qui entraîne de ce qui subit.")
    source(s, "Sources : mémoire, chapitre 6 ; figure produite par le script 29 ; comparaison au jumeau copule, chapitre 10.")
    notes(s, """
[1:30] Le point intuitif : une gouvernance defaillante retarde la detection des
incidents ; l'inverse n'est pas vrai au meme degre. Une dependance symetrique
donne le meme nombre dans les deux sens, donc elle ne peut pas servir a
prioriser une remediation. La cascade, si.
Ne PAS entrer dans la normalisation de Leontief : slide de sauvegarde.
""")

    # ---- 7. La non-identifiabilite ---------------------------------------
    s = nouvelle(prs)
    titre(s, "La direction n'est pas identifiable, et c'est un résultat",
          "Le coeur du mémoire")
    xd = figure_gauche(s, "Z11_reversibilite_martingale.png")
    ld = L - MARGE - xd
    lignes(s, xd, Y_CORPS + Inches(0.25), ld, [
        ("La matrice se décompose en une partie symétrique et une partie "
         "antisymétrique.", "texte"),
        ("La donnée identifie la première, la co-occurrence.", "fort"),
        ("Elle n'identifie pas la seconde, la direction.", "alerte"),
        ("Une matrice et sa transposée sont indistinguables pour la donnée, et "
         "donnent pourtant un capital et une décision différents.", "texte"),
        ("Ce n'est pas un échec du modèle : c'est ce qui interdit de publier une "
         "direction comme si elle avait été observée.", "note"),
    ], taille=15, interligne=15)
    message(s, "un résultat d'identification, et non une limite de l'estimation.")
    source(s, "Sources : mémoire, chapitre 8 ; script 40.")
    notes(s, """
[2:00] LA SLIDE DU MEMOIRE. Prendre le temps.
Trois phrases : la matrice se decompose en symetrique plus antisymetrique ; la
donnee identifie la co-occurrence, donc la partie symetrique ; une matrice et sa
transposee sont indistinguables pour la donnee et donnent pourtant un capital et
une decision DIFFERENTS.
Dire explicitement : ce n'est pas un echec, c'est un resultat d'identification.
Transition : « la question devient donc : que publie-t-on quand on ne peut pas
identifier ? »
""")

    # ---- 8. Du point a la bande ------------------------------------------
    s = nouvelle(prs)
    titre(s, "Du point à la bande : borner plutôt que poser",
          "Identification partielle sur l'ensemble des matrices admissibles")
    xd = figure_gauche(s, "Z_identification_partielle.png")
    ld = L - MARGE - xd
    lignes(s, xd, Y_CORPS + Inches(0.25), ld, [
        ("Plutôt que de poser la direction, le capital est borné sur l'ensemble "
         "des matrices compatibles avec ce que la donnée identifie.", "texte"),
        ("1 024 sommets, énumérés exhaustivement", "fort"),
        ("L'ignorance directionnelle se paye linéairement, et son coût maximal est "
         "connu d'avance : c'est plus favorable qu'un intervalle de confiance "
         "ordinaire.", "texte"),
        ("Le niveau affiché reste illustratif.", "alerte"),
    ], taille=15, interligne=15)
    message(s, "la bande quantifie une incertitude structurelle au lieu de la masquer derrière un point.")
    source(s, "Sources : mémoire, chapitre 9 ; scripts 30 et 40.")
    notes(s, """
[2:00] Le mecanisme : plutot que de poser la direction, on borne le capital sur
l'ENSEMBLE des matrices compatibles avec ce que la donnee identifie. 1 024
sommets, enumeration exhaustive, donc pas un echantillonnage.
Le point qui plait a un jury : le cout de l'ignorance est LINEAIRE et son maximum
est connu d'avance, ce qui est plus favorable qu'un intervalle de confiance
ordinaire.
Precaution a exprimer : le NIVEAU affiche est illustratif ; c'est le rapport et la
hierarchie qui sont defendus.
""")

    # ---- 9. Les quatre canaux -------------------------------------------
    s = nouvelle(prs)
    titre(s, "Quatre canaux déplacés, et leurs effets ne s'additionnent pas",
          "Au secteur, et non à l'échelle d'une entité")
    figure(s, "S24_interaction_canaux.png", bas=Inches(2.85))
    lignes(s, MARGE, Inches(4.85), LARG, [
        ("Au secteur, le besoin de capital passe de 6 049 à 20 188 M€, soit un "
         "facteur 3,34. La non-conformité n'ajoute aucune pénalité : elle déplace "
         "quatre paramètres de la loi de perte.", "texte"),
    ], taille=14, h=Inches(0.70))
    lc = (LARG - Inches(0.48)) / 3
    for i, (t, v) in enumerate([("Canaux isolés", "9 138 M€"),
                                ("Écart total", "14 139 M€"),
                                ("Interaction", "5 001 M€, soit 35 %")]):
        b = _rect(s, MARGE + i * (lc + Inches(0.24)), Inches(5.58), lc,
                  Inches(0.58), CLAIR, bord=FILET, epaisseur=0.75)
        b.text_frame.word_wrap = True
        b.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        morceaux(b.text_frame, [(t + "   ", GRIS, False, POLICE),
                                (v, ACCENT, True, POLICE)], 14, premier=True,
                 aligne=PP_ALIGN.CENTER)
    message(s, "remédier un canal rapporte davantage à une entité défaillante partout : c'est la colonne de fermeture qu'un plan doit citer.")
    source(s, "Sources : mémoire, chapitre 10 ; scripts 43 et 68.")
    notes(s, """
[1:40] Trois nombres, pas plus : 9 138, 14 139, 5 001.
Dire d'abord AU SECTEUR. Sans ce mot, le jury lit vingt milliards pour une entite
et la question de l'echelle part avant qu'on ait pu la cadrer.
Dire le mecanisme : les canaux isoles ne somment pas au total parce que la
cascade est super-additive SUR SES CANAUX. Ajouter aussitot la nuance qui evite
une erreur : elle est quasi additive sur les PILIERS, et l'additivite des COUTS
au sein d'un sinistre est une troisieme chose, une hypothese non testee.
NE JAMAIS additionner les quatre leviers pour chiffrer une remediation partielle :
deux des quatre sont des bornes posees, pas des budgets.
""")

    # ---- 10. Les tiers ----------------------------------------------------
    s = nouvelle(prs)
    titre(s, "Le pilier des tiers concentre, il ne propage pas seulement",
          "Contagion et accumulation sont deux mécanismes distincts")
    figure(s, "Z9_p4_accumulation.png", bas=Inches(2.20))
    lignes(s, MARGE, Inches(5.55), LARG, [
        ("Un prestataire commun crée un choc partagé entre entités : ce n'est plus "
         "de la contagion d'un pilier vers un autre dans une même entité, c'est de "
         "l'accumulation.", "texte"),
    ], taille=14, h=Inches(0.70))
    message(s, "c'est exactement ce que DORA demande de cartographier : la dépendance à des prestataires TIC critiques.")
    source(s, "Sources : mémoire, annexe C (adaptations par pilier) ; script 22.")
    notes(s, """
[1:00] Distinguer les deux mecanismes, parce qu'un jury les confond souvent :
la CONTAGION va d'un pilier a l'autre dans une meme entite ; l'ACCUMULATION vient
d'un prestataire commun a plusieurs entites. Le modele porte les deux, par deux
canaux differents.
Reserve a exprimer si on insiste : le canal d'accumulation est une borne posee,
pas une calibration.
""")

    # ---- 11. La donnee manquante devient un livrable ---------------------
    s = nouvelle(prs)
    titre(s, "La donnée manquante devient une exigence de reporting",
          "Le registre d'incidents comme instrument de capital")
    xd = figure_gauche(s, "Z18_valeur_information.png")
    ld = L - MARGE - xd
    y = tete(s, xd, Y_CORPS + Inches(0.25), ld, 1,
             "Quatre champs, hiérarchisés par ce qu'ils resserrent")
    lignes(s, xd, y, ld, [
        ("Horodatage des incidents", "alerte"),
        ("Domaine de contrôle touché", "alerte"),
        ("Cause commune consolidée", "alerte"),
        ("Champs renseignés obligatoires", "alerte"),
        ("Le modèle ne dit pas seulement qu'il manque une donnée : il dit laquelle, "
         "et ce qu'elle rapporte en resserrement de bande.", "note"),
    ], taille=15, interligne=13)
    message(s, "chaque champ renseigné resserre la bande, et la limite de données devient un livrable.")
    source(s, "Sources : mémoire, chapitre 12 ; script 55.")
    notes(s, """
[1:40] L'UNE DES DEUX SLIDES LES PLUS IMPORTANTES, avec la non-identifiabilite.
C'est la que la limite devient un livrable : le modele ne dit pas seulement
« il manque une donnee », il dit LAQUELLE et CE QU'ELLE RAPPORTE en resserrement
de bande.
C'est aussi la recommandation la plus directement actionnable par une direction
des risques, et celle qu'une relecture de praticien a confirmee comme deja
pratiquee sous une autre forme.
""")

    # ---- 12. Decision pour l'entite --------------------------------------
    s = nouvelle(prs)
    titre(s, "Trois décisions, et une confusion à ne pas commettre",
          "Ce que la borne autorise, et ce qu'elle n'autorise pas")
    lb = (LARG - Inches(0.60)) / 3
    for i, (t, ls) in enumerate([
            ("Remédier", ["Prioriser les canaux calibrables :",
                          "fréquence et détection"]),
            ("Détenir", ["Le capital immobilisé coûte",
                         "chaque année, pas une seule fois"]),
            ("Transférer", ["Comparer au prix de marché",
                            "du même risque"])]):
        carte(s, MARGE + i * (lb + Inches(0.30)), Y_CORPS + Inches(0.30), lb,
              Inches(1.90), t, ls, ARDOISE, taille=13)
    bd = _rect(s, MARGE, Inches(4.40), LARG, Inches(0.80), CLAIR)
    _rect(s, MARGE, Inches(4.40), Pt(6), Inches(0.80), ACCENT)
    bd.text_frame.word_wrap = True
    bd.text_frame.margin_left = Inches(0.20)
    bd.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(bd.text_frame, "Une borne de capital n'est pas un budget de remédiation : "
                        "deux des quatre canaux sont des bornes posées, et leur part "
                        "n'est pas une enveloppe à dépenser.", 15, ACCENT, gras=True,
         premier=True)
    lignes(s, MARGE, Inches(5.50), LARG, [
        ("Le bénéfice d'une remédiation a deux composantes, et la plus grosse n'est "
         "pas le capital libéré mais la perte évitée.", "texte"),
    ], taille=14, h=Inches(0.60))
    message(s, "le retour calculé sur le seul portage de capital est un majorant, pas un plancher.")
    source(s, "Sources : mémoire, chapitre 10 ; scripts 50 et 83.")
    notes(s, """
[1:20] Les trois decisions, puis la mise en garde, qui est le vrai message.
Si on demande un chiffre de retour sur investissement : le retour calcule sur le
seul portage de capital est un MAJORANT, pas un plancher, parce que la seconde
composante du benefice, la sinistralite evitee, n'est pas monetisee dans ce
calcul. Ne pas donner le nombre d'annees sans dire le sens de la borne.
""")

    # ---- 13. Limites ------------------------------------------------------
    s = nouvelle(prs)
    titre(s, "Ce que ce travail n'établit pas, et ce qui tient malgré cela",
          "Les deux colonnes se présentent ensemble, jamais la gauche seule")
    separation_colonnes(s)
    lg = MILIEU - MARGE - Inches(0.30)
    xd = MILIEU + Inches(0.28)
    ld = L - MARGE - xd
    carte(s, MARGE, Y_CORPS, lg, Inches(0.34), "Non établi", [], ACCENT, taille=14)
    lignes(s, MARGE, Y_CORPS + Inches(0.52), lg, [
        ("La direction de contagion n'est pas identifiée", "puce"),
        ("Le niveau absolu est illustratif, et c'est une borne supérieure à "
         "l'échelle d'une entité", "puce"),
        ("L'incertitude de queue est large", "puce"),
        ("Deux canaux sur quatre sont bornés, non calibrés", "puce"),
        ("Le niveau de sévérité dérive dans le temps, et le backtest le mesure", "puce"),
    ], taille=14, interligne=11, h=Inches(2.85))
    carte(s, xd, Y_CORPS, ld, Inches(0.34), "Établi malgré cela", [], ARDOISE, taille=14)
    lignes(s, xd, Y_CORPS + Inches(0.52), ld, [
        ("Le signe et l'ordre de l'écart entre états", "puce"),
        ("La hiérarchie des piliers par contribution", "puce"),
        ("Le cadre de bornage et son coût, mesuré", "puce"),
        ("La recommandation de reporting et sa priorité", "puce"),
        ("La loi de comptage et la forme de la queue, validées hors échantillon", "puce"),
    ], taille=14, interligne=11, h=Inches(2.85))
    lignes(s, MARGE, Inches(5.30), LARG, [
        ("Une thèse de départ a été réfutée par son auteur, et un chiffre d'entité "
         "requalifié en borne supérieure. Ce sont des résultats.", "alerte"),
    ], taille=15, h=Inches(0.60))
    message(s, "ces limites sont publiées, pas concédées, et c'est ce qui rend le reste défendable.")
    source(s, "Sources : mémoire, chapitre 11, table des limites en deux colonnes.")
    notes(s, """
[1:10] Presenter les deux colonnes ENSEMBLE, jamais la gauche seule.
Insister sur un point que le texte de l'Institut recompense explicitement : la
non-transitivite, qui donnait son titre au projet, a ete REFUTEE par son auteur,
et le chiffre d'entite a ete requalifie en borne superieure. Ce sont des
resultats, pas des faiblesses.
""")

    # ---- 14. Conclusion ---------------------------------------------------
    s = nouvelle(prs)
    titre(s, "Trois messages", "Et la réponse à la question posée en ouverture")
    for i, (t, d) in enumerate([
            ("La non-conformité à DORA se traduit en coût de risque et en capital",
             "par le déplacement de quatre paramètres de la loi de perte, et non "
             "par une pénalité ajoutée"),
            ("La dépendance directionnelle ne doit pas être calibrée sur des "
             "données qui ne l'identifient pas",
             "d'où une bande, et le coût de l'ignorance mesuré plutôt que masqué"),
            ("La limite de données devient une recommandation actionnable",
             "pour l'entité comme pour le régulateur, hiérarchisée par ce que "
             "chaque champ rapporte")]):
        y = Y_CORPS + Inches(0.15) + i * Inches(1.05)
        tf = zone(s, MARGE, y, LARG, Inches(0.95))
        morceaux(tf, [("%d.   " % (i + 1), ACCENT, True, TITRAGE),
                      (t, ARDOISE, True, POLICE)], 16, premier=True)
        para(tf, "      " + d, 14, GRIS, espace_avant=4)
    bd = _rect(s, MARGE, Inches(4.95), LARG, Inches(1.05), CLAIR)
    _rect(s, MARGE, Inches(4.95), Pt(6), Inches(1.05), ACCENT)
    bd.text_frame.word_wrap = True
    bd.text_frame.margin_left = Inches(0.22)
    bd.text_frame.margin_right = Inches(0.22)
    bd.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(bd.text_frame, "Quand la dépendance n'est pas identifiable, la bonne "
                        "réponse actuarielle n'est pas la fausse précision : c'est "
                        "une borne, une hiérarchie de données et une décision mieux "
                        "informée.", 17, ARDOISE, gras=True, premier=True,
         police=TITRAGE)
    source(s, "Sources : mémoire, chapitre 13.")
    notes(s, """
[0:30] Trois phrases, puis la phrase encadree, dite lentement et sans la lire mot
a mot. C'est la derniere chose que le jury entend avant les questions : elle doit
etre la reponse a la question posee au debut.
""")

    cloture(prs)

    # ======================================================================
    # SAUVEGARDE
    # ======================================================================
    intercalaire(prs, "Annexes")

    def sauv(rang, t, sous, items=None, fig=None, src="", note=""):
        s = annexe(prs, rang, t, sous)
        if fig:
            figure(s, fig, haut=Inches(1.62), bas=Inches(0.62))
        if items:
            lignes(s, MARGE, Inches(1.72), LARG, items, taille=16, interligne=14,
                   h=Inches(4.90))
        source(s, src)
        notes(s, note)
        return s

    sauv(1, "Sept sources, et chacune avec son statut de preuve",
         "Ce qui est rejouable, et ce qui ne l'est pas",
         [("Sévérité en euros : base internationale de pertes opérationnelles", "fort"),
          ("Chronologie de brèches : fréquence et étude d'événement", "puce"),
          ("Corpus de rapports post-mortem : structure de la direction", "puce"),
          ("États réglementaires publiés : quatre bilans réels, anonymisés", "puce"),
          ("Comptage d'incidents par vecteur : structure, jamais niveau", "puce"),
          ("Étude de marché cyberassurance : contexte, aucune calibration", "puce"),
          ("Deux statuts distingués : versionné et rejouable, ou citation externe "
           "non recalculable", "fort")],
         src="Sources : mémoire, chapitre 4 ; scripts 62 et 63.",
         note="Si le jury demande la tracabilite : chaque nombre publie sort d'un script versionne, et un harnais verifie les 2 346 nombres du document.")

    sauv(2, "Les paramètres, et ce qui est estimé, posé ou gelé",
         "La thèse dépend de l'ordre, pas du niveau",
         [("Sévérité : loi de Pareto généralisée au-delà du seuil, indice de queue 0,5954", "puce"),
          ("Seuil 20,03 M€, 91 excès, calibration gelée depuis le 7 août 2026", "puce"),
          ("Fréquence : binomiale négative, validée hors échantillon", "puce"),
          ("Gain de propagation : trois valeurs POSÉES, 0,45 / 0,68 / 0,90", "alerte"),
          ("Le capital est croissant en ce gain : l'ordre suffit à produire l'écart, "
           "l'amplitude est un scénario", "fort")],
         src="Sources : mémoire, annexe D ; scripts 07, 08b, 63 et 66.",
         note="Le point qui desamorce la question sur les valeurs posees : la these ne depend pas de leur niveau mais de leur ORDRE, et la monotonie est demontree.")

    sauv(3, "Pourquoi une loi de valeurs extrêmes pour la sévérité",
         "Adéquation, et ce que le backtest valide",
         fig="J3_validation_adequation.png",
         src="Sources : mémoire, chapitre 5 ; scripts 07 et 47.",
         note="Deux theoremes autorisent l'extrapolation au-dela du plus grand sinistre observe. L'ajustement passe Anderson-Darling et Kolmogorov-Smirnov. Le backtest hors echantillon valide la FORME de la queue ; le NIVEAU derive, et c'est declare.")

    sauv(4, "La cascade est un processus de branchement sous-critique",
         "Rayon spectral et taux de reproduction",
         fig="K3_branchement_R0.png",
         src="Sources : mémoire, chapitre 6 ; script 03.",
         note="Rayon spectral 0,506, taux de reproduction 0,054 : la cascade s'eteint. La normalisation de Leontief garantit que le pilier le plus prolifique engendre au plus g descendants directs.")

    sauv(5, "Ce que le corpus documentaire corrobore, et ce qu'il ne lève pas",
         "Le biais de narration est mesuré, borné, et non levé",
         fig="Z17_postmortem_direction.png",
         src="Sources : mémoire, chapitre 8 ; scripts 53, 59 et 64.",
         note="Le corpus donne un signal de direction, mais il porte un biais de narration : une narration choisit un ordre. Le biais est MESURE, borne et non leve. Une relecture de praticien a donne un exemple compatible avec les deux explications, ce qui corrobore la frontiere et non la matrice.")

    sauv(6, "La bande de capital et ses trois étages d'incertitude",
         "Trois sources à ne jamais fondre en une seule barre",
         fig="J4_bande_modele.png",
         src="Sources : mémoire, chapitre 11 ; script 48.",
         note="Trois etages a ne jamais fondre en une seule barre : le bruit de calcul, reductible par la machine ; l'incertitude de parametre, portable par un intervalle ; et l'ambiguite de famille, epistemique, qui ne se moyenne pas.")

    sauv(7, "L'attribution par canal : trois lectures non interchangeables",
         "Isolée, fermeture et Shapley répondent à trois questions",
         fig="S15_allocation_shapley_euler.png",
         src="Sources : mémoire, chapitre 10 ; scripts 68 et 82.",
         note="Isolee, fermeture et Shapley repondent a trois questions differentes. Shapley est la seule colonne additive, mais c'est une CONVENTION d'attribution : deux canaux sur quatre sont des bornes, leur part n'est pas un budget. L'intuition suffit, ne pas ecrire la formule.")

    sauv(8, "Défaillances simultanées : une sortie du modèle, pas une lacune",
         "La loi est exacte, par énumération de la progéniture",
         fig="S30_defaillances_simultanees.png",
         src="Sources : mémoire, annexe D ; script 74.",
         note="PIEGE DE PREMISSE FREQUENT. A l'etat non conforme, 62,31 % des sinistres touchent plus d'un pilier, contre 31,15 % a l'etat conforme. La loi est EXACTE, par enumeration de la progeniture, donc citable sans bruit.")

    sauv(9, "Les hypothèses, par ordre de ce qu'elles coûtent",
         "La fragilité est dans la queue, pas dans la contagion",
         fig="S32_tornado_normalise.png",
         src="Sources : mémoire, annexe D ; scripts 76 et 81.",
         note="Resultat contre-intuitif a assumer : la fragilite est dans l'ajustement de valeurs extremes, PAS dans la contagion. L'hypothese la plus lourde et non testee est l'additivite des couts au sein d'un sinistre.")

    sauv(10, "Glossaire", "Et la distinction qui a produit une confusion en séance",
         [("DORA : règlement européen sur la résilience opérationnelle numérique", "puce"),
          ("SCR : capital de solvabilité requis sous Solvabilité II", "puce"),
          ("VaR : quantile de la charge annuelle agrégée, ici à 99,5 %", "puce"),
          ("Quantile de sévérité : quantile d'un sinistre isolé, ce n'est pas une "
           "mesure de capital", "alerte"),
          ("GPD : loi de Pareto généralisée, pour les excès au-delà d'un seuil", "puce"),
          ("Copule : structure de dépendance symétrique, sans direction", "puce"),
          ("Shapley : convention d'attribution d'un effet total entre leviers", "puce"),
          ("Cascade : propagation dirigée entre domaines de contrôle", "puce")],
         src="Sources : mémoire, annexe F, table des notations.",
         note="La distinction en rouge est celle qui a produit une confusion en seance le 7 aout 2026 : le quantile de severite d'un sinistre n'est pas une mesure de capital.")

    prs.save(SORTIE)
    n = len(prs.slides.__iter__.__self__._sldIdLst)
    print(f"ecrit  {os.path.relpath(SORTIE, ICI)}")
    print(f"       {n} diapositives : {_numero['n']} numerotees (couverture, sommaire,")
    print(f"       14 de contenu, cloture), 1 intercalaire, 10 de sauvegarde")


if __name__ == "__main__":
    construire()
