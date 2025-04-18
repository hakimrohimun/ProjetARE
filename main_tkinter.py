import tkinter as tk
from tkinter import ttk
import models
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

nombre_joueurs = 10
portefeuille_init = 1000

prop_strat = {
    'gentil': 0.2, 
    'mechant': 0.2, 
    'aleatoire': 0.2, 
    'copieur': 0.2, 
    'trader': 0.2,
}

couleurs = {
    "gentil": "green",
    "mechant": "red",
    "aleatoire": "gray",
    "copieur": "blue",
    "trader" : "purple",
}


def creer_prop_dict(prop_strat):
    """
    adapte le dictionaire tkinter avec de Double var pour avoir le dictionaire utilisable dans partie
    """
    return {
        key: (val.get() if isinstance(val, tk.DoubleVar) else val)
        for key, val in prop_strat.items()
    }


class PartieTkinter:

    def __init__(self, button_frame, results_frame, graph_frame):
        self.button_frame = button_frame
        self.results_frame = results_frame
        self.graph_frame = graph_frame
        self.partie = None

        # Historique des totaux d'argent
        self.argent_history = []
        self.tour = 0

        # Boutons Créer / Jouer
        self.create_btn = ttk.Button(
            button_frame, text="Créer une partie", command=self.create_game
        )
        self.play_btn = ttk.Button(
            button_frame, text="Jouer un tour",
            command=self.play_turn, state='disabled'
        )
        self.create_btn.pack(side='left', expand=True, padx=5)
        self.play_btn.pack(  side='left', expand=True, padx=5)

        # Configuration du graphe (créé une seule fois)
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax  = self.fig.add_subplot(121)
        self.his  = self.fig.add_subplot(122)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='NSEW')
        # rendre le canevas responsive
        self.graph_frame.rowconfigure(0, weight=1)
        self.graph_frame.columnconfigure(0, weight=1)

    def create_game(self):
        """Initialise (ou ré‑initialise) la partie et les affichages."""
        # Vide le cadre des résultats
        for w in self.results_frame.winfo_children():
            w.destroy()

        self.ax.clear()
        self.his.clear()

        # Ré‑initialise l'historique argent
        if len(self.argent_history) < 2:
            self.argent_history.append([])
        else :
            self.argent_history.pop(0)
            self.argent_history.append([])

        # Crée le modèle Partie
        props = creer_prop_dict(prop_strat)
        self.partie = models.Partie(
            nombre_joueurs,
            portefeuille_init = portefeuille_init,
            liste_proportion_strategie=props
        )
        self.tour = 0

        self._update_results()
        self._update_graph()
        self._update_histogram()
        self.canvas.draw()

        # Active le bouton « Jouer un tour »
        self.play_btn.config(state='normal')

    def play_turn(self):
        """Exécute un seul tour, met à jour résultats et graphique."""
        # Effectue toutes les transactions du tour
        for j1, j2 in self.partie.paires_joueurs:
            self.partie.echange(j1, j2)
        # Mémorise le total après ce tour
        self._update_results()
        self._update_graph()
        self._update_histogram()

        self.canvas.draw()

    def _update_results(self):
        """Réaffiche les portefeuilles et stratégies de tous les joueurs."""
        for w in self.results_frame.winfo_children():
            w.destroy()

        for idx, joueur in enumerate(self.partie.liste_joueurs):
            couleur = couleurs.get(joueur.strategie.nom_strategie, 'black')
            ttk.Label(self.results_frame, text=f"{joueur.identifiant} ({joueur.strategie.nom_strategie}) - Pièces: {joueur.portefeuille}", foreground=couleur).grid(row=idx, column=0, sticky='W', padx=5, pady=2)

    def _update_graph(self):
        """Met à jour le graphique de l'argent total en circulation."""
        # Calcule le total actuel
        total = sum(j.portefeuille for j in self.partie.liste_joueurs)

        # Ajoute un nouveau point dans l'historique
        self.tour += 1
        self.argent_history[-1].append(total)
        
        self.ax.clear()
        self.ax.plot(
            [i for i in range(self.tour)],
            self.argent_history[-1],
            marker='o', label="Argent total actuel"
        )
        self.ax.plot(
            [i for i in range(self.tour) if i < len(self.argent_history[0])],
            [self.argent_history[0][i] for i in range(self.tour) if i < len(self.argent_history[0])],
            marker='o', label="Argent total tour précédent"
        )
        self.ax.set_xlabel("Numéro de tour")
        self.ax.set_ylabel("Argent en circulation ($)")
        self.ax.set_title("Évolution de l'argent par tour")
        self.ax.legend(loc='best')
        self.ax.grid(True)

    
    def _update_histogram(self):
        totals = {}
        for joueur in self.partie.liste_joueurs:
            strat = joueur.strategie.nom_strategie
            totals[strat] = totals.get(strat, 0) + joueur.portefeuille
        strategies = list(totals.keys())
        valeurs = list(totals.values())
        self.his.clear()
        self.his.bar(strategies, valeurs)
        self.his.set_xlabel("Stratégie")
        self.his.set_ylabel("Argent total ($)")
        self.his.set_title("Répartition de l'argent par stratégie")
        self.his.grid(axis='y', linestyle='--', alpha=0.5)



