import sys, math, random
import os.path as path
import pygame
import pygame.draw
import numpy as np
import heapq
from queue import PriorityQueue

# Global variable that may be changed when loading maze
__screenSize__ = (2000,1200)
__cellSize__ = 10
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))
__defaultMazeSize__ = (90, 50)

__colors__ = [(255, 255, 255), (0, 0, 0), (180, 180, 180), (30, 30, 30), (100, 10, 10)]
cost = {'X':1}
def getColorCell(n):
    assert n < len(__colors__)
    return __colors__[n]

class Grid:
    _grid = None
    def __init__(self, mazename = None):
        if mazename is None:
            self._grid = np.empty(__defaultMazeSize__, dtype='int8')

        else:
            self.loadTextMaze(mazename)
            print("Creating a grid of dimensions", self._grid.shape)

    def loadTextMaze(self, f):
        values = {'.':0,'X':1,'x':2, 's':11, 'S':12, 'f':21, "F":22}
        ls = []
        with open(f,"r") as fin:
            size = tuple([int(x) for x in fin.readline().rstrip().split(' ')])
            print("Reading Midimaze file of size", size)
            for s in fin:
                ls.append([values[x] for x in s.rstrip()])
            matrix = np.array(ls, dtype='int8')
        matrix = np.rot90(np.fliplr(matrix))

        self._grid = matrix

## algo  a-etoile recherche de intineraire trouve le chemon

    def saveTextMaze(self, f):
        values = {0:".", 1:"X", 2:"x", 11:"s", 12:"S", 21:"f", 22:"F"}
        d = self._grid.shape

        with open(f,"w") as fout:
            print(d[0], d[1], file=fout)
            print("Saving Midimaze-like file",f)
            for y in range(d[1]):
                for x in range(d[0]):
                    print(values[self._grid[x,y]], end="", file=fout)
                print(file=fout)


    def addWallFromMouse(self, coord, w):
        x = int(coord[0] / __cellSize__)
        y = int(coord[1] / __cellSize__)
        self._grid[x,y] = w
        self._grid[self._grid.shape[0]-x-1,self._grid.shape[1]-y-1] = w

    def loadGrid(self, grid):
        assert len(grid) == len(self._grid)
        self._grid = np.flipud(np.array(grid, dtype='int8'))

    def drawMe(self):
        pass

class Agent:
    def __init__(self, team):
        self.x = 300
        self.y = 300
        self.angleOrientation = 90 # de 0 à 359 
        self.radius = 11
        self.lenOrientationVector = 20

        self.health = 100
        self.team = team

    def _angleToVector(self, angle):
        return (math.cos(math.radians(angle)), -math.sin(math.radians(angle)))

    def _tupleMul(self, t,a):
        return tuple([x * a for x in t])

    def _angleToOrientVector(self, angle, length = None):
        if length is None:
            length = self.lenOrientationVector
        x, y = self._angleToVector(angle)
        return (x * length, y * length) 

    def drawMe(self, screen):
        #pygame.draw.circle(screen, (10,10,80), (self.x, self.y), self.radius, 10)
        orientation = self._angleToOrientVector(self.angleOrientation) 
        tmp = self.angleOrientation+50
        if tmp > 359:
            tmp -= 360
        orientation1 = self._angleToOrientVector(tmp, 100)
        orientation1 = (self.x+orientation1[0], self.y+orientation1[1])
        tmp = self.angleOrientation-50
        if tmp < 0:
            tmp += 360
        orientation2 = self._angleToOrientVector(tmp, 100)
        #orientation2 = (self.x+orientation2[0], self.y+orientation2[1])
        #pygame.draw.polygon(screen, (200,200, 20,180), [(self.x,self.y), orientation1, orientation2])
        #pygame.draw.line(screen, (10,10,80), (self.x, self.y), (self.x+orientation[0], self.y + orientation[1]),10)
        self.angleOrientation += 3 
        if self.angleOrientation > 359:
            self.angleOrientation = 0
        pass

class Assets:
    def __init__(self):
        global __cellSize__ 
        self.explosionAnim = []
        img_dir = "."
        for i in range(9):
            filename = 'assets/regularExplosion0{}.png'.format(i)
            print(filename)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey((0,0,0))
            img = pygame.transform.scale(img, (__cellSize__ * 3, __cellSize__ * 3))
            self.explosionAnim.append(img)

