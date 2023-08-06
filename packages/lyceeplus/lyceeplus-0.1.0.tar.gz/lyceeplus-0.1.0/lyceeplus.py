# -*- coding: utf-8 -*-
#

"""
Le module lycee est un module python réalisé par le groupe AMIENS PYTHON
est à pour objectif de simplifier un certain nombre de manipulations
avec python au lycée (cosinus en degré, calcul d'une moyenne d'une liste,
représentation statistiques variées, ...)

Pour l'utiliser, il suffit d'ajouter en début de programme

from lycee import *
"""

import math
import random as alea

import matplotlib.axes
import matplotlib.pyplot as plot
import numpy
from matplotlib.patches import Rectangle, Polygon, Circle
import numpy as np
import builtins
from scipy.stats import norm, linregress

__version__ = '2.6'
__angle_mode_str: str = "rad"
__angle_mode = 1

print("...module lycee actif....")
pi = math.pi
AlphabetAP = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;!?&àâéèêëîïù#'(-_){}[]|\@=+°§$<>%*/"
reel = float
entier = int
nombre = reel | entier
__figure, __axe = None, None
__ligne, __colonne = 0, 0
__ligne_max, __colonne_max = 0, 0
__fill_color = "grey"
__no_fill = False
__stroke = "blue"
__stroke_width = 1
__xmini = __xmaxi = __ymini = __ymaxi = None
__grille = True
__abscisse = "x"
__ordonnee = "y"
__repere = False
x, y, z = 0, 0, 0
__couleur = ["r","g","c","m","y","b","w"]

def set_x_min_max(xmini,xmaxi):
    """initialise les valeurs xmini et xmaxi d'un graphique"""
    global __xmini,__xmaxi
    __xmini = xmini
    __xmaxi = xmaxi

def set_y_min_max(ymini,ymaxi):
    """initialise les valeurs ymini et ymaxi d'un graphique"""
    global __ymini,__ymaxi
    __ymini = ymini
    __ymaxi = ymaxi

# -------------------------------------------------------
#    FONCTIONS ENTREE - SORTIE
# -------------------------------------------------------

def texte_demande(prompteur: str) -> str:
    """
    prompteur est une chaine de caractères
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Ouvre une fenêtre avec le message "prompteur" et attend une chaine de caractères.
    retourne une chaine de caractères
    """
    return input(prompteur)


def demande(prompteur: str) -> nombre:
    """
    prompteur est une chaine de caractères
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Ouvre une fenêtre avec le message "prompteur" et attend un nombre.
    retourne un nombre ou une erreur quand le texte saisi n'est pas convertible en nombre
    """
    if prompteur == "":
        prompteur = "Saisir une valeur numérique"
    if prompteur[-2:] != "\n":
        prompteur = prompteur + "\n"
    try:
        return eval(input(prompteur))
    except:
        raise ValueError("vous devez saisir une valeur numérique")


def formule_demande(prompt):
    i = input(prompt)
    return eval(i)


# -------------------------------------------------------
#    FONCTIONS MATHEMATIQUES
# -------------------------------------------------------

def pgcd(a: entier, b: entier) -> entier:
    """
    a et b sont 2 entiers
    renvoie le Plus Grand Diviseur Commun des 2 nombres
    """
    if a < 0 or b < 0:
        return pgcd(abs(a), abs(b))
    if b == 0:
        if a == 0:
            raise ValueError("a et b ne peuvent pas être nuls")
        else:
            return a
    else:
        return pgcd(b, a % b)


def abs2(x: nombre) -> nombre:
    """
    x est un nombre.
    Renvoie la valeur absolue du nombre x, c'est a dire sa distance à 0
    """
    if x > 0:
        return x
    else:
        return -x


def puissance(a: nombre, n: nombre) -> nombre:
    """
    a,n sont des nombres
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Cette fonction renvoie le resultat de a^n
    """
    return a ** n


def reste(a: entier, b: entier) -> entier:
    """
    a,b sont des nombres entiers (b non nul)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Cette fonction renvoie le reste de la division de a par b
    """
    r = a % b
    if r < 0: r = r + abs(b)
    return r


def quotient(a: entier, b: entier) -> entier:
    """
    a,b sont des nombres entiers (b non nul)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Cette fonction renvoie le quotient de la division de a par b
    """
    return int((a - reste(a, b)) / b)


def angleMode(mode_angle: str = "") -> str:
    """
    mode_angle :  type d'unité d'angle à utiliser (str)
    cette fonction permet de définir l'unité d'angle utiliser par les fonctions trigonométriques
    du module "lycee"
    'rad' les angles des fonctions trigonométriques seront pris comme des radians (défaut)\n
    'deg' les angles des fonctions trigonométriques seront pris comme des degrés\n
    'grd' les angles des fonctions trigonométriques seront pris comme des grades\n
    Une exception est levée en cas d'erreur de paramètre
    retourne la valeur précedente de mode et si mode_angle == "" la valeur actuelle de mode est retournée (str)
     """
    global __angle_mode_str, __angle_mode
    angle_mode = __angle_mode_str
    if mode_angle == "":
        return __angle_mode_str
    elif mode_angle.lower() == "deg":
        __angle_mode = math.pi / 180
        __angle_mode_str = "deg"
    elif mode_angle.lower() == "grd":
        __angle_mode = math.pi / 200
        __angle_mode_str = "grd"
    elif mode_angle.lower() == "rad":
        __angle_mode = 1
        __angle_mode_str = "rad"
    else:
        raise ValueError
    return angle_mode


def cos(angle: reel) -> reel:
    """
    retourne le cosinus de angle en fonction du mode choisi (defaut : radian)
    """
    return math.cos(angle * __angle_mode)


def acos(value: reel) -> reel:
    """
    Retourne la valeur de l'angle telle que cos(angle) = valeur dans l'unité définie par angleMode().
    le résultat est compris entre 0 et pi rd  si mode("rad").
    le résultat est compris entre 0 and 180° si mode("deg").
    le résultat est compris entre 0 and 200 grd si mode("grd").
    """
    return math.acos(value) / __angle_mode


def sin(angle: reel) -> reel:
    """
    retourne le sinus de angle en fonction du mode choisi (defaut : radian)
    """
    return math.sin(angle * __angle_mode)


def asin(value: reel) -> reel:
    """
    Retourne la valeur de l'angle telle que sin(angle) = valeur dans l'unité définie par angleMode().
    le résultat est compris entre 0 et pi rd  si mode("rad").
    le résultat est compris entre 0 et 180° si mode("deg").
    le résultat est compris entre 0 et 200 grd si mode("grd").
    """
    return math.asin(value) / __angle_mode


def tan(angle: reel) -> reel:
    """
    retourne le tangent de angle en fonction du mode choisi (defaut : radian)
    """
    return math.tan(angle * __angle_mode)


def atan(value: reel) -> reel:
    """
    Retourne la valeur de l'angle telle que tan(angle) = valeur dans l'unité définie par angleMode().
    le résultat est compris entre 0 et pi rd  si mode("rad").
    le résultat est compris entre 0 et 180° si mode("deg").
    le résultat est compris entre 0 et 200 grd si mode("grd").
    """
    return math.atan(value) / __angle_mode


