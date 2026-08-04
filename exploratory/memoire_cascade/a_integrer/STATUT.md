# ARCHIVE MORTE : ne rien lire ici comme un état du mémoire

Ce dossier n'est **appelé par aucun `\input`** de `main.tex`. Il ne compile pas, il ne
contribue à rien, et son contenu est **antérieur** au mémoire vivant. Vérifié le 4 août 2026.

Le mémoire vivant est `../main.tex` + `../chapitres/`. Rien d'autre.

## Pourquoi ce dossier est un piège

1. **`version_autonome/` duplique trois chapitres vivants** dans un état périmé :
   - `chapitre_identifiabilite.tex` → remplacé par `../chapitres/09_identifiabilite.tex`
   - `chapitre_positionnement.tex` → remplacé par `../chapitres/03_etat_art_positionnement.tex`
   - `chapitre_robustesse.tex` → remplacé par `../chapitres/13_inventaire_hypotheses.tex`
     et `../chapitres/17_pieces_justificatives.tex`

2. **Plusieurs squelettes portent la non-transitivité comme un chantier à faire**
   (`01_introduction.tex`, `04_modele_cascade.tex`, `12_conclusion.tex`, et
   `version_autonome/chapitre_positionnement.tex`). Cette revendication est **réfutée** :
   zéro violation de transitivité sur 420 triplets, valeur propre minimale +0,405, zéro
   cycle. Le mémoire vivant l'a retirée et l'a remplacée par la dépendance à l'ordre. La
   figure `G1_non_transitivite.png` n'est plus utilisée nulle part.

3. **`07_elicitation.tex` et `B_elicitation.tex`** décrivent un chantier d'élicitation qui
   n'aura pas lieu.

4. **`macros_requises.tex`** n'est chargé par personne : les macros vivantes sont dans
   `../preambule.tex`.

## Que faire

Le dossier est conservé pour l'historique de rédaction seulement. Il peut être supprimé
sans aucun effet sur la compilation (git en garde la trace). Ne pas y reprendre de texte
sans le confronter au chapitre vivant correspondant.
