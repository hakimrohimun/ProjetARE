import random

# MODELS

class Joueur:
    def __init__(self, portefeuille, identifiant, strategie):
        self.identifiant = 'Joueur' + str(identifiant)
        self.portefeuille_init = portefeuille
        self.portefeuille = portefeuille 
        self.strategie = Strategie(strategie)
        self.historique_transaction = []

    def solde(self, resultat):
        self.portefeuille += resultat

    def applyStrat(self,):
        if self.strategie.strategie.__name__ == "copieur" and len(self.historique_transaction):
            try:
                ancien_joueur_adv = [element for element in self.historique_transaction[-1] if element not in ["Gagnant", self.identifiant]]
                return self.strategie.strategie(self.historique_transaction[-1][ancien_joueur_adv[0]]['mise'])
            except :
                return self.strategie.strategie(True)

            return self.strategie.strategie(self.historique_transaction[-1][ancien_joueur_adv[0]]['mise'])
        elif self.strategie.strategie.__name__ == "trader":
            return self.strategie.strategie(self.portefeuille_init, self.portefeuille)
        else:
            return self.strategie.strategie()
    
    def __str__(self):
        return f'{self.identifiant} | {self.strategie.strategie.__name__} => Solde : {self.portefeuille}'


class Partie:
    def __init__(self, nombre_joueurs, portefeuille_depart, liste_proportion_strategie):
        self.nombre_joueurs = nombre_joueurs
        self.portefeuille_depart = portefeuille_depart
        self.liste_strategies = self.proportionStrategies(liste_proportion_strategie)
        self.liste_joueurs = self.initJoueurs(self.nombre_joueurs, self.portefeuille_depart)
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
            indice_strategie = int((random.random()*100)%(len(self.liste_strategies)))
            nouveau_joueur = Joueur(portefeuille_depart, index_joueur, self.liste_strategies[indice_strategie])
            liste_joueurs.append(nouveau_joueur)
        return liste_joueurs

    def __str__(self):
        return f"< Partie | {self.nombre_joueurs} Joueurs | {self.portefeuille_depart}$ >"


class Echange:
    def __init__(self, joueur1, joueur2, nb_echanges=10):
        self.joueurs = (joueur1.identifiant, joueur2.identifiant)
        self.resume = self.jeu(joueur1, joueur2, nb_echanges)
        
    def jeu(self, joueur1, joueur2, nb_echanges):
        historique = []
        
        for _ in range(nb_echanges):
            transaction = {}
            mise_joueur1 = joueur1.applyStrat()
            mise_joueur2 = joueur2.applyStrat()
            
            if mise_joueur1:
                if mise_joueur2:
                    joueur1.solde(gain_sans_triche-mise)
                    joueur2.solde(gain_sans_triche-mise)
                    transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'Gains': gain_sans_triche-mise}
                    transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'Gains': gain_sans_triche-mise}
                    transaction["Gagnant"] = "Cooperation"
                else:
                    joueur1.solde(-mise)
                    joueur2.solde(gain_une_triche)
                    transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'Gains': -mise}
                    transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'Gains': gain_une_triche}
                    transaction["Gagnant"] = joueur2.identifiant
            elif mise_joueur2:
                joueur1.solde(gain_une_triche)
                joueur2.solde(-mise)
                transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'Gains': gain_une_triche}
                transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'Gains': -mise}
                transaction["Gagnant"] = joueur1.identifiant
            else:
                joueur1.solde(gain_deux_triche)
                joueur2.solde(gain_deux_triche)
                transaction[joueur1.identifiant] = {'mise': mise_joueur1, 'Gains': gain_deux_triche}
                transaction[joueur2.identifiant] = {'mise': mise_joueur2, 'Gains': gain_deux_triche}
                transaction["Gagnant"] = "Tromperie"
            joueur1.historique_transaction.append(transaction)
            joueur2.historique_transaction.append(transaction)
            historique.append(transaction)
        joueur1.historique_transaction.append({})
        joueur2.historique_transaction.append({})
        
        return historique



class Strategie:
    def __init__(self, strategie):
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


# MAIN
# Paramètres initiaux
nb_joueurs = 20
nb_tour = 20
portefeuille_init = 1000
mise = 1
gain_sans_triche = 2
gain_une_triche = 2
gain_deux_triche = 0

prop_strat = [('gentil', 0), ('mechant', 0.2), ('aleatoire', 0.1), ('copieur', 0.4), ('trader', 0.2)]

new_game = Partie(nb_joueurs, portefeuille_init, prop_strat)

# DEBUT SIMULATION
for tour in range(nb_tour):    
    for paire in new_game.paires_joueurs:
        joueur1, joueur2 = paire
        new_transaction = Echange(joueur1, joueur2, 10)
        new_game.liste_transaction.extend(new_transaction.resume)
    mini=-1
    maxi=-1
    for joueur in new_game.liste_joueurs:
        if mini==-1 or mini.portefeuille>joueur.portefeuille:
            mini=joueur
        if maxi==-1 or maxi.portefeuille<joueur.portefeuille:
            maxi=joueur
    mini.strategie = maxi.strategie


# Affichage des résultats
print("\n=== Résultats finaux ===")
for joueur in new_game.liste_joueurs:
    print(joueur)