def atan2(y: reel, x: reel) -> reel:
    """
    Retourne la valeur de l'angle telle que tan(angle) = y/x dans l'unité définie par angleMode().
    le résultat est compris entre -pi et pi rd  si mode("rad").
    le résultat est compris entre -180 et 180° si mode("deg").
    le résultat est compris entre -200 et 200 grd si mode("grd").
    le signe de x et de y sont pris en compte.
    cette fonction retourne un résultat différent de tan(y/x)
    """
    return math.atan2(y, x) / __angle_mode


def radians(angle: reel) -> reel:
    """convertit l'angle dont l'unité est définie dans angleMode() en radian"""
    return angle * __angle_mode


def degres(angle: reel) -> reel:
    """convertit l'angle dont l'unité est définie dans angleMode() en degré"""
    return angle * __angle_mode * 180 / math.pi


def grades(angle: reel) -> reel:
    """convertit l'angle dont l'unité est définie dans angleMode() en grades"""
    return angle * __angle_mode * 200 / math.pi


def sqrt(x: nombre) -> reel:
    """
    x est un nombre positif
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie la racine carree du nombre x
    """
    return math.sqrt(x)


def racine(x: nombre) -> reel:
    """
    x est un nombre positif
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie la racine carree du nombre x
    """
    return math.sqrt(x)


def factoriel(n: int) -> int:
    """
    n est un nombre entier positif
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie n! = n x (n-1) x ... x 3 x 2 x 1
    """
    return math.factorial(n)


def floor(x: reel) -> entier:
    """
    x est un nombre decimal.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne la partie entière du nombre x, c'est a dire le plus grand entier inférieur au reel x.
    """
    return math.floor(x)


def exp(x: nombre) -> reel:
    """
    x est un nombre decimal.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne l'image du nombre x par la fonction exponentielle e^x.
    """
    return math.exp(x)


def ln(x: nombre) -> reel:
    """
    x est un nombre strictement positif.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne l'image du nombre x par la fonction logarithme népérien.
    """
    return math.log(x)


# -------------------------------------------------------
#    FONCTIONS STAT & PROBAS
# -------------------------------------------------------
def binomial(n: entier, p: entier):
    """
    n et p sont deux entiers.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne coefficient binomial p parmi n, c'est à dire le nombre de chemins de l’arbre réalisant p succès pour n répétitions.
    """
    if p <= n:
        return quotient(math.factorial(n), math.factorial(p) * math.factorial(n - p))
    else:
        return 0


def randint(min: entier, max: entier):
    """
    min et max sont deux entiers.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un entier choisi de manière (pseudo)aléatoire et équiprobable
    dans l'intervalle [min,max].
    """
    return alea.randint(min, max)


def choice(liste: list) -> nombre | str:
    """
    liste est une list.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un élément de la liste list choisi (pseudo)aléatoirement et de manière équipropable
    """
    return alea.choice(liste)


def random() -> reel:
    """
    Pas d'argument.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie au hasard un décimal de l'intervalle [0;1[
    """
    return alea.random()


def uniform(min: nombre, max: nombre) -> reel:
    """
    min et max sont deux nombres.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un nombre décimal choisi de manière (pseudo)aléatoire et
    uniforme de l'intervalle [min,max[.
    """
    return alea.uniform(min, max)


def intervalle(debut: entier, fin: entier, pas: entier = 'optionnel') -> list:
    """
    debut, fin et pas sont des entiers.
    Le paramètre pas est optionnel.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne une liste d’entiers :
      – De l’intervalle [deb; fin] si 2 paramètres sont renseignés
      – De l’intervalle [deb; fin] mais en réalisant une suite arithmétique de raison pas si les 3 paramètres sont renseignés.
    """
    if pas == 'optionnel':
        return list(builtins.range(debut, fin + 1))
    else:
        return list(builtins.range(debut, fin + 1, pas))


def range(debut: entier, fin: entier = 'optionnel', pas: entier = 'optionnel'):
    """
    debut, fin et pas sont des entiers.
    Les paramètres debut et pas sont optionnels.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne une liste d’entiers :
      – De l’intervalle [0; deb[ si un seul paramètre est renseigné.
      – De l’intervalle [deb; fin[ si 2 paramètres sont renseignés
      – De l’intervalle [deb; fin[ mais en réalisant une suite arithmétique de raison pas si les 3 paramètres sont renseignés.
    """
    if pas == 'optionnel':
        if fin == 'optionnel':
            return list(builtins.range(debut))
        else:
            return list(builtins.range(debut, fin))
    else:
        return list(builtins.range(debut, fin, pas))


# -------------------------------------------------------
#    FONCTIONS SUR LES CHAINES
# -------------------------------------------------------
def aligne(chaine: str, taille, aligner="g"):
    """aligne une chaine sur un espace donné de caractères (taille)"""
    if aligner in ["gauche", "left", "g", "l"]:
        return f"{chaine:<{taille}}"
    elif aligner in ["centrer", "center", "c"]:
        return f"{chaine:^{taille}}"
    elif aligner in ["droite", "right", "d", "r"]:
        return f"{chaine:>{taille}}"
    else:
        raise ValueError(f"mauvais format d'alignement : '{aligner}' ne convient pas")


def cadre(chaine: str, taille: int = 0, **kwargs):
    """créer un cadre autour d'une chaine de caractères"""
    aligner = kwargs.get("aligner", "left")
    chaine = chaine.split("\n")
    maxi = 0
    for s in chaine:
        if len(s) > maxi:
            maxi = len(s)
    if taille > maxi:
        maxi = taille
    ligne = "-" * maxi
    print(f"+{ligne}+")
    for s in chaine:
        print(f"|{aligne(s, taille, aligner)}|")
    print(f"+{ligne}+")


def affiche_tableau(tableau: list, taille: list = [], **kwargs):
    """
        affiche tableau (list) a une ou deux dimension dans la console
        taille est une list qui permet de donner la taille de chaque colonne
        si taille n'est pas renseignée la largeur optimale est calculée
        paramètres optionnels:
        padx: espace ajouté avant et après la données
        mini: int : largeur mini d'une colonne
        maxi: int : largeur maxi d'une colonne
        sep_ligne : bool si True les lignes seront séparées
        aligner: chaine de caractère définissant l'alignement des colonnes "dcdg"
            la première colonne sera alignée à droite
            la deuxième sera centrée
            la troisième sera alignée à droite
            les derniéres seront alignée à gauche
        entete: bool : si True la première ligne du tableau sera considérée comme
            une ligne d'entête
    """
    padx = kwargs.get("padx", 0)
    mini = kwargs.get("mini", 1)
    maxi = kwargs.get("maxi", 20)
    pied = kwargs.get("pied", False)
    sep_ligne = kwargs.get("sep_ligne", True)
    aligner = kwargs.get("aligner", "g")
    entete = kwargs.get("entete", False)
    markdown = kwargs.get("markdown", False)

    def ligne(aligner=None):
        if markdown:
            d = "-"
            f = "-|"
            s = "|"
        else:
            d = "-"
            f = "-+"
            s = "+"

        for i, t in enumerate(taille):
            if markdown:
                if aligner is not None:
                    if aligner[i] == "g":
                        d = ":"
                        f = "-|"
                    elif aligner[i] == "c":
                        d = ":"
                        f = ":|"
                    elif aligner[i] == "d":
                        d = "-"
                        f = ":|"
            s += d + "-" * (t + padx * 2 - 2) + f
        print(s)

    padx = 1
    if isinstance(tableau[0], list):
        largeur = len(tableau[0])
        hauteur = len(tableau)
    else:
        largeur = len(tableau)
        hauteur = 1
    if len(aligner) < largeur:
        aligner = aligner + aligner[-1] * (largeur - len(aligner))

    if taille != [] and len(taille) != largeur:
        print("taille des colonnes incorrecte")
    if taille == [] or len(taille) != largeur:
        taille = [mini for i in range(largeur)]
        for j in range(largeur):
            for i in range(hauteur):
                if hauteur > 1:
                    l = len(str(tableau[i][j]))
                else:
                    l = len(str(tableau[j]))
                if taille[j] < l:
                    taille[j] = min(l, maxi)
    if not markdown:
        ligne()
    for i in range(hauteur):
        s = "|"
        for j in range(largeur):
            if hauteur > 1:
                val = str(tableau[i][j])
            else:
                val = str(tableau[j])
            if len(val) > maxi:
                val = val[0:maxi - 1] + ">"
            s += " " * padx + aligne(val, taille[j], aligner=aligner[j]) + " " * padx + "|"
        print(s)
        if not markdown:
            if (sep_ligne and not entete) or (entete and i == 0) or (pied and i == hauteur - 2):
                ligne()
        else:
            if i == 0:
                ligne(aligner)
    if not sep_ligne or entete and not markdown:
        ligne()