class Explosion(pygame.sprite.Sprite):
    ''' A simple class to take care of animated explosions by sprites from pygame '''
    def __init__(self, center, anim):
        pygame.sprite.Sprite.__init__(self)
        self.anim = anim
        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        print(self.rect)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Scene:
    _Noeud = None
    _mouseCoords = (20,0)
    _grid = None
    _font = None
    _drawGrid = False
    allsprites = pygame.sprite.Group()

    def __init__(self, mazename = None):
        global __screenSize__, __gridDim__
        pygame.init()
        self._grid = Grid(mazename)
        __screenSize__ = tuple(s * __cellSize__ for s in self._grid._grid.shape)
        __gridDim__ = self._grid._grid.shape
        self._screen = pygame.display.set_mode(__screenSize__)
        
        self.assets = Assets()
        self._font = pygame.font.SysFont('Arial',25)
        self.agents = [Agent(1)]
        #self.agents[1].x = 100
        #self.agents[1].y = 100
        #self.agents[2].angleOrientation = 76
        #self.agents[2].x = 290
        #self.agents[2].y = 310
        #self.agents[2].angleOrientation = 176
        #self.agents[2].x = 200
        #self.agents[2].y = 310
        #self.agents[2].angleOrientation = 188

    def moveAgents(self):
        for a in self.agents:
            a.x += 3
            a.y += 3

    def drawMe(self):
        if self._grid._grid is None:
            return
        if self._drawGrid:
            self._screen.fill((128,128,128))
        else:
            self._screen.fill((255,255,255))

        for agent in self.agents:
            agent.drawMe(self._screen)

        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                if self._drawGrid:
                    pygame.draw.rect(self._screen,
                        getColorCell(self._grid._grid.item((x,y))),
                        (x*__cellSize__+1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))
                if self._grid._grid.item(x,y) != 0:
                    pygame.draw.rect(self._screen,
                        getColorCell(self._grid._grid.item((x,y))),
                        (x*__cellSize__ , y*__cellSize__, __cellSize__, __cellSize__))

        self.allsprites.draw(self._screen)
