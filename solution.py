"""
==============================================================
Day 10 Lab: Build Your First Automated ETL Pipeline
==============================================================
Student ID: AI20K-2A202600723  (<-- Thay XXXX bang ma so cua ban)
Name: Nguyen Thi Vang

Nhiem vu:
   1. Extract:   Doc du lieu tu file JSON
   2. Validate:  Kiem tra & loai bo du lieu khong hop le
   3. Transform: Chuan hoa category + tinh gia giam 10%
   4. Load:      Luu ket qua ra file CSV

Cham diem tu dong:
   - Script phai chay KHONG LOI (20d)
   - Validation: loai record gia <= 0, category rong (10d)
   - Transform: discounted_price + category Title Case (10d)
   - Logging: in so record processed/dropped (10d)
   - Timestamp: them cot processed_at (10d)
==============================================================
"""

import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'


def extract(file_path):
    """
    Task 1: Doc du lieu JSON tu file.

    Goi y:
       - Dung json.load() de doc file JSON
       - Xu ly truong hop file khong ton tai (FileNotFoundError)

    Returns:
        list: Danh sach cac records (dictionaries)
    """
    print(f"Extracting data from {file_path}...")

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully extracted {len(data)} records from {file_path}")
        return data
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {file_path}. Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during extraction: {e}")
        return None


def validate(data):
    """
    Task 2: Kiem tra chat luong du lieu.

    Quy tac validation:
       - Price phai > 0 (loai bo gia am hoac bang 0)
       - Category khong duoc rong

    Goi y:
       - Dung record.get('price', 0) de lay gia
       - Dung record.get('category') de kiem tra category
       - In ra so luong record hop le va khong hop le

    Returns:
        list: Danh sach cac records hop le
    """
    if not data:  # Check if data is empty (None or [])
        print("Warning: No data to validate.")
        return []
    
    valid_records = []
    error_count = 0
    for record in data:
        # Check if price is valid (greater than 0)
        price = record.get('price', 0)
        if price <= 0:
            error_count += 1
            continue  # Skip this record
        
        # Check if category is valid (not empty/None/whitespace)
        category = record.get('category')
        if not category or not str(category).strip():
            error_count += 1
            continue  # Skip this record
        
        valid_records.append(record)
    
    print(f"Validation complete: {len(valid_records)} processed, {error_count} dropped.")
    return valid_records


def transform(data):
    """
    Task 3: Ap dung business logic.

    Yeu cau:
       - Tinh discounted_price = price * 0.9 (giam 10%)
       - Chuan hoa category thanh Title Case (vi du: "electronics" -> "Electronics")
       - Them cot processed_at = timestamp hien tai

    Goi y:
       - Dung pd.DataFrame(data) de tao DataFrame
       - df['discounted_price'] = df['price'] * 0.9
       - df['category'] = df['category'].str.title()
       - df['processed_at'] = datetime.datetime.now().isoformat()

    Returns:
        pd.DataFrame: DataFrame da duoc transform
    """
    # TODO: Tao DataFrame va ap dung transformations
    if not data:  # Check if data is empty (None or [])
        print("Warning: No data to transform.")
        return None
    
    try:
        df = pd.DataFrame(data)
        
        # Check required columns exist
        required_cols = ['price', 'category', 'product']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"Error: Missing required columns in data: {missing_cols}")
            return None
        
        # 3.1: Apply discount (10% off)
        # Ensure price is numeric, coercing errors to NaN
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Drop rows where price couldn't be converted to numeric
        original_count = len(df)
        df = df.dropna(subset=['price'])
        dropped_numeric = original_count - len(df)
        
        if dropped_numeric > 0:
            print(f"Warning: Dropped {dropped_numeric} records due to non-numeric price values.")
        
        df['discounted_price'] = df['price'] * 0.9
        
        # 3.2: Standardize category (Title Case)
        df['category'] = df['category'].astype(str).str.title()
        
        # 3.3: Add processed_at timestamp
        df['processed_at'] = datetime.datetime.now().isoformat()
        
        print(f"Transformations applied. Resulting DataFrame has {len(df)} records.")
        return df
    except Exception as e:
        print(f"Error during transformation: {e}")
        return None


def load(df, output_path):
    """
    Task 4: Luu DataFrame ra file CSV.

    Goi y:
       - df.to_csv(output_path, index=False)
    """
    if df is None:
        print("Error: No DataFrame to load.")
        return
    
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving data to {output_path}: {e}")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None:
            load(final_df, OUTPUT_FILE)
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned None. Check your transform() function.")
    else:
        print("\nPipeline aborted: No data extracted.")
