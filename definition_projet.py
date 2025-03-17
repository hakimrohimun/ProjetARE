from random import random

class Joueur():
    liste_strategie = ['confiance', 'tricheur']
    def __init__(self, portefeuille, identifiant):
        self.identifiant = identifiant
        self.portefeuille = portefeuille 
        self.strategie = self.strategie(self.liste_strategie)

    def solde(self, portefeuille, resultat):
        return portefeuille + resultat

    def strategie(self, liste_strategie):
        strategie = liste_strategie[int((random()*100)%(len(self.liste_strategie)))]
        return strategie

    def __str__(self):
        return f'Joueur n°{self.identifiant} => Solde : {self.portefeuille}'


class Partie():
    def __init__(self, nombre_joueurs):
        self.nombre_joueurs = nombre_joueurs
        self.liste_joueurs = self.init_joueurs()
        self.strategies = self.proportion_strategies()

    def proportion_strategies(self):
        return 0

    def init_joueurs(self):
        liste_joueurs = {}
        for joueur in range(self.nombre_joueurs):
            liste_joueurs[f"joueur{joueur}"] = Joueur(990, joueur)
        return liste_joueurs



class Strategie():
    def altruiste():
        return 19


new_game = Partie(10)
for (key, value) in new_game.liste_joueurs.items() :
    print(key, value.strategie)
print("\n")
for (key, value) in new_game.liste_joueurs.items() :
    print(key, value.strategie)
