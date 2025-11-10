import os
import json
import psycopg2
from psycopg2.extras import Json

# Database connection parameters - update these with your actual database credentials
DB_PARAMS = {
    'dbname': 'postgres',  # replace with your database name
    'user': 'devangkankaria',     # replace with your password
    'host': 'localhost',
    'port': '5432'
}

def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def process_json_files(folder_path):
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()
    processed = 0
    errors = 0

    try:
        # Get list of all JSON files in the directory
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json') and f != 'README.txt']
        total_files = len(json_files)
        print(f"Found {total_files} JSON files to process")

        for i, filename in enumerate(json_files, 1):
            file_path = os.path.join(folder_path, filename)
            file_id = os.path.splitext(filename)[0]  # Use filename without extension as ID
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # Insert into database
                cursor.execute(
                    "INSERT INTO public.odiwc2023 (id, metadata) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                    (file_id, Json(json_data))
                )
                
                processed += 1
                if i % 10 == 0 or i == total_files:
                    print(f"Processed {i}/{total_files} files...")
                    
            except json.JSONDecodeError as je:
                print(f"Error decoding JSON in {filename}: {je}")
                errors += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                errors += 1
                
        conn.commit()
        print(f"\nProcessing complete!")
        print(f"Successfully processed: {processed}")
        print(f"Files with errors: {errors}")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_folder = os.path.join(script_dir, "odis_male_json")
    
    if not os.path.exists(json_folder):
        print(f"Error: Directory not found: {json_folder}")
    else:
        process_json_files(json_folder)
