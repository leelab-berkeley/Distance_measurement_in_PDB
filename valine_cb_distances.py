import os
import math

def parse_pdb(file_path):
    """
    Parse the PDB file and extract coordinates of CB atoms of valine residues.
    """
    valine_cb_coords = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                atom_name = line[12:16].strip()
                res_name = line[17:20].strip()
                chain_id = line[21].strip()
                res_seq = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())

                # Check for CB atom in valine residues
                if res_name == 'VAL' and atom_name == 'CB':
                    valine_cb_coords.append(((chain_id, res_seq), (x, y, z)))

    return valine_cb_coords

def calculate_distances(valine_cb_coords):
    """
    Calculate all pairwise distances between CB atoms of valine residues.
    """
    distances = []
    for i, (id1, coord1) in enumerate(valine_cb_coords):
        for j, (id2, coord2) in enumerate(valine_cb_coords):
            if i < j:  # Avoid double counting and self-distance
                dist = math.sqrt(
                    (coord1[0] - coord2[0]) ** 2 +
                    (coord1[1] - coord2[1]) ** 2 +
                    (coord1[2] - coord2[2]) ** 2
                )
                distances.append(((id1, id2), dist))
    return distances

def save_distances_to_file(output_file, distances):
    """
    Save the calculated distances to a text file.
    """
    with open(output_file, 'w') as file:
        file.write("Pairwise distances between CB atoms of valine residues:\n\n")
        for ((id1, id2), dist) in distances:
            file.write(f"Residue {id1} - Residue {id2}: {dist:.3f}\n")

def main():
    input_file = input("Enter the path to the PDB file: ").strip()

    if not os.path.exists(input_file):
        print("Error: File does not exist.")
        return

    # Extract file name without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = base_name + "_valine_CB_distances.txt"

    # Parse PDB file and calculate distances
    valine_cb_coords = parse_pdb(input_file)
    distances = calculate_distances(valine_cb_coords)

    # Save distances to output file
    save_distances_to_file(output_file, distances)

    print(f"Distances have been saved to {output_file}")

if __name__ == "__main__":
    main()
