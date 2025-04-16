import tkinter as tk
import random

class Joueur:
    def __init__(self, identifiant, strategie, total_tours=100):
        self.id = identifiant
        self.strategie = strategie
        self.pieces = 5
        self.derniere_action = True
        self.pertes_consecutives = 0
        self.tour_actuel = 0
        self.total_tours = total_tours
        self.historique_pieces = [self.pieces]

    def choisir_action(self, dernier_choix_adversaire=None):
        self.tour_actuel += 1
        if self.strategie == "gentil":
            return True
        elif self.strategie == "méchant":
            return False
        elif self.strategie == "aléatoire":
            return random.choice([True, False])
        elif self.strategie == "copieur" and dernier_choix_adversaire is not None:
            return dernier_choix_adversaire
        elif self.strategie == "opportuniste":
            return self.derniere_action
        elif self.strategie == "pacifiste":
            return self.pertes_consecutives < 2
        elif self.strategie == "vengeur" and dernier_choix_adversaire is not None:
            return dernier_choix_adversaire
        elif self.strategie == "tricheur_pair":
            return self.tour_actuel % 2 != 0
        elif self.strategie == "tricheur_impair":
            return self.tour_actuel % 2 == 0
        elif self.strategie == "mi_parcours":
            return self.tour_actuel <= self.total_tours // 2
        return True

class Jeu:
    def __init__(self, root):
        self.joueurs = []
        self.joueurs_elimines = []
        self.root = root
        self.tour = 1

        self.nb_joueurs_var = tk.IntVar(value=10)
        self.scale_joueurs = tk.Scale(root, from_=2, to=10, orient="horizontal", variable=self.nb_joueurs_var, label="Nombre de joueurs")
        self.scale_joueurs.pack()

        self.label_tour = tk.Label(root, text="Tour: 1", font=("Arial", 12))
        self.label_tour.pack(pady=5)

        self.frame_etat = tk.Frame(root)
        self.frame_etat.pack()

        self.bouton_tour = tk.Button(root, text="Lancer la simulation", command=self.lancer_simulation)
        self.bouton_tour.pack(pady=5)

        self.label_elimines = tk.Label(root, text="", fg="red")
        self.label_elimines.pack()

    def lancer_simulation(self):
        nb_joueurs = self.nb_joueurs_var.get()
        strategies = ["gentil", "méchant", "aléatoire", "copieur", "opportuniste", "pacifiste", "vengeur", "tricheur_pair", "tricheur_impair", "mi_parcours"]
        self.joueurs = [Joueur(i + 1, strategies[i % len(strategies)]) for i in range(nb_joueurs)]
        self.joueurs_elimines = []
        self.tour = 1
        self.label_tour.config(text="Tour: 1")

        for widget in self.frame_etat.winfo_children():
            widget.destroy()

        self.bouton_jouer_tour = tk.Button(self.root, text="Jouer un tour", command=self.jouer_tour)
        self.bouton_jouer_tour.pack(pady=5)
        self.mettre_a_jour_affichage()

    def joueur_couleur(self, strategie):
        couleurs = {
            "gentil": "green",
            "méchant": "red",
            "aléatoire": "gray",
            "copieur": "blue",
            "opportuniste": "orange",
            "pacifiste": "purple",
            "vengeur": "darkred",
            "tricheur_pair": "brown",
            "tricheur_impair": "magenta",
            "mi_parcours": "teal"
        }
        return couleurs.get(strategie, "black")

    def mettre_a_jour_affichage(self):
        for widget in self.frame_etat.winfo_children():
            widget.destroy()

        for j in self.joueurs:
            couleur = self.joueur_couleur(j.strategie)
            txt = f"Joueur {j.id} ({j.strategie}) - Pièces: {j.pieces}"
            tk.Label(self.frame_etat, text=txt, fg=couleur).pack(anchor="w")

    def jouer_tour(self):
        if len(self.joueurs) <= 1:
            self.afficher_resultat_final()
            return

        for i, joueur1 in enumerate(self.joueurs):
            for j, joueur2 in enumerate(self.joueurs):
                if i < j:
                    choix1 = joueur1.choisir_action(joueur2.derniere_action)
                    choix2 = joueur2.choisir_action(joueur1.derniere_action)

                    if choix1 and choix2:
                        joueur1.pieces += 2
                        joueur2.pieces += 2
                    elif choix1 and not choix2:
                        joueur1.pieces -= 1
                        joueur2.pieces += 3
                        joueur1.pertes_consecutives += 1
                        joueur2.pertes_consecutives = 0
                    elif not choix1 and choix2:
                        joueur1.pieces += 3
                        joueur2.pieces -= 1
                        joueur2.pertes_consecutives += 1
                        joueur1.pertes_consecutives = 0
                    else:
                        joueur1.pertes_consecutives = 0
                        joueur2.pertes_consecutives = 0

                    joueur1.derniere_action = choix1
                    joueur2.derniere_action = choix2

        elimines = [j for j in self.joueurs if j.pieces <= 0]
        for e in elimines:
            if all(e.id != x[0] for x in self.joueurs_elimines):
                self.joueurs_elimines.append((e.id, e.strategie, self.tour))

        self.joueurs = [j for j in self.joueurs if j.pieces > 0]
        self.tour += 1
        self.label_tour.config(text=f"Tour: {self.tour}")
        self.mettre_a_jour_affichage()
        self.mettre_a_jour_elimines()

        if len(self.joueurs) <= 1:
            self.afficher_resultat_final()

    def mettre_a_jour_elimines(self):
        if not self.joueurs_elimines:
            self.label_elimines.config(text="")
            return
        texte = "Joueurs éliminés :\n"
        for j in self.joueurs_elimines:
            texte += f"- Joueur {j[0]} ({j[1]}) au tour {j[2]}\n"
        self.label_elimines.config(text=texte)

    def afficher_resultat_final(self):
        gagnant = self.joueurs[0] if self.joueurs else None
        resume = tk.Toplevel(self.root)
        resume.title("Résultat Final")

        message = f"Gagnant : Joueur {gagnant.id} ({gagnant.strategie}) avec {gagnant.pieces} pièces" if gagnant else "Aucun joueur n'a survécu."
        tk.Label(resume, text=message, font=("Arial", 14), fg="blue").pack(pady=10)

        tk.Label(resume, text="\nJoueurs éliminés :", fg="red").pack()
        for j in self.joueurs_elimines:
            txt = f"- Joueur {j[0]} ({j[1]}) au tour {j[2]}"
            tk.Label(resume, text=txt, anchor="w").pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulation ARE - Niveau Expert")
    jeu = Jeu(root)
    root.mainloop()
