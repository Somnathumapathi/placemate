import os
import glob
import pandas as pd

def is_person_shortlisted(directory):
    """
    Searches for Excel files in the given directory and checks if hardcoded
    person data exists in any of them.

    Args:
        directory (str): Path to the directory containing Excel files.

    Returns:
        dict: Results for each person showing if they are shortlisted.
    """
    # Hardcoded test data
    test_persons = [
        {
            'name': 'Thendral Kabilan',
            'usn': '1DS22CB057',
            'email': 'thendral22.kabilan@example.com'
        },
        {
            'name': 'Somnath U', 
            'usn': '1DS22CS215',
            'email': 'somnathumapathi7@example.com'
        }
    ]
    
    results = {}
    
    # Search for Excel files
    patterns = ['*.xlsx', '*.xls']
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(directory, pattern), recursive=False))

    for person in test_persons:
        person_found = False
        
        for file in files:
            try:
                # Read all sheets in the Excel file
                xls = pd.ExcelFile(file)
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    
                    # Search in all string columns
                    for col in df.select_dtypes(include='object').columns:
                        # Check for name, USN, or email
                        if (df[col].astype(str).str.lower().str.contains(person['name'].lower(), na=False).any() or
                            df[col].astype(str).str.lower().str.contains(person['usn'].lower(), na=False).any() or
                            df[col].astype(str).str.lower().str.contains(person['email'].lower(), na=False).any()):
                            person_found = True
                            break
                    
                    if person_found:
                        break
                        
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue
            
            if person_found:
                break
        
        results[person['name']] = person_found
    
    return results

