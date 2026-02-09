import os
from huggingface_hub import HfApi, create_repo

# --- Configuration ---
# Get the Hugging Face token from the environment variables
hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN")
# Define the name of the new space
new_space_name = "todo_fullstack_app_backend"
# Get the username from the environment
username = os.environ.get("HF_USERNAME")

# --- Deletion of the old space (if it exists) ---
try:
    api = HfApi(token=hf_token)
    api.delete_repo(repo_id=f"{username}/{new_space_name}", repo_type="space")
    print(f"Space '{username}/{new_space_name}' deleted successfully.")
except Exception as e:
    print(f"Space '{username}/{new_space_name}' not found or could not be deleted. Continuing...")

# --- Creation of the new space ---
try:
    repo_url = api.create_repo(
        repo_id=f"{username}/{new_space_name}",
        repo_type="space",
        space_sdk="docker",
        space_hardware="cpu-basic",
        private=False,
    )
    print(f"Space '{repo_url}' created successfully.")
except Exception as e:
    print(f"Could not create space '{username}/{new_space_name}'. Error: {e}")
    exit()

# --- Uploading the backend code to the new space ---
try:
    api.upload_folder(
        folder_path="backend",
        repo_id=f"{username}/{new_space_name}",
        repo_type="space",
        path_in_repo=".",
    )
    print("Backend code uploaded successfully.")
except Exception as e:
    print(f"Could not upload backend code. Error: {e}")
    exit()

print("Deployment to Hugging Face Space completed.")
