# -*- coding: utf-8 -*-
"""

apos@gmx.de


Install Anaconda
https://www.anaconda.com/

Install Spyder Editor inside Anaconda


This script ist devered from
https://ddi.ifi.lmu.de/probestudium/2016/ws-i-3d-programmierung/tutorials/kreisbewegung-bei-planeten/planeten.py/view


"""

# -*- coding: utf-8 -*-
# einfaches Planetensystem
# Sonne (km,km,kg):
s_radius=1.39e6
s_masse=2e30
# Merkur (km,d,d):
mer_radius=2439
mer_umkreiszeit=88
mer_rotzeit=59
s_abstand_merkur=58e6
# Venus (km,d,d):
v_radius=6050
v_umkreiszeit=224.7
v_rotzeit=243
s_abstand_venus=108e6
# Erde (km, km, kg,°,d):
e_radius=12730
s_abstand_erde=150e6
e_masse=5,97e24
e_neigungswinkel=23.44
e_rotzeit=1
e_umkreiszeit=365
# Mond (km, kg)
m_radius=1738
e_abstand_mond=384400
m_masse=7.35e22
m_rotzeit=29
m_umkreiszeit=29
# Mars (km, d, d, km):
ma_radius=3397
ma_rotzeit=24.5
ma_umkreiszeit=687
s_abstand_mars=227e6
# Jupiter():
j_radius=71490
s_abstand_jupiter=777e6
j_umkreiszeit=365*11+316
j_rotzeit=0.35

# 1 Tag = 1 Minute bei zfakt=250
# 1 Tag = 1 Sekunde bei zfakt=4.16
zfakt = 250

# OBSOLET, nun vpython - https://stackoverflow.com/questions/28592211/importerror-no-module-named-visual 
# from visual import *        # das 3D-Modul

# Vpython benötigt Python Version > 3.5
#  Ubuntu 20.04: sudo apt install python-is-python3
# conda install -c vpython vpython
from vpython import *

from threading import *     # das Modul für Nebenläufigkeit

# Wird durch vpython mit installiert:
# from math import *          # das Mathe-Modul (sin, cos, log)


#-----------------------------------------------------------------

#-- Oberflächen Mond und Mars (do it yourself ...) ------------
# conda install -c anaconda pillow
from PIL import Image

name   = "moon"
width  = 1024 
height = 512 
im = Image.open(name+".tga")
# material is obsolet in VPython7: https://groups.google.com/u/1/g/vpython-users/c/H-53IPpxego
# materials.saveTGA(name,im)
textures.saveTGA(name,im)
mondtextur = textures.texture(data=im, mapping="spherical")

name = "mars"
width, height = 1024/2, 512/2
im = Image.open(name+".tga")
textures.saveTGA(name,im)
marstextur = textures.texture(data=im, mapping="spherical")

#-----------------------------------------------------------------

def scale_dist(rohdaten):
    "globale Hilfsfunktion: skaliert Entfernungen"
    return sqrt(rohdaten)

def scale_rad(rohdaten):
    "globale Hilfsfunktion: skaliert Radien"
    return sqrt(rohdaten)


