# Démarrage sur un poste neuf

Page de prise en main. Deux minutes de lecture, puis une commande.
Le fond est dans `CLAUDE.md`, l'état daté et le journal dans `REPRISE.md`.

---

## En une commande

```bash
python exploratory/memoire_cascade/refaire_tout.py
```

Elle **génère** la version Institut depuis la version ENSAE, **compile** les deux,
**contrôle** tout ce que le projet exige, passe le **harnais** sur les vingt-cinq chapitres,
**recopie** les deux fichiers déposés et **nettoie** les intermédiaires. Elle rend `0` si tout
passe, `1` sinon, et elle nomme chaque contrôle en échec.

Elle commence par vérifier les prérequis, donc elle s'arrête en trois secondes s'il en manque un
plutôt que de le découvrir après trois minutes de compilation.

Ajouter `--sans-harnais` pour sauter l'étape la plus lente quand on n'a touché qu'à la mise en
page.

---

## Ce qui n'est pas dans le dépôt, et qu'il faut apporter

| Quoi | Pourquoi il n'y est pas | Sans lui |
|---|---|---|
| `data/raw/` | donnée **sous licence**, ne jamais committer | le mémoire compile ; **aucun script d'analyse ne tourne** |
| `memoire/tectonic` | binaire, ~30 Mo, propre à l'OS | rien ne compile |
| `.venv/` | environnement Python | rien ne tourne |

**La donnée brute n'est nécessaire que pour rejouer un calcul.** Le mémoire se compile sans elle :
tous les nombres publiés vivent dans `sorties_verif/`, qui est versionné.

```bash
# environnement
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install 'matplotlib==3.11.0'   # version EXACTE, voir plus bas
```

**tectonic** se pose dans `memoire/`, sous le nom `tectonic.exe` (Windows) ou `tectonic` (macOS).
`refaire_tout.py` le cherche là, puis dans le PATH.

---

## Les deux PDF sont lisibles sans rien installer

Depuis le 22 septembre 2026, `main_ensae.pdf` et `main_institut.pdf` sont **versionnés**. Un
clone suffit donc pour lire le mémoire.

| Fichier | Quoi |
|---|---|
| `exploratory/memoire_cascade/main_ensae.pdf` | **le mémoire déposé à l'ENSAE**, avec le chapitre du stage |
| `exploratory/memoire_cascade/main_institut.pdf` | **la version Institut des Actuaires**, identique sauf le stage |

Les deux copies au nom imposé (`KADDOURI_Kelian_3A25.pdf`, `KADDOURI_Kelian_institut.pdf`) restent
ignorées : elles sont identiques à l'octet à leur source et `refaire_tout.py` les régénère.

---

## Les quatre chiffres à connaître avant de toucher quoi que ce soit

| Grandeur | Valeur | Ce qui se passe si on l'ignore |
|---|---|---|
| **Pages, version ENSAE** | **195**, limite **impérative 200** | on dépasse sans s'en apercevoir |
| **Débordements, ligne de base** | **2** | comparer à 5 ou 6 fait passer des débordements neufs pour normaux |
| **Harnais** | **1 881 sur 1 881** | — |
| **Hors contrôle non déclaré** | **0**, et c'est lui qui compte | un taux de 100 % peut masquer une section entière hors contrôle |

La ligne de base est passée de 5 à 2 le 22 septembre : les marges élargies en ont absorbé trois.

---

## Les cinq pièges qui ont déjà coûté du temps

1. **tectonic écrit ses avertissements sur `stderr`.** Un `> log.txt` ne capture **rien** des
   débordements, et le contrôle passe à vide en donnant zéro partout. Deux contrôles ont été
   annoncés faux le 9 septembre pour cette raison. `refaire_tout.py` capture les deux flux.
2. **Le contrôle « 0 référence indéfinie » ne se lit pas dans la sortie de tectonic**, qui n'émet
   aucun avertissement pour un `\ref` cassé : un grep renvoie zéro quoi qu'il arrive. Cinq
   « cité au chapitre ?? » ont ainsi été publiés. Le seul test fiable **compte les `??` sur le
   PDF produit**.
3. **Les débordements se comptent par emplacement, pas par ligne d'avertissement.** Les deux
   passes de tectonic ne donnent pas toujours la même largeur au dernier chiffre, et le même
   paragraphe ressort alors deux fois.
4. **Les fichiers déposés se périment à la moindre recompilation.** On a déjà demandé si le
   fichier était prêt à envoyer alors que la copie avait une heure douze de retard.
5. **Épingler `matplotlib==3.11.0`.** Le numéro de version est écrit dans les métadonnées du PNG :
   en 3.11.1 les pixels sont identiques mais le fichier diffère de cinq octets, et `git status`
   signale alors comme modifiée une figure qui ne l'est pas.

---

## Où sont les choses

| Quoi | Où |
|---|---|
| Contexte de fond, conventions, décisions | `CLAUDE.md` |
| État daté, journal, pièges cumulés | `REPRISE.md` |
| Fichier maître | `exploratory/memoire_cascade/main_ensae.tex` |
| Version Institut, **générée** | `build_institut.py` → `main_institut.tex`, ne pas l'éditer |
| Chapitres | `exploratory/memoire_cascade/chapitres/*.tex` |
| Préambule et style | `exploratory/memoire_cascade/preambule_v2.tex` |
| Scripts de calcul | `exploratory/vasicek_lab/<N>_<theme>/<num>_<nom>.py` |
| Sorties versionnées, **source de tous les nombres publiés** | `sorties_verif/NN.txt` |
| Harnais, un chapitre | `verif_chiffres.py <sorties_verif> <chapitre.tex>` |
| Contrôles PDF seuls | `controles_memoire.py` |

---

## Le point ouvert du 22 septembre

**Le script 106 est écrit mais n'a jamais tourné**, faute de `data/raw/` sur le poste où il a été
écrit. Il mesure si **une seule observation commande l'estimation de la queue**, ce que le mémoire
ne publie nulle part — c'est une question qu'un jury pose devant une queue ajustée sur 91 excès.

```bash
.venv/bin/python exploratory/vasicek_lab/1_fondations/106_influence_plus_grosses_pertes.py \
    > sorties_verif/106.txt
```

Il **refuse de tourner** si l'échantillon a dérivé : le compte d'excès doit valoir exactement 91
et $\hat\xi$ rester à moins de 5 % de la valeur gelée. Ce garde-fou a été éprouvé à vide.

**Aucun texte n'a été écrit au mémoire à son sujet, et c'est délibéré** : rédiger le commentaire
avant d'avoir lu la sortie est l'erreur que ce dossier a commise sept fois et qu'il documente.
