import pandas as pd
from typing import Tuple, List, Dict

def load_csv_as_documents(csv_path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Reads the CSV file with robust encoding handling and better error messages
    """
    # Try these encodings in order
    encodings = ['cp1252', 'utf-8-sig', 'utf-8', 'latin1', 'iso-8859-1']
    errors = []
    
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=encoding, on_bad_lines='warn')
            print(f"Successfully loaded CSV with encoding: {encoding}")
            
            texts = []
            metadatas = []
            
            # Process each row with error handling
            for idx, row in df.iterrows():
                try:
                    # Clean and convert values
                    cleaned_row = {
                        k: str(v).strip() if pd.notna(v) else ""
                        for k, v in row.items()
                    }
                    
                    # Create content string
                    content = " ".join(
                        f"{col}: {val}" for col, val in cleaned_row.items() if val
                    )
                    
                    texts.append(content)
                    metadatas.append({
                        "source": csv_path,
                        "row": idx,
                        "company": cleaned_row.get("Virgin Company", "")
                    })
                    
                except Exception as e:
                    print(f"Warning: Skipping row {idx} due to error: {str(e)}")
                    continue
            
            return texts, metadatas
            
        except Exception as e:
            errors.append(f"{encoding}: {str(e)}")
            continue
    
    # If we get here, all encodings failed
    error_msg = "\n".join(errors)
    raise ValueError(f"Failed to read CSV with any encoding:\n{error_msg}")