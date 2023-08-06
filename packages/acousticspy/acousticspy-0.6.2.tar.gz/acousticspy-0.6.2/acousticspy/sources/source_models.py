import numpy as np
import scipy.linalg as la
import scipy.special as sp
import matplotlib.pyplot as plt

def baffled_circular_piston_directivity(radius,frequency,theta):
    c = 343
    k = 2*np.pi*frequency/c
    return 2*sp.jv(1,k*radius*np.sin(theta)) / (k*radius*np.sin(theta))

def get_circle_elements(total_area,num_elements):
    
    radius = np.sqrt(total_area/np.pi)
    
    diameter = 2*radius

    square_positions, square_areas = get_square_elements(diameter**2,num_elements*4/np.pi)
    
    areas = np.zeros(1)
    positions = np.zeros([1,3])
    
    # Cut out points that aren't in the circle
    for i in range(len(square_areas)):
        
        if la.norm(square_positions[i,:]) <= radius:
            areas = np.append(areas,square_areas[i])
            positions = np.append(positions,[square_positions[i,:]],axis = 0)
        
    # Removing the zeros at the top of the arrays
    areas = areas[1:]
    positions = positions[1:]
        
    return positions, areas

def get_square_elements(total_area,num_elements):
    
    length = np.sqrt(total_area)
    
    elements_length = int(np.sqrt(num_elements))
    
    dy = length/elements_length
    dz = dy
    
    areas = np.zeros(1)
    positions = np.zeros([1,3])
    
    for i in range(elements_length):
        for j in range(elements_length):
            y = (dy*i - length/2) + dy/2
            z = (dz*j - length/2) + dz/2
            areas = np.append(areas,dy*dz)
            positions = np.append(positions,[[0,y,z]],axis = 0)
            
    # Removing the zeros at the top of the arrays
    areas = areas[1:]
    positions = positions[1:]

    return positions, areas

"""
Define an array of loudspeakers
"""

def define_loudspeaker_array(num_speakers,cone_diameter,cone_separation,
                             cone_strengths = [1],
                             cone_phases = [0],
                             num_points = 100,
                             show_plots = False):

    if np.size(cone_strengths) == 1:
        cone_strengths = np.ones(num_speakers) * cone_strengths
        
    if np.size(cone_phases) == 1:
        cone_phases = np.ones(num_speakers) * cone_phases

    total_length = cone_diameter*num_speakers + cone_separation*num_speakers

    cone_positions = np.array([])
    for i in range(num_speakers):
        cone_positions = np.append(cone_positions,i*cone_separation + cone_diameter/2)
        
    # Centering about the origin
    cone_positions = cone_positions - max(cone_positions)/2 - cone_diameter/4


    # Creating the array of mini-sources
    positions = np.linspace(min(cone_positions) - cone_diameter/2,max(cone_positions)+cone_diameter/2,num_points)
    strengths = np.zeros(len(positions))
    phases = np.zeros(len(positions))
    for i in range(0,len(positions)):

        for j in range(0,num_speakers):

            if np.abs(positions[i] - cone_positions[j]) <= cone_diameter:
                strengths[i] = cone_strengths[j]
                phases[i] = cone_phases[j]

    if show_plots:
        plt.figure()
        plt.plot(positions,strengths)
        plt.title("Speaker Cone Source Strengths")
        plt.xlabel("Position (m)")
        plt.ylabel("Cone Source Strength (m^3/s)")
        
        plt.figure()
        plt.plot(positions,phases)
        plt.title("Speaker Cone Source Phases")
        plt.xlabel("Position (m)")
        plt.ylabel("Cone Phase (rad/s)")

        plt.show()
        
    return positions, strengths, phases, cone_positions

"""
Modeling a moving-coil loudspeaker. This is not fully trusted, but gives some results as expected based
on class notes in BYU PHSCS 660, Winter 2022. If you need definitive results, you should write your own
code for find a trusted solver. This is intended (and only trusted) to give you an idea of what the 
different parameters do.
"""

