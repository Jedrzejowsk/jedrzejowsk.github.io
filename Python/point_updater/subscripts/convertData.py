# This subscript was created by G. Jedrzejowski
# It takes a CSV input and converts it into the data structure compatible with makeJSON.write_json function

import csv
import re


def convert_csv_to_data(csv_path):
    data = []
    
    # Starting states
    current_gender = "male"
    current_field = "static"
    current_element = ""
    current_type = "" 
    active_grips = [] 
    
    field_map = {
        "STATIC": "static",
        "STRENGTH DYNAMICS": "strength dynamics",
        "ACROBATIC DYNAMICS": "acrobatic dynamics"
    }

    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            # 1. Prepare search strings
            row_str = " ".join(row).upper()
            # search_text is for finding GENDER and FIELD keywords
            search_text = re.sub(r'[^A-Z ]', '', row_str)
            
            clean_row = [cell.strip() for cell in row if cell.strip()]
            if not clean_row:
                continue
                
            first_cell = clean_row[0]
            # check_text removes superscripts and symbols to verify if a word is UPPERCASE
            check_text = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰*]', '', first_cell).strip()

            # 2. GENDER & FIELD DETECTION
            if "WOMEN" in search_text or ("MEN" in search_text and ("STATIC" in search_text or "DYNAMIC" in search_text)):
                if "WOMEN" in search_text:
                    current_gender = "female"
                else:
                    current_gender = "male"
                
                for key in field_map:
                    if key in search_text:
                        current_field = field_map[key]
                continue

            # 3. ELEMENT DETECTION (e.g., RINGS MALTESE¹, PLANCHE)
            # Must be a single-item row and, once cleaned of indices, be all UPPERCASE
            elif len(clean_row) == 1 and check_text.isupper():
                current_element = check_text.lower()
                current_type = "" # Reset type for new element
                continue

            # 4. TYPE DETECTION (e.g., Standard, Wide 45°)
            # Single-item row that is NOT all uppercase and NOT the word "Element"
            elif len(clean_row) == 1 and not check_text.isupper() and check_text.lower() != "element":
                current_type = check_text.lower()
                continue

            # 5. DYNAMIC GRIP MAPPING (The 'Element, Cat...' label row)
            elif check_text.lower() == "element":
                # Captures PB, BS, or P-BARS, BAR, etc. from column 3 onwards
                active_grips = [g.strip() for g in clean_row[2:] if g]
                continue

            # 6. DATA ROW PROCESSING
            elif len(clean_row) >= 2:
                variation = first_cell.lower().strip()
                category = clean_row[1].strip()
                
                # Check if this row is actually a label row that slipped through
                if variation == "element":
                    continue

                points_list = []
                for i, grip in enumerate(active_grips):
                    col_index = i + 2
                    if col_index < len(row):
                        val = row[col_index].strip()
                        if val and val not in ['-', '', ' ']:
                            points_list.append({
                                "grip": grip,
                                "points": val
                            })
                
                # Only add if the row actually contains point values
                if points_list:
                    data.append({
                        "field": current_field,
                        "gender": current_gender,
                        "element": current_element,
                        "type": current_type,
                        "variation": variation,
                        "category": category,
                        "points": points_list
                    })

    # Summary report
    male_count = len([d for d in data if d['gender'] == 'male'])
    female_count = len([d for d in data if d['gender'] == 'female'])
    print(f"Success: Processed {male_count} male and {female_count} female entries.")
    
    return data