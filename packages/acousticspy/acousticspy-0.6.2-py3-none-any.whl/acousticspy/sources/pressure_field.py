import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

"""
Creating an entire pressure field based on the locations of various sources
"""
def pressure_field(positions,frequencies,
                    field_points = -1,
                    time = 0.0,
                    areas = [0.001],
                    velocities = [0.01],
                    strengths = [0.01],
                    phases = [0],
                    x_range = [-1,1],
                    y_range = [-1,1],
                    z_range = [-1,1],
                    point_density = 100,
                    directivity_distance = 1000,
                    num_directivity_points = 10000,
                    method = "Monopole Addition",
                    dimensions = 2,
                    directivity_only = False,
                    directivity_plot_alone = False,
                    show_plots = False,
                    pressure_limits = [-100,100]):
    
    # Making all arrays that describe the sources be equal lengths
    num_sources = len(positions)
    positions = np.asarray(positions)
    
    if np.size(frequencies) == 1:
        frequencies = np.ones(num_sources) * frequencies
    
    if np.size(areas) == 1:
        areas = np.ones(num_sources) * areas
        
    if np.size(strengths) == 1:
        strengths = np.ones(num_sources) * strengths
        
    if np.size(phases) == 1:
        phases = np.ones(num_sources) * phases

    if np.size(velocities) == 1:
        velocities = np.ones(num_sources) * velocities

    # Enabling the user to custom-select points in the field
    if np.all(field_points == -1):
        custom_points = False
    else:
        custom_points = True

    time = complex(time)

    if dimensions == 1 and not custom_points:
        numPoints_x = int(np.floor((x_range[1] - x_range[0]) * point_density))
        x = np.linspace(x_range[0],x_range[1],numPoints_x)
        x = x[x != 0]
        field_points = x.reshape(-1,1)
        grid = x

    elif dimensions == 2 and not custom_points:
        numPoints_x = int(np.floor((x_range[1] - x_range[0]) * point_density))
        numPoints_y = int(np.floor((y_range[1] - y_range[0]) * point_density))
        x = np.linspace(x_range[0],x_range[1],numPoints_x)
        y = np.linspace(y_range[0],y_range[1],numPoints_y)

        grid = np.meshgrid(x,y)
        field_points = np.append(grid[0].reshape(-1,1),grid[1].reshape(-1,1),axis=1)
        X = grid[0]
        Y = grid[1]

    elif dimensions == 3 and not custom_points:
        numPoints_x = int(np.floor((x_range[1] - x_range[0]) * point_density))
        numPoints_y = int(np.floor((y_range[1] - y_range[0]) * point_density))
        numPoints_z = int(np.floor((z_range[1] - z_range[0]) * point_density))
        x = np.linspace(x_range[0],x_range[1],numPoints_x)
        y = np.linspace(y_range[0],y_range[1],numPoints_y)
        z = np.linspace(z_range[0],z_range[1],numPoints_z)

        grid = np.meshgrid(x,y,z)
        field_points = np.append(grid[0].reshape(-1,1),np.append(grid[1].reshape(-1,1),grid[2].reshape(-1,1),axis = 1),axis=1)
        X = grid[0]
        Y = grid[1]
        Z = grid[2]
    
    if not directivity_only:
        pressure_field = get_field(positions,frequencies,strengths,velocities,areas,phases,field_points,time,method)
        if not custom_points:
            pressure_field = pressure_field.reshape(-1,len(x)) # It's the number of points in the x-direction that you use here
    else:
        pressure_field = 0
    
    # Getting the directivity at a given distance. Default is 1000 meters away
    if not dimensions == 1 and not custom_points:
        directivity_points, theta = define_arc(directivity_distance,num_directivity_points)
        directivity = np.abs(get_field(positions,frequencies,strengths,velocities,areas,phases,directivity_points,time,method))
        directivity = directivity / np.max(directivity)
    
    # Only show plots if you calculated the entirie pressure field
    if dimensions == 1 and not custom_points:
        plot_1D(x,pressure_field,positions,show_plots,pressure_limits,directivity_only)
        theta = 0
        directivity = 0

    if dimensions == 2 and not custom_points:
        plot_2D(X,Y,pressure_field,positions,method,theta,directivity,show_plots,directivity_only,directivity_distance,directivity_plot_alone,pressure_limits)

    if dimensions == 3 and not custom_points:
        plot_3D(X,Y,Z,pressure_field,positions,method,theta,directivity,show_plots,directivity_only,directivity_distance,directivity_plot_alone,pressure_limits)
        
    if not custom_points:    
        return pressure_field, grid, directivity, theta
    else:
        return pressure_field

