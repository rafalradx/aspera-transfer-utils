# Aspera Transfer with SLURM

This project provides a way to transfer raw cryoEM data (tiff images) to EMPIAR database using Aspera in combination with SLURM for job scheduling. The configuration file allows you to customize the settings for your transfer and SLURM job. The scripts were developed to be compatible with Athena supercomputer enviroment in Academic Computer Centre Cyfronet AGH.

## Prerequisites

- Aspera Connect installed and configured.
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

# Number of files in a batch to be sent in one SLURM job
BATCH_SIZE=1500

# SLURM job settings
JOB_NAME=aspera_transfer

# Job max lifetime (in hours)
TIME=48

# Grant SLURM name (Athena style name)
ACCOUNT=mygrant-gpu-a100
```
### 4. Run the `empiar_prep.py` script
```bash
python empiar_prep.py
```
The script splits files into batches and moves them into subdirectories: subdir1, subdir2, etc. It may take some time. Be patient.
Once it's done it generates SLURM submission scripts for each batch of files.
Example of output:
```bash
Number of files to send: 3027
Number of batches: 4
Files split and sbatch scripts created successfully!
```
If the script does not find any files in provided directory (`TIFF_PATH`), it assumes that the files are already split in subdirectories.
So you can safely run the script twice on the same directory if you want to adjust your configuration.

### 5. Submit a SLURM job by running sbatch for each script created
``` bash
sbatch super_important_sample_subdir1.sh
```
### 6. Use `check_status.py` script to monitor upload progress 
```batch
python check_status.py transfer_log/super_important_sample_subdir1_err.txt
```
Run this script for each error log in `transfer_log` directory. 
Example output:
```batch
Total files to transfer: 1133
Transfers started: 58
Transfers completed successfully: 56
Progress: 4.94%
Total transfer time: 0.65 h
```
## Notes
* Ensure that the `ASCP_PATH` is correctly set to the Aspera Connect ascp binary installed on your cyfronet Athena account.
* The SLURM job will output log files named ${NAME_ID}_subdir1_log.txt and ${NAME_ID}_subdir1_err.txt in `transfer_log` directory for each subdirectory submitted for file transfer.
## License
This project is licensed under the MIT License.
## Acknowledgments
Thanks to Łukasz Koziej for providing invaluable information on how to use Aspera in ACC AGH Athena environment
