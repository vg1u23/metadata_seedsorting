import pandas as pd
import os
import shutil
import glob

# === Configuration ===
metadata_file_list = "/iridisfs/scratch/vg1u23/test/filtered_by_study/metadata_file_list.xlsx"
metadata_folder = "/iridisfs/scratch/vg1u23/test/metadataperstudy"
filtered_fastq_folder = "/iridisfs/scratch/vg1u23/test/filtered_by_study"
output_by_primer = "/iridisfs/scratch/vg1u23/test/by_primer_fw_rev"
os.makedirs(output_by_primer, exist_ok=True)

# === Load metadata file list ===
try:
    metadata_list = pd.read_excel(metadata_file_list)
except Exception as e:
    print(f"❌ Failed to read metadata file list: {metadata_file_list}")
    print(e)
    exit()

# === Process each metadata file ===
for metadata_filename in metadata_list["filename"]:
    print(f"\n📄 Processing metadata: {metadata_filename}")
    
    # Extract study name (e.g., "PRJCA008115_with_family.xlsx" → "PRJCA008115")
    study_name = metadata_filename.split("_with_family")[0]
    
    metadata_path = os.path.join(metadata_folder, metadata_filename)
    study_fastq_path = os.path.join(filtered_fastq_folder, study_name)

    if not os.path.exists(metadata_path):
        print(f"❌ Metadata file not found: {metadata_path}")
        continue

    if not os.path.isdir(study_fastq_path):
        print(f"❌ FASTQ folder not found for study: {study_fastq_path}")
        continue

    # Load metadata file
    try:
        metadata = pd.read_excel(metadata_path)
    except Exception as e:
        print(f"❌ Error reading {metadata_filename}: {e}")
        continue

    # Ensure required columns exist
    if "run_accession" not in metadata.columns or "primer_fw_rev" not in metadata.columns:
        print(f"⚠️ Missing 'run_accession' or 'primer_fw_rev' column in {metadata_filename}")
        continue

    for _, row in metadata.iterrows():
        run_id = str(row["run_accession"]).strip()
        primer_fw_rev = str(row["primer_fw_rev"]).strip().replace("/", "-")

        # Output folder by primer_fw_rev and study
        primer_study_output_path = os.path.join(output_by_primer, primer_fw_rev, study_name)
        os.makedirs(primer_study_output_path, exist_ok=True)

        # Wildcard-based matching to catch any naming variation
        matched = False
        pattern = os.path.join(study_fastq_path, f"{run_id}*")
        print(f"🔍 Searching for: {pattern}")
        for src in glob.glob(pattern):
            fq_name = os.path.basename(src)
            dst = os.path.join(primer_study_output_path, fq_name)
            shutil.copy2(src, dst)
            print(f"✅ Copied: {fq_name} → {primer_fw_rev}/{study_name}/")
            matched = True

        if not matched:
            print(f"⚠️ No FASTQ file found for run: {run_id} in study: {study_name}")

print("\n🎉 Done! All FASTQ files sorted by primer_fw_rev and grouped by study.")