def plot_1D(x,pressure_field,positions,show_plots,pressure_limits,directivity_only):

    if show_plots and not directivity_only:
        # Defining the figure
        fig = plt.figure()
        fig.set_size_inches(8,8)

        # Plotting the real part
        ax = fig.add_subplot(221)
        ax.plot(x,np.real(pressure_field)[0,:])
        ax.scatter(positions[:,0],np.zeros(len(positions[:,0])),color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax.set_aspect('auto')
        ax.set_title("Real Part")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Re{Pressure}")
        ax.set_ylim(pressure_limits[0],pressure_limits[1])
        ax.grid("on")

        # Plotting the imaginary part
        ax = fig.add_subplot(223)
        ax.plot(x,np.imag(pressure_field)[0,:])
        ax.scatter(positions[:,0],np.zeros(len(positions[:,0])),color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax.set_aspect('auto')
        ax.set_title("Imaginary Part")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Im{Pressure}")
        ax.set_ylim(pressure_limits[0],pressure_limits[1])
        ax.grid("on")

        # Plotting the magnitude
        ax = fig.add_subplot(222)
        ax.plot(x,np.abs(pressure_field)[0,:])
        ax.scatter(positions[:,0],np.zeros(len(positions[:,0])),color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax.set_aspect('auto')
        ax.set_title("Magnitude")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("|Pressure|")
        ax.set_ylim(pressure_limits[0]*0.05,pressure_limits[1])
        ax.grid("on")
        
        fig.tight_layout(pad = 0.5)
        fig.show()
        

def plot_2D(X,Y,pressure_field,positions,method,theta,directivity,show_plots,directivity_only,directivity_distance,directivity_plot_alone,pressure_limits):

    if show_plots and not directivity_only:
        # Defining the figure
        fig, ax = plt.subplots(2,2)
        fig.set_size_inches(8,8)

        # Plotting the real part
        c = ax[0,0].pcolormesh(X,Y,np.real(pressure_field),shading = "gouraud",cmap = "RdBu",vmin = pressure_limits[0],vmax = pressure_limits[1])
        ax[0,0].scatter(positions[:,0],positions[:,1],color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax[0,0].set_aspect('equal')
        ax[0,0].set_title("Real Part")
        ax[0,0].set_xlabel("X (m)")
        ax[0,0].set_ylabel("Y (m)")
        fig.colorbar(c,ax = ax[0,0],fraction=0.046, pad=0.04)

        # Plotting the imaginary part
        c = ax[1,0].pcolormesh(X,Y,np.imag(pressure_field),shading = "gouraud",cmap = "RdBu",vmin = pressure_limits[0],vmax = pressure_limits[1])
        ax[1,0].scatter(positions[:,0],positions[:,1],color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax[1,0].set_aspect('equal')
        ax[1,0].set_title("Imaginary Part")
        ax[1,0].set_xlabel("X (m)")
        ax[1,0].set_ylabel("Y (m)")
        fig.colorbar(c,ax = ax[1,0],fraction=0.046, pad=0.04)

        # Plotting the magnitude
        c = ax[0,1].pcolormesh(X,Y,np.abs(pressure_field),shading = "gouraud",cmap = "jet",vmin = 0,vmax = pressure_limits[1])
        ax[0,1].scatter(positions[:,0],positions[:,1],color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax[0,1].set_aspect('equal')
        ax[0,1].set_title("Pressure Magnitude")
        ax[0,1].set_xlabel("X (m)")
        ax[0,1].set_ylabel("Y (m)")
        fig.colorbar(c,ax = ax[0,1],fraction=0.046, pad=0.04)

        # Plotting the directivity
        ax[1,1].axis("off")
        ax = fig.add_subplot(224,projection = 'polar')
        c = ax.plot(theta,20*np.log10(directivity))
        ax.set_rmin(-40)
        ax.set_rticks([0,-10,-20,-30,-40])
        ax.set_aspect('equal')
        ax.set_title(str("Beam Pattern (dB) at {0} m".format(directivity_distance)))

        fig.show()

        
        if method == "Rayleigh":
            ax.set_thetamin(-90)
            ax.set_thetamax(90)
        
        fig.tight_layout(pad = 0.5)
        fig.show()
        
    if directivity_plot_alone:
        fig, ax = plt.subplots(1,2,subplot_kw={'projection': 'polar'})
        ax[0].plot(theta,directivity)
        ax[0].set_title("Normalized Directivity")
        
        ax[1].plot(theta,20*np.log10(directivity))
        ax[1].set_title("Beam Pattern (dB)")
        ax[1].set_rmin(-40)
        ax[1].set_rticks([0,-10,-20,-30,-40])
        
        fig.tight_layout()
        fig.set_size_inches(8,8)
        fig.show()

def plot_3D(X,Y,Z,pressure_field,positions,method,theta,directivity,show_plots,directivity_only,directivity_distance,directivity_plot_alone,pressure_limits):

    if show_plots and not directivity_only:
        # Defining the figure
        fig = plt.figure()
        fig.set_size_inches(8,8)

        # Adding opacity to the colormap
        cmap = plt.cm.RdBu_r
        my_RdBu = cmap(np.arange(cmap.N))
        my_RdBu[:,-1] = np.linspace(-1,1,cmap.N)
        my_RdBu[:,-1] = np.abs(my_RdBu[:,-1])
        my_RdBu = colors.ListedColormap(my_RdBu)

        cmap = plt.cm.jet
        my_jet = cmap(np.arange(cmap.N))
        my_jet[:,-1] = np.linspace(0,1,cmap.N)
        my_jet = colors.ListedColormap(my_jet)

        # Plotting the real part
        ax = fig.add_subplot(221,projection = '3d')
        c = ax.scatter(X,Y,Z,np.real(pressure_field), c = np.real(pressure_field),cmap = my_RdBu,vmin = pressure_limits[0],vmax = pressure_limits[1],edgecolors = None)
        ax.scatter(positions[:,0],positions[:,1],positions[:,2],color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax.set_aspect('auto')
        ax.set_title("Real Part")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        fig.colorbar(c,ax = ax,fraction=0.046, pad=0.04)

        # Plotting the imaginary part
        ax = fig.add_subplot(223,projection = '3d')
        c = ax.scatter(X,Y,Z,np.imag(pressure_field), c = np.imag(pressure_field),cmap = my_RdBu,vmin = pressure_limits[0],vmax = pressure_limits[1],edgecolors = None)
        ax.scatter(positions[:,0],positions[:,1],positions[:,2],color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax.set_aspect('auto')
        ax.set_title("Imaginary Part")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        fig.colorbar(c,ax = ax,fraction=0.046, pad=0.04)

        # Plotting the magnitude
        ax = fig.add_subplot(222,projection = '3d')
        c = ax.scatter(X,Y,Z,np.abs(pressure_field), c = np.abs(pressure_field),cmap = my_jet,vmin = 0,vmax = pressure_limits[1],edgecolors = None)
        ax.scatter(positions[:,0],positions[:,1],positions[:,2],color = "black",marker = "o",facecolors = "white",linewidth = 1.5,s = 10)
        ax.set_aspect('auto')
        ax.set_title("Magnitude")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        fig.colorbar(c,ax = ax,fraction=0.046, pad=0.04)

        # Plotting the directivity
        ax = fig.add_subplot(224,projection = 'polar')
        c = ax.plot(theta,20*np.log10(directivity))
        ax.set_rmin(-40)
        ax.set_rticks([0,-10,-20,-30,-40])
        ax.set_aspect('equal')
        ax.set_title(str("Beam Pattern (dB) at {0} m".format(directivity_distance)))

        fig.show()

        
        if method == "Rayleigh":
            ax.set_thetamin(-90)
            ax.set_thetamax(90)
        
        fig.tight_layout(pad = 0.5)
        fig.show()
        
    if directivity_plot_alone:
        fig, ax = plt.subplots(1,2,subplot_kw={'projection': 'polar'})
        ax[0].plot(theta,directivity)
        ax[0].set_title("Normalized Directivity")
        
        ax[1].plot(theta,20*np.log10(directivity))
        ax[1].set_title("Beam Pattern (dB)")
        ax[1].set_rmin(-40)
        ax[1].set_rticks([0,-10,-20,-30,-40])
        
        fig.tight_layout()
        fig.set_size_inches(8,8)
        fig.show()

"""
Creating a field
"""

def get_field(positions,frequencies,strengths,velocities,areas,phases,field_points,time,method):
    
    # Convert everything to a numpy array
    positions = np.asarray(positions)
    strengths = np.asarray(strengths)
    phases = np.asarray(phases)
    velocities = np.asarray(velocities)
    areas = np.asarray(areas)
    field_points = np.asarray(field_points)

    if np.size(positions[0]) == 2 and np.size(field_points[0]) == 1:
        new_points = np.zeros([len(field_points),2])
        for i in range(len(field_points)):
            new_points[i] = np.array([field_points[i],0.0])
        field_points = new_points

    if np.size(positions[0]) == 3 and np.size(field_points[0]) == 1:
        new_points = np.zeros([len(field_points),3])
        for i in range(len(field_points)):
            new_points[i] = np.array([field_points[i],0.0,0.0])
        field_points = new_points

    if np.size(positions[0]) == 3 and np.size(field_points[0]) == 2:
        new_points = np.zeros([len(field_points),3])
        for i in range(len(field_points)):
            new_points[i] = np.array([field_points[i,0],field_points[i,1],0.0])
        field_points = new_points

    # Initialize the responses
    responses = np.zeros([len(field_points),len(strengths)], dtype = complex)
    
    # Define constants
    c = 343 # Phase speed in air
    rho_0 = 1.2 # Density of air

    # Creating Early Mesh Grids. This creates some that only need to be created once
    # We need each column of the DISTANCES grid to equal the distance to each source
    DISTANCES = np.zeros([len(field_points),len(strengths)])
    FREQUENCIES = np.zeros([len(field_points),len(strengths)])
    PHASES = np.zeros([len(field_points),len(strengths)])
    STRENGTHS = np.zeros([len(field_points),len(strengths)])
    AREAS = np.zeros([len(field_points),len(strengths)])
    VELOCITIES = np.zeros([len(field_points),len(strengths)])

    for i in range(np.size(strengths)):
        DISTANCES[:,i] = la.norm(field_points - positions[i,:],axis = 1)
        FREQUENCIES[:,i] = np.ones(len(field_points)) * frequencies[i]
        PHASES[:,i] = np.ones(len(field_points)) * phases[i]
        STRENGTHS[:,i] = np.ones(len(field_points)) * strengths[i]
        AREAS[:,i] = np.ones(len(field_points)) * areas[i]
        VELOCITIES[:,i] = np.ones(len(field_points)) * velocities[i]

    omegas = 2 * np.pi * FREQUENCIES
    k = omegas/c
    A = 1j*rho_0*c*k/(4*np.pi) * STRENGTHS

    for i in range(len(strengths)):

        if method == "Monopole Addition":
            responses = responses + A * np.exp(-1j*k*DISTANCES)/DISTANCES * np.exp(1j * PHASES) * np.exp(1j*omegas*time)
        elif method == "Rayleigh":
            responses = responses + (1j * omegas * rho_0 / (2 * np.pi) * 
                                VELOCITIES * 
                                np.exp(-1j * k * DISTANCES)/DISTANCES * 
                                np.exp(1j*PHASES) * np.exp(1j*omegas*time) * 
                                AREAS)

    # Each column represents the contribution to a point by a particular source. We must sum them up at each point
    responses = np.sum(responses,axis = 1)
            
    return responses

"""
Define an arc for whatever reasons you may want to do so
"""
def define_arc(radius,numPoints,theta_lims = (0,360), dimensions = 2):
    theta_min = theta_lims[0] * np.pi/180
    theta_max = theta_lims[1] * np.pi/180
    theta = np.linspace(theta_min,theta_max,numPoints)
    
    points = np.empty([0,dimensions])
    
    for i in range(0,numPoints):
        points = np.append(points,radius * np.array([[np.cos(theta[i]), np.sin(theta[i])]]),axis = 0)
        
    return points, theta