#recherche etinrraire dans un labbirin
#algo A-etoile sur la recherche de l'intineraire

    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def _mapOnPath(self, x1, y1, x2, y2, fmap):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        xincr = 1 if x1 < x2 else -1
        yincr = 1 if y1 < y2 else -1

        x = x1; y = y1
        if dx > dy:
            e = dx // 2
            for i in range(dx):
                x += xincr; e += dy
                if e > dx:
                    e -= dx; y += yincr
                if (retIfNotNone := fmap(x,y)) is not None:
                    return retIfNotNone
        else:
            e = dy // 2
            for i in range(dy):
                y += yincr; e += dxs
                if e > dy:
                    e -= dy; x += xincr
                if (retIfNotNone := fmap(x,y)) is not None:
                    return retIfNotNone
        return None

    def canSee(self, x1, y1, x2, y2, fog = 30):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # 1) Checks the distance
        manhattanDistance = abs(x1 - x2) + abs(y1 - y2)
        if manhattanDistance > fog:
            return False

        # 2) Checks the angles (NPC cannot see other players outside of their vision) TODO

        # 3) Checks on the tiles (Brensenham)
        _mapLevel = lambda x, y : True if self._grid._grid[x, y] == 0 else None
        return self._mapOnPath(x1, y1, x2, y2, _mapLevel) is None 

    # None if there is no obstacle on the path, otherwise gives the first obstacle coordinates

    def firstObstacle(self, x1, y1, x2, y2):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        _mapLevel = lambda x, y : (x,y) if self._grid._grid[x, y] > 0 else None
        return self._mapOnPath(x1, y1, x2, y2, _mapLevel)
    def all_obstacles(self):
        liste_obstacle = []
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                if self._grid._grid.item(x,y) != 0:
                    liste_obstacle.append((x, y))
        #print(liste_obstacle)
        return  liste_obstacle

    def est_obstacle(self,x, y, obstacles):
        if (x, y) in obstacles:
            print("x ,y est un obstacle")
            return True
        return False


    def update(self):
        self.moveAgents()
        self.allsprites.update()


    def heuristic(self,cell1,cell2):
        self.x1,self.y1 = cell1
        self.x2,self.y2 = cell2
        return  abs(self.x1 - self.x2) + abs(self.y1 - self.y2)
        #return  ((self.x1 - self.x2)**2 - (self.y1 - self.y2)**2)*0.5

    def neighbors(self, cell):
        self.grid = self._grid._grid
        x, y = cell
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)]

        results = filter(lambda x: x[0] >= 0 and x[0] < len(self.grid) and x[1] >= 0 and x[1] < len(self.grid[0]), results)
        #results = filter(lambda x: self.grid[int(x[0])][int(x[1])] != 'x', results)

        return results

    def dist_between(self,a, b):
        return 1
    def reconstruct_path(self,came_from, current):
        self.total_path = [current]

        while current in came_from:
            current = came_from[current]
            self.total_path.append(current)
        return self.total_path[::-1]

    def is_valid_move(self, next):
        self.grid = self._grid._grid
        x, y = next
        if self.grid.item(int(x),int(y)) == 0:
            return True
        return False



    def a_Etoile(self, start, goal):
        # initialize data structures
        # fonctionnel A garder
        self.grid = self._grid._grid

        queue = [(1, start)]
        heapq.heapify(queue)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while queue:
            # récupérer et de supprimer l'élément de plus petite dans la liste
            current = heapq.heappop(queue)[1]

            if current == goal:
                break

            for next in self.neighbors(current):
                if self.grid[int(next[0])][int(next[1])] > 0:
                    continue
                elif not self.is_valid_move(next):  # check if it is a valid move
                    continue
                new_cost = cost_so_far[current] + self.cost(current, next) + self.dist_between(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(queue, (priority, next))
                    came_from[next] = current
            # current = goal
        while current != start:
            x2, y2 = current
            pygame.draw.rect(scene._screen, (255, 0, 0), (x2 * 10, y2 * 10, 10, 10))
            current = came_from[current]


        pygame.display.flip()
        return False


    def cost(self, current, next):
        self.grid = self._grid._grid
        return self.grid[int(next[0])][int(next[1])]



    def recordMouseMove(self, coord):
        pass
scene = Scene()
margin = 5

def main():
    #_, grid = loadmidimazefile("mazes/WS32.MAZ")
    buildingGrid = False #True if the user can add / remove walls / weights
    scene = Scene() #Scene("mazes/WS32-bis.MAZ")
    scene._grid.loadTextMaze("maze.maz")
    print(scene._grid.loadTextMaze("maze.maz"))
    print(scene._grid._grid)

    x1 = __screenSize__[0]/3/__cellSize__  # x et Y du point de depart
    y1 = __screenSize__[1]/2/__cellSize__

    done = False
    clock = pygame.time.Clock()
    wallWeight = 1
    print(scene.all_obstacles())
    scene.est_obstacle(0,45,scene.all_obstacles())

    while done == False:
        clock.tick(0)
        scene.update()
        scene.drawMe()

        if buildingGrid:
            additionalMessage = ": BUILDING (" + str(int(wallWeight*100)) + "%)"
        else:
            additionalMessage = ""

        x2 = pygame.mouse.get_pos()[0]/__cellSize__
        y2 = pygame.mouse.get_pos()[1]/__cellSize__


        scene.a_Etoile((34, 44), (int(pygame.mouse.get_pos()[0] / 10), int(pygame.mouse.get_pos()[1] / 10)))

        # Draw the first obstacle on the path
        #pygame.draw.line(scene._screen, (25,60,60) if checksee else (60, 255, 60),  (x1*__cellSize__, y1 *__cellSize__), pygame.mouse.get_pos())
        if (obstacle := scene.firstObstacle(x1, y1, x2, y2)) is not None:
            ox, oy = obstacle
            pygame.draw.rect(scene._screen, (200,100,100),(ox*__cellSize__ , oy*__cellSize__, __cellSize__, __cellSize__))


        scene.drawText("CFT" + additionalMessage, (10,10))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting")
                done=True
            if event.type == pygame.KEYDOWN: 
                print(event.unicode)
                if event.unicode in ["0", "1", "2"]:
                    wallWeight = int(event.unicode) 
                    break
                if event.key == pygame.K_q or event.key==pygame.K_ESCAPE: # q
                    print("Exiting")
                    done = True
                    break
                if event.key == pygame.K_s: # s
                    np.save("matrix.npy",scene._grid._grid)
                    print("matrix.npy saved")
                    break
                if event.key == pygame.K_l: # l
                    print("matrix.npy loaded")
                    scene._grid._grid = np.load("matrix.npy")
                    scene._grid.saveTextMaze("maze.maz")
                    break
                if event.key == pygame.K_n:
                    buildingGrid = False
                    break
                if event.key == pygame.K_b :


                    buildingGrid = True
                # if event.key == pygame.K_o:
                #     int(pygame.mouse.get_pos()[0] / 10), int(pygame.mouse.get_pos()[1] / 10)
                #     scene.a_starTest_bon((34, 44), (10, 26))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buildingGrid:
                    scene._grid.addWallFromMouse(event.dict['pos'], wallWeight)
                else:
                    scene.eventClic(event.dict['pos'],event.dict['button'])
                    # Add an explosion (just to show how to do that)
                    scene.allsprites.add(Explosion(event.dict['pos'], scene.assets.explosionAnim))
                    x1, y1 = event.dict['pos'][0]/__cellSize__, event.dict['pos'][1] / __cellSize__
                    print(x1,y1)

            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict['pos'])

    pygame.quit()

if not sys.flags.interactive: 
    main()
