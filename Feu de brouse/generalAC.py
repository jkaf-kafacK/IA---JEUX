import sys, math, random
import pygame
import pygame.draw
import numpy as np
from random import sample
import time
from matplotlib.pyplot import figure
import math

import matplotlib.pyplot as plt
# mettre aussi les abres apres le feu
__screenSize__ = (900,900) #(1280,1280)
__cellSize__ = 10
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))
__density__ = 0.7
controle = False
#__colors__ = [(255,255,255),(0,0,0),(140,140,140)]

__colors__ = [(255,255,240),(57,255,20),(251,90, 65),(191,191,191)]
liss_dist = {}
CLAY = 0
TREE = 1
FIRE = 2
DAI = 3
list_a = []
lista_percent = []
listaArbreResta=[]
glidergun=[
  [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
  [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
  [1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]]

COLORS = ["ivory", "lime green", "red", "gray75"]


def getColorCell(n):
    return __colors__[n]

class Grid:
    _grid= None
    _gridbis = None
    _indexVoisins = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    def __init__(self):
        print("Creating a grid of dimensions " + str(__gridDim__))
        self._grid = np.zeros(__gridDim__, dtype='int8')
        self._gridbis = np.zeros(__gridDim__, dtype='int8')

        nx, ny = __gridDim__

        # if False:  # True to init with one block at the center
        #     self._grid[nx // 2, ny // 2] = 1
        #     self._grid[nx // 2 + 1, ny // 2] = 1
        #     self._grid[nx // 2, ny // 2 + 1] = 1
        #     self._grid[nx // 2 + 1, ny // 2 + 1] = 1
        #     for i in self._grid:
        #         print("primo",i)
        if True: # True to init with random values at the center

            units = [(line, col) for col in range(90) for line in range(90)]
            self.ntrees = int(90 ** 2 * __density__)
            trees = sample(units, self.ntrees)
            for i,j in trees:
                self._grid[i, j] = 1
            #self._grid
            #print(self._grid[20])
            #for i in self._grid:
             # print("secondo ",i)
        # elif False:  # True to init with random values at the center
        #     mx, my = 20, 16
        #     ones = np.random.random((mx, my)) > 0.75
        #     self._grid[nx // 2 - mx // 2:nx // 2 + mx // 2, ny // 2 - my // 2:ny // 2 + my // 2] = ones
        # else:  # Else if init with glider gun
        #     a = np.fliplr(np.rot90(np.array(glidergun), 3))
        #     mx, my = a.shape
        #     self._grid[nx // 2 - mx // 2:nx // 2 + mx // 2, ny // 2 - my // 2:ny // 2 + my // 2] = a



    def indiceVoisins(self, x,y ):
        return [(dx+x,dy+y) for (dx,dy) in self._indexVoisins if dx+x >=0 and dx+x < __gridDim__[0] and dy+y>=0 and dy+y < __gridDim__[1]  ]

    def indiceVoisinstype(self, x,y,indice):
        return [(dx+x,dy+y) for (dx,dy) in self._indexVoisins if dx+x >=0 and dx+x < __gridDim__[0] and dy+y>=0 and dy+y < __gridDim__[1] and self._grid.item(x,y) == indice ]



    def voisins(self,x,y):
        return [self._grid[vx,vy] for (vx,vy) in self.indiceVoisins(x,y) ]
   
    def sommeVoisins(self, x, y):
        return sum(self.voisins(x,y))

    def sumEnumerate(self):
        return [(c, self.sommeVoisins(c[0], c[1])) for c, _ in np.ndenumerate(self._grid)]

    def drawMe(self):
        pass

    def voisinss(self, i, j):
        return [(a, b) for (a, b) in  [(i + 1, j), (i, j - 1), (i - 1, j), (i, j + 1),(i-1,j-1),(i-1,j+1),(i+1,j-1),(i+1,j+1)]
                if a in range(len(self._grid)) and b in range(len(self._grid))]
    def somme_Voisins(self,i,j):
        return  sum(self.voisins(i,j))

gr = Grid()

class Vegetation:
    def __init__(self, density, height, dryness):
        self.density = density
        self.height = height
        self.dryness = dryness

class Scene:

    _mouseCoords = (0,0)
    _grid = None
    _font = None
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode(__screenSize__)
        self._font = pygame.font.SysFont('Arial',25)
        self._grid = Grid()
        self.ntree_fire = 0


    def drawMe(self):
        if self._grid._grid is None:
            return
        self._screen.fill((255,255,255))

        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen,
                        getColorCell(self._grid._grid.item(x,y)),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))
        #print(self._grid._grid.item((x, y)))
        self.drawText("Automaton", (20,20))
        self.drawText("Arbre Brules : ", (25, 40))
        self.drawText(str(sum(self._grid._grid[i,j] == 3 for i in range(__gridDim__[0]) for j in range(__gridDim__[1]))), (182,40))
        self.drawText("Densite : ", (25, 60))
        self.drawText(str(__density__*100) + " %", (120, 60))





    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,0,color),position)

    def update(self):
        '''B234/S rule'''
        for c, s in self._grid.sumEnumerate():
            self._grid._gridbis[c[0], c[1]] = 1 if (2 <= s <= 4) and self._grid._grid[c[0],c[1]] == 0 else 0 
        self._grid._grid = np.copy(self._grid._gridbis)

    def updatebis(self):
        for c, s in self._grid.sumEnumerate():
            if self._grid._grid[c[0],c[1]] == 1:
                ret = 2 <= s <= 3 
            else:
                ret = s == 3
            self._grid._gridbis[c[0], c[1]] = 1 if ret else 0
        self._grid._grid = np.copy(self._grid._gridbis)

    def updateBrain(self):
        for c, s in self._grid.sumEnumerate():

            if self._grid._grid[c[0],c[1]] == 2:
                ret = 0
            elif self._grid._grid[c[0],c[1]] == 1:
                ret = 2
            else:
                ret = 1 if s == 2 else 0
            self._grid._gridbis[c[0], c[1]] = ret
        self._grid._grid = np.copy(self._grid._gridbis)

    def updateRule(self, B, S):
        # Maze is B3/S12345
        ''' Many rules in https://www.conwaylife.com/wiki/List_of_Life-like_cellular_automata '''
        for c, s in self._grid.sumEnumerate():
            if self._grid._grid[c[0],c[1]] == 1:
                ret = s in S
            else:
                ret = s in B
            self._grid._gridbis[c[0], c[1]] = 1 if ret else 0
        self._grid._grid = np.copy(self._grid._gridbis)



    def eventClic(self, coord, b):
        pass

    def recordMouseMove(self, coord):
        pass

    def update2(self):
        '''B234/S rule'''
        for c , s in gr.sumEnumerate():
            line,col = c[0],c[1]
            if self._grid._grid[line][col] == 1:
                for (i,j) in gr.indiceVoisins(line,col):
                    if (gr.sommeVoisins(i,j) <= 3):
                        self._grid._gridbis[i][j] = 3
                        print(gr.sommeVoisins(line,col))
            self._grid._grid = np.copy(self._grid._gridbis)

    def update_states_fire(self):
        to_fire = []
        for line in range(__gridDim__[1]):
            for col in range(__gridDim__[0]):
                if self._grid._grid[line][col] == FIRE:
                    self._grid._grid[line][col] = DAI
                    for (i, j) in gr.indiceVoisins(line, col):
                        if self._grid._grid[i][j] == TREE:
                            if gr.sommeVoisins(i,j)>4:
                            #print(self._grid._grid[i,j])
                                to_fire.append((i, j))
                            #print(gr.voisinss(line, col))
        #self.ntree_fire = sum(self._grid._grid[i,j] == 3 for i in range(__gridDim__[0]) for j in range(__gridDim__[1]))

        wind = 3
        for (a, b) in to_fire:
            self._grid._grid[a, b] = FIRE


        if self._grid._grid[int(pygame.mouse.get_pos()[0] / 10), int(pygame.mouse.get_pos()[1] / 10)] == TREE:
            self._grid._grid[int(pygame.mouse.get_pos()[0] / 10), int(pygame.mouse.get_pos()[1] / 10)] = FIRE


    def peutBrulerVentNordOuest(self):
        au_feu = []
        for line in range(__gridDim__[0]):
            for col in range(__gridDim__[1]):
                if self._grid._grid[line][col] == FIRE:
                    self._grid._grid[line][col] = DAI
                    for (i, j) in gr.indiceVoisinstype(line, col,1):
                        # direction droite
                        for x in range(max(0, j - 1), j):
                            if self._grid._grid[i, x] == 1:
                                #self._grid._grid[i,x] = 2
                                au_feu.append((i,x))
                        # diagonale haute
                        for hy in range(i, min(__gridDim__[0], i + 1)):
                            for hx in range(max(0, j - 1), j-1):
                                if self._grid._grid[hy, hx] == 1:
                                    #self._grid._grid[hy, hx] = 2
                                    au_feu.append((hy,hx))
                        # diagonale basse
                        for by in range(max(0, i - 1), i):
                            for bx in range(max(0, j - 1), j):
                                if self._grid._grid[by, bx] == 1:
                                    #self._grid._grid[by, bx] = 2
                                    au_feu.append((by,bx))
                                #print(au_feu)
        for (a, b) in au_feu:
            self._grid._grid[a, b] = FIRE
        if self._grid._grid[int(pygame.mouse.get_pos()[0] / 10), int(pygame.mouse.get_pos()[1] / 10)] == TREE:
            self._grid._grid[int(pygame.mouse.get_pos()[0] / 10), int(pygame.mouse.get_pos()[1] / 10)] = FIRE




    def feuOrientation(self):
        to_fire = []
        for line in range(__gridDim__[1]):
            for col in range(__gridDim__[0]):
                if self._grid._grid[line][col] == FIRE:
                    self._grid._grid[line][col] = DAI
                    for (i, j) in gr.indiceVoisins(line, col):
                        if self._grid._grid[i][j] == TREE:
                            # print(self._grid._grid[i,j])
                            to_fire.append((i, j))

        prob = math.comb(8, 3) / 2 ** 8
        for lin in to_fire:
            line = lin[0]
            col = lin[1]
            # feu dans la direction x croissants
            if line < __gridDim__[0]-1:
                 if 2 <= gr.sommeVoisins(line,col):
                    if self._grid._grid[line+1][col] == 1:
                        self._grid._grid[line+1][col] = 2

            #feu dans la direction x décroissants
            if line >0:
               if 2<= gr.sommeVoisins(line, col):
                   if self._grid._grid[line-1][col] == 1:
                       self._grid._grid[line-1][col] = 2

            # feu dans la direction y croissants
            if col < __gridDim__[1]-1:
               if 2 <= gr.sommeVoisins(line, col):
                   if self._grid._grid[line][col+1] == 1:
                       self._grid._grid[line][col+1] = 2

            # feu dans la direction x décroissants
            if col > 0:
               if 2 <= gr.sommeVoisins(line, col):
                   if self._grid._grid[col -1][line] == 1:
                       self._grid._grid[col- 1][line] = 2

        # if gr.sommeVoisins(line,col) < random.randint(1,8):
        self._grid._grid[45,45] = 2

    def Feu_Ouest_est(self):

        k = 0  # compteur des itérations de la boucle

        Vmax = 60  # correspond à un vent de 60 km/h
        nbCasesVertsAtteignables = 0
        # ici vent de direction ouest vers est
        Vx = 45  # valeur choisie arbitrairement pour cette simulation : peut être modifiée
        Vy = 0
        # probabilité que le feu se propage à un point voisin (VERT vers ROUGE)
        proba_VERT_vers_ROUGE = 0.4
        # probabilité qu'une case passe de l'état brûlant à l'état brûlé (ROUGE vers NOIR)
        proba_ROUGE_vers_CENDRE = 0.3
        # Calcul des 4 facteurs d'après la loi décrit dans le rapport
        facteur_propagation_vx_plus = (Vx / Vmax) * ((1 - proba_VERT_vers_ROUGE) / proba_VERT_vers_ROUGE) + 1
        facteur_propagation_vx_moins = (1 - Vx / Vmax) * (1 / proba_VERT_vers_ROUGE)
        # Le feu ne se propage pas différemment latéralement donc on ne modifie pas la valeur de la probabilité dans la direction y
        facteur_propagation_vy_croisant = 1
        facteur_propagation_vy_decroissant = 1
        to_fire = []

        for line1 in range(__gridDim__[1]):
            for col1 in range(__gridDim__[0]):
                if self._grid._grid[line1][col1] == FIRE:
                    self._grid._grid[line1][col1] = DAI
                    for (i, j) in gr.indiceVoisins(line1, col1):
                        if self._grid._grid[i][j] == TREE:
                            # print(self._grid._grid[i,j])
                            to_fire.append((i, j))
        controle = False

        for lin in to_fire:
            line = lin[0]
            col = lin[1]
            if line == __gridDim__[0]-1:
                controle = True

            if line < __gridDim__[0] - 1 and controle == False:
                if self._grid._grid[col][line + 1] == 1:
                    # incrémentation du nombre de points verts atteignables
                    nbCasesVertsAtteignables += 1
                    print("som", facteur_propagation_vx_plus * proba_VERT_vers_ROUGE * 100)
                    # propagation du feu dans la direction x croissants
                    nombre_aleat_case_voisine = random.randint(1, 100)
                    if nombre_aleat_case_voisine < facteur_propagation_vx_plus * proba_VERT_vers_ROUGE * 100:
                        self._grid._grid[col][line+1] = 2

            print(nbCasesVertsAtteignables)
            if line > 0 and controle == False:
                if self._grid._grid[col][line+1] == 1:
                    nbCasesVertsAtteignables += 1
                    # propagation du feu dans la direction x décroissants
                    nombre_aleat_case_voisine = random.randint(1, 100)
                    if nombre_aleat_case_voisine < facteur_propagation_vx_plus * proba_VERT_vers_ROUGE * 100:
                        self._grid._grid[col][line - 1] = 2

            if col < __gridDim__[1] - 1 and controle == False:
                if self._grid._grid[col][line-1] == 1:
                    nbCasesVertsAtteignables += 1
                    # propagation du feu dans la direction y croissants
                    nombre_aleat_case_voisine = random.randint(1, 100)
                    if nombre_aleat_case_voisine < facteur_propagation_vx_plus * proba_VERT_vers_ROUGE * 100:
                        self._grid._grid[col+1][line] = 2
            if col > 0 and controle == False:
                if self._grid._grid[col - 1][line-1] == 1:
                    nbCasesVertsAtteignables += 1
                    # propagation du feu dans la direction y décroissants
                    nombre_aleat_case_voisine = random.randint(1, 100)
                    if nombre_aleat_case_voisine < facteur_propagation_vx_plus * proba_VERT_vers_ROUGE * 100:
                        self._grid._grid[col-1][line] = 2
            self._grid._grid[20,60] = 2








    def n_fire(self):
            self.count = 1
            self.ntrees = int(90 ** 2 * __density__)
            self.ntree_fire = sum(self._grid._grid[i,j] == 3 for i in range(__gridDim__[0]) for j in range(__gridDim__[1]))
            self.count  += self.ntree_fire
            self.percent = (self.count /self.ntrees) *100
            self.listerestante = sum(self._grid._grid[i,j] == 1 for i in range(__gridDim__[0]) for j in range(__gridDim__[1]))
            list_a.append(self.ntree_fire)
            lista_percent.append(self.percent)
            listaArbreResta.append(self.listerestante)
            self.drawText(str(self.ntree_fire), (20, 40))
            return list_a , lista_percent

    def replanter(self):
        prob = math.comb(8, 3)*2**8
        reste_arbre =  int(90 ** 2 * __density__) - self.ntree_fire

        print("reste ", reste_arbre)
        print(int(90 ** 2 * __density__)*90/100)
        for c, s in gr.sumEnumerate():
            for (a,k) in gr.indiceVoisinstype(c[0],c[1],1):
                if 3 <= gr.sommeVoisins(a,k) < 5 and reste_arbre <= int(90 ** 2 * __density__)*50/100:
                    for i in range(gr.sommeVoisins(a,k)) :
                        self._grid._grid[(a, k)] = 1



