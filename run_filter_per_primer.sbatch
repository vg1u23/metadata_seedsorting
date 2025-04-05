#!/bin/bash
#SBATCH --job-name=filter_seed_fastq
#SBATCH --output=filter_seed_fastq_%j.out
#SBATCH --error=filter_seed_fastq_%j.err
#SBATCH --time=03:00:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=70
#SBATCH --nodes=1

source ~/.bashrc

# Load conda and activate your pandas environment
conda activate pandas

# Run your Python script
python filter_per_primer.py
