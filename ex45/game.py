#-----------------------------------
# Viruses Are Go
# by Adam M Deeley
# ----------------------------------

# Description:

# " "

#To Do
# 1. Add a look for each object
# 2. Add callable inventory
# 3. Put map in separate file and have each room display a local version
import time
import random
from random import randint
import sys, traceback
import ex45_map

class Scene(object):
    
    inventory = {
    'pocket_knife': True,
    'note': False,
    'finger': False,
    'lab_cabinet_key': False,
    'strength_serum': False,
    'gloves': False,
    'map': False,
    'pistol': False,
    }
    
    enemies = {
    'morgue_baddie': True,
    }
    
    cut_scenes = {
    'in_patients': False
    }
    
    misc = {
    'boss_room_code': random.randint(1000, 9999)
    }
    
    def dot_delay(self):
        print ".", 
        time.sleep(1)
        print "\r..",
        time.sleep(1)
        print "\r..."
    
class Engine(object):
    
    def __init__(self, scene_map):
        self.scene_map = scene_map
    
    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('Exit')
        
        while current_scene != last_scene:
            
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)
        
        current_scene.enter()

class Intro(Scene):

    def enter(self):
        print """    
    You burst in through the flapping door and quickly look around for a 
barricade. The baseball bat in that dead guy's hand will do. You run the bat through the
bars only moments before three of your pursuers slam their bodies into the perspex doors, 
making a deafening ba-da-bam! sound. They growl and snarl at you through the semi-opaque
barrier before becoming destracted by easier folley and departing. 
        """
        return "entrance_area"
    
class EntranceArea(Scene):

    def enter(self):
        print """
DOME ENTRANCE
-------------
        """
        finger = self.inventory['finger']
        while True:
            choice = raw_input("\nWhat do you do? ").lower()
            if 'look' in choice:
                print """
    A cursory look reveals your surroundings to be oppresively-clean bubble like structure.   
This must have been one of the emergency laboratories flown in to deal with the mess. A dead 
lab technician, from whom you took the bat, lies slumped in the corner; hand open. The door 
to the south is locked by a fingerprint scanner.        
                """
            elif 'north' in choice:
                print "The outside world. You think better of it."
            elif 'east' in choice:
                print 'The dead lab technician is slumped against the wall'
            elif 'west' in choice:
                print 'A solid looking perspex wall'
            elif 'tech' in choice or 'search body' in choice:
                print 'You search the lab tech and find a digital map of the facility.'
                self.inventory['map'] = True
            elif 'finger' in choice:
                print """
    With your pocket-knife you, rather grusomely, collect the finger of the cadaver. 
...wierdo."""
                self.inventory['finger'] = True

            elif 'door' in choice or 'south' in choice and self.inventory['finger'] == True:
                print """
'Bing-bong' sings the door as it swooshes open. You enter the quarantine area and are
showered with disinfectant that smells strongly of alcohol. The door on the other side
opens and you make your way through.
                """
                return "laboratory"
            elif 'door' in choice or 'south' in choice and self.inventory['finger'] == False:
                print "\nNEEEERK! The door roars in repulsion from your fingerprints"
            elif 'map' in choice and self.inventory['map'] == True:
                print ex45_map.maps['entrance']
            else:
                print "Sorry, I didn't recognise that."
                
            

