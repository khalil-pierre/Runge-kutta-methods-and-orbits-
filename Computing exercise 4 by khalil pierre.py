# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 15:21:55 2018

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt

Gravitational_constant=6.67e-11

class Object:
    def __init__(self,Name,Mass,Position,Velocity,Radius):
        self.Name=Name
        self.Mass=Mass
        self.Position=Position
        self.Velocity=Velocity
        self.Radius=Radius 
        
    def Plot(self):
        '''Use's the equation of a circle in polar corrdinates to plot circular bodies \n
        at the position specifeied for the object.'''
        Plot_x=[]
        Plot_y=[]
        theta=np.linspace(0,2*np.pi,100)
        
        for i in theta:
            Plot_x+=[self.Position[0]+self.Radius*np.cos(i)]
            Plot_y+=[self.Position[1]+self.Radius*np.sin(i)]
        
        return [Plot_x,Plot_y]
    
    def Kinetic_energy(self):
        '''Finds the kinetic energy of an object from its velocity and mass.'''
        Ke=0.5*self.Mass*np.linalg.norm(self.Velocity)**2
        return Ke
    
    def Potential_energy(self,moon='False'):
        '''Finds the potential energy of an obejcect in the gravitational potential \n
        well of the earth if moon==False and the potential energy of an object in the potential \n
        well of the moon earth system if moon==True.'''
        if moon=='False':
            U=-Gravitational_constant*self.Mass*5.972e24/np.linalg.norm(self.Position)
            return U
        
        if moon=='True':
            U=-Gravitational_constant*self.Mass*5.972e24/np.linalg.norm(self.Position)
            Um=-Gravitational_constant*self.Mass*7.34767309e22/np.linalg.norm(self.Position-np.array([0,384400e3]))
            return U+Um
            
    

def function(r):
    '''Calcualtes the acceleration of an object due to earths gravitational attraction.\n
    Uses the position of the object r to calcualte the radial distance bettween the center of the \n
    earth (0,0) and the object. Gravitational acceleration is a function of radial position only.'''
    R=-Earth.Mass*Gravitational_constant*r/np.linalg.norm(r)**3
    return R 

def function2(r):
    '''Calcualtes the acceleration of an object due to the earth and moons\n
    gravitational attraction.Uses the position of the object r to calcualte \n
    the radial distance bettween the center of the earth (0,0) and the object \n
    and the center of the moon and the object.'''
    Acceleration_moon=-Gravitational_constant*Moon.Mass*(r-Moon.Position)/(np.linalg.norm(r-Moon.Position)**3)
    Acceleration_earth=-Gravitational_constant*Earth.Mass*r/(np.linalg.norm(r)**3)
    return Acceleration_moon+Acceleration_earth

def Orbital_runge_kutta(func,position,velocity,Time_step):
    '''Uses the runge kutta method to numerically solve the equation of motion \n
    of an object moving through a gravitational well. Out puts the change in position \n
    and velocity for a small time step. func is the function that is being solved, \n
    position is the inital position of the object, velocity is the the intial velocity of \n
    the object and time step is the change in time.'''
    
    K1x=velocity
    K1v=func(position)
    
    K2x=velocity+(Time_step*K1v/2)
    K2v=func(position+Time_step*K1x/2)
    
    K3x=velocity+(Time_step*K2v/2)
    K3v=func(position+Time_step*K2x/2)
    
    K4x=velocity+Time_step*K3v
    K4v=func(position+Time_step*K3x)
    
    Position_step=Time_step*(K1x+2*K2x+2*K3x+K4x)/6
    Velocity_step=Time_step*(K1v+2*K2v+2*K3v+K4v)/6
    
    return {'position':Position_step,'velocity':Velocity_step}

def Escape_velocity(position):
    '''Calculates the minimum velocity required to escape the earths gravitational potential well. \n
    Uses the position of the object as the escape velocity is dependent on the radial position of \n 
    the object.'''
    
    Ve=np.sqrt(2*Gravitational_constant*Earth.Mass/np.linalg.norm(position))
    return Ve

def Circular_orbit(position):
    '''Calcualtes the tangetial velocity required for an object to have a circualr orbit around the \n
    earth. Position is used to calculate the radial distance between the earth and the object.'''
    
    Vc=np.sqrt(Gravitational_constant*Earth.Mass/np.linalg.norm(position-Earth.Position))
    return Vc

