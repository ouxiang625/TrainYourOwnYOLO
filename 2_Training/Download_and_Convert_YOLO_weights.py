import os
import subprocess
import time
import argparse

FLAGS = None

# https://stackoverflow.com/questions/16771894/python-nameerror-global-name-file-is-not-defined
# The C version will give you the original path of the source file. This is useful in logging errors 
#   and knowing which source file has the bug.
# Python's __file__ only gives you the name of the currently executing file, which may not be 
# very useful in log output.
# 
# This is the 2-level parent dir of rundir. e.g.: "/Users/feil/yolo3" --> root_folder is "/Users".
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# print(os.path.join(root_folder, "2_Training", "src", "keras_yolo3")) --> /Users/2_Training/src/keras_yolo3
download_folder = os.path.join(root_folder, "2_Training", "src", "keras_yolo3")
data_folder = os.path.join(root_folder, "Data")
model_folder = os.path.join(data_folder, "Model_Weights")

if __name__ == "__main__":
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    """
    Command line options
    """
    parser.add_argument(
        "--download_folder",
        type=str,
        default=download_folder,
        help="Folder to download weights to. Default is " + download_folder,
    )

    parser.add_argument(
        "--is_tiny",
        default=False,
        action="store_true",
        help="Use the tiny Yolo version for better performance and less accuracy. Default is False.",
    )

    FLAGS = parser.parse_args()

    if not FLAGS.is_tiny:
        weights_file = "yolov3.weights"
        h5_file = "yolo.h5"
        cfg_file = "yolov3.cfg"
        # Original URL: https://pjreddie.com/media/files/yolov3.weights
        gdrive_id = "1ENKguLZbkgvM8unU3Hq1BoFzoLeGWvE_"

    else:
        weights_file = "yolov3-tiny.weights"
        h5_file = "yolo-tiny.h5"
        cfg_file = "yolov3-tiny.cfg"
        # Original URL: https://pjreddie.com/media/files/yolov3-tiny.weights
        gdrive_id = "1mIEZthXBcEguMvuVAHKLXQX3mA1oZUuC"

    if not os.path.isfile(os.path.join(download_folder, weights_file)):
        print(f"\nDownloading Raw {weights_file}\n")
        start = time.time()
        call_string = " ".join(
            [
                "cd ..",
                "\n",
                "cd",
                download_folder,
                "\n",
                "gdown", # gdown: download to google drive
                f"https://drive.google.com/uc?id={gdrive_id}",
            ]
        )

        subprocess.call(call_string, shell=True)

        end = time.time()
        print(f"Downloaded Raw {weights_file} in {end - start:.1f} seconds\n")

        call_string = f"python convert.py {cfg_file} {weights_file} {h5_file}"

        subprocess.call(call_string, shell=True, cwd=download_folder)
