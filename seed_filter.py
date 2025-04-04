import pandas as pd
import os
import shutil

# === Configuration ===

# Excel file listing metadata filenames (1 column: 'filename')
metadata_file_list = "metadata_file_list.xlsx"

# Folder where all metadata Excel files are stored
metadata_folder = "/scratch/vg1u23/test/metadataperstudy"

# Folder where all PRJ* subfolders with FASTQ files are stored
seq_folder = "/scratch/vg1u23/test"

# Base output directory (each study gets its own subfolder here)
base_output_folder = "/scratch/vg1u23/test/filtered_by_study"
os.makedirs(base_output_folder, exist_ok=True)

# === Load the metadata file list ===

metadata_list = pd.read_excel(metadata_file_list)

# === Loop through each metadata file ===

for metadata_filename in metadata_list["filename"]:
    print(f"\n📄 Processing metadata file: {metadata_filename}")
    
    # Extract study name (e.g., PRJCA008115)
    study_folder = metadata_filename.split("_with_family")[0]
    
    # Build paths
    study_seq_folder = os.path.join(seq_folder, study_folder)
    metadata_path = os.path.join(metadata_folder, metadata_filename)
    study_output_folder = os.path.join(base_output_folder, study_folder)
    os.makedirs(study_output_folder, exist_ok=True)

    print(f"🔍 Looking for FASTQ files in: {study_seq_folder}")
    print(f"📁 Will copy matching files to: {study_output_folder}")
    
    # Read metadata
    try:
        metadata = pd.read_excel(metadata_path)
    except Exception as e:
        print(f"❌ Failed to read metadata file: {metadata_path}")
        print(e)
        continue

    run_ids = metadata["run_accession"].dropna().astype(str).tolist()

    # Copy files
    for run_id in run_ids:
        for suffix in ["_1.fastq.gz", ".fastq.gz","_f1.fq.gz"]:
            filename = f"{run_id}{suffix}"
            source_path = os.path.join(study_seq_folder, filename)
            target_path = os.path.join(study_output_folder, filename)

            print(f"→ Checking: {source_path}")
            if os.path.exists(source_path):
                shutil.copy(source_path, target_path)
                print(f"✅ Copied: {filename} to {study_folder}/")
            else:
                print(f"⚠️ Missing: {filename} in {study_folder}/")
