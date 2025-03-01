# **mm-dashboards (v0.1.0)**
<p align="center">
    <img src="https://img.shields.io/pypi/dm/rxiv-types?style=flat-square" />
    <img src="https://img.shields.io/pypi/l/rxiv-types?style=flat-square"/>
    <img src="https://img.shields.io/pypi/v/rxiv-types?style=flat-square"/>
</p>

---

## **Introduction**  

This project utilizes **Solara** to create dashboards for **MM workflows**. While we initially used **NGLView** for dynamic visualizations, Solara's rendering capabilities are **limited to static content** and basic HTML/JS embedding. It lacks native support for **complex interactive JavaScript frameworks** like **NGLView** or **Mol***.  

To address this limitation, we integrated **FastAPI** to serve **NGLView-generated HTML files**, allowing us to seamlessly embed **dynamic visualizations** within the dashboard.

---

## **Installation**  

### **Install Required Packages**  
```bash
conda env create -f environment.yml
conda activate dashboard
```

---

## **Usage**  

### **Start the FastAPI Server**  
You need to first **run `server.py`** to serve the HTML files using **FastAPI**:  
```bash
uvicorn server:app --reload
```

### **Run the Dashboard**  
Once the server is running, start the **Solara dashboard**:  
```bash
SOLARA_ROOT_PATH=${JUPYTERHUB_SERVICE_PREFIX}/proxy/8765 solara run dashboard.py
```

---

## **Notes**  
- **FastAPI is used** to serve dynamic visualization files.  
- **Solara is used** for rendering the dashboard interface.  
- **Ensure all dependencies are installed** before running the dashboard.  

---



