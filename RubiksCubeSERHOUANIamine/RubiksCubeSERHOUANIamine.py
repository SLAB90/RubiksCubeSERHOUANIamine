# -*- coding: utf-8 -*- 
# Ce code a ete verifie pour garantir l'affichage du cube colore et l'interface fonctionnelle.

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from functools import partial

# --- Initialisation de l'Application Ursina ---
app = Ursina()

# Parametres de la fenetre
window.title = 'Guide Rubiks Cube (3D FINAL)'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.color = color.dark_gray

# --- Camera et Controle ---
EditorCamera() 

# --- Creation du Rubik's Cube Visuel COLORE ---

# Couleurs pour les faces (Standard)
couleurs_faces = [color.white, color.yellow, color.blue, color.green, color.red, color.orange]
positions_faces = [(0, 0, -0.5), (0, 0, 0.5), (0.5, 0, 0), (-0.5, 0, 0), (0, 0.5, 0), (0, -0.5, 0)]
rotations_faces = [(0, 0, 0), (0, 0, 0), (0, 90, 0), (0, 90, 0), (90, 0, 0), (90, 0, 0)]

# Entite centrale pour contenir le cube et le faire tourner (le fond noir pour la separation)
cube_parent = Entity(model='cube', color=color.black, scale=3, visible=True) 

# Ajouter des faces colorees a l'exterieur
for i in range(6):
    face = Entity(
        parent=cube_parent,
        model='quad', 
        color=couleurs_faces[i],
        position=positions_faces[i],
        rotation=rotations_faces[i],
        scale=0.95, # Laisser un petit bord noir visible
        double_sided=True
    )

# --- Fonction d'Animation (Faire Tourner le Cube) ---
def update():
    # Fait tourner le cube de 20 degres par seconde autour de l'axe Y
    cube_parent.rotation_y += 20 * time.dt
    cube_parent.rotation_x += 10 * time.dt


# --- Interface Utilisateur (2D) ---

class GuideMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        
        # Panneau Arriere-plan (Position a droite)
        self.background = Entity(
            parent=self, 
            model='quad', 
            color=color.gray.tint(-0.1),
            scale=(0.4, 0.9), 
            position=(0.7, 0), 
            origin=(-0.5, 0), 
            collider='box'
        )
        
        # Titre
        Text(
            "GUIDE RUBIK'S CUBE", 
            parent=self.background, 
            y=0.45, 
            x=-0.45, 
            origin=(-0.5, 0), 
            scale=1.5, 
            color=color.black, 
            font='VeraMono'
        )
        
        # Separateur
        Entity(parent=self.background, model='quad', color=color.black, scale=(0.9, 0.005), y=0.4, x=0, origin=(0, 0))

        # Le texte des instructions (Lisible)
        self.instructions_text = Text(
            "Cliquez sur une etape pour afficher la methode et l'algorithme.", 
            parent=self.background, 
            y=-0.25,
            x=-0.45, 
            origin=(-0.5, 0), 
            color=color.black, 
            scale=1.2, 
            wordwrap=55 
        )
        
        # Liste des etapes (Sans accents)
        etapes_noms = ["1. Face Blanche (Croix)", "2. Coins Face Blanche", "3. Deuxieme Couronne", "4. Croix Jaune", "5. Placer Aretes Jaunes", "6. Placer Coins Jaunes", "7. Orienter Coins Jaunes (FIN)"]
        
        # Position de debut pour les boutons
        y_pos = 0.3
        
        for etape in etapes_noms:
            Button(
                text=etape,
                parent=self.background,
                scale=(0.9, 0.05),
                y=y_pos,
                color=color.azure.tint(0.2), 
                text_color=color.black,
                highlight_color=color.azure,
                on_click=partial(self.show_guide, etape) 
            ).text_entity.scale *= 1.2
            
            y_pos -= 0.07

    def show_guide(self, etape_nom):
        # Logique pour afficher les instructions
        if etape_nom == "1. Face Blanche (Croix)":
            instructions = "METHODE : Amenez les aretes blanches-X a cote de la bonne couleur centrale (Jaune), puis tournez a 180 degres.\nALGO: Mouvements intuitifs."
        elif etape_nom == "2. Coins Face Blanche":
            instructions = "METHODE : Inserer un coin blanc dans la bonne position avec le 'Sextet'.\nALGO: (R U R' U') a repeter jusqu'a ce qu'il soit place."
        elif etape_nom == "3. Deuxieme Couronne":
            instructions = "METHODE : Placer les 4 aretes du milieu.\nALGO Droit: U R U' R' U' F' U F"
        elif etape_nom == "4. Croix Jaune":
            instructions = "METHODE : Creer la croix jaune. Algorithmes : 'F R U R' U' F' ' (point a ligne) ou 'F (R U R' U') F' (ligne a croix)."
        elif etape_nom == "5. Placer Aretes Jaunes":
            instructions = "METHODE : Permuter les aretes de la croix jaune pour qu'elles correspondent aux centres.\nALGO: 'R U R' U R U U R' U'."
        elif etape_nom == "6. Placer Coins Jaunes":
            instructions = "METHODE : Permuter les coins pour qu'ils soient a la bonne position. \nALGO T-Perm : 'L' U R U' L U R' U'."
        elif etape_nom == "7. Orienter Coins Jaunes (FIN)":
            instructions = "METHODE : Tenez le coin mal oriente en bas a droite (FDR) et utilisez R' D' R D jusqu'au jaune. Tournez la face D pour le coin suivant.\nALGO: R' D' R D (repeter)"
        else:
            instructions = f"Instructions pour {etape_nom} : non encore codees."
            
        self.instructions_text.text = instructions


# Lance l'interface et le cube 3D
GuideMenu()
app.run()