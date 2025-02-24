import os
import solara
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

# Get the JupyterHub proxy prefix
jupyterhub_service_prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "")
root_path = f"{jupyterhub_service_prefix}/proxy/8000"  # Change port if needed

# Define the assets directory path on the server
ASSETS_DIR = "/home/jovyan/work/dashboard/assets"  # Change to your server path

# Ensure the directory exists
os.makedirs(ASSETS_DIR, exist_ok=True)

# Create FastAPI app with the correct root path for JupyterHub
app = FastAPI(root_path=root_path)

# Serve static HTML files from the `assets` folder
@app.get("/assets/{filename}", response_class=HTMLResponse)
async def serve_html_file(filename: str, request: Request):
    file_path = os.path.join(ASSETS_DIR, filename)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    else:
        return HTMLResponse(content="<h1>File Not Found</h1>", status_code=404)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": f"FastAPI is running on {root_path}"}

# Print the port at startup for debugging
#print(f"Starting FastAPI on port 8765 with root path: {root_path}")

# Run FastAPI server on the correct port
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
