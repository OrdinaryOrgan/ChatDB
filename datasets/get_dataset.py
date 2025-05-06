import kagglehub

if __name__ == '__main__':
    # Download latest version
    path = kagglehub.dataset_download("artyomkruglov/gaming-profiles-2025-steam-playstation-xbox")
    print("Path of dataset files:", path)