def Orbital_period(position):
    '''Calculates the orbital period of an object moving in a circular orbit. Position is used to \n
    calculate the radial radial distance between the earth and the object'''
    
    return 2*np.pi*np.sqrt(np.linalg.norm(position)**3/(Gravitational_constant*Earth.Mass))
    


MyInput = '0'
while MyInput != 'q':
    MyInput = input('Enter a choice, "a","b","e" or "q" to quit: ')
    
    time=0
    dt=1
    
    Moon=Object('Moon',7.34767309e22,np.array([0,384400e3]),np.array([1017.96097024,0]),1737e3)
    Earth=Object('Earth',5.972e24,np.zeros(2),np.zeros(2),6.371e6)
    Rocket=Object('Rocket',2970000,0,0,0)
    
    #uses the plot function in the object class to calculate the 
    Earth_plot=Earth.Plot()
    Moon_plot=Moon.Plot()
    
    Position_x=[]
    Position_y=[]
    
    Moon_distance=[]
    
    Kinetic=[]
    Potential=[]
    t=[]
    Total_energy=[]
    
    if MyInput == 'a':
        print('You have chosen part (a)')
        print('In part a the motion of a rocket can be predicted.')
        print('To do this the rocket\'s inital position and velocity need to be choosen')
        
        heghit=float(input('Choose an inital radial position of the rocket above the earth surface (m): '))
        
        initial_position=heghit+Earth.Radius
        Rocket.Position=np.array([initial_position,0])
        
        print('\nThe escape velocity at this position is ' + str(Escape_velocity(Rocket.Position)) +'m/s.')
        print('The velocity of an circular orbit is ' + str(Circular_orbit(Rocket.Position)) +'m/s.')
        
        initial_velocity=float(input('Please select an inital orbital velocity (m/s): '))
        
        Rocket.Velocity=np.array([0,initial_velocity])
        
        print('The time taken for a circular orbit at ' + str(heghit) + 'm, is ' + str(Orbital_period(Rocket.Position)) + 's') 
        
        dt=float(input('Choose a time step: '))
        Run_time=float(input('Please select the run time of this simulation: '))  
        
                
        while time<Run_time and np.linalg.norm(Rocket.Position)>=Earth.Radius:
            #Loop stops if the run time is exceded or if the radial position of the earth
            #becomes less then the earths radius i.e. it crashes.
            #Each itteration the change in the rockets position and velocity is calculated via the runge 
            #kutta funtion and added to the variable Rocket.Position and Rocket.Velocity.
            
            time+=dt
            t+=[time]
            pos_vel=Orbital_runge_kutta(function,Rocket.Position,Rocket.Velocity,dt)
            
            Rocket.Position+=pos_vel['position']
            Rocket.Velocity+=pos_vel['velocity']
            
            Position_x+=[Rocket.Position[0]]
            Position_y+=[Rocket.Position[1]]
            
            Kinetic+=[Rocket.Kinetic_energy()]
            Potential+=[Rocket.Potential_energy()]
            
            Total_energy+=[Rocket.Kinetic_energy()+Rocket.Potential_energy()]
            
        
        plt.title('Rocket trajectory')
        plt.ylabel('Y (m)')
        plt.xlabel('X (m)')
        plt.plot(Position_x,Position_y,label='Rocket trajectory')
        plt.plot(Earth_plot[0],Earth_plot[1],label='Earth')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
        plt.clf()
        
        plt.title('Energy plots')
        plt.ylabel('Energy (J)')
        plt.xlabel('Time (s)')
        plt.plot(t,Kinetic,label='Kinetic energy')
        plt.plot(t,Potential,label='Potential')
        plt.plot(t,Total_energy,label='Total energy')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
        plt.clf()
        
        plt.plot(t,Total_energy)
        plt.show()

    elif MyInput == 'b':
        print('You have chosen part (b)')
        print('A rocket was launched from low earth orbit in a mission to take photos of the dark side of the moon.')
        print('The rocket then had to pass close enough to the earth for the photos to be sent via radiowaves.')
        print('The following flight path was plotted.')
        
        dt=20
        
        Rocket.Position=np.array([0,Earth.Radius+6.5e3])
        Rocket.Velocity=np.array([200,Escape_velocity(Rocket.Position)-90])

        while time<12000000 and \
        np.linalg.norm(Rocket.Position)>=Earth.Radius \
        and np.linalg.norm(Rocket.Position-Moon.Position)>=Moon.Radius:
            
            time+=dt
            t+=[time]
            
            pos_vel=Orbital_runge_kutta(function2,Rocket.Position,Rocket.Velocity,dt)
            Rocket.Position+=pos_vel['position']
            Rocket.Velocity+=pos_vel['velocity']
            
            Position_x+=[Rocket.Position[0]]
            Position_y+=[Rocket.Position[1]]
            
            Kinetic+=[Rocket.Kinetic_energy()]
            Potential+=[Rocket.Potential_energy(moon='True')]
            
            Total_energy+=[Rocket.Kinetic_energy()+Rocket.Potential_energy(moon='True')]
            
            Moon_distance+=[np.linalg.norm(Rocket.Position-Moon.Position)-Moon.Radius]
        
        plt.title('Rocket trajectory')
        plt.ylabel('Y (m)')
        plt.xlabel('X (m)')
        plt.plot(Position_x,Position_y,label='Rocket trajectory')
        plt.plot(Earth_plot[0],Earth_plot[1],label='Earth')
        plt.plot(Moon_plot[0],Moon_plot[1],label='Moon')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
        plt.clf()
        
        plt.title('Energy plots')
        plt.ylabel('Energy (J)')
        plt.xlabel('Time (s)')
        plt.plot(t,Kinetic,label='Kinetic energy')
        plt.plot(t,Potential,label='Potential')
        plt.plot(t,Total_energy,label='Total energy')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
        plt.clf()
        
        print('Total flight time was ' + str(time) + 's.')
        print('Closest approach to moon\'s surface was ' + str(min(Moon_distance)) + 'm')
        
        
    elif MyInput == 'e':
        
        Rocket.Position=np.array([0,Earth.Radius+6.5e3])
        
        print('You have choosen section e')
        print('In this section you can generate multiple rocket trajectorys.')
        print('To do this you must choose an inital velocity and a range of directions you want the'\
              + ' rocket to be fired in.')
        
        print('To do this you must choose an inital and a final angual displacment from the y axis.')
        print('This is how I found the inital conditions used in part b.')
        print('The escape velocity is ' + str(Escape_velocity(Rocket.Position)) + 'm/s.')
        print('The solid angle of the moon is 0.009 degress.')
        
        initial_velocity=float(input('Please choose an inital velocity: '))
        
        initial_angular_displacment=float(input('Please choose an inital angular displacment: '))
        final_angular_displacment=float(input('Please choose a finial angular displacment: '))
        
        N=int(input('Please choose how many plots you would like to see: '))
        
        angular_displacment=np.linspace(initial_angular_displacment,final_angular_displacment,N)
        
        Run_time=float(input('Choose a run time for each simulation: '))
        dt=float(input('Choose a time step: '))
        
        plt.title('Rocket trajectory for an inital velocity of ' + str(initial_velocity) + ('m/s'))
        plt.ylabel('Y (m)')
        plt.xlabel('X (m)')
        
        for i in angular_displacment:
            
            vy=initial_velocity*np.cos(i)
            vx=initial_velocity*np.sin(i)
            
            time=0
            
            Position_x=[]
            Position_y=[]
            
            Rocket.Position=np.array([0,Earth.Radius+6.5e3])
            Rocket.Velocity=np.array([vx,vy])
            
            while time<Run_time and \
            np.linalg.norm(Rocket.Position)>=Earth.Radius and\
            np.linalg.norm(Rocket.Position-Moon.Position)>=Moon.Radius:
                
                time+=dt
            
                pos_vel=Orbital_runge_kutta(function2,Rocket.Position,Rocket.Velocity,dt)
                Rocket.Position+=pos_vel['position']
                Rocket.Velocity+=pos_vel['velocity']
                
                Position_x+=[Rocket.Position[0]]
                Position_y+=[Rocket.Position[1]]
  
                
            plt.plot(Position_x,Position_y,label='Angular displacment =' + str(i) + 'degress')
            
       
        plt.plot(Earth_plot[0],Earth_plot[1],label='Earth')
        plt.plot(Moon_plot[0],Moon_plot[1],label='Moon')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
        plt.clf()

        
    elif MyInput != 'q':
        print('This is not a valid choice')
    
print('Goodbye')