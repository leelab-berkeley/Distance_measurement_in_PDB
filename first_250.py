import os

# Define the input and output directories
input_folder = "./Documents/"
output_folder = "./Documents/"
input_pdb_file = os.path.join(input_folder, "test.pdb")  # Input file
output_pdb_file = os.path.join(output_folder, "test_first_250_amino_acids.pdb")  # Output file

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Read the PDB file and extract the first 250 amino acids
amino_acid_lines = []
current_residue_id = None
residue_count = 0

with open(input_pdb_file, 'r') as pdb_file:
    for line in pdb_file:
        if line.startswith("ATOM"):
            # Extract residue ID (chain ID + residue sequence number)
            chain_id = line[21]
            residue_id = line[22:26].strip()
            unique_residue_id = f"{chain_id}:{residue_id}"

            if unique_residue_id != current_residue_id:
                current_residue_id = unique_residue_id
                residue_count += 1

            # Stop after collecting 250 amino acids
            if residue_count > 250:
                break

            # Append lines belonging to the current amino acid
            amino_acid_lines.append(line)

# Save the first 250 amino acids to a new PDB file
with open(output_pdb_file, 'w') as output_file:
    output_file.writelines(amino_acid_lines)

print(f"First 250 amino acids saved to {output_pdb_file}")
