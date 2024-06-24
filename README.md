# Aspera Transfer with SLURM

This project provides a way to transfer raw cryoEM data (tiff images) to EMPIAR database using Aspera in combination with SLURM for job scheduling. The configuration file allows you to customize the settings for your transfer and SLURM job.

## Prerequisites

- Aspera Connect installed and configured.
- SLURM installed and configured.
- Python installed.

## Usage 

### 1. Clone the repository
```bash
git clone https://github.com/rafalradx/aspera-transfer-utils
cd aspera-transfer-utils
```
### 2. Make sure you have `python-dotenv` installed
```bash
pip install python-dotenv
```
### 3. Configuration

Edit the `config.txt` file to specify your settings:

```bash
# Aspera settings
ASCP_PATH=/home/user/.aspera/connect/bin/ascp
ASPERA_TOKEN=EMPIAR_upload_token
ASPERA_SCP_PASS=EMPIAR_super_secret_password
TRANSFER_SPEED=200M

# Path to raw images (tiff's) directory
TIFF_PATH=/home/user/cryoEM/data

# Unique name for scripts naming (project, sample, id, etc)
NAME_ID=super_important_sample

# Number of files in a batch to send in one SLURM job
BATCH_SIZE=1500

# SLURM job settings
JOB_NAME=aspera_transfer

# Job max lifetime (in hours)
TIME=48

# Grant SLURM name (Athena style name)
ACCOUNT=mygrant-gpu-a100
```
### 4. Run script 'empiar_prep.py' 
```bash
python empiar_prep.py
```
The script splits files into batches and moves them files subdirectories: subdir1, subdir2, etc. It may take some time. Be patient.
Once done it generates SLURM scripts for each batch of files
### 5. Submit a SLURM job by running sbatch for each script created
``` bash
sbatch super_important_sample_subdir1.sh
```
