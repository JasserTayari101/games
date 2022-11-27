from os import system #usage with clearing console

class EmptyObject:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        
    def __bool__(self):
        return False
    
    def __repr__(self):
        return "."
    

class Actor:
    
    def __init__(self,map,x,y,hp=100):
        self.x = x
        self.y = y
        self.hp = hp    #health
        self.map = map
        
    @staticmethod
    def check_movement(func):
        """Check if the movement function can be done or not based on the map limits"""
        def outer(selfe,*args):
            old_x = selfe.x
            old_y = selfe.y
            func(selfe,args)
            if selfe.x>=map.width or selfe.x<0 or selfe.y<0 or selfe.y>=map.height:
                selfe.x = old_x
                selfe.y = old_y
        return outer
    
    
class Player(Actor):
    def __init__(self,map,x,y,hp=100):
        super().__init__(self,x,y,hp)
    
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
        return 'E'
    
    def get_input(self):
        """Choose from q/z/d/s/ to move"""
        choices = list('qzds')
        move = input("Where to move?(q/z/d/s)? : ")
        while move not in choices:
            move = input("Where to move?(q/z/d/s)? : ")
        
        self.move_to(move)

class Map:
    def __init__(self,width,height):
        self.map = tuple([EmptyObject(x=x,y=y) for x in range(width)] for y in range(height) )
        self.width = width
        self.height = height
    
    def __bool__(self):
        return any([any(vector) for vector in self.map] )
    
    def __repr__(self):
        return repr(self.map)

    def set(self,x,y,val):
        assert isinstance(val,EmptyObject) or isinstance(val,Player)
        
        self.map[y][x] = val
    
    def update(self):
        """Used to update object coords that has been changed"""
        for y,row in enumerate(self.map):
            for x,obj in enumerate(row):
                if(obj.x!=x or obj.y!=y):
                    self.map[y][x] = EmptyObject(x,y)
                    self.map[obj.y][obj.x] = obj 
    
    def show(self):
        system('clear')
        for _ in range(2*(self.width+1)):
            print("#",end='')
        print()
        for y in range(self.height):
            print("#",end='')
            for x in range(self.width):
                print(self.map[y][x],end=',')
            print()
        
 
map = Map(10,10)

player = Player(map,0,0)

map.set(0,0,player)

game_over = False

while not game_over:
    map.show()
    move = player.get_input()
    map.update()
    
