import random

#MODELS

class Joueur:
    #Initialisation de l'entité Joueur défini par une quantité d'argent, un identifiant, une stratégie et un historique de jeu.
    def __init__(self, portefeuille, identifiant, strategie):
        self.identifiant = 'Joueur' + str(identifiant) #Initialisation de l'id type : 'Joueur0'
        self.portefeuille_init = portefeuille
        self.portefeuille = portefeuille 
        self.strategie = Strategie(strategie)
        self.historique_transaction = []

    def solde(self, resultat):
        self.portefeuille += resultat

    def applyStrat(self):
        if self.strategie.strategie.__name__ == "copieur" and len(self.historique_transaction):
            ancien_joueur_adv = [element for element in self.historique_transaction[-1] if element not in ["Gagnant", self.identifiant]]
            return self.strategie.strategie(self.historique_transaction[-1][ancien_joueur_adv[0]])
        elif self.strategie.strategie.__name__ == "trader" :
            return self.strategie.strategie(self.portefeuille_init, self.portefeuille)
        else :
            return self.strategie.strategie()
    
    def __str__(self):
        return f'{self.identifiant} | {self.strategie.strategie.__name__} => Solde : {self.portefeuille}'


class Partie:
    #Initie la partie par en créant les joueurs en fonction du nombre de joueur passé en paramètre 
    def __init__(self, nombre_joueurs, portefeuille_depart, liste_proportion_strategie):
        self.nombre_joueurs = nombre_joueurs #Initie la variable nombre de joueur qui est définie pour la partie
        self.portefeuille_depart = portefeuille_depart #Initie la valeur des portefeuille de chaque joueurs au départ
        self.liste_strategies = self.proportionStrategies(liste_proportion_strategie) #Definie une liste avec 100 element qui represente la répartition des strategies à partir d'une liste d'entre formaté. On l'appellera pour assigné une stratégie à un joueur.
        self.liste_joueurs = self.initJoueurs(self.nombre_joueurs, self.portefeuille_depart) #Initie tous les joueurs avec un portefeuille de départ et une strategie basée sur la proportion de strategie de départ.
        self.liste_transaction = []

    #Definie une liste de 100 element dont la réccurence de chaque element est equivalent à la proportion d'appartition de la stratégie dans la population. Cette liste est crée à partir d'une liste formaté type : [('strategie', (int)proportion)] 
    def proportionStrategies(self, liste_proportion_strategie):
        liste_strategies = []
        normalize = sum([element[1] for element in liste_proportion_strategie])
        if normalize != 1:
            liste_proportion_strategie = [(element[0], element[1]/normalize) for element in liste_proportion_strategie] #Normalise la liste des strategie en entre telle qu'elle soit repartie sur 1 
        for element in liste_proportion_strategie: 
            for nb_element in range(round(element[1]*100)) :
                liste_strategies.append(element[0])
        return liste_strategies

    def initJoueurs(self, nombre_joueurs, portefeuille_depart):
        liste_joueurs = [] #Dictionnaire de recensement de tous les Joueurs de la partie avec un identifiant en key et leur objet en Value  
        for index_joueur in range(nombre_joueurs):
            indice_strategie = int((random.random()*100)%(len(self.liste_strategies)))
            nouveau_joueur = Joueur(portefeuille_depart, index_joueur, self.liste_strategies[indice_strategie])
            liste_joueurs.append(nouveau_joueur)
        return liste_joueurs

    def __str__(self):
        return f"< Partie | {self.nombre_joueurs} Joueurs | {self.portefeuille_depart}$ >"



