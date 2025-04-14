import models
import tkinter

# MAIN
# Paramètres initiaux
nb_joueurs = 10
nb_tour = 30
portefeuille_init = 1000
mise = 1
gain_sans_triche = 2
gain_une_triche = 2
gain_deux_triche = 0

prop_strat = [('gentil', 0.1), ('mechant', 0.2), ('aleatoire', 0.3), ('copieur', 0.4), ('trader', 0.2)]

new_game = models.Partie(nb_joueurs, portefeuille_init, prop_strat)

# DEBUT SIMULATION
for tour in range(nb_tour):    
    for paire in new_game.paires_joueurs:
        joueur1, joueur2 = paire
        new_transaction = new_game.echange(joueur1, joueur2)

# Affichage des résultats
print("\n=== Résultats finaux ===")
for joueur in new_game.liste_joueurs:
    print(joueur)

print(new_game.liste_transaction)