def len(objet: str | list) -> entier:
    """
    objet peut être une chaine de caractères ou une liste.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne la longueur de cette chaine ou de cette liste
    """
    return builtins.len(objet)


def fich2chaine(fichier='optionnel'):
    """
    fichier est le nom complet (avec le chemin) d'un fichier contenant du texte brut.
    Si fichier n'est pas précisé, ouvre une boite de dialogue pour
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne chaine formée du contenu du fichier 'fichier'
    """
    if fichier == 'optionnel':
        fichier = texte_demande("Vous n'avez pas précisé de fichier.\nEntrer son nom : ")
    if fichier != 'optionnel':
        try:
            filin = open(fichier, 'r')
            f = "\n".join([line.strip() for line in filin])
            filin.close()
            return f
        except:
            print("Fichier non trouvé")
    else:
        return ""


def chaine2fich(ch, fichier='optionnel', **kwargs):
    """
    ch est une chaine de caractères
    fichier est le nom complet (avec le chenin) d'un fichier contenant du texte brut.
    Si fichier n'est pas précisé, ouvre une boite de dialogue pour
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Enregistre sous le nom 'fichier' la chaine ch
    """
    affiche = kwargs.get("affiche", False)
    if fichier == 'optionnel':
        fichier = texte_demande("Vous n'avez pas précisé de fichier.\nEntrer son nom : ")
    if fichier != 'optionnel':
        filout = open(fichier, 'w')
        filout.write(ch)
        if affiche:
            print(ch)
        filout.close()
        return True
    else:
        return False


def codeAAP(caract):
    """
    caract est un caractère.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Donne le rang (entre 0 et 101) dans l'Alphabet AmiensPython du caractère caract
    Renvoie 0 si le caractère est inconnu.
    """
    c = caract
    try:
        c = unicode(caract, 'cp1252')
    except:
        c = c
    a = AlphabetAP.find(c);
    if a == -1: a = 0
    return a


def decodeAAP(pos):
    """
    pos est un entier entre 0 et 101.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie le caractère qui se trouve à la position pos dans l'Alphabet AmiensPython
    Renvoie le caractère 0 en cas de dépassement d'indice
    """
    a = pos
    if a < 0 or a >= len(AlphabetAP): a = 0
    return AlphabetAP[a]


# -------------------------------------------------------
#    FONCTIONS SUR LES LISTES
# -------------------------------------------------------
def CSV2liste(num: int | str, fichier='optionnel', sep=';', dec='.') -> list:
    """
    num peut contenir un numéro de ligne ou un nom de colonne ('A' à 'Z' )
    fichier est le nom complet (avec le chemin) d'un fichier contenant du texte brut.
    Si fichier n'est pas précisé, ouvre une boite de dialogue pour le choisir
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne une liste correspondant à la colonne ou la ligne fichier 'fichier'
    """
    ch = fich2chaine(fichier)
    if type(num) == int:
        l = ch.split("\n")
        r = []
        if len(l) >= num:
            for n in l[num - 1].split(sep):
                try:
                    r.append(int(n))
                except:
                    try:
                        r.append(float(n.replace(dec, '.')))
                    except:
                        r.append(n)
        return r
    if type(num) == str:
        num = num.upper()
        c = ord(num) - 65
        r = []
        for m1 in ch.split("\n"):
            m2 = m1.split(sep)
            n = m2[c] if len(m2) > c else ""
            try:
                r.append(int(n))
            except:
                try:
                    r.append(float(n.replace(dec, '.')))
                except:
                    r.append(n)
        return r


def liste2CSV(liste: list, fichier: str = 'optionnel', **kwargs):
    """
    liste est une list
    fichier est le nom complet (avec le chenin) d'un fichier contenant du texte brut.
    Si fichier n'est pas précisé, ouvre une boite de dialogue pour
    Si paramètre optionnel affiche = True le contenu du fichier est affiché dans la console
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Enregistre sous le nom 'fichier' la liste au format CSV
    """
    for i in range(len(liste)):
        liste[i] = [str(v) for v in liste[i]]
        liste[i] = ";".join(liste[i])
    chaine2fich("\n".join(liste), fichier, **kwargs)


def liste_demande(prompt: str):
    """
    prompteur est une chaine de caractères
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Ouvre une fenêtre avec le message "prompteur" et attend une liste de valeurs séparées par des vigules.
    """
    return list(demande(prompt + "\n(liste de valeurs séparées par des vigules)"))


def affiche_poly(liste: list, **kwargs):
    """
    liste est une list
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Affiche la liste sous forme d'un polynôme (liste[n] étant le coefficient de degré n).
    le paramètre facultatif format=python permet d'écrire le polynôme au format python
    """
    format = kwargs.get("format")
    poly = ""
    for i in range(len(liste)):
        c = liste[i]
        if c != 0 and poly != "": poly = poly + '+'
        if c != 0:
            if i > 0:
                if c == -1: poly = poly + '-'
                if abs(c) != 1: poly = poly + str(c)
            else:
                poly = poly + str(c)
            if i > 0:
                if format is None:
                    poly = poly + 'x'
                elif format.lower() == "python":
                    poly = poly + '*x'
                if i > 1:
                    if format is None:
                        poly = poly + '^' + str(i)
                    elif format.lower() == "python":
                        poly = poly + '**' + str(i)
    if poly == "": poly = 0
    return poly


# -------------------------------------------------------
#    FONCTIONS SUR NUMPY
# -------------------------------------------------------
def vecteur(x, y, z='optionnel') -> numpy.array:
    """
    x et y sont des nombres
    z est un nombre optionnel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un vecteur de coordonées (x,y) ou (x,y,z)
    """
    if z == 'optionnel':
        return np.array([x, y])
    else:
        return np.array([x, y, z])


