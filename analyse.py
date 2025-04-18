from models import Partie, Echange, Joueur
import matplotlib.pyplot as plt
import settings
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

portefeuille_init = settings.PORTEFEUILLE_INIT
nb_echanges = settings.NB_ECHANGES
parametres = settings.DEFAULT

Gentil = Joueur(0, 'gentil', portefeuille_init)
Mechant = Joueur(1, 'mechant', portefeuille_init)
Trader = Joueur(2, 'trader', portefeuille_init)
Copieur = Joueur(3, 'copieur', portefeuille_init)
Aleatoire = Joueur(4, 'aleatoire', portefeuille_init)


def affichage_argent(perso1, perso2, nb_echanges):
    """ """
    liste_argent1 = [perso1.portefeuille]
    liste_argent2 = [perso2.portefeuille]
    Echange(perso1, perso2, nb_echanges, parametres)
    liste_argent1.append(perso1.portefeuille)
    liste_argent2.append(perso2.portefeuille)
    i = 0
    while i < (nb_echanges - 1) and perso1.portefeuille > 0 and perso2.portefeuille > 0:
        Echange(perso1, perso2, nb_echanges, parametres)
        liste_argent1.append(perso1.portefeuille)
        liste_argent2.append(perso2.portefeuille)
        i += 1
    while len(liste_argent1) < nb_echanges+1:
        liste_argent1.append(perso1.portefeuille)
        liste_argent2.append(perso2.portefeuille)
    
    plt.plot([j for j in range(nb_echanges+1)], liste_argent1)
    plt.plot([k for k in range(nb_echanges+1)],liste_argent2)
    plt.ylabel("Tours")
    plt.xlabel("Argent")
    return (liste_argent1,liste_argent2)


def moyenne_des_graphes(perso1, perso2, nb_echanges, nb_simulations=20):
    resultats = []
    
    for _ in range(nb_simulations):
        liste_argent = affichage_argent(perso1, perso2, nb_echanges)
        print(perso1.portefeuille, perso2.portefeuille)
        resultats.append(liste_argent)
    
    nb_tours = nb_echanges + 1
    moy1 = [0] * nb_tours
    moy2 = [0] * nb_tours
    
    for i in range(nb_tours):
        moy1[i] = sum([resultats[j][0][i] for j in range(nb_simulations)]) / nb_simulations
        moy2[i] = sum([resultats[j][1][i] for j in range(nb_simulations)]) / nb_simulations
    
    print(moy1, moy2)

    plt.plot(range(nb_tours), moy1, label="Moyenne Perso1")
    plt.plot(range(nb_tours), moy2, label="Moyenne Perso2")
    plt.xlabel("Tours")
    plt.ylabel("Argent")
    plt.legend()
    plt.show()

    return moy1, moy2


# === TEST ===


#Changer le protefeuille initial ?
