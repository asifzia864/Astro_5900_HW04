import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------- Functions ------------------
def acceleration_jupyter(x_j,y_j):
    ax_j = - ((G*M*x_j)/(x_j**2 + y_j**2)**1.5)
    ay_j = - ((G*M*y_j)/(x_j**2 + y_j**2)**1.5)
    return ax_j,ay_j

def acceleration_voyager(x_v,y_v,x_j,y_j):
    ax_sun = - ((G*M*x_v)/(x_v**2 + y_v**2)**1.5)
    ay_sun = - ((G*M*y_v)/(x_v**2 + y_v**2)**1.5)

    r_jup = np.sqrt((x_v - x_j)**2 + (y_v - y_j)**2)
    ax_jup = -G * M_jup * (x_v - x_j) / r_jup**3
    ay_jup = -G * M_jup * (y_v - y_j) / r_jup**3
    
    return ax_sun + ax_jup, ay_sun + ay_jup

def Leapfrog_step_jupyter(vx, vy, x, y, dt):
    ax, ay = acceleration_jupyter(x, y)
    
    # KICK: velocity at the half-step (t + dt/2)
    vx_half = vx + ax * (dt / 2)
    vy_half = vy + ay * (dt / 2)
    
    # DRIFT: position by the full-step (t + dt) using half-step velocity
    x_next = x + vx_half * dt
    y_next = y + vy_half * dt
    
    # NEW acceleration (at time t + dt) using the new positions
    ax_next, ay_next = acceleration_jupyter(x_next, y_next)
    
    # KICK: final velocity at the full-step (t + dt)
    vx_next = vx_half + ax_next * (dt / 2)
    vy_next = vy_half + ay_next * (dt / 2)
    
    return vx_next, vy_next, x_next, y_next
    
def Leapfrog_step_voyager(vx, vy, x_v, y_v, x_jup_current, y_jup_current, x_jup_next, y_jup_next, dt):
    # Initial acceleration uses Jupiter's position at time t
    ax_v, ay_v = acceleration_voyager(x_v, y_v, x_jup_current, y_jup_current)
    
    # KICK: velocity at the half-step (t + dt/2)
    vx_half = vx + ax_v * (dt / 2)
    vy_half = vy + ay_v * (dt / 2)
    
    # DRIFT: position by the full-step (t + dt) using half-step velocity
    x_next = x_v + vx_half * dt
    y_next = y_v + vy_half * dt
    
    # NEW acceleration (at time t + dt) using Jupiter's NEW position at t + dt
    ax_next, ay_next = acceleration_voyager(x_next, y_next, x_jup_next, y_jup_next)
    
    # KICK: final velocity at the full-step (t + dt)
    vx_next = vx_half + ax_next * (dt / 2)
    vy_next = vy_half + ay_next * (dt / 2)
    
    return vx_next, vy_next, x_next, y_next

# Parameters 
r0 = 1             # distance from sun to earth 
G = 4*np.pi**2     # Gravitational constant
M = 1              # Solar Mass 
M_jup = 0.000954*M
# Time array
dt = 0.001
time_arr = np.arange(0,10,dt)

# Jupyter arrays
x_jup = np.zeros(len(time_arr))
y_jup = np.zeros(len(time_arr))
vx_jup = np.zeros(len(time_arr))
vy_jup = np.zeros(len(time_arr))

# Voyager arrays
x_v = np.zeros(len(time_arr))
y_v = np.zeros(len(time_arr))
vx_v = np.zeros(len(time_arr))
vy_v = np.zeros(len(time_arr))

# Initial conditions for Jupiter (Circular orbit at 5.2 AU)
theta_jup = 1.648 
v_circ_jup = np.sqrt(G * M / (5.2 * r0)) # circular velocity for 5.2 AU

x_jup[0] = 5.2 * r0 * np.cos(theta_jup)
y_jup[0] = 5.2 * r0 * np.sin(theta_jup)
vx_jup[0] = -v_circ_jup * np.sin(theta_jup)
vy_jup[0] = v_circ_jup * np.cos(theta_jup) 