def norme(v: numpy.array) -> float:
    """
    v est un vecteur du plan ou de l'espace
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie la norme du vecteur v
    """
    l = v ** 2;
    n = 0
    for i in range(len(l)):
        n = n + l[i]
    return sqrt(n)


def abscisse(v: numpy.array) -> float:
    """
    v est un vecteur du plan ou de l'espace
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie l'abscisse du vecteur v
    """
    return v[0]


def ordonnee(v: numpy.array) -> float:
    """
    v est un vecteur du plan ou de l'espace
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie l'ordonnée du vecteur v
    """
    return v[1]


def cote(v) -> float:
    """
    v est un vecteur de l'espace
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie la cote du vecteur v
    """
    return v[2]


# -------------------------------------------------------
#    FONCTIONS DIAGRAMME COURBE
# -------------------------------------------------------
def fill(couleur: str):
    global __fill_color, __no_fill
    __fill_color = couleur
    __no_fill = False


def noFill():
    global __fill_color
    __no_fill = True


def stroke(couleur: str):
    global __stroke, __no_stroke
    __stroke = couleur
    __no_stroke = False


def strokeWeight(largeur: int):
    global __stroke_width
    __stroke_width = largeur


def noStroke():
    global __stroke
    __stroke = ""


def add_key(dico, key, default_value=None, renamed_key=None):
    dico[key] = dico.get(key, default_value)
    if renamed_key is not None:
        if dico.get(renamed_key) is None:
            dico[renamed_key] = dico.pop(key)
        else:
            dico.pop(key)


def teste_dico_figure(dico: dict):
    add_key(dico, "fill", __fill_color, "fc")
    add_key(dico, "stroke", __stroke, "ec")
    add_key(dico, "stroke_weight", __stroke_width, "linewidth")
    if dico.get("noFill") is True:
        dico["fill"] = False
        dico.pop("noFill")
    if dico.get("noStroke") is True:
        dico["ec"] = None
        dico.pop("noStroke")


def teste_dico_trait(dico: dict):
    add_key(dico, "c", dico.get("stroke", __stroke))
    add_key(dico, "stroke", __stroke, "c")
    add_key(dico, "stroke_weight", __stroke_width, "linewidth")


def delkeys(dico: dict, keys: list):
    if isinstance(keys, str):
        keys = [keys]
    for k in keys:
        if k in dico.keys():
            dico.pop(k)


def trace_fonction(fx: str | list[str], **kwargs):
    """trace une fonction ou des fonctions dans le repere défini par repere()"""
    if __xmini is None:
        raise "il faut definir le repere avec repere()"
    else:
        if isinstance(fx, str):
            fx = [fx]
        dx = __xmaxi - __xmini
        d = round(100 / dx)
        mini = __xmini * d
        maxi = __xmaxi * d + 1
        xi = [i / d for i in range(mini, maxi)]
        yi=[]
        for f in fx:
            yi.append([eval(f) for x in xi])
        trace_courbe(xi, *yi, **kwargs)


def trace_courbe(xi: list, yi: list, *args: list, **kwargs):
    """trace une ou des courbes défini par une liste d'abscisses et
    une ou des listes d'ordonnées"""
    teste_dico_trait(kwargs)
    titre = kwargs.get("titre", "")
    if not __repere:
        abscisse = kwargs.get("abscisse", __abscisse)
        ordonnee = kwargs.get("ordonnee", __ordonnee)
    labels = kwargs.get("labels", None)
    couleurs = kwargs.get("couleurs", None)
    if couleurs is None:
        couleurs = [kwargs.get("c")]+ __couleur
    delkeys(kwargs, ["titre", "abscisse", "ordonnee", "labels", "c", 'couleurs'])
    if labels is not None:
        if isinstance(labels, str):
            labels = [labels]
        if isinstance(labels, list):
            if len(args) > 0:
                if len(labels) < len(args) + 1:
                    labels = labels + ["?"] * (len(args) + 1 - len(labels))
    axe = pos_to_axe()
    axe.set_axis_on()
    axe.set_title(titre)
    if not __repere:
        axe.set_ylabel(ordonnee)
        axe.set_xlabel(abscisse)
    ordonnees = [yi] + list(args)

    if __ymaxi is None:
        maxy = max(ordonnees[0])
        miny = min(ordonnees[0])
    else:
        maxy = __ymaxi
        miny = __ymini

    if isinstance(xi[0],str):
        xlabels = [s for s in xi]
        xi= [i for i in range(len(xi))]
    else:
        xlabels=None
    i = 0
    for y in ordonnees:
        if labels is not None:
            axe.plot(xi, y, label=labels[i], c=couleurs[i], **kwargs)
        else:
            axe.plot(xi, y, c=couleurs[i], **kwargs)
        i += 1
        maxy = max(max(y), maxy)
        miny = min(min(y), miny)
    axe.grid(visible=__grille)
    if xlabels is not None:
        axe.set_xticks(xi, xlabels, minor=False)
    if __xmini is None:
        axe.axis([min(xi) - 0.1, max(xi) + 0.1, miny - 0.1, maxy + 0.1])
    else:
        axe.axis([__xmini, __xmaxi, __ymini, __ymaxi])
    if labels is not None:
        axe.legend()

def nuage(xi: list, yi: list, *args: list, **kwargs):
    """trace un ou des nuages de point défini par une liste d'abscisses et
    une ou des listes d'ordonnées"""
    teste_dico_trait(kwargs)
    titre = kwargs.get("titre", "")
    abscisse = kwargs.get("abscisse", __abscisse)
    ordonnee = kwargs.get("ordonnee", __ordonnee)
    labels = kwargs.get("labels", None)
    couleurs = kwargs.get("couleurs", None)
    if couleurs is None:
        couleurs = [kwargs.get("c")]+ __couleur
    delkeys(kwargs, ["titre", "abscisse", "ordonnee", "labels", "c", 'couleurs'])
    if labels is not None:
        if isinstance(labels, str):
            labels = [labels]
        if isinstance(labels, list):
            if len(args) > 0:
                if len(labels) < len(args) + 1:
                    labels = labels + ["?"] * (len(args) + 1 - len(labels))
    axe = pos_to_axe()
    axe.set_axis_on()
    axe.set_title(titre)
    axe.set_ylabel(ordonnee)
    axe.set_xlabel(abscisse)
    ordonnees = [yi] + list(args)
    i = 0
    if __ymaxi is None:
        maxy = max(ordonnees[0])
        miny = min(ordonnees[0])
    else:
        maxy = __ymaxi
        miny = __ymini

    if isinstance(xi[0],str):
        xlabels = [s for s in xi]
        xi= [i for i in range(len(xi))]
    else:
        xlabels=None

    for y in ordonnees:
        if labels is not None:
            axe.scatter(xi, y, label=labels[i], c=couleurs[i], **kwargs)
        else:
            axe.scatter(xi, y, c=couleurs[i], **kwargs)
        i += 1
        maxy = max(max(y), maxy)
        miny = min(min(y), miny)
    axe.grid(visible=__grille)
    if xlabels is not None:
        axe.set_xticks(xi, xlabels, minor=False)
    if __xmini is None:
        axe.axis([min(xi) - 0.1, max(xi) + 0.1, miny - 0.1, maxy + 0.1])
    else:
        axe.axis([__xmini, __xmaxi, __ymini, __xmaxi])
    if labels is not None:
        axe.legend()

