import random
import settings
from collections import namedtuple

Transaction = namedtuple("Transaction", ["round", "details"])
# === JOUEUR ===

class Joueur:
    def __init__(self, identifiant, strategie, portefeuille_init):
        self.identifiant = 'Joueur' + str(identifiant)
        self.portefeuille_init = portefeuille_init
        self.portefeuille = portefeuille_init 
        self.strategie = Strategie(strategie)
        self.historique_transaction = []

    def solde(self, resultat):
        self.portefeuille += resultat

    def applyStrat(self,):
        if self.strategie.strategie.__name__ == "copieur" and len(self.historique_transaction):
            try:
                if isinstance(self.historique_transaction[-1], dict) and len(self.historique_transaction[-1]) > 1:
                    ancien_joueur_adv = [j for j in self.historique_transaction[-1] if j not in ["Gagnant", self.identifiant]]
                    if ancien_joueur_adv:
                        mise = self.historique_transaction[-1].get(ancien_joueur_adv[0], {}).get("mise", True)
                        return self.strategie.strategie(mise)
            except :
                return self.strategie.strategie(True)

        elif self.strategie.strategie.__name__ == "trader":
            return self.strategie.strategie(self.portefeuille_init, self.portefeuille)
        else:
            return self.strategie.strategie()
    
    def __str__(self):
        return f'{self.identifiant} | {self.strategie.strategie.__name__} => Solde : {self.portefeuille}'


# === Partie ===

class Partie:
    
    def __init__(self, nombre_joueurs=settings.NB_JOUEURS, portefeuille_init=settings.PORTEFEUILLE_INIT, liste_proportion_strategie=settings.PROPORTION_STRAT, parametres=settings.DEFAULT, nb_echanges=settings.NB_ECHANGES):
        self.nombre_joueurs = nombre_joueurs
        self.parametres = parametres
        self.nb_echanges = nb_echanges
        self.portefeuille_init = portefeuille_init
        self.liste_strategies = self.proportionStrategies(liste_proportion_strategie)
        self.liste_joueurs = self.initJoueurs(self.nombre_joueurs, self.portefeuille_init)
        self.liste_transaction = []
        self.paires_joueurs = self.creerPaires()

    def creerPaires(self):
        paires = []
        for i in range(len(self.liste_joueurs)):
            for j in range(i+1, len(self.liste_joueurs)):
                paires.append((self.liste_joueurs[i], self.liste_joueurs[j]))
        return paires

    def proportionStrategies(self, liste_proportion_strategie):
        liste_strategies = []
        normalize = sum([element[1] for element in liste_proportion_strategie])
        if normalize != 1:
            liste_proportion_strategie = [(element[0], element[1]/normalize) for element in liste_proportion_strategie]
        for element in liste_proportion_strategie: 
            for nb_element in range(round(element[1]*100)):
                liste_strategies.append(element[0])
        return liste_strategies

    def initJoueurs(self, nombre_joueurs, portefeuille_depart):
        liste_joueurs = []
        for index_joueur in range(nombre_joueurs):
            nouveau_joueur = Joueur(index_joueur, random.choice(self.liste_strategies), portefeuille_depart)
            liste_joueurs.append(nouveau_joueur)
        return liste_joueurs

    def echange(self, joueur1, joueur2):
        echange = Echange(joueur1, joueur2, self.parametres, settings.NB_ECHANGES)
        print(echange.historique)
        self.liste_transaction.append(echange.historique)

    def __str__(self):
        return f"< Partie | {self.nombre_joueurs} Joueurs | {self.portefeuille_init}$ >"


# === Echange ===

class Echange:
    def __init__(self, joueur1, joueur2, parametres, nb_echanges):
        self.joueurs = (joueur1.identifiant, joueur2.identifiant)
        self.parametres = parametres
        self.gain_sans_triche = self.parametres["gain_sans_triche"]
        self.gain_une_triche = self.parametres["gain_une_triche"]
        self.gain_deux_triche = self.parametres["gain_deux_triche"]
        self.mise = self.parametres["mise"]
        self.historique = self.jeu(joueur1, joueur2, nb_echanges)

    def jeu(self, joueur1, joueur2, nb_echanges):
        historique = []
        for round_num in range(1, nb_echanges + 1):
            transaction = {}
            mise_joueur1 = joueur1.applyStrat()
            mise_joueur2 = joueur2.applyStrat()

            if mise_joueur1:
                if mise_joueur2:
                    joueur1.solde(self.gain_sans_triche - self.mise)
                    joueur2.solde(self.gain_sans_triche - self.mise)
                    transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'gains': self.gain_sans_triche - self.mise}
                    transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'gains': self.gain_sans_triche - self.mise}
                    transaction["Gagnant"] = "Cooperation"
                else:
                    joueur1.solde(-self.mise)
                    joueur2.solde(self.gain_une_triche)
                    transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'gains': -self.mise}
                    transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'gains': self.gain_une_triche}
                    transaction["Gagnant"] = joueur2.identifiant
            elif mise_joueur2:
                joueur1.solde(self.gain_une_triche)
                joueur2.solde(-self.mise)
                transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'gains': self.gain_une_triche}
                transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'gains': -self.mise}
                transaction["Gagnant"] = joueur1.identifiant
            else:
                joueur1.solde(self.gain_deux_triche)
                joueur2.solde(self.gain_deux_triche)
                transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'gains': self.gain_deux_triche}
                transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'gains': self.gain_deux_triche}
                transaction["Gagnant"] = "Tromperie"

            joueur1.historique_transaction.append(transaction)
            joueur2.historique_transaction.append(transaction)
            historique.append(transaction)
        joueur1.historique_transaction.append(Transaction(round=round_num, details=transaction))
        joueur2.historique_transaction.append(Transaction(round=round_num, details=transaction))
        return historique



# === Stratégie ===

class Strategie:
    def __init__(self, strategie):
        self.nom_strategie = strategie
        self.strategie = getattr(self, strategie, None)
        if not self.strategie:
            raise ValueError(f"Stratégie inconnue : '{strategie}'")

    def gentil(self):
        return True

    def mechant(self):
        return False

    def aleatoire(self):
        return random.choice([True, False])
    
    def copieur(self, reponse=None):
        if reponse is None or reponse:
            return True
        return False
    
    def trader(self, portefeuille_init, portefeuille):
        facteur_risque = (portefeuille_init - portefeuille) / portefeuille_init
        proba_de_jouer = 1 - facteur_risque
        return random.random() < proba_de_jouer