# Initial conditions for Voyager 2 (Escape velocity from 1 AU)
x_v[0] = r0
y_v[0] = 0
vx_v[0] = 0
vy_v[0] = np.sqrt(2 * G * M / r0)        # sqrt(2) * circular velocity

# Dynamics Loop
for i in range (0,len(time_arr)-1):
    vx_jup[i+1], vy_jup[i+1], x_jup[i+1], y_jup[i+1] = Leapfrog_step_jupyter(vx_jup[i], vy_jup[i], x_jup[i], y_jup[i], dt)
    
    vx_v[i+1], vy_v[i+1], x_v[i+1], y_v[i+1] = Leapfrog_step_voyager(vx_v[i], vy_v[i], x_v[i], y_v[i], x_jup[i], y_jup[i], x_jup[i+1], y_jup[i+1], dt)


Speed= np.sqrt(vx_v**2 + vy_v**2)

# Plotting speed
plt.plot(time_arr,Speed,label = 'Speed_leapfrog')
plt.xlabel('time (1 yr)')
plt.ylabel('Speed (1 AU/yr)')
plt.legend()
plt.grid(True)
plt.show()


# fig, ax = plt.subplots(figsize=(8, 8))
# ax.set_aspect('equal')
# # Expanded limits to see Jupiter's orbit (r = 5.2 AU) and beyond
# ax.set_xlim(-8.0, 8.0)
# ax.set_ylim(-8.0, 8.0)

# # Static Sun
# ax.plot(0, 0, 'yo', markersize=15, label="Sun")

# # Jupiter elements
# point_jup, = ax.plot([], [], 'o', color='orange', markersize=10, label="Jupiter")
# line_jup, = ax.plot([], [], '-', color='orange', alpha=0.5, linewidth=1)

# # Voyager 2 elements
# point_v, = ax.plot([], [], 'k.', markersize=5, label="Voyager 2")
# line_v, = ax.plot([], [], 'k-', alpha=0.8, linewidth=1)

# # Dynamic Text for Time and Speed
# time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12)
# speed_text = ax.text(0.05, 0.90, '', transform=ax.transAxes, fontsize=12)

# # Initialization Function
# def init():
#     point_jup.set_data([], [])
#     line_jup.set_data([], [])
#     point_v.set_data([], [])
#     line_v.set_data([], [])
#     time_text.set_text('')
#     speed_text.set_text('')
#     return point_jup, line_jup, point_v, line_v, time_text, speed_text

# # Update Function
# def update(i):
#     # Update Jupiter
#     point_jup.set_data([x_jup[i]], [y_jup[i]])
#     line_jup.set_data(x_jup[:i], y_jup[:i])

#     # Update Voyager
#     point_v.set_data([x_v[i]], [y_v[i]])
#     line_v.set_data(x_v[:i], y_v[:i])

#     # Convert time from years to months
#     current_time_months = time_arr[i] * 12
#     time_text.set_text(f'Time: {current_time_months:.1f} months')

#     # Calculate speed in AU/yr, then convert to km/s (1 AU/yr = 4743 m/s = 4.743 km/s)
#     speed_au_yr = np.sqrt(vx_v[i]**2 + vy_v[i]**2)
#     speed_km_s = speed_au_yr * 4.743
#     speed_text.set_text(f'Voyager Speed: {speed_km_s:.2f} km/s')

#     return point_jup, line_jup, point_v, line_v, time_text, speed_text

# # Create the animation (skipping frames to speed up playback)
# ani = FuncAnimation(fig, update, frames=range(0, len(time_arr), 10), 
#                     init_func=init, blit=True, interval=20)

# plt.legend(loc="lower right")
# plt.grid(True)
# plt.title("Voyager 2 Gravity Assist Simulation")

# # --- Saving the Movie ---
# # ani.save('voyager_assist.mp4', writer='ffmpeg', fps=30)

# plt.show()