def repere(xmini, xmaxi, ymini, ymaxi, **kwargs):
    """défini un repère orthogonal en fonction de
      xmini, xmaxi, ymini, ymaxi"""
    global __xmini, __xmaxi, __ymini, __ymaxi, __grille,__repere
    __repere = True
    titre = kwargs.get("titre", "")
    abscisse = kwargs.get("abscisse", __abscisse)
    ordonnee = kwargs.get("ordonnee", __ordonnee)
    labels = kwargs.get("labels", None)
    add_key(kwargs, "grille", True, "visible")
    norme = kwargs.get("norme", False)
    __grille = kwargs["visible"]
    delkeys(kwargs, ["titre", "abscisse", "ordonnee", "norme"])
    axe = pos_to_axe()
    axe.set_axisbelow(True) #grille au dessus
    axe.set_axis_on()
    axe.set_title(titre)
    axe.set_ylabel(ordonnee, loc="top")
    axe.set_xlabel(abscisse, loc="right")
    axe.axis([xmini, xmaxi, ymini, ymaxi])
    if norme:
        axe.axis('equal')
    axe.spines['top'].set_color('none')
    axe.spines['right'].set_color('none')
    if xmini <= 0 <= xmaxi:
        axe.spines['left'].set_position(('data', 0))
    if ymini <= 0 <= ymaxi:
        axe.spines['bottom'].set_position(('data', 0))
    axe.plot(0, 1, "^k", transform=axe.get_xaxis_transform(), clip_on=False)
    axe.plot(1, 0, ">k", transform=axe.get_yaxis_transform(), clip_on=False)
    axe.plot([xmini, xmaxi, xmini, xmaxi], [ymini, ymini, ymaxi, ymaxi], "white", visible=False)
    plot.xlim(xmini, xmaxi)
    plot.ylim(ymini, ymaxi)
    axe.grid(**kwargs)
    __xmini, __xmaxi, __ymini, __ymaxi = xmini, xmaxi, ymini, ymaxi


def segment(x1, y1, x2, y2, **kwargs):
    """dessine un segment dans la zone courante
    """
    pt = kwargs.get("point", True)
    noms = kwargs.get("noms", ["", ""])
    add_key(kwargs,"couleur",__stroke,"c")
    delkeys(kwargs,["point","noms"])
    # "couleur = kwargs.get("couleur", __stroke)"
    ligne = kwargs.get("ligne", False)
    axe = pos_to_axe()

    axe.plot([x1, x2], [y1, y2], **kwargs)
    if pt:
        point(x1, y1, nom=noms[0], ligne=ligne)
        point(x2, y2, nom=noms[1], ligne=ligne)

def ligne(x1, y1, x2, y2, **kwargs):
    """trace un segment sans point d'extrémité"""
    kwargs['point'] = False
    segment(x1, y1, x2, y2,**kwargs)

def point(x, y, **kwargs):
    """dessine un point dans la zone courante"""
    couleur = kwargs.get("couleur", __stroke)
    nom = kwargs.get("nom", "")
    ligne = kwargs.get("ligne", False)
    marker = kwargs.get("marker", ".")
    axe = pos_to_axe()
    if ligne:
        axe.plot([0, x, x], [y, y, 0], linestyle=':', c="grey")
    axe.scatter(x, y, c=couleur, marker=marker)
    axe.annotate(f"  {nom}({x};{y})", (x, y))


def rectangle(x, y, largeur, hauteur, **kwargs):
    """ dessine un rectangle dans la zone courante"""
    teste_dico_figure(kwargs)
    my_rect = Rectangle((x, y), largeur, hauteur, **kwargs)
    plot.gca().add_patch(my_rect)


def carre(x, y, largeur, **kwargs):
    """ dessine un carré dans la zone courante"""
    rectangle(x, y, largeur, largeur, **kwargs)


def polygone(xyi: list[list], **kwargs):
    """ dessine un polygone dans la zone courante"""
    teste_dico_figure(kwargs)
    p = Polygon(xyi, **kwargs)
    plot.gca().add_patch(p)


def triangle(x1, y1, x2, y2, x3, y3, **kwargs):
    """ dessine un triangle dans la zone courante"""
    polygone([[x1, y1], [x2, y2], [x3, y3]], **kwargs)


def cercle(x, y, rayon, **kwargs):
    """ dessine un cercle dans la zone courante"""
    teste_dico_figure(kwargs)
    marker = kwargs.get("marker", "+")
    centre = kwargs.get("centre", False)
    ligne = kwargs.get("ligne", False)
    nom = kwargs.get("nom", "")
    delkeys(kwargs, ["centre", "nom", "ligne", "marker"])

    axe = pos_to_axe()

    plot.gca().add_patch(Circle((x, y), radius=rayon, **kwargs))
    if centre:
        point(x, y, nom=nom, ligne=ligne, marker=marker)


# -------------------------------------------------------
#    FONCTIONS DIAGRAMME STAT
# -------------------------------------------------------
def figure(nb_lignes=1, nb_cols=1, **kwargs):
    """crée une ou des zones graphiques.
    il faut obligatoirement crée au minimun une zone pour pouvoir réaliser
    un graphique"""
    global __figure, __axe, __ligne, __colonne, __ligne_max, __colonne_max,__repere
    titre = kwargs.get("titre", "")
    if titre != "":
        kwargs.pop("titre")
    if kwargs.get("figsize", None) is None:
        kwargs["figsize"] = (5 * nb_cols, nb_lignes * 4 + 0.5)
    __figure, __axe = plot.subplots(nb_lignes, nb_cols, **kwargs)
    __ligne, __colonne = 0, 0
    __ligne_max, __colonne_max = nb_lignes, nb_cols
    __repere = False
    for i in range(nb_lignes):
        for j in range(nb_cols):
            axe = pos_to_axe(i, j)
            axe.set_axis_off()
    __figure.suptitle(titre)


def pos_to_axe(ligne=None, colonne=None) -> matplotlib.axes.Axes:
    """retourne la zone graphique qui correspond à ligne, colonne
    Si ligne et colonne sont omis, c'est la zone courante qui est
    renvoyée"""
    if ligne is None:
        ligne = __ligne
    if colonne is None:
        colonne = __colonne
    if __colonne_max == 1 and __ligne_max == 1:
        return __axe
    elif __colonne_max == 1:
        return __axe[ligne]
    elif __ligne_max == 1:
        return __axe[colonne]
    else:
        return __axe[ligne][colonne]


def test_figure():
    """Vérifie qu'une figure a été crée"""
    global __ligne, __colonne
    if __figure is None:
        raise ValueError("Avant toute chose il créer une figure() pour afficher un graphique")
    if __ligne >= __ligne_max or __colonne >= __colonne_max:
        raise ValueError("Pas assez du place sur figure()")


def suivant():
    """Quand figure() défini plusieurs zones graphique suivant() passe à la zonne suivante"""
    global __ligne, __colonne
    if (__colonne + 1) % __colonne_max == 0:
        __colonne = 0
        __ligne += 1
    else:
        __colonne += 1


