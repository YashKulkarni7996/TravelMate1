import os

KNOWLEDGE_BASE_DIR = "KNOWLEDGE_BASE"
deleted_count = 0
kept_count = 0

print(f"Starting cleanup of {KNOWLEDGE_BASE_DIR}...")

for filename in os.listdir(KNOWLEDGE_BASE_DIR):
    file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
    
    # Check if it's a file
    if not os.path.isfile(file_path):
        continue
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(100).strip() # Read first 100 chars
            
        # If the file starts with #REDIRECT, delete it
        if content.upper().startswith("#REDIRECT"):
            os.remove(file_path)
            deleted_count += 1
        else:
            kept_count += 1
            
    except Exception as e:
        print(f"Could not read {filename}, skipping: {e}")

print("\n--- Cleanup Complete ---")
print(f"Deleted: {deleted_count} redirect files.")
print(f"Kept:    {kept_count} valid article files.")