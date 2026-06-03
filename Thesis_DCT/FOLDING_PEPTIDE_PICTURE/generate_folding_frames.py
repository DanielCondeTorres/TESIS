import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_frames(output_dir, num_frames=240):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Configuration parameters
    N = 15  # Number of residues (beads)
    np.random.seed(42)  # For reproducibility of the random coil state
    
    # 2. Define the Alpha-Helix structure (t = 1)
    # The helix lies horizontally along the Y-axis (membrane surface parallel)
    # This represents an amphipathic peptide lying flat at the interface
    omega = 100 * np.pi / 180.0  # 100 degrees per residue
    R = 2.3  # Radius of alpha helix in Angstroms
    h = 1.5  # Rise per residue in Angstroms
    
    helix_coords = np.zeros((N, 3))
    for i in range(N):
        # Helix axis is the Y-axis. X and Z wind around it.
        # As beads wind, their Z coordinate oscillates between +R and -R
        # representing the amphipathic partition (some beads above, some below the plane)
        helix_coords[i] = [R * np.cos(i * omega), (i - (N - 1) / 2.0) * h, R * np.sin(i * omega)]
    
    # 3. Define the Random Coil structure (t = 0)
    # We generate this as a random walk of N steps with step size around 3.8 Angstroms
    coil_coords = np.zeros((N, 3))
    for i in range(1, N):
        step = np.random.normal(size=3)
        step = step / np.linalg.norm(step) * 3.8
        coil_coords[i] = coil_coords[i-1] + step
    # Center the random coil at the origin
    coil_coords -= np.mean(coil_coords, axis=0)
    
    # 4. Color gradient along the peptide (USCBlue to Cyan/Teal)
    colors = []
    for i in range(N):
        t_color = i / (N - 1)
        r = 0.0
        g = 0.29 * (1 - t_color) + 0.75 * t_color
        b = 0.56 * (1 - t_color) + 0.63 * t_color
        colors.append((r, g, b))
        
    print(f"Generating {num_frames} frames in '{output_dir}'...")
    
    # Dynamically find the maximum span across all frames to minimize padding and zoom in tightly
    # We simulate the exact coordinates for the span calculation
    max_span = 0.0
    for f in range(1, num_frames + 1):
        t = (f - 1) / (num_frames - 1)
        if t <= 0.4:
            # Phase 1: Approach (t_1 from 0 to 1)
            t_1 = t / 0.4
            Z_shift = 9.0 * (1 - t_1)
            coords = coil_coords.copy()
            coords[:, 2] += Z_shift
        else:
            # Phase 2: Folding (t_2 from 0 to 1)
            t_2 = (t - 0.4) / 0.6
            coords = (1 - t_2) * coil_coords + t_2 * helix_coords
        max_span = max(max_span, np.max(np.abs(coords)))
    # Add a small buffer to avoid cropping beads (tight crop to maximize peptide size)
    limit = max_span + 0.65
    
    # Setup matplotlib figure
    fig = plt.figure(figsize=(6, 6))
    
    # We iterate and save each frame
    for f in range(1, num_frames + 1):
        # progress t from 0 (first page) to 1 (last page)
        t = (f - 1) / (num_frames - 1)
        
        # 5. Calculate coordinates based on the two phases
        if t <= 0.4:
            # Phase 1: Approach (from Z = +9 to Z = 0)
            t_1 = t / 0.4
            Z_shift = 9.0 * (1 - t_1)
            current_coords = coil_coords.copy()
            current_coords[:, 2] += Z_shift
        else:
            # Phase 2: Folding (from random coil to alpha-helix at Z = 0)
            t_2 = (t - 0.4) / 0.6
            current_coords = (1 - t_2) * coil_coords + t_2 * helix_coords
            
        # Clear previous frame and setup 3D plot
        fig.clf()
        ax = fig.add_subplot(111, projection='3d')
        
        # Set white background for seamless LaTeX integration
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        ax.set_axis_off()
        
        # 6. Draw the interface plane at Z=0 (translucent surface)
        # Represents the membrane surface. It spans from -limit to +limit in X and Y
        xx, yy = np.meshgrid(np.linspace(-limit, limit, 2), 
                             np.linspace(-limit, limit, 2))
        zz = np.zeros_like(xx)
        ax.plot_surface(xx, yy, zz, color='#9370DB', alpha=0.15, shade=False, zorder=1)
        
        # 7. Draw hydrogen bonds (i to i+4)
        # They will fade in as the peptide folds (only in Phase 2)
        max_dist = 9.0
        min_dist = 6.2
        for i in range(N - 4):
            p1 = current_coords[i]
            p2 = current_coords[i+4]
            dist = np.linalg.norm(p1 - p2)
            if dist < max_dist:
                # Opacity increases as distance gets closer to the helical hydrogen-bond distance
                alpha_h = (max_dist - dist) / (max_dist - min_dist)
                alpha_h = max(0.0, min(0.6, alpha_h))
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                        color='#FF6B6B', linestyle='--', linewidth=3.0, alpha=alpha_h, zorder=5)
        
        # 8. Draw the peptide backbone (covalent bonds)
        ax.plot(current_coords[:, 0], current_coords[:, 1], current_coords[:, 2],
                color='#2C3E50', linewidth=7.5, solid_capstyle='round', zorder=10)
        
        # 9. Draw the amino acid beads (Calpha atoms)
        # Using white outlines for a premium 3D look
        for i in range(N):
            ax.scatter([current_coords[i, 0]], [current_coords[i, 1]], [current_coords[i, 2]],
                       s=260, color=colors[i], edgecolor='white', linewidth=2.0, alpha=1.0, zorder=15)
            
        # 10. Set fixed limits to prevent scaling jumps and ensure stability
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        
        # 11. Set camera angle (smooth rotation + subtle nod)
        elev = 18 + 4 * np.sin(2 * np.pi * t)
        azim = 35 + 100 * t  # 100-degree rotation across the book
        ax.view_init(elev=elev, azim=azim)
        
        # Save frame
        file_path = os.path.join(output_dir, f"folding_{f}.png")
        plt.savefig(file_path, dpi=120, bbox_inches='tight', pad_inches=0, facecolor='white')
        
        # Print progress occasionally
        if f % 30 == 0 or f == num_frames:
            print(f"  Frame {f}/{num_frames} saved.")
            
    plt.close(fig)
    print("All frames generated successfully!")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    generate_frames(script_dir)
