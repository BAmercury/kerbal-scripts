# Simple rocket simulation in 1D
from matplotlib import pyplot as plt
from math import pi
# Mass props
m_parachute = 0.10 * 1000 # kg
m_cmd_pod = 0.84 * 1000 # kg (total mass)
m_fins = 4 * 0.01 * 1000 # kg, 4 fins
m_booster_full = 3.5625 * 1000 # kg, full
m_booster_empty = 0.75 * 1000 # kg, empty 
m_pilot = 45 # kg 

# Mass of rocket (no motor)
m_r = m_parachute + m_cmd_pod + m_fins + m_pilot
# Booster thrust
T_atm = 197.90 * 1000 # N
T_vac = 227.0 * 1000 # N
# Booster I_sp (s)
# thrust per rate of fuel consumption 
# change of momentum per amount of fuel consumed
Isp_atm = 170 # sec
Isp_vac = 195 # sec
# 
booster_burn_time_atm = 24.2 # sec, atm
booster_burn_time_vac = 23.7 # sec, vac
# burn time = Impulse / Thrust
Impulse_atm = booster_burn_time_atm * T_atm
# print(Impulse_atm)
# vac threshold
vac_thres = 20000 # m, when we reach the vac of space

# Constants
Cd = 0.75
d = 1.25 # meters, diameter
d = 0.0
A = pi * (d/2)**2
rho = 1.2 # kg/m^3 air density 
g = 9.807 # acceleration due to gravity m/s^2

run_sim = True
dt = 0.1
t_i = [0.0] # time
t_prev = 0.0 # time previous 

state = "boost" # state of rocket
loc = "atm" # if rocket is in atm or vac

# Fuel consumption 
m_prop = m_booster_full - m_booster_empty # mass of prop onboard rocket, kg
m_prop_dec_units = 15.83 # units/s
fuel_units = 375 # units of fuel
m_fuel = m_prop / fuel_units # mass of fuel, kg
# mass being used per second
m_prop_dec = m_prop_dec_units * m_fuel # kg/s

m_prop_i = [m_prop] # prop mass at index i
v_i = [0.0] # velocity at index i
y_i = [0.0] # height at index i 
F_thrust_i = T_atm # thrust 
F_wind_i = 0.0 # drag is zero on launch pad
alt_prev = 0.0
v_max = 0.0 # velocity at burnout
i = 0 # index
while (run_sim):
    # Get mass props
    if (state == "boost"):
        m_t = m_r + (m_booster_empty + m_prop_i[i]) # average mass of rocket burning fuel
        m_prop_i.append(m_prop_i[i] - m_prop_dec*dt)

    else:
        # if in coast
        m_prop_i.append(0) # used all fuel in burn 
        m_t = m_r + m_booster_empty # mass of a rocket in coast
    

    # Check if in atmosphere
    if (y_i[i] < vac_thres):
        # in atmosphere
        loc = "atm"
        F_thrust_i = T_atm
        # Calculate drag
        k = 0.5 * rho * Cd * A
        F_wind_i = k * v_i[i]**2
        # check if in coast
        if (t_i[i] > booster_burn_time_atm): # if time exceeds booster burn time in atmosphere
            state = "coast" # change state
            v_max = v_i[i]
            F_thrust_i = 0
            #print("Reached coast in atm")
    else:
        # in vac
        loc = "vac"
        F_thrust_i = T_vac
        F_wind_i = 0.0
        # check if in coast
        if (t_i[i] > booster_burn_time_vac):
            state = "coast"
            v_max = v_i[i]
            F_thrust_i = 0
            #print("Reached coast in vac")


    # Total force
    print(m_t)
    R = 600*1000 # radius of Kerbain in m
    accel_g = g * (R / (R + y_i[i]))**2
    F_total = F_thrust_i - F_wind_i - m_t*accel_g
    # accel
    acc = F_total / m_t
    # velocity 
    v_i.append(v_i[i] + acc*dt)
    y_i.append(y_i[i] + v_i[i]*dt)






    # update time
    t_i.append(t_i[i] + dt)
    i = i + 1
    # stop simulation when we see altitude start to decrease 
    if (y_i[i] - alt_prev) < 0:
        run_sim = False
        exit
    else:
        alt_prev = y_i[i]

    
print("Velocity at end of coast", end='\n')
print(v_i[-1], end='\n') 

print("Velocity at end of boost", end='\n')
print(v_max, end='\n')

print("Height at end of coast", end='\n')
print(y_i[-1], '\n')

print("Total time of flight", end='\n')
print(t_i[-1], end='\n')

print("Mass Prop at the end", end='\n')
print(m_prop_i[-1])

# plot(x, y)
plt.figure()
plt.plot(t_i, v_i)
plt.xlabel('time')
plt.ylabel('vel m/s')

plt.figure()
plt.plot(t_i, y_i)
plt.xlabel('time')
plt.ylabel('height (m)')

plt.figure()
plt.plot(t_i, m_prop_i)
plt.xlabel('time')
plt.ylabel('mass prop kg')

plt.show()
            


