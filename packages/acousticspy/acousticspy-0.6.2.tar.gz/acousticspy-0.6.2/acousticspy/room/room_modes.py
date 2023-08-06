import pandas as pd
import numpy as np

def calculate_room_modes(Lx, Ly, Lz, N, c = 340, search_mode = 'exhaustive'):
    
    if search_mode == 'fast':
        N_searched = int(np.sqrt(N))
    elif search_mode == 'exhaustive':
        N_searched = N
    else:
        print("Invalid Search Method")
    
    f = np.empty(0)
    NX = np.empty(0)
    NY = np.empty(0)
    NZ = np.empty(0)
    for nx in range(0,N_searched):
        
        for ny in range(0,N_searched):
            
            for nz in range(0,N_searched):
                
                f = np.append(f,c/2 * np.sqrt((nx/Lx)**2 + (ny/Ly)**2 + (nz/Lz)**2))
                NX = np.append(NX,nx)
                NY = np.append(NY,ny)
                NZ = np.append(NZ,nz)
                
    
    data = {'Frequency' : f, 'nx' : NX, 'ny' : NY, 'nz' : NZ}
    df = pd.DataFrame(data = data)
    df = df.sort_values('Frequency')

    df = df.reset_index(drop = True)
    
    df = df[0:N+1]
    
    return df