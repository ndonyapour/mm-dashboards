import solara
import os
import nglview as nv
import pytraj as pt
import numpy as np
import re

def extract_rank_from_filename(filename):
    """Extracts the rank number from the filename for labeling."""
    match = re.search(r'rank(\d+)', filename)
    if match:
        return f"Rank {match.group(1)}"
    return ""

def make_view(base_dir, pdb_file, sdf_files):
    """Generates an NGLView visualization combining a protein and multiple ligands."""
    pdb_file_path = os.path.join(base_dir, pdb_file)
    if not os.path.exists(pdb_file_path):
        print(f"Protein file not found: {pdb_file_path}")
        return None
    
    traj = pt.load(pdb_file_path)
    view = nv.show_pytraj(traj)
    view.add_representation('cartoon', selection='protein', color='blue')

    for sdf_file in sdf_files:
        sdf_file_path = os.path.join(base_dir, sdf_file)
        if os.path.exists(sdf_file_path):
            ligand_traj = pt.load(sdf_file_path)
            view.add_trajectory(ligand_traj)
            centroid = np.mean(ligand_traj.xyz[0], axis=0) + np.array([0.5, 0.5, 0.5])
            label = extract_rank_from_filename(sdf_file_path)
            view.shape.add_label(centroid.tolist(), [0, 0, 0], 5, label)
            print(f"Ligand {label} loaded.")
        else:
            print(f"Ligand file not found: {sdf_file}")

    view.center()
    view.control.zoom(0.2)
    return view

# Define the JupyterHub proxy base URL
jupyterhub_service_prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "")
base_url  = f"{jupyterhub_service_prefix}/proxy/8000/assets/" 

# Define the assets folder where HTML files are stored
assets_folder = "/home/jovyan/work/dashboard/assets"
os.makedirs(assets_folder, exist_ok=True)

# NGLView HTML File
html_file_name = "nglview_demo.html"
html_file_path = os.path.join(assets_folder, html_file_name)

# ------------------ GENERATE NGLVIEW HTML ------------------
# Generate NGLView visualization and save as HTML
demo_view = make_view('./data',"protein_fix_amides.pdb", ["rank1_confidence-1.77.sdf", "rank1_confidence-0.05.sdf"])
if demo_view:
    nv.write_html(html_file_path, [demo_view])

# ------------------ SOLARA COMPONENT ------------------
@solara.component
def Page():
    """Solara UI Page"""
    try:
        # List all files in the assets folder
        asset_files = [
            file for file in os.listdir(assets_folder) if os.path.isfile(os.path.join(assets_folder, file))
        ]
    except FileNotFoundError:
        asset_files = []  # If folder doesn't exist, return an empty list

    # UI Layout
    with solara.Card(title="Assets", subtitle="Click on a file to open it"):
        # Add a button for the NGLView demo HTML file explicitly
        if html_file_name in asset_files:
            file_url = base_url + html_file_name
            solara.Button(
                label="Open NGLView Demo",
                icon_name="mdi-file-document",
                attributes={"href": file_url, "target": "_blank"},
                text=True,
                outlined=True
            )

        # Add buttons for all other files in the assets folder
        for file_name in asset_files:
            if file_name != html_file_name:  # Skip the NGLView demo file (already added)
                file_url = base_url + file_name
                solara.Button(
                    label=f"Open {file_name}",
                    icon_name="mdi-file-document",
                    attributes={"href": file_url, "target": "_blank"},
                    text=True,
                    outlined=True
                )