def affiche_graphique():
    """affiche les graphiques précédemment calculés"""
    plot.show()


def baton(xi, ni='optionnel', **kwargs):
    """
    xi est une liste de valeurs
    ni est la liste des effectifs associés, c'est un paramètre optionnel.
    couleur donne la couleur du diagramme (optionnel)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Génére le diagramme en bâtons relatif à la liste.
    """
    print(__figure.get_size_inches())
    couleur = kwargs.get('couleur', 'optionnel')
    titre = kwargs.get("titre", "Diagramme en bâtons de la liste")
    abscisse = kwargs.get("abscisse", 'Valeurs de la liste')
    ordonnee = kwargs.get("ordonnee", 'Effectifs')
    test_figure()
    if couleur == 'optionnel': couleur = 'b'
    if type(ni) != list:
        xi, ni = compte(xi, 'effectif')
    axe = pos_to_axe()
    axe.set_axis_on()
    axe.set_title(titre)
    axe.set_ylabel(ordonnee)
    axe.set_xlabel(abscisse)
    for i in range(len(xi)):
        axe.plot([xi[i], xi[i]], [0, ni[i]], couleur, lw=2)
    if __ymaxi is None:
        axe.axis([min(xi) - 0.1, max(xi) + 0.1, 0, max(ni)])
    else:
        axe.axis([min(xi) - 0.1, max(xi) + 0.1, 0, max(ni+[__ymaxi])])
    suivant()


def secteur(valeurs: list, etiquettes: list, **kwargs):
    """Génère un diagramme secteur"""
    if len(valeurs) != len(etiquettes):
        raise IndexError("le nombres de valeur doit être égal aux nombres d'étiquettes")
    test_figure()
    axe = pos_to_axe()
    titre = kwargs.get("titre", "Diagramme en secteur")
    axe.set_title(titre)
    delkeys(kwargs, "titre")
    axe.pie(valeurs, labels=etiquettes, normalize=True, **kwargs)
    axe.legend()


def ligne_brisee(xi: list, yi: list, *args: list, **kwargs):
    """Trace courbes"""
    trace_courbe(xi, yi, *args, **kwargs)

def table(table_2d: list[list], **kwargs):
    """Génere un tableau 1d ou 2d"""
    test_figure()
    nb_cols = len(table_2d[0])
    nb_lignes = len(table_2d)
    entete_col = kwargs.get("entete_col", False)
    couleur_entete = kwargs.get("couleur_entete", None)
    if couleur_entete is not None:
        if isinstance(couleur_entete, str):
            kwargs["colColours"] = [kwargs.pop("couleur_entete")] * nb_cols
        elif isinstance(couleur_entete, list):
            kwargs["colColours"] = kwargs.pop("couleur_entete") + [couleur_entete[-1]] * (nb_cols - len(couleur_entete))
    entete_ligne = kwargs.get("entete_ligne", False)
    titre = kwargs.get("titre", "")
    if titre != "":
        kwargs.pop("titre")
    colWidths: int | list = kwargs.get("colWidths", 1)

    if isinstance(colWidths, int | float):
        kwargs["colWidths"] = [colWidths / 20 for i in range(nb_cols)]
    else:
        if len(colWidths) < nb_cols:
            colWidths = colWidths + [colWidths[-1] for i in range(nb_cols - len(colWidths))]
        cw = []
        for i in range(nb_cols):
            if colWidths[i] < 1:
                cw.append(colWidths[i])
            else:
                cw.append(colWidths[i] / 20)
        kwargs["colWidths"] = cw
    debut_col, debut_ligne = 0, 0
    rl, cl = None, None
    if entete_col:
        debut_col = 1
        cl = table_2d[0]
        kwargs.pop("entete_col")
    if entete_ligne:
        debut_ligne = 1
        rl = [table_2d[i][0] for i in range(1, len(table_2d))]
        kwargs.pop("entete_ligne")
    axe = pos_to_axe()
    axe.set_title(titre)
    axe.table(cellText=[[str(table_2d[r][c]) for c in range(debut_ligne, nb_cols)] for r in
                        range(debut_col, nb_lignes)], rowLabels=rl, colLabels=cl, loc='upper left', **kwargs)
    suivant()


def histop(Liste, Classes='optionnel', **kwargs):
    """
    Liste est une liste de valeurs
    Si seulement Liste est renseigné, les valeurs seront réparties en 10 classes.
    Si Classes est un entier, les valeurs seront réparties en ce nombre de classes.
    Sinon, vous pouvez choisir vos classes d'amplitudes variées
        en indiquant comme Classes    la liste ordonnée des bornes.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Génère l'histogramme relatif à la Liste d'aire totale 1.
    """
    test_figure()
    axe = pos_to_axe()
    C = Classes
    if C == 'optionnel': C = 10
    if type(C) == int:
        pas = (max(Liste) - min(Liste)) / C
        a = min(Liste)
        C = []
        while a <= max(Liste):
            C.append(a)
            a = a + pas
    Eff = [0] * (len(C) - 1)
    for v in Liste:
        i = 0
        while i < len(C) - 1:
            if v >= C[i] and (v < C[i + 1] or (i == len(C) - 2 and v == C[i + 1])):
                Eff[i] = Eff[i] + 1
                i = len(C)
            else:
                i = i + 1
    taille = [C[i + 1] - C[i] for i in range(len(C) - 1)]
    TotalEff = sum(Eff)
    H = [Eff[i] / (taille[i] * TotalEff) for i in range(len(C) - 1)]
    axe.bar(C[:-1], H, width=taille)
    n = int(len(Liste) / (len(C) - 1) / 5)
    if n == 0: n = 1
    if n > 9:
        d = int(ln(n) / ln(10)) - 1
        n = int(round(n * (10 ** (-d)))) * 10 ** d
    xi, ni = compte(taille, 'effectif')
    m = max(ni)
    l, i = 0, 0
    while l == 0:
        if ni[i] == m:
            l = xi[i]
        else:
            i = i + 1
    for i in range(len(taille)):
        if taille[i] == l and Eff[i] != 0:
            h = H[i] * n / Eff[i]
    xc = C[0]
    yc = max(H) * 1.1
    axe.plot([xc, xc + l], [yc, yc], 'b')
    axe.plot([xc, xc + l], [yc + h, yc + h], 'b')
    axe.plot([xc, xc], [yc, yc + h], 'b')
    axe.plot([xc + l, xc + l], [yc, yc + h], 'b')
    txt = " " + str(n) + " individu"
    if n > 1: txt = txt + "s"
    txt = txt + ", soit " + str(round(n / len(Liste) * 10000) / 100) + "% de la population"
    axe.text(xc + l * 1.1, yc + h / 2, txt, verticalalignment='center')
    suivant()


