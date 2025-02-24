import solara
import os
import re
import nglview as nv
import uvicorn
import threading
from typing import Dict

# Define the JupyterHub proxy base URL
jupyterhub_service_prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "")
base_url = f"{jupyterhub_service_prefix}proxy/8000/assets/"

# Define the assets folder where HTML files are stored
assets_folder = "/home/jovyan/work/dashboard/assets"
os.makedirs(assets_folder, exist_ok=True)

# Regex pattern to extract SMILES from HTML files
SMILES_PATTERN = re.compile(r'<div class="smiles-entry">([^<]+)</div>', re.IGNORECASE)

# Function to extract SMILES mapping from HTML files
def extract_smiles_mapping() -> Dict[str, str]:
    smiles_to_file = {}
    for file_name in os.listdir(assets_folder):
        file_path = os.path.join(assets_folder, file_name)
        if file_name.endswith(".html") and os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    matches = SMILES_PATTERN.findall(content)  # Extract SMILES matches
                    if matches:
                        smiles = matches[0].strip()  # Get the first SMILES found
                        smiles_to_file[smiles] = file_name  # Store file name, not full path
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
    return smiles_to_file

@solara.component
def Page():
    """Solara UI Page - Dropdown for selecting a SMILES to open its corresponding HTML file"""
    
    # Introduction text displayed at the top of the page
    solara.Markdown(
        """
        ## Virtual Screening Docking Poses
        These docking poses are generated using **DiffDock** within the Virtual Screening workflow.
        The compounds are from the **NIH Protease Inhibitory Library**, and the docking was performed
        against the **TDP-43 protein structure**, which was predicted by **OpenFold**.
        
        Select a SMILES below to view its corresponding docking visualization.
        """
    )

    smiles_mapping = extract_smiles_mapping()
    smiles_options = list(smiles_mapping.keys())

    # Ensure there are available options
    if not smiles_options:
        solara.Text("No HTML files with SMILES found in the assets folder.")
        return

    # Reactive state for selected SMILES and file URL
    selected_smiles, set_selected_smiles = solara.use_state(smiles_options[0])
    selected_file_url, set_selected_file_url = solara.use_state(base_url + smiles_mapping[selected_smiles])

    def on_smiles_change(value):
        """Updates the selected SMILES and file URL dynamically."""
        if value in smiles_mapping:
            set_selected_smiles(value)  # Update selected SMILES
            set_selected_file_url(base_url + smiles_mapping[value])  # Update file URL

    with solara.Card(title="SMILES Selection", subtitle="Select a SMILES to view its HTML file"):
        # Dropdown list for SMILES selection
        solara.Select(
            label="Select SMILES",
            values=smiles_options,
            value=selected_smiles,
            on_value=on_smiles_change
        )

        # Reactive block to update the button dynamically
        solara.Button(
            label=f"Open {selected_smiles}",
            icon_name="mdi-file-document",
            attributes={"href": selected_file_url, "target": "_blank"},
            text=True,
            outlined=True
        )