def main():
    start = time.time()
    scene = Scene()
    done = False

    buildingGrid = None
    wallWeight = 1
    #print(scene.proba(50))

    clock = pygame.time.Clock()

    while done == False:
        scene.drawMe()
        pygame.display.flip()
        #decommnter pour lancer les differentes fonctions
        scene.update_states_fire()
        #scene.peutBrulerVentNordOuest()
        #scene.Feu_Ouest_est()
        #scene.feuOrientation()
        scene.n_fire()

        scene.replanter()

        clock.tick(10)

        end = time.time()
        elapsed = (end - start) *1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done =True
            if event.type == pygame.MOUSEBUTTONDOWN:

                 figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
                 liss_dist = [{"RESTE_ARBRE":  int(90 ** 2 * __density__) - list_a[-1] ,"POURCENT_ARBRE_B_EN_%":lista_percent[-1],"NOMBRE_ABRE_BRULE" :list_a[-1],"DENSITE": __density__,"DURE_DU_FEU" : elapsed,"VITESSSE_PROGATION_FEU": lista_percent[-1]/elapsed}]
                 print(liss_dist)
                 print("time start ",start)
                 print("time end" ,end)
                 import csv

                 field_names = ["RESTE_ARBRE",'POURCENT_ARBRE_B_EN_%', 'NOMBRE_ABRE_BRULE', 'DENSITE','DURE_DU_FEU',"VITESSSE_PROGATION_FEU"]
                 with open('dataset_sans_orientation.csv', 'a') as csvfile:
                     writer = csv.DictWriter(csvfile, fieldnames=field_names,lineterminator = '\n')
                     #writer.writeheader()
                     writer.writerows(liss_dist)
                     csvfile.close()



    pygame.quit()
if not sys.flags.interactive: main()

