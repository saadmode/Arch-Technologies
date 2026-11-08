# Lost Data Retrieval: JPEG Recovery Using Python

## Overview

I worked on this project as part of my cybersecurity internship to gain practical exposure to digital forensics and data recovery using Python.

The purpose of this project is to read a storage device at the raw byte level, find deleted JPEG pictures using their file signature, and save them as normal image files. This technique is known as file carving.

## Project Setup

* Python 3
* pytsk3 (only for the folder-based recovery script)
* Windows 10
* USB flash drive used as the test drive
* Administrator privileges for raw drive access

## Features

The recovery tools provide the following features:

* Read a drive directly at the raw byte level using sector-aligned reads
* Detect JPEG files by their start signature (`FF D8 FF`)
* Find the real end of each picture by walking the JPEG structure, so embedded thumbnails do not cut files short
* Save each recovered picture as a separate `.jpg` file
* Keep damaged or cut-off pictures with a `_partial` suffix
* Ignore very small (under 4 KB) and very large (over 40 MB) candidates
* Skip unreadable sectors and stop cleanly at the end of the drive
* Show scan progress and a final summary
* Recover only the pictures deleted from one specific folder, with their original names (`recover_folder.py`)

## Files in This Project

| File | Purpose |
|------|---------|
| `recover_jpg.py` | Scans a whole drive and carves out JPEG files |
| `recover_folder.py` | Recovers only the deleted pictures from one chosen folder using the file table |

## Activity Performed

During this project, I worked with Python-based recovery scripts to:

* Copy pictures to a USB flash drive and delete them
* Read the USB drive as a raw device
* Search the raw data for JPEG signatures
* Recover the deleted pictures into a folder on a different drive
* Test the scripts on simulated disk images before using a real drive
* Fix problems found during testing, such as an incorrect signature, an endless loop at the end of the drive, and pictures cut short by embedded thumbnails

## How to Run

### 1. Prepare

Install Python 3. The main script needs no extra libraries. For the folder-based script, install:

```bash
python -m pip install pytsk3
```

Open `recover_jpg.py` and set the two paths at the top of the file:

```python
DRIVE = r"\\.\D:"                # drive to recover from
OUT_DIR = r"E:\path\to\recover"  # folder to save recovered files
```

Always save recovered files to a different drive from the one being recovered.

### 2. Recover All JPEG Files from a Drive

Open Command Prompt as Administrator and run:

```bash
python recover_jpg.py
```

### 3. Recover Only the Files Deleted from One Folder

Set `DRIVE`, `SOURCE_FOLDER`, and `OUT_DIR` at the top of `recover_folder.py`, then run:

```bash
python recover_folder.py
```

Recovered files from the main script are named `0.jpg`, `1.jpg`, and so on, because carving does not restore original file names. Run the scripts with Administrator privileges.

## What I Learned

This project helped me understand what happens to data when a file is deleted and why it can often be recovered until it is overwritten.

I also gained exposure to file signatures, the internal structure of the JPEG format, raw disk access, and the difference between file carving and file-table based recovery.

## Skills Practiced

* Python
* Digital Forensics Basics
* Data Recovery
* File Carving
* Raw Disk Access
* Testing and Debugging

## Limitations

This project recovers JPEG pictures only. Fragmented files, which are stored in non-contiguous pieces, may be recovered damaged or as `_partial` files.

Data that has been overwritten cannot be recovered, and on SSDs the TRIM feature may erase deleted data quickly. The folder-based script depends on the file table entry still existing, so it will not work after a format or once the entry has been reused.

The main script scans the whole drive, so it also recovers pictures that were not deleted.

## Disclaimer

These tools should only be used on drives and data that you own or have explicit permission to examine. Recovered files may contain private information and should be handled carefully.

## Project Evidence

Screenshots and a demonstration video can be added to document the scripts running and recovering the deleted pictures successfully.