def barre(liste: list, a='optionnel', pas='optionnel', **kwargs):
    """
    liste est une liste de valeurs
    Si seulement Liste est renseigné, les valeurs seront réparties en 10 classes.
    Si Liste et a sont renseignés, les valeurs seront réparties en a classes.
    Si les trois paramètres sont renseignés:
            a est le centre de la première classe,
            et pas est l'amplitude des classes.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Génère le diagramme en barres relatif à la Liste.
    """
    test_figure()
    axe = pos_to_axe()
    axe.set_axis_on()
    effectifs = kwargs.get("eff", None)
    titre = kwargs.get("titre", "Diagramme en bâtons de la liste")
    abscisse = kwargs.get("abscisse", 'Valeurs de la liste')
    ordonnee = kwargs.get("ordonnee", 'Effectifs')
    axe.set_title(titre)
    axe.set_ylabel(ordonnee)
    axe.set_xlabel(abscisse)
    add_key(kwargs, "couleur", "blue", "color")
    delkeys(kwargs, ["eff", "titre", "ordonnee", "abscisse"])
    if pas == 'optionnel':
        if a == 'optionnel': a = 10
        axe.hist(liste, bins=a, **kwargs)
    else:
        n = a - pas / 2
        C = []
        if effectifs is None:
            while n < max(liste) + pas:
                C.append(n)
                n = n + pas
            Eff = [0] * (len(C) - 1)
            for v in liste:
                i = 0
                while i < len(C) - 1:
                    if v >= C[i] and v < C[i + 1] or (i == len(C) - 2 and v == C[i + 1]):
                        Eff[i] = Eff[i] + 1
                        i = len(C)
                    else:
                        i = i + 1
            C = C[:-1]
        else:
            Eff = liste
            C = [i * pas for i in range(len(liste))]
        for i in range(len(C)):
            C[i] += a
        axe.bar(C, Eff, width=pas, **kwargs)
    suivant()


def colonne(liste, a='optionnel', pas='optionnel', **kwargs):
    """Trace un graphique en colonne idem barre"""
    barre(liste, a, pas, **kwargs)


def compte(liste, option='optionnel'):
    """
    liste est une liste de nombres
    option est un paramètre optionnel: "frequence" , "effectif"
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne la liste triée sans les doublons et
      – Si l'option est "effectif", la liste est retournée avec les effectifs des valeurs.
      – Si l'option est "frequence", la liste est retournée avec les fréquences des valeurs.
    """

    def divliste(x):  # Définition de la fonction pour diviser par l'effectif total
        return x / len(liste)

    liste = sorted(liste)  # On trie la liste pour rencontrer les éléments par ordre croissant.
    listf = [liste[0]]  # Initialise la liste des valeurs avec la première valeur
    eff = [liste.count(liste[0])]  # Initialise la liste des effectifs avec le premier effectif associé
    for i in range(len(liste)):  # On parcourt la série
        if liste[i] not in listf:
            listf.append(liste[i])  # Si l'élément n'a pas encore été rencontré, il est ajouté à la liste.
            eff.append(
                liste.count(liste[i]))  # Ajoute à la liste des effectifs, l'effectif associé à cette nouvelle valeur
    if option == 'effectif':
        return sorted(listf), eff
    elif option == 'frequence' or option == 'frequences':
        return sorted(listf), list(map(divliste, eff))  # Calcul des fréquences par division par l'effectif total.
    else:
        return sorted(listf)


def listeRand(n):
    """
    n est est un nombre
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne une liste de n nombres décimaux aléatoires dans l'intervalle [ 0, 1[.
    """
    if n == 0:
        return []
    else:
        list = []
        for i in range(n):
            list.append(random())
        return list


def listeRandint(min, max, n):
    """
    min est un nombre
    max est un nombres
    n est est un nombre
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne une liste de n nombres entiers aléatoires dans l'intervalle [min , max].
    """
    if n == 0:
        return []
    else:
        list = []
        for i in range(n):
            list.append(randint(min, max))
        return list


def centres(L):
    """
    L est une liste de taille n
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie une liste de longueur n-1 contenant les valeurs (L[i]+L[i+1])/2.
    """
    R = []
    for i in range(len(L) - 1):
        R.append((L[i] + L[i + 1]) / 2)
    return R


def ECC(xi, ni='optionnel'):
    """
    xi est une liste de valeurs
    ni est la liste des effectifs associés, c'est un paramètre optionnel.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Génère les effectifs cumulés croissants d'une liste.
    """
    if ni == 'optionnel': xi, ni = compte(xi, 'effectif')
    T = 0;
    E = []
    for i in range(len(ni)):
        T = T + ni[i]
        E.append(T)
    return xi, E


def FCC(xi, ni='optionnel'):
    """
    xi est une liste de valeurs
    ni est la liste des effectifs associés, c'est un paramètre optionnel.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Génère les fréquences cumulées croissantes d'une liste.
    """
    xi, ni = ECC(xi, ni)
    for i in range(len(ni)): ni[i] = ni[i] / ni[len(ni) - 1]
    return xi, ni


def polygoneECC(xi, ni='optionnel', couleur='b', **kwargs):
    """
    xi est une liste de valeurs
    ni est la liste des effectifs associés, c'est un paramètre optionnel.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Génére le polygone des Effectifs cumulés croissants de la liste
    """
    test_figure()
    axe = pos_to_axe()
    axe.set_axis_on()
    xi, ec = ECC(xi, ni)
    if len(xi) == len(ec) + 1:
        ec.insert(0, 0)
    axe.plot(xi, ec, couleur + 'o')
    axe.plot(xi, ec, couleur)
    axe.set_title('Polygone des Effectifs Cumules Croissants')
    axe.set_ylabel('Effectifs')
    axe.set_xlabel('Valeurs de la liste')
    suivant()


def polygoneFCC(xi, ni='optionnel', couleur='b', **kwargs):
    """
    xi est une liste de valeurs
    ni est la liste des effectifs associés, c'est un paramètre optionnel.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Génére le polygone des fréquences cumulées croissantes de la liste
    """
    test_figure()
    axe = pos_to_axe()
    axe.set_axis_on()
    xi, ec = FCC(xi, ni)
    if len(xi) == len(ec) + 1:
        ec.insert(0, 0)
    axe.plot(xi, ec, couleur + 'o')
    axe.plot(xi, ec, couleur)
    axe.set_title("Polygone des frequences cumulees Croissantes")
    axe.set_ylabel('Frequences')
    axe.set_xlabel('Valeurs de la liste')
    suivant()


def moyenne(xi, ni='optionnel'):
    """
    xi est une série de valeurs (ou les extrémité des classes)
    ni est la série des effectifs associés (optionnelle)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie la moyenne de la liste
    """
    if ni == 'optionnel': xi, ni = compte(xi, 'effectif')
    if len(xi) == len(ni) + 1: xi = centres(xi)  # Si on travaille avec des classes
    s = 0
    # print xi,ni
    for i in range(len(xi)):
        s = s + xi[i] * ni[i]
    return s / sum(ni)


def mediane(xi, ni='optionnel', option='optionnel'):
    """
    xi est une série de valeurs
    ni est la série (optionnelle) des effectifs associés
    option est un paramètre optionnel: 1 ou 2
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie la médiane de la liste
    - L'option par défaut est l'option 1.
    - Si l'option est 1, la médiane est la valeur centrale (valeur de la série ou moyenne arithmétique)
    - Si l'option est 2, la médiane est la valeur pour laquelle on dépasse 50% des valeurs.

    """
    if ni == 'optionnel':  # On vérifie si ni existe
        xi, ni = compte(xi, 'effectif')
    elif ni == 2 or ni == 1:  # On vérifie si option existe
        option = ni
        xi, ni = compte(xi, 'effectif')
    else:  # ni existe, on vérifie si xi est ordonnée sinon on trie xi et ni
        if xi != sorted(xi) and type(ni) == list:
            xi, ni = trier_liste(xi, ni)
    i = 0
    k = ni[0]
    while k < sum(ni) / 2:
        i = i + 1
        k = k + ni[i]
    if option == 2:  # Option 2
        if k <= sum(ni) / 2:
            return xi[i + 1]
        else:
            return xi[i]
    else:  # Option 1 par défaut
        if sum(ni) % 2 == 0:
            if k <= sum(ni) / 2:
                return (xi[i] + xi[i + 1]) / 2
            else:
                return xi[i]
        else:
            if k <= sum(ni) / 2:
                return xi[i + 1]
            else:
                return xi[i]


