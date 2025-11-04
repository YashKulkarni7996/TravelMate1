import bz2
import xml.etree.ElementTree as ET
import wikitextparser as wtp
import os
import re

DUMP_FILE = "enwikivoyage-latest-pages-articles-multistream.xml.bz2"
OUTPUT_DIR = "KNOWLEDGE_BASE"
ARTICLE_COUNT = 0
ERROR_COUNT = 0

# --- Helper function to create safe filenames ---
def clean_filename(title):
    if title.startswith("Wikivoyage:"):
        title = title[len("Wikivoyage:"):]
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = title.replace(" ", "_")
    return title[:100]

# --- Create the output directory ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Created directory: {OUTPUT_DIR}")

print(f"Starting extraction from {DUMP_FILE}... This will take 5-10 minutes.")

# --- We will stream the file to save memory ---
# 1. Open the BZ2 file in text mode
with bz2.open(DUMP_FILE, "rt", encoding="utf-8") as bz2_file:
    
    # 2. Use iterparse to stream the XML
    # This reads the file bit by bit, not all at once
    in_page = False
    current_title = ""
    current_text = ""
    
    for event, elem in ET.iterparse(bz2_file, events=('start', 'end')):
        
        # Get the tag name without the long namespace
        tag = elem.tag.split('}')[-1]

        # --- At the start of a <page> tag ---
        if event == 'start' and tag == 'page':
            in_page = True
            current_title = ""
            current_text = ""
        
        # --- While inside a <page> tag ---
        if in_page:
            if event == 'end' and tag == 'title':
                current_title = elem.text
            
            if event == 'end' and tag == 'text':
                current_text = elem.text

            # --- At the end of a </page> tag ---
            if event == 'end' and tag == 'page':
                try:
                    # Make sure we have valid data and it's a real article
                    if current_title and current_text and not (
                        current_title.startswith("Template:") or
                        current_title.startswith("File:") or
                        current_title.startswith("User:") or
                        current_title.startswith("Wikivoyage:")
                    ):
                        
                        # 3. This is the magic: parse the wikitext
                        parsed = wtp.parse(current_text)
                        
                        # 4. Get the clean, plain text
                        clean_text = parsed.plain_text()
                        
                        # 5. Save the file
                        safe_title = clean_filename(current_title)
                        if safe_title and clean_text:
                            output_path = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
                            with open(output_path, 'w', encoding='utf-8') as out_f:
                                out_f.write(clean_text)
                            ARTICLE_COUNT += 1

                except Exception as e:
                    ERROR_COUNT += 1
                
                # Reset for the next page
                in_page = False
                
        # Clear the element from memory
        if event == 'end':
            elem.clear()

print("\n--- EXTRACTION COMPLETE ---")
print(f"Successfully created: {ARTICLE_COUNT} .txt files.")
print(f"Skipped due to errors: {ERROR_COUNT} files.")

# --- Verify the result ---
print("\n--- Here are some files from your new Knowledge Base: ---")