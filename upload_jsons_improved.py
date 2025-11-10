import os
import json
import psycopg2
from psycopg2.extras import Json
import time

# Database connection parameters - update these with your actual database credentials
DB_PARAMS = {
    'dbname': 'postgres',
    'user': 'devangkankaria',
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

def process_json_files(folder_path, batch_size=20):
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()
    processed = 0
    errors = 0
    batch_count = 0
    error_log = []

    try:
        # Get list of all JSON files in the directory
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json') and f != 'README.txt']
        total_files = len(json_files)
        print(f"Found {total_files} JSON files to process")

        for i, filename in enumerate(json_files, 1):
            file_path = os.path.join(folder_path, filename)
            file_id = os.path.splitext(filename)[0]  # Use filename without extension as ID
            
            try:
                # Read and validate JSON
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                except json.JSONDecodeError as je:
                    error_msg = f"Invalid JSON in {filename}: {je}"
                    print(f"\n{error_msg}")
                    error_log.append(error_msg)
                    errors += 1
                    continue
                
                # Process each file in its own transaction
                try:
                    cursor.execute(
                        """
                        INSERT INTO "odiwc2023" (id, metadata) 
                        VALUES (%s, %s) 
                        ON CONFLICT (id) DO NOTHING
                        """,
                        (file_id, Json(json_data))
                    )
                    processed += 1
                    batch_count += 1
                    
                    # Commit after each batch
                    if batch_count >= batch_size:
                        conn.commit()
                        print(f"Committed batch of {batch_count} files. Processed {i}/{total_files} files...")
                        batch_count = 0
                        time.sleep(0.1)  # Small delay to prevent overwhelming the database
                        
                except psycopg2.Error as pe:
                    error_msg = f"Database error with {filename}: {pe}"
                    print(f"\n{error_msg}")
                    error_log.append(error_msg)
                    conn.rollback()
                    errors += 1
                    
                    # Reconnect if connection was lost
                    try:
                        conn = connect_to_db()
                        if conn:
                            cursor = conn.cursor()
                        else:
                            print("Failed to reconnect to database. Exiting...")
                            break
                    except Exception as e:
                        print(f"Error reconnecting to database: {e}")
                        break
                    
            except Exception as e:
                error_msg = f"Unexpected error processing {filename}: {e}"
                print(f"\n{error_msg}")
                error_log.append(error_msg)
                errors += 1
                continue
                
            # Progress update
            if i % 10 == 0 or i == total_files:
                print(f"Progress: {i}/{total_files} files processed (Success: {processed}, Errors: {errors})", end='\r')
        
        # Final commit for any remaining files
        if batch_count > 0:
            conn.commit()
            print(f"\nCommitted final batch of {batch_count} files.")
            
        # Write errors to a log file
        if error_log:
            with open('error_log.txt', 'w') as f:
                f.write("\n".join(error_log))
            print(f"\nWrote {len(error_log)} errors to error_log.txt")
            
        print("\n" + "="*50)
        print(f"Processing complete!")
        print(f"Total files processed: {processed}")
        print(f"Files with errors: {errors}")
        if errors > 0:
            print(f"Check error_log.txt for details")
        print("="*50)

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Committing processed files...")
        if batch_count > 0:
            conn.commit()
            print(f"Committed {batch_count} files from the current batch.")
        print(f"Successfully processed {processed} files before interruption.")
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_folder = os.path.join(script_dir, "odis_male_json")
    
    if not os.path.exists(json_folder):
        print(f"Error: Directory not found: {json_folder}")
    else:
        print("Starting JSON processing...")
        print("Press Ctrl+C to stop processing and save progress")
        print("-" * 50)
        process_json_files(json_folder)
