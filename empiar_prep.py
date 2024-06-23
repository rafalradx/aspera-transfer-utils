from dotenv import dotenv_values
import os
import shutil


def split_files_into_batches(source_dir, batch_size=2000):
    # Get the list of all files in the source directory
    files = [
        f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))
    ]

    if not files:
        print("No files found in source dir. Assuming split into subdirs")
        subdir_paths = [
            os.path.join(source_dir, subdir) for subdir in os.listdir(source_dir)
        ]
        print(f"Subdirs found: {len(subdir_paths)}")
        return subdir_paths

    print(f"Number of files to send: {len(files)}")

    # Calculate the number of batches required
    num_batches = (len(files) + batch_size - 1) // batch_size

    print(f"Number of batches: {num_batches}")

    # subdir paths
    subdir_paths = []

    for n in range(num_batches):
        # Create a new subdirectory for each batch
        subdir_name = os.path.join(source_dir, f"subdir{n+1}")
        os.makedirs(subdir_name, exist_ok=True)
        subdir_paths.append(subdir_name)

        # Get the files for the current batch
        batch_files = files[n * batch_size : (n + 1) * batch_size]

        for file_name in batch_files:
            # Construct full file path
            file_path = os.path.join(source_dir, file_name)
            # Move file to the new subdirectory
            shutil.move(file_path, subdir_name)

    return subdir_paths


if __name__ == "__main__":
    # load configuration
    config = dotenv_values("config.txt")

    # splits files, returns paths to subdirs
    subdirs = split_files_into_batches(
        source_dir=config["TIFF_PATH"], batch_size=int(config["BATCH_SIZE"])
    )

    # current folder
    current_path = os.getcwd()
    # create dir for logs
    log_dir = os.path.join(current_path, "transfer_logs")
    os.makedirs(log_dir, exist_ok=True)

    # prepare SLURM job script to transfer file from each subdir with aspera
    NAME_ID = config["NAME_ID"]
    for subdir in subdirs:
        # folder name from the path
        subdir_name = os.path.basename(subdir)

        # lines of sbatch script to write
        lines = [
            "#!/bin/bash\n",
            "#SBATCH --job-name aspera_transfer\n",
            f"#SBATCH -A {config['ACCOUNT']}\n",
            "#SBATCH --partition plgrid-gpu-a100\n",
            f"#SBATCH --time=0-{config['TIME']}\n",
            "#SBATCH --nodes=1\n",
            "#SBATCH --ntasks-per-node=4\n",
            "#SBATCH --gres=gpu:0\n",
            "#SBATCH --cpus-per-task=1\n",
            "#SBATCH --mem=10000MB\n",
            f'#SBATCH -o "{log_dir}/{NAME_ID}_{subdir_name}_log.txt"\n',
            f'#SBATCH -e "{log_dir}/{NAME_ID}_{subdir_name}_err.txt"\n',
            "\n",
        ]

        # name of sbatch script for each batch of files
        file_name = f"{NAME_ID}_{subdir_name}_empriar_upload.sh"

        # ascp command
        ascp_command_parts = [
            f"ASPERA_SCP_PASS={config['ASPERA_SCP_PASS']}",
            config["ASCP_PATH"],
            f"-QT -P 33001 -l {config['TRANSFER_SPEED']} -L- -k3",
            f"{config['TIFF_PATH']}/{subdir_name}/*.tiff",
            f"emp_dep@hx-fasp-1.ebi.ac.uk:upload/{config['ASPERA_TOKEN']}/data",
        ]

        ascp_command = " ".join(ascp_command_parts)

        with open(file_name, "w") as fn:
            fn.writelines(lines)
            fn.write(ascp_command)

    print("Files split and sbatch scripts created successfully!")
