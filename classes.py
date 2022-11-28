from os import system #usage with clearing console
import random


class EmptyObject:
    """A class to represent an empty cell in a map"""
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    @property
    def coords(self):
        return (self.x,self.y)
    
    def __bool__(self):
        return False
    
    def __repr__(self):
        return "."
    

class Actor:
    """A super class for a non empty cell like Enemie or Player"""
    
    def __init__(self,map,x,y,hp=100):
        self.x = x
        self.y = y
        self.hp = hp    #health
        self.map = map  #used for some reverse operations
        
    @staticmethod
    def check_movement(func):
        """Check if the movement function can be done or not based on the map limits if
        it can't then undo them,based on the knowledge that all movement are 1 step at a time
        """

        def outer(self,*args):
            old_x = self.x
            old_y = self.y
            func(self,args)
            if self.x>=map.width or self.x<0 or self.y<0 or self.y>=map.height:
                self.x = old_x
                self.y = old_y
        return outer
    
    @property
    def coords(self):
        return (self.x,self.y)
    
class Player(Actor):
    def __init__(self,map,x,y,hp=100):
        super().__init__(map,x,y,hp)
    
    @Actor.check_movement
    def move_to(self,move):
        """Move the player based on (q/z/s/d)"""
        move = move[0]
        
        if(move=='z'):
            self.y-=1
            
        if(move=='s'):
            self.y+=1

        if(move=='q'):
            self.x-=1

        if(move=='d'):
            self.x+=1

    def __repr__(self):
        return 'P'
    
    def get_input(self,move):
        """Choose from q/z/d/s/ to move"""
        choices = list('qzds')
        self.move_to(move)


class Enemie(Actor):
    def __init__(self,map,x,y,hp=100):
        super().__init__(map,x,y,hp)
    
    @Actor.check_movement
    def shortest_path_to(self,target):
        """Calculate the shortest direction to target(usually player)"""
        
        #based on the difference between the coords of self and target either move one cell vetically or horizontaly
        if self.x!=target.x:
            self.x+=(target.x-self.x)/abs(target.x-self.x)
        elif self.y!=target.y:
            self.y+=(target.y-self.y)/abs(target.y-self.x)

    def __repr__(self):
        return "E"


class Map:
    def __init__(self,width,height):
        self.map = tuple([EmptyObject(x=x,y=y) for x in range(width)] for y in range(height) )
        self.width = width
        self.height = height
        self.spawned = 0    #number of enemies on the map
    
    def __bool__(self):
        return any([any(vector) for vector in self.map] )
    
    def __repr__(self):
        return repr(self.map)

    def set(self,*actors):
        for actor in actors:
            assert isinstance(actor,Enemie) or isinstance(actor,Player) or isinstance(actor,EmptyObject)
            self.map[actor.y][actor.x] = actor
        
    def update(self):
        """Used to update object coords that has been changed"""
        for y,row in enumerate(self.map):
            for x,obj in enumerate(row):
                if(obj.x!=x or obj.y!=y):
                    self.map[y][x] = EmptyObject(x,y)   #put an emptyobject in the old position
                    
                    if(isinstance(self.map[obj.y][obj.x],Enemie)):  #if the player collide with an enemie decrease the number of enemies
                        self.spawned-=1
                    
                    self.map[obj.y][obj.x] = obj
                    
    
    def show(self):
        """Used to display the map"""
        system('clear')
        for _ in range(2*(self.width+1)):
            print("#",end='')
        print()
        for y in range(self.height):
            print("#",end='')
            for x in range(self.width):
                print(self.map[y][x],end=',')
            print("#")
        for _ in range(2*(self.width+1)):
            print("#",end='')
        print()
        
    def spawn_enemies(self):
        while self.spawned<3:
            row = random.choice(self.map)
            obj = random.choice(row)
            
            if isinstance(obj,EmptyObject):
                row[obj.x] = Enemie(self,obj.x,obj.y)
                self.spawned+=1
                
                
map = Map(10,10)

player = Player(map,0,0)

map.set(player)
map.spawn_enemies()

def main(key):
    try:
        if key.char in "qzds":
            player.get_input(key.char)
            map.update()
            map.show()
            map.spawn_enemies()
    except AttributeError:
        print("You Move with (q/z/d/s)!!")

from pynput import keyboard


map.show()

with keyboard.Listener(on_press=main) as listener:
    listener.join()