def rescale():
    """
    Normalise les scales de la fenètre tkinter
    """
    total = sum(var.get() for var in prop_strat.values() if isinstance(var, tk.DoubleVar))
    if total <= 0:
        return
    for key, var in prop_strat.items():
        if isinstance(var, tk.DoubleVar):
            var.set(var.get() / total)


def init_button_frame(frame, prop_strat):
    """
    Initialise la frame avec les scales et prépare la frame buttons pour plus tard
    """

    count_vars = {}

    def onsclale(value):
        rescale()
        for strat in count_vars.keys():
            count_vars[strat].set(
                round(prop_strat[strat].get() * nombre_joueurs)
            )

    for idx, strat in enumerate(prop_strat):
        lbl = ttk.Label(frame, text=strat.capitalize())
        lbl.grid(row=idx, column=0, sticky='W', padx=5, pady=2)

        prop_strat[strat] = tk.DoubleVar(value=prop_strat[strat])
        count_vars[strat] = tk.IntVar(value=round(prop_strat[strat].get() * nombre_joueurs))
        sl = ttk.Scale(
            frame, from_=0, to=1,
            variable=prop_strat[strat],
            command=onsclale
        )
        sl.grid(row=idx, column=1, sticky='EW', padx=5, pady=2)
        value_strat = ttk.Label(frame, textvariable=count_vars[strat])
        value_strat.grid(row=idx, column=2, sticky='E', padx=5, pady=2)

    frame.columnconfigure(1, weight=1)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(
        row=len(prop_strat),
        column=0, columnspan=2,
        pady=10, sticky='EW'
    )
    return btn_frame
        

def main():
    root = tk.Tk()
    root.title("Simulation ARE")
    root.geometry("1000x700")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    #Creation des frames d'affichages
    results_frame = ttk.Frame(root, borderwidth=2, relief='groove')
    manipulation_frame = ttk.Frame(root, borderwidth=2, relief='groove')
    graph_frame = ttk.Frame(root, borderwidth=2, relief='groove')

    results_frame.grid(row=0, column=0, columnspan=1,rowspan=1, padx=10, pady=10, sticky='NSEW')
    manipulation_frame.grid(row=0, column=1, padx=10,columnspan=1,rowspan=1, pady=10, sticky='NSEW')
    graph_frame.grid(row=1, column=0, columnspan=2, rowspan=1, padx=10, pady=10, sticky='NSEW')

    #Initialisation de la fenetre boutton
    button_frame = init_button_frame(manipulation_frame, prop_strat)

    #Initionalisation de l'app
    app = PartieTkinter(button_frame, results_frame, graph_frame)

    root.mainloop()


if __name__ == "__main__":
    main()
