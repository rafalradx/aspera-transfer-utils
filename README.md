# Aspera Transfer with SLURM

This project provides a way to transfer files using Aspera in combination with SLURM for job scheduling. The configuration file allows you to customize the settings for your transfer and SLURM job.

## Prerequisites

- Aspera Connect installed and configured.
- SLURM installed and configured.
- Bash shell.

## Configuration

Edit the `aspera_config.sh` file to specify your settings:

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
