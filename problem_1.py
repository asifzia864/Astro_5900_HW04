import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------- Functions ------------------
def acceleration(x,y):
    ax = - ((G*M*x)/(x**2 + y**2)**1.5)
    ay = - ((G*M*y)/(x**2 + y**2)**1.5)
    return ax,ay

def Euler_step(vx,vy,x,y,dt):
    ax,ay = acceleration(x,y)
    vx_next = vx + ax*dt
    vy_next = vy + ay*dt
    x_next = x + vx*dt 
    y_next = y + vy*dt 
    return vx_next,vy_next,x_next,y_next
    
def Leapfrog_step(vx, vy, x, y, dt):
    ax, ay = acceleration(x, y)
    
    # KICK: velocity at the half-step (t + dt/2)
    vx_half = vx + ax * (dt / 2)
    vy_half = vy + ay * (dt / 2)
    
    # DRIFT: position by the full-step (t + dt) using half-step velocity
    x_next = x + vx_half * dt
    y_next = y + vy_half * dt
    
    # NEW acceleration (at time t + dt) using the new positions
    ax_next, ay_next = acceleration(x_next, y_next)
    
    # KICK: final velocity at the full-step (t + dt)
    vx_next = vx_half + ax_next * (dt / 2)
    vy_next = vy_half + ay_next * (dt / 2)
    
    return vx_next, vy_next, x_next, y_next
    
# Parameters 
r0 = 1             # distance from sun to earth 
G = 4*np.pi**2     # Gravitational constant
M = 1              # Solar Mass 

# Time array
dt = 0.001
time_arr = np.arange(0,10,dt)

# Euler Arrays
x_e = np.zeros(len(time_arr))
y_e = np.zeros(len(time_arr))
vx_e = np.zeros(len(time_arr))
vy_e = np.zeros(len(time_arr))

# Leapfrog Arrays
x_lf = np.zeros(len(time_arr))
y_lf = np.zeros(len(time_arr))
vx_lf = np.zeros(len(time_arr))
vy_lf = np.zeros(len(time_arr))

# Set Initial Conditions for both (they start at the same point)
x_e[0] = x_lf[0] = r0
y_e[0] = y_lf[0] = 0
vx_e[0] = vx_lf[0] = 0
vy_e[0] = vy_lf[0] = 0.8* np.sqrt(G*M/r0)
for i in range (0,len(time_arr)-1):
    vx_e[i+1], vy_e[i+1], x_e[i+1], y_e[i+1] = Euler_step(vx_e[i],vy_e[i],x_e[i],y_e[i],dt)
    vx_lf[i+1], vy_lf[i+1], x_lf[i+1], y_lf[i+1] = Leapfrog_step(vx_lf[i],vy_lf[i],x_lf[i],y_lf[i],dt)

Speed_euler = np.sqrt(vx_e**2 + vy_e**2)
Speed_leapfrog = np.sqrt(vx_lf**2 + vy_lf**2)

# Energy = Kinetic + Potential
energy_e = 0.5 * Speed_euler**2 - (G * M) / np.sqrt(x_e**2 + y_e**2)
energy_lf = 0.5 * Speed_leapfrog**2 - (G * M) / np.sqrt(x_lf**2 + y_lf**2)

# Plotting speed
plt.plot(time_arr,Speed_euler,label = 'Speed_euler')
plt.plot(time_arr,Speed_leapfrog,label = 'Speed_leapfrog')
plt.xlabel('time (1 yr)')
plt.ylabel('Speed (1 AU/yr)')
plt.legend()
plt.grid(True)
plt.show()

# Plotting energy
plt.plot(time_arr,energy_e,label = 'Energy_euler')
plt.plot(time_arr,energy_lf,label = 'Energy_leapfrog')
plt.xlabel('time (1 yr)')
plt.ylabel('Energy (t)')
plt.legend()
plt.grid(True)
plt.show()

# Animation
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)
ax.plot(0, 0, 'yo', markersize=12, label="Sun")
point_e, = ax.plot([], [], 'ro', markersize=7, label="Euler")
line_e, = ax.plot([], [], 'r-', alpha=1, linewidth=1)
point_lf, = ax.plot([], [], 'bo', markersize=7, label="Leapfrog")
line_lf, = ax.plot([], [], 'b-', alpha=1, linewidth=1)

# Initialization Function
def init():
    point_e.set_data([], [])
    line_e.set_data([], [])
    point_lf.set_data([], [])
    line_lf.set_data([], [])
    return point_e, line_e, point_lf, line_lf

# Update Function
def update(i):
    point_e.set_data([x_e[i]], [y_e[i]])
    line_e.set_data(x_e[:i], y_e[:i])
    point_lf.set_data([x_lf[i]], [y_lf[i]])
    line_lf.set_data(x_lf[:i], y_lf[:i])

    return point_e, line_e, point_lf, line_lf

# range(0, len(time_arr), 10) is used to skip frames 
ani = FuncAnimation(fig, update, frames=range(0, len(x_e), 5), 
                    init_func=init, blit=True, interval=20)

plt.legend(loc="upper right")
plt.grid(True)
plt.show()