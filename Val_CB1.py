import os
import matplotlib.pyplot as plt
from Bio.PDB import PDBParser
from scipy.spatial.distance import pdist
import numpy as np

# -----------------------------------------------------------------------------
# Specify the input folder containing PDB files and output folder
# -----------------------------------------------------------------------------
pdb_folder = "./Documents/edited pdb"  # Folder containing PDB files
output_folder = "./Documents/edited pdb/results/"  # Output folder for results
os.makedirs(output_folder, exist_ok=True)

# -----------------------------------------------------------------------------
# Parse and process each PDB file in the folder
# -----------------------------------------------------------------------------
parser = PDBParser(QUIET=True)

for pdb_filename in os.listdir(pdb_folder):
    if pdb_filename.endswith(".pdb"):  # Process only .pdb files
        pdb_path = os.path.join(pdb_folder, pdb_filename)
        output_base_name = os.path.splitext(pdb_filename)[0]

        # Output files
        output_distance_data = os.path.join(output_folder, f"{output_base_name}_distances.txt")
        output_histogram_image = os.path.join(output_folder, f"{output_base_name}_histogram.jpeg")

        print(f"Processing file: {pdb_path}")
        
        # -----------------------------------------------------------------------------
        # Parse the PDB file
        # -----------------------------------------------------------------------------
        try:
            structure = parser.get_structure(output_base_name, pdb_path)
        except Exception as e:
            print(f"Error parsing {pdb_path}: {e}")
            continue

        # -----------------------------------------------------------------------------
        # Extract coordinates of Valine CB atoms
        # -----------------------------------------------------------------------------
        valine_cb_coords = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    if residue.get_resname() == "VAL":
                        if "CB" in residue:
                            valine_cb_coords.append(residue["CB"].coord)

        if len(valine_cb_coords) < 2:
            print(f"Not enough Valine CB atoms in {pdb_path} to calculate pairwise distances.")
            continue

        # -----------------------------------------------------------------------------
        # Calculate pairwise distances
        # -----------------------------------------------------------------------------
        pairwise_distances = pdist(valine_cb_coords)

        # -----------------------------------------------------------------------------
        # Save all distances to a text file
        # -----------------------------------------------------------------------------
        print(f"Saving all pairwise distances to: {output_distance_data}")
        with open(output_distance_data, "w") as f:
            f.write("# Pairwise distances between all Valine CB atoms (in Å)\n")
            for dist in pairwise_distances:
                f.write(f"{dist:.4f}\n")

        # -----------------------------------------------------------------------------
        # Create and save the histogram plot
        # -----------------------------------------------------------------------------
        print(f"Creating histogram and saving figure to: {output_histogram_image}")
        plt.figure(figsize=(8, 6))
        plt.hist(pairwise_distances, bins=30, color="blue", alpha=0.7, edgecolor="black")
        plt.title(f"Histogram of Distances: {output_base_name}")
        plt.xlabel("Distance (Å)")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig(output_histogram_image, format="jpeg")
        plt.close()

print("All files processed successfully!")