class Laboratory(Scene):
    
    def enter(self):
        print """
LABORATORY
----------
        """
        
        lab_cabinet_key = self.inventory['lab_cabinet_key'] 
        gloves = self.inventory['gloves']
        while True:
            choice = raw_input("\nWhat do you do? ").lower()
            if 'look' in choice:
                print """
    This, much larger dome must be the mail laboratory. An airy and utilitarian 
space with five rows of benches in a rectangle in the centre of the room, each adorned with 
the full complement of stereotypical lab equipment. A hollow semicircle of cabinets lines a 
portion of the back wall 
    Doors are available on each wall.                 
                """
            elif 'north' in choice:
                return 'entrance_area'   
            elif 'east' in choice:
                return 'morgue'
            elif 'south' in choice and self.cut_scenes['in_patients'] == False:
                print """
    The door is firmly locked. Through the window you think you can make out a figure through 
the frosted glass. Your mind must be playing games on you."""   
            elif 'south' in choice and self.cut_scenes['in_patients'] == True:
                return 'test_area'
            
            elif 'west' in choice:
                print 'The door is locked by a code. Type the code or "exit" to leave'
                chances = 3
                while True:
                    if chances == 0:
                        print """
    The door fuses shut with a sloppy sound and a deafening alarm jumps to life. 
You are swarmed and torn apart by creatures.
                """
                        return 'death'
                    else:
                        pass
                    
                    choice = raw_input("\n**Enter Code**: ").lower()
                    if choice == self.misc['boss_room_code']:
                        print 'The door swooshes open'    
                        return 'boss_room'
                    elif choice == 'exit':
                        break
                    elif choice != self.misc['boss_room_code']:
                        chances -= 1
                        print 'Incorrect!! %d chances remaining' % chances
                    
                                    
            elif 'cabinet' in choice and lab_cabinet_key == True:
                print """
    You open the cabinet with the key. Inside is a metal test tube with 'x-45-b1' typed
in old ink on the side. You take the test tube.                
                """
                self.inventory['strength_serum'] = True
            elif 'cabinet' in choice and lab_cabinet_key == False:
                print """The cabinets jutter as you try the handle, but stay stubbornly 
closed."""
                
            elif 'bench' in choice and gloves == False:
                print """
Upon closer inspection desks are mostly bare of useful items or potions. You find a pair 
of safety gloves in one of the drawers and decide it best to retain these.
                """
                self.inventory['gloves'] = True
            elif 'bench' in choice and gloves == True:
                print "You find nothing further of note"
            elif 'map' in choice and self.inventory['map'] == True:
                print ex45_map.maps['laboratory']

class Morgue(Scene):
    
    def enter(self):
        print """
MORGUE
------
        """
        
        if self.enemies['morgue_baddie'] == True:
            print """
    As you step into the morgue you are rushed by a crazed man; bloodied and snarling
he grabs you by the neck and lunges to bite you.
            """
            chances = 3
            while True:
            
                choice = raw_input("\nWhat do you do? ").lower()
                if 'stab' in choice or 'knife' in choice:
                    print """
    You manage to pull your knife out just in time to slam the blade in the maniac's left 
eye. He falters a second before collapsing onto the floor in a bloody mess.                    
                    """
                    self.enemies['morgue_baddie'] = False
                    break
                elif 'run' in choice:
                    print """
    As you attempt to run the man sinks his broken teeth into your throat. You suffocate on 
your own blood as the man suckles from your insides.                
                    """
                    return 'death'
                elif chances == 0:
                    print "You are torn apart by fevered hands."
                    return 'death'
                else:
                    print """
    It didn't work. His grip tightens
                  """
                    chances -= 1
        else:  
            pass
                
        while True:
            choice = raw_input("\nWhat do you do? ").lower()
            
            if 'north' in choice:
                print 'Nothing of interst'
            elif 'east' in choice:
                print 'Nothing of interest'
            elif 'south' in choice:
                return 'in_patients'   
            elif 'west' in choice:
                return 'laboratory'
            elif 'look' in choice:
                print """
    You are in the morgue. Two empty metal tables are to the east of the room. One tabe 
supports what appears to be a box of flasks.
    Cupboards containing a myriad of medical equipment stand behind the tables. The stench 
of the morge is a mixture between burnt rubber and honey.
                """
            elif 'map' in choice and self.inventory['map'] == True:
                print ex45_map.maps['morgue']
            elif 'body' in choice or 'man' in choice:
                print "You search the man and find a key."
                self.inventory['lab_cabinet_key'] = True
            elif 'box' in choice or 'flask' in choice:
                print 'You search the box and take one of the flasks'
                
                
            
                
class TestArea(Scene):
    
    def enter(self):
        print """
TEST AREA
---------
        """
      
        while True:
            choice = raw_input("\nWhat do you do? ").lower()
            if 'north' in choice:
                return 'laboratory'
            elif 'east' in choice:
                return 'in_patients'
            elif 'south' in choice:
                print 'Nothing of interest'
            elif 'west' in choice:
                return 'nothing interesting'
            elif 'map' in choice and self.inventory['map'] == True:
                print ex45_map.maps['test_area']
            elif 'look' in choice:
                print """
The room has a single lamp over the operating table you stepped off. On the wall opposite
lies a cabinet.
                """
            elif 'cabinet' in choice:
                print """
A search of the cabinet reveals a well used 9mm pistol. You feel it wise to retain this."""
                self.inventory['pistol'] = True

