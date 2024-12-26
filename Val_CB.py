import os

def extract_val_cb_coordinates(file_path):
    # Extract VAL CB Cartesian coordinates from the PDB file
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        val_cb_lines = [line for line in lines if line.startswith(('ATOM', 'HETATM')) and ' VAL ' in line and ' CB ' in line]

        # Generate the output file name
        output_file_path = f"{os.path.splitext(file_path)[0]}_val_cb_coordinates.txt"

        # Write the VAL CB Cartesian coordinates to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.writelines(val_cb_lines)

        print(f"Valine CB coordinates have been saved to {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to process all .pdb files in a folder
def process_folder_for_val_cb(folder_path):
    try:
        # List all files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                extract_val_cb_coordinates(file_path)
    except Exception as e:
        print(f"An error occurred while processing the folder: {e}")

# Example usage
# Replace 'your_folder_path' with the path to your folder containing .pdb files
folder_path = './Documents/edited pdb/'
process_folder_for_val_cb(folder_path)