def trier_liste(xi, ni):
    for i in range(len(xi)):
        index = i
        mini = xi[i]
        for j in range(i + 1, len(xi)):
            if xi[j] < mini:
                mini = xi[j]
                index = j
        xi[i], xi[index] = xi[index], xi[i]
        ni[i], ni[index] = ni[index], ni[i]
    return xi, ni


def quartile(xi, ni='optionnel', valeur='optionnel'):
    """
    xi est une série de valeurs
    ni est la série des effectifs associés (optionnelle)
    valeur est le quartile que l'on souhaite 1 ou 3 (optionnelle)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne les quartiles de la liste.
    - Si valeur=1, retourne le premier quartile.
    - Si valeur=3, retourne le troisième quartile.
    - Par défaut, le premier et le troisième quartile sont retournés
    """
    if ni == 'optionnel':  # On vérifie si ni existe
        xi, ni = compte(xi, 'effectif')
    elif ni == 3 or ni == 1:  # On vérifie si valeur existe
        valeur = ni
        xi, ni = compte(xi, 'effectif')
    else:  # ni existe, on vérifie si xi est ordonnée sinon on trie xi et ni
        if xi != sorted(xi) and type(ni) == list:
            xi, ni = trier_liste(xi, ni)
    q1pos = sum(ni) // 4  # On définit la position de q1
    q3pos = (3 * sum(ni)) // 4  # On définit la position de q3
    k = ni[0]
    i = 0
    while k < q1pos:  # On cherche q1
        i = i + 1
        k = k + ni[i]
    q1 = xi[i]  # On définit q1
    while k < q3pos:  # On cherche q3
        i = i + 1
        k = k + ni[i]
    q3 = xi[i]  # On définit q3
    if valeur == 1:  # Affichage du 1er quartile
        return q1
    if valeur == 3:  # Affichage du 3ème quartile
        return q3
    if valeur != 1 and valeur != 3:  # Option par défaut
        return q1, q3


def decile(xi, ni='optionnel', valeur='optionnel'):
    """
    xi est une série de valeurs
    ni est la série des effectifs associés (optionnelle)
    valeur est le decile que l'on souhaite 1 ou 9 (optionnelle)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne les déciles de la liste.
    - Si valeur=1, retourne le premier décile.
    - Si valeur=9, retourne le neuvième décile.
    - Par défaut, le premier et le neuvième décile sont retournés
    """
    if ni == 'optionnel':  # On vérifie si ni existe
        xi, ni = compte(xi, 'effectif')
    elif ni == 9 or ni == 1:  # On vérifie si valeur existe
        valeur = ni
        xi, ni = compte(xi, 'effectif')
    else:  # ni existe, on vérifie si xi est ordonnée sinon on trie xi et ni
        if xi != sorted(xi) and type(ni) == list:
            xi, ni = trier_liste(xi, ni)

    d1pos = int(sum(ni) / 10)  # On définit la position de d1
    d9pos = int(9 * sum(ni) / 10)  # On définit la position de d9
    k = 0
    i = 0
    while k < d1pos:  # On cherche d1
        k = k + ni[i]
        i = i + 1
    d1 = xi[i]  # On définit d1
    while k < d9pos:  # On cherche d19
        k = k + ni[i]
        i = i + 1
    d9 = xi[i]  # On définit d9
    if valeur == 1:  # Affichage du 1er décile
        return d1
    if valeur == 9:  # Affichage du 9eme décile
        return d9
    if valeur != 1 and valeur != 9:  # Option par défaut
        return d1, d9


def variance(xi, ni='optionnel'):
    """
    xi est une série de valeurs (ou les extrémité des classes)
    ni est la série des effectifs associés (optionnelle)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne la variance de la liste.
    """
    if type(ni) != list:
        xi, ni = compte(xi, 'effectif')
    if len(xi) == len(ni) + 1: xi = centres(xi)  # Si on travaille avec des classes
    v = 0
    xbar = moyenne(xi, ni)
    for i in range(len(xi)):
        v = v + (xi[i] - xbar) ** 2 * ni[i]
    return v / (sum(ni))


def ecartype(xi, ni='optionnel'):
    """
    xi est une série de valeurs (ou les extrémité des classes)
    ni est la série des effectifs associés (optionnelle)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Retourne l'écart-type de la liste
    """
    return sqrt(variance(xi, ni))


# ----------------------------------------------------------
# Nouvelles fonctions EduPython 2.0 (2.1 en fait)
# ----------------------------------------------------------
def sac_de_boule(boules:list):
    return boules[randint(0,len(boules)-1)]

def lance_de_de(nbre_de_face:int=6)->int:
    return randint(1,6)

def uniform(min, max):
    """
    min et max sont deux nombres.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un nombre décimal choisi de manière (pseudo)aléatoire et
    uniforme de l'intervalle [min,max[.
    """
    return alea.uniform(min, max)


def tirageBinomial(n, p):
    """
    n et p sont les paramètres de la loi binomiale à simuler.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un nombre entier choisi de manière aléatoire selon
    une loi de binomiale B(n,p).
    """
    s = 0
    for i in range(n):
        if random() < p:
            s = s + 1
    return s


def expovariate(l: reel):
    """
    l est un réel strictement positif.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un nombre réel choisi de manière aléatoire
    selon une loi exponentielle de paramètre l.
    """
    return alea.expovariate(l)


def gauss(mu, sigma):
    """
    mu et sigma sont deux réels.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie un nombre réel choisi de manière aléatoire
    selon une loi normale d'espérance mu et d'écart type sigma.
    """
    return alea.gauss(mu, sigma)


def normalFRep(a, b, mu, sigma):
    """
    a, b, mu et sigma sont quatre réels.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie une estimation de la probobilité P(a < X < b)
    lorsque X suit une loi normale d'espérance mu et d'écart type sigma.
    """
    if a < b:
        return norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)
    else:
        return 0


def invNorm(k, mu, sigma):
    """
    k, mu et sigma sont trois réels.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie la valeur du réel x telle que  P(X < x) = k
    lorsque X suit une loi normale d'espérance mu et d'écart type sigma.
    """
    return norm.ppf(k, mu, sigma)


def ajustement_affine(X, Y):
    """
    X et Y sont deux listes de nombre même taille
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Renvoie le couple (m,p) tel que y=mx+p soit l'ajustement affine de
    la série (X,Y) par méthode des moindres carrés.
    """
    m, p, _, _, _ = linregress(X, Y)
    return m, p


if __name__ == '__main__':
    for i in range(10):
        print(randint(0, 2))