class InPatients(Scene):
    
    def enter(self):
        print """
IN PATIENTS
-----------
        """

        if self.cut_scenes['in_patients'] == False:
            print """
    As you step through the door your begin to ring and you feel faint. Lifting your 
throbbing right foot up reveals a large hypodermic needle sticking through the heel of your 
foot. As you pull the bent needle out you crash to the floor and black-out.
    You wake up groggy with a bright light shining in your face. Sitting up you can see that
you have been moved to an operating table. As you brace yourself to stand up and find that 
a bandaged stump lays where your right hand used to be...
            """
            self.cut_scenes['in_patients'] = True
            return 'test_area'
            
            
        while True:
            choice = raw_input("\nWhat do you do? ").lower()
            if 'north' in choice:
                return 'morgue'
            elif 'east' in choice:
                print 'nothing of interest'
            elif 'south' in choice:
                return 'yard'
            elif 'west' in choice:
                return 'test_area'
            elif 'map' in choice and self.inventory['map'] == True:
                print ex45_map.maps['in_patients']
               
class Yard(Scene):
   
   def enter(self):
        print """
YARD
----
        """
        
        while True:
            choice = raw_input("\nWhat do you do? ").lower()
            if 'north' in choice:
                return 'in_patients'
            elif 'east' in choice:
                print 'Nothing of interest'
            elif 'south' in choice:
                print 'Nothing of interest'
            elif 'west' in choice:
                print 'Nothing of interest'
            elif 'map' in choice and self.inventory['map'] == True:
                print ex45_map.maps['yard']
            elif 'look' in choice:
                print """
    The yard is a small area surrounded by a tough looking wire fence, two fences deep. You
see people on the other side struggling to get into the compound, but to no avail.
    Directly in front of you is a crate.
                """
            elif 'crate' in choice:
                print 'You search the crate and find a note - "The code is: %d"'% (
                       self.misc['boss_room_code'])
                
# CHANGE NAME OF BOSS ROOM
class BossRoom(Scene):
    
    def enter(self):
        print """
BOSS ROOM
---------
As you enter a giant from the other side of the room stands up and approaches. As he
nears you can see that he is a towering creature with a bloated stomach. He picks up a 
support strut for the room and launches this at you. 
        """
        while True:
            choice = raw_input("\nWhat do you do? ").lower()
            if 'dodge' in choice:
                print '''
You forward roll and dodge the projectile just in time, though as you look up the creature
lifts it's foot to smash you.
                '''
                choice = raw_input("\nWhat do you do? ").lower()
                if 'shoot' in choice:
                    print '''
You pull your gun out and shoot the creature in the exposed part of it's stomach. The 
creature reels back and buckles over in pain. As a last effort the creature charges you 
with all it's might.                   
                    '''
                    if 'shoot' in choice:
                        print 'An inert mass lies in front of you'
                        return Victory()
                        
            elif 'map' in choice and self.inventory['map'] == True:
                print ex45_map.maps['boss_room']


class Victory(Scene):
    
    def enter(self):
        print '''
You emerge through the quarantine doors on the other side of the bubble-tent and jump in the
car. Screeching off into the sunset.        
        '''
        sys.exit(1)

class Death(object):

    def enter(self):
        print "***GAME OVER***"
        sys.exit(1)

class Exit(object):

    def enter(self):
        print "You blew up the space ship and escaped"
        sys.exit(1)

class Map(object):

    scenes = {
        'intro': Intro(),
        'entrance_area': EntranceArea(),
        'laboratory': Laboratory(),
        'morgue': Morgue(),
        'test_area': TestArea(),
        'in_patients': InPatients(),
        'yard': Yard(),
        'boss_room': BossRoom(),
        'death': Death(),
        'victory': Victory(),
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        return val

    def opening_scene(self):
        return self.next_scene(self.start_scene)

print "\n\n\n\n\n---------------"
print "Viruses Are Go"
print "---------------\n\n"

a_map = Map('intro')
a_game = Engine(a_map)
a_game.play()
