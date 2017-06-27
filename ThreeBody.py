import os
import numpy
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
G = 1.0

def calRstenF(F1,F2):
	F = F1
	F['x'] = F1['x'] + F2['x']
	F['y'] = F1['y'] + F2['y']
	F['z'] = F1['z'] + F2['z']
	return F
def calStatus(body,F,dt):
	body_new = body
	body_new['vx'] = F['x']/body_new['m']*dt + body['vx']
	body_new['vy'] = F['y']/body_new['m']*dt + body['vy']
	body_new['vz'] = F['z']/body_new['m']*dt + body['vz']
	body_new['x'] = (body_new['vx'] + body['vx'])*dt/2 + body['x']
	body_new['y'] = (body_new['vy'] + body['vy'])*dt/2 + body['y']
	body_new['z'] = (body_new['vz'] + body['vz'])*dt/2 + body['z']
	body_new['t'] = dt + body['t']
	return body_new
def calF(body1,body2):
	r_vect = {'x':body1['x'] - body2['x'],'y':body1['y'] - body2['y'],'z':body1['z'] - body2['z']}
	r_dist = (r_vect['x']**2 + r_vect['y']**2 +r_vect['z']**2 )**0.5
	F_scale = G*body1['m']*body2['m']/r_dist**2
	F12 = {'x':F_scale*r_vect['x']/r_dist,'y':F_scale*r_vect['y']/r_dist,'z':F_scale*r_vect['z']/r_dist,'t':body1['t']}
	return F12

def GetTrack(Track,body):
	Track['x'].append(body['x'])
	Track['y'].append(body['y'])
	Track['z'].append(body['z'])
	Track['t'].append(body['t'])
	return Track

def plotTrack(B,ax,lab):
	x, y, z = B['x'],B['y'],B['z']
	ax.plot(x, y, z,label = lab)


B_origin = {'m':1.0,'x':0.0,'y':0.0,'z':0.0,'vx':0.0,'vy':0.0,'vz':0.0,'t':0.0,'name':''}
F = {'x':0.0,'y':0.0,'z':0.0,'t':0.0}
Ba,Bb,Bc = B_origin.copy(),B_origin.copy(),B_origin.copy()
#print Ba,Bb,Bc
Ba['x'] = 1.0
Ba['vx'] = 0.7

Bb['y'] = 1.0
#Bc['z'] = 1.0
Bc['m'] = 0.0
Ba['name'] = 'a'
Bb['name'] = 'b'
Bc['name'] = 'c'
#print Ba,Bb,Bc

dt = 0.01
T = 10000
fig = plt.figure()  
ax = fig.add_subplot(111, projection='3d')
Track_a = {'x':[],'y':[],'z':[],'t':[]}
Track_b = {'x':[],'y':[],'z':[],'t':[]}
Track_c = {'x':[],'y':[],'z':[],'t':[]}



for N in range(1,int(T/dt)):
	Fa = calRstenF(calF(Bb,Ba),calF(Bc,Ba))
	Fb = calRstenF(calF(Ba,Bb),calF(Bc,Bb))
	#Fc = calRstenF(calF(Ba,Bc),calF(Bb,Bc))
	Fc = F
	Ba = calStatus(Ba,Fa,dt)
	#Bb = calStatus(Bb,Fb,dt)
	#Bc = calStatus(Bc,Fc,dt)
	Track_a = GetTrack(Track_a,Ba)
	Track_b = GetTrack(Track_b,Bb)
	Track_c = GetTrack(Track_c,Bc)

	#print (Ba['x'],Ba['y'],Ba['z'])
plotTrack(Track_a, ax,'track of Body_a, dt = %f, T = %f'%(dt,T))
plotTrack(Track_b, ax,'track of Body_b, dt = %f, T = %f'%(dt,T))
plotTrack(Track_c, ax,'track of Body_c, dt = %f, T = %f'%(dt,T))
ax.legend()
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