def moving_coil_loudspeaker(Cms = 1.0e-4, # m/N (Suspension Mechanical Compliance)
                            Rms = 0.020, # kg/s (Suspension Mechanical Resistance)
                            Mmd = 0.05, # kg (Diaphragm moving mass in Mechanicial Domain)
                            Sd = 0.20, # m^2 (Diaphragm effectice surface area)
                            Re = 7.0, # Ohms (Resistance in the voice coil)
                            Le = 1.0e-3, # Henries (Inductance in the voice coil)
                            Bl = 20, # telsa meters (Motor Strength)
                            Rg = 0, # Ohms (Voltage Source Internal Resistance)
                            eg = 1, # Volts (Input voltage)
                            c = 343, # m/s (Speed of sound)
                            show_TVR = True, # whether to show the TVR plot
                            show_Analysis_Plots = False, # Whether to show impedance plots
                            r = 1, # Distance at which to calculate everything
                            f = np.logspace(0,3,1000)
                            ):

    omega = 2*np.pi*f
    k = omega / c
    a = np.sqrt(Sd/np.pi)
    ka = k*a
    rho_0 = 1.2

    gamma_p = ka**2 / (1 - sp.jv(1,2*ka)/ka)
    Xmr = sp.struve(1,2*ka)/ka
    Rmr = ka**2 / gamma_p

    Rm = Bl**2 * (Rg + Re) / ((Rg + Re)**2 + (omega*Le)**2) + Rms + 2*Rmr
    Xm = - Bl**2*(omega*Le) / ((Rg + Re)**2 + (omega*Le)**2) + omega*Mmd - 1/(omega*Cms) + 2*Xmr
    Zm = Rm + 1j*Xm

    u_d = eg*Bl / ((Rg + Re + 1j*omega*Le)*Zm)

    p = np.abs(u_d)/r * ka * np.sqrt(rho_0*c/(4*np.pi))

    if show_Analysis_Plots:
        plt.figure()
        plt.semilogx(f,Rmr,label = "$R_{MR}$")
        plt.semilogx(f,Xmr,label = "$X_{MR}$")
        plt.semilogx(f,np.abs(Rmr + 1j*Xmr),label = "$|Z_{MR}$|")
        plt.legend()
        plt.grid()
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Value")
        plt.title("Radiation Impedance Values")

        plt.figure()
        plt.semilogx(f,Rm,label = "$R_{M}$")
        plt.semilogx(f,Xm,label = "$X_{M}$")
        plt.semilogx(f,np.abs(Zm),label = "$|Z_{M}|$")
        plt.legend()
        plt.grid()
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Value")
        plt.title("Mechanical Impedance Values")

        plt.figure()
        plt.semilogx(f,np.real(u_d),label = "$Re\{ u_D \}$")
        plt.semilogx(f,np.imag(u_d),label = "$Im\{ u_D \}$")
        plt.semilogx(f,np.abs(u_d),label = "$|u_D|$")
        plt.legend()
        plt.grid()
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Value")
        plt.title("Diaphragm Velocity")

        plt.figure()
        plt.semilogx(f,p,label = "p(r)")
        plt.legend()
        plt.grid()
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Value")
        plt.title("Far-field Pressure")

    if show_TVR:
        p = np.abs(u_d)/1.0 * ka * np.sqrt(rho_0*c/(4*np.pi))

        # Accession to inertia (equation 4.826)
        Mmr = 8/3 * rho_0 * a**3
        omega_0 = np.sqrt(1/(Cms*(Mmd + 2*Mmr)))
        f_0 = omega_0/(2*np.pi)

        TVR = 20*np.log10((p/eg)/20e-6)

        plt.figure()
        plt.semilogx(f,TVR,label = "TVR")
        plt.semilogx([1,2],[min(TVR),12 + min(TVR)],label = "12 dB / Octave",linestyle = "--")
        plt.vlines(f_0,ymin = min(TVR), ymax = max(TVR),label = "$f_0$",color = "red",linestyle = "--")
        plt.vlines(10*f_0,ymin = min(TVR), ymax = max(TVR),label = "$10*f_0$",color = "purple",linestyle = "--")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("$\hat{p}/\hat{e}_g$")
        plt.title("Transmitting Voltage Response")
        plt.grid()
        plt.legend()