class Echange:
    def __init__(self, joueur1, joueur2):
        self.joueurs = (joueur1.identifiant, joueur2.identifiant)
        self.resume = self.jeu(joueur1, joueur2)
        joueur1.historique_transaction.append(self.resume)
        joueur2.historique_transaction.append(self.resume)

    def jeu(self, joueur1, joueur2):
        """simulation d'un échange entre deux individus
        r1 et r2 correspondent aux réponses des deux individus respectifs au tour précédent (None signifie qu'il s'agit du premier 
        tour)"""
        transaction = {} #Resume la transaction qui sera incluse dans l'historique de chaque Joueur 
        mise_joueur1 = joueur1.applyStrat()
        mise_joueur2 = joueur2.applyStrat()
        if mise_joueur1:
            if mise_joueur2:
                joueur1.solde(gain_sans_triche-mise) #Adapte le solde des participant à actuel+gain si les deux ont mis
                joueur2.solde(gain_sans_triche-mise)
                transaction[joueur1.identifiant] = {'mise' : mise_joueur1, 'Gains' : gain_sans_triche-mise}
                transaction[joueur2.identifiant] = {'mise' : mise_joueur2, 'Gains' : gain_sans_triche-mise}
                transaction["Gagnant"] = "Cooperation"
            else : 
                joueur1.solde(-mise) #Adapte le solde des participant à actuel+gain si le Joueur2 n'a pas mis
                joueur2.solde(gain_une_triche)
                transaction[joueur1.identifiant] = {'mise' : mise_joueur1, 'Gains' : -mise}
                transaction[joueur2.identifiant] = {'mise' : mise_joueur2, 'Gains' : gain_une_triche}
                transaction["Gagnant"] = joueur2.identifiant
        elif mise_joueur2:
            joueur1.solde(gain_une_triche) #Adapte le solde des participant à actuel+gain si le Joueur1 n'a pas mis
            joueur2.solde(-mise)
            transaction[joueur1.identifiant] = {'mise' : mise_joueur1, 'Gains' : gain_une_triche}
            transaction[joueur2.identifiant] = {'mise' : mise_joueur2, 'Gains' : -mise}
            transaction["Gagnant"] = joueur1.identifiant
        else :
            transaction[joueur1.identifiant] = {'mise' : mise_joueur1, 'Gains' : gain_deux_triche}
            transaction[joueur2.identifiant] = {'mise' : mise_joueur2, 'Gains' : gain_deux_triche}
            transaction["Gagnant"] = "Tromperie"
        return transaction



class Strategie:
    def __init__(self, strategie):
        # Associe la stratégie à la méthode correspondante
        self.strategie = getattr(self, strategie, None)
        if not self.strategie:
            raise ValueError(f"Stratégie inconnue : '{strategie}'")

    def gentil(self):
        """L'individu met tout le temps une pièce"""
        return True

    def mechant(self):
        """L'individu ne met jamais de pièce"""
        return False

    def aleatoire(self):
        """L'individu décide aléatoirement de mettre ou non une pièce"""
        return random.choice([True, False])
    
    def copieur(self, reponse=None):
        """L'individu commence par mettre une pièce, puis copie la réponse précédente"""
        if reponse is None or reponse:  # Première fois ou copie d'un coup favorable
            return True
        return False
    
    def trader(self, portefeuille_init, portefeuille):
        """ foncton de stratégie de jeu ,prend une liste de joeurs en entrée : plus le joueur perd de son portefeuille, 
        moins il joue"""
        facteur_risque = (portefeuille_init - portefeuille) / portefeuille_init
        proba_de_jouer = 1 - facteur_risque
        if random.random() < proba_de_jouer:
            return True
        else:
            return False


#MAIN

#Parametre initiaux définis par l'utilisateur ?

#nombre de joueurs
nb_joueurs = 50
#Nombre de Tours
nb_tour = 150
#definition du portefeuille de départ. Voire si il est le meme pour tous ou variable en fonctrion de certain critère à définir
portefeuille_init = 1000
#nb pièces pour la mise c a d True
mise = 1
#différent gain en fonction des mises. Les gains sont indiqué comme le retour de pièce. c a d avec un gain sans triche de 2, l'utilisateur gagne réellement seulement 1 piece car mise = 1
gain_sans_triche = 2
gain_une_triche = 3
gain_deux_triche = 0

#definition d'une liste de répartition des stratégies dans la partie 
prop_strat = [('gentil', 0.2), ('mechant', 0.2), ('aleatoire', 0.1), ('copieur', 0.01), ('trader', 0.02)]

#Creation d'une partie avec un nombre de joueur, un portefeuille de départ pour la population, une liste de répartition des stratégies dans la population
new_game = Partie(nb_joueurs, portefeuille_init, prop_strat)


#DEBUT SIMULATION

#recupération de la liste de joueurs
liste_Joueurs = new_game.liste_joueurs

for tour in range(nb_tour):
    index_echange = 1
    for nb_echanges in range(len(liste_Joueurs)-1):
        for indice_joueur in range(len(liste_Joueurs)) :
            joueur1 = liste_Joueurs[indice_joueur]
            joueur2 = liste_Joueurs[(indice_joueur + index_echange) % nb_joueurs]
            new_transation = Echange(joueur1, joueur2)
            new_game.liste_transaction.append(new_transation.resume)
            #print(joueur1, "\t\t", joueur2, "\n")
            #print(f'RESUME DE LA TRANSACTION : \n {new_transation.resume}\n')
        index_echange += 1

for joueurs in liste_Joueurs:
    print(joueurs)
        