class Planet(Thread):
    "Klasse erstellt Planetenobjekte"
    def __init__(self, form=0, pos=(0,0,0), radius=e_radius, color=(1,1,1), rotzeit=1, umkreiszeit=365, zentrum=None,\
                 abstand_zentrum=0, texture=textures.earth, neigungswinkel=23.4, spurlaenge=500, spurfarbe=(0.3,0,0)):
        Thread.__init__(self)
        self.f = frame(pos=pos)
        self.planet = sphere(frame=self.f)
        self.planet.texture = texture
        self.planet.radius = radius
        self.planet.color = color
        self.planet.frame=self.f
        self.neigungswinkel=neigungswinkel            
        self.rotzeit=rotzeit
        self.umkreiszeit = umkreiszeit
        self.zentrum=zentrum
        self.abstand_zentrum = abstand_zentrum
        self.trail = curve(color=spurfarbe)
        self.spurlaenge = spurlaenge
        

    def run(self):
        x=0.0
        while 1:
            rate(25)                                                                                            # max. 50 Berechnungen pro Sekunde
            self.planet.rotate(angle=pi/zfakt*5/self.rotzeit, axis=(0,1,0))                                         # Eigendrehung: 1d = 1min
            self.f.axis = (cos(radians(self.neigungswinkel)),sin(radians(self.neigungswinkel)),0)               # Neuausrichtung der Frame-Axis für Planetenneigungswinkel
            if self.zentrum:
                self.f.pos = (self.zentrum.f.pos.x+self.abstand_zentrum*sin(x/self.umkreiszeit/zfakt), 0 ,self.zentrum.f.pos.z+self.abstand_zentrum*cos(x/self.umkreiszeit/zfakt))   #Bewegung um Zentrum
                self.trail.append(pos=self.f.pos, retain=int(self.spurlaenge*zfakt))
                x+=1

if __name__ == '__main__':          # falls Skript gestartet...
    scene.width=800                 # Fensterbreite
    scene.height=400                # Fensterhöhe
    scene.forward-=vector(0,0.03,0.1) # Blickpunkt in Zentrum über den Bahnen...(Vektoraddition)
    scene.forward             # Kontrollausgabe des Vektors
    scene.lights=[distant_light(direction=(0.22, 0.44, 0.88), color=color.gray(0.4))] # nur schwaches 'Weltraumlicht'
    
    sonne  = Planet(pos=(0,0,0),radius=scale_dist(s_radius), color = (1,1,0), texture=textures.emissive)
    sonnenlicht = local_light(pos=(0,0,0), color=color.white)
    merkur = Planet(pos=(0,0,scale_dist(s_abstand_merkur)),radius=scale_rad(mer_radius), color = (1,0.6,0.2), texture=textures.wood, rotzeit=mer_rotzeit, \
                    umkreiszeit=mer_umkreiszeit, zentrum=sonne, abstand_zentrum=scale_dist(s_abstand_merkur))
    venus  = Planet(pos=(0,0,scale_dist(s_abstand_venus)), radius=scale_rad(v_radius), color=(0.4,0.6,0.8), texture=textures.marble, rotzeit=v_rotzeit, \
                    umkreiszeit=v_umkreiszeit, zentrum=sonne, abstand_zentrum=scale_dist(s_abstand_venus), spurlaenge=1000)
    erde   = Planet(pos=(0,0,scale_dist(s_abstand_erde)), radius=scale_rad(e_radius), rotzeit=e_rotzeit, texture=textures.earth, neigungswinkel=e_neigungswinkel,\
                   zentrum=sonne, umkreiszeit=e_umkreiszeit, abstand_zentrum=scale_dist(s_abstand_erde))
    mond   = Planet(pos=(0,0,0), radius=scale_rad(m_radius), zentrum=erde, abstand_zentrum=scale_dist(e_abstand_mond), \
                   texture=mondtextur, rotzeit=m_rotzeit, umkreiszeit=m_umkreiszeit, spurlaenge=20000)
    """
    mars   = Planet(pos=(0,0,scale_dist(s_abstand_mars)), radius=scale_rad(ma_radius), zentrum=sonne, abstand_zentrum=scale_dist(s_abstand_mars),\
                    umkreiszeit=ma_umkreiszeit, rotzeit=ma_rotzeit, texture=marstextur, spurlaenge=300000)
    jupiter= Planet(pos=(0,0,scale_dist(s_abstand_jupiter)), radius=scale_rad(j_radius), zentrum=sonne, abstand_zentrum=scale_dist(s_abstand_jupiter),\
                    umkreiszeit=j_umkreiszeit, rotzeit=j_rotzeit, color=(0.7,0.3,0.2), texture=textures.marble, spurlaenge=300000)
    """
    
    # Planeten-Threads einzeln starten...
    merkur.start()
    venus.start()
    erde.start()
    mond.start()
    """
    mars.start()
    jupiter.start()
    """

