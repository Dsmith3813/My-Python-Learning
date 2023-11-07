'''
Specialty program to backup my image files into 1gb zip files for one of my remote (online) storage. 

Libvrary used:

TQMD library for progress bar.
ZIPFILE for zip file processing.

'''

import os
import datetime
import time
from tqdm import tqdm
from zipfile import ZipFile

# Clear the screen
os.system('clear')

# Variables
pic_path = "/Users/dennis/Desktop/Cindy Pictures"
bkup_path = "/Volumes/X10 Pro /Backup/"
pw = b'Password'  # NOTE: Python doesn't support passwords on write
now = datetime.datetime.now()
zipname = f'{bkup_path}BK{now.year}{now.month:02}{now.day:02}'

# Counts and such
max_packet_size = 1e+9  # Just slightly under 1 gb.
total_size = 0          # Use to report total bytes copied
byte_cnt = 0            # User to accumulate current amount of bytes copied.
zip_cnt = 0             # Number of zip files created.
lines = ''              # Log file
file_packet_cnt = 0     # Number of packets created.
file_packet_block = []  # Hold the files to be added to the zip file.


def Handle_Entries(entry):
    '''
    Function to determine if the entry passed is a file or a directory.

    NOTE: That this function is called from two different points. From the main line, to handles files in the starting directory. And from Handle_Directory, to handle files from a directory found within the starting directory. Following the directory structure. Could be considered recursively called.
    '''
    global lines

    if entry.is_file(follow_symlinks=True):
        Handle_File(entry)
    elif entry.is_dir(follow_symlinks=True):
        Handle_Directory(entry)
    else:
        lines += f'\nUnknown entry type: {entry}\n\n'


def Handle_File(entry):
    '''
    Will handle the files to be processed. A file entry has been passed into this function. We add it to the file_packet_block that will be passed to the Write_Zip() function when we have reached the max_packet_size for a zip file. Other accumulators are gathered for later reporting. 
    '''
    global total_size, byte_cnt, file_packet_cnt, lines, file_packet_block

    # Bypass hidden files on macos.
    if entry.name.startswith('.'):
        return

    # Capture the complete file name and size.
    p = entry.path                  # Path to the file including file name
    s = entry.stat(follow_symlinks=False).st_size

    # Add the file to the packet block
    file_packet_block.append(p)

    # Accumulate
    total_size += s
    byte_cnt += s

    # Write to log file
    lines += (f'\n{p}  {s:,}')

    # Did we hit our threshold? If so kick out a zip file.
    if byte_cnt > max_packet_size:
        byte_cnt = 0
        file_packet_cnt += 1
        Write_Zip(file_packet_block, file_packet_cnt)
        file_packet_block = []
        lines += f'\n\nFile Packet: {file_packet_cnt} Created\n'


def Handle_Directory(entry):
    '''
    Handles a directory entry. Basically, it scans the directory and then calls, Handle_Entries() to process the files recursively
    '''
    global lines

    lines += f'\n\n{entry}'
    p = entry.path                  # Path of this directory

    # Scan this directory
    with os.scandir(p) as dir_entries:
        for entry in tqdm(dir_entries,
                          desc=f"Processing files in {entry}",
                          unit=" files",
                          ncols=100
                          ):
            Handle_Entries(entry)   # Go back thought the process.
            # time.sleep(0.0001)


def Write_Zip(files, cnt):
    '''
    Writes the zip file with the files found in the file_packet_block.
    '''
    global zipname, lines, zip_cnt

    # Take the zip file high level qualifier and add a P number to it.
    zn = f'{zipname}_P{cnt}.zip'

    with ZipFile(zn, 'w') as zip:
        for file in files:
            zip.write(file)

    zip.close()

    zip_cnt += 1
    lines += f'\n\nZip file: {zn} created\n'


"""
Main Line
"""
t1 = time.perf_counter()                # Elapse time captures.

print(f"\nDennis' Pictures Backup Program\n\n")
lines += f'\nFiles to be backed up\n'

# Scan the starting directory.
with os.scandir(pic_path) as entries:
    for entry in tqdm(entries,
                      desc="Processing file",
                      unit=" files",
                      ncols=100
                      ):
        Handle_Entries(entry)
        # time.sleep(0.0001)

# Check to be sure that we pick up any partial file_packet_block and
# write the zip file out.
if byte_cnt > 0:
    file_packet_cnt += 1
    Write_Zip(file_packet_block, file_packet_cnt)

# Write the log file
with open('./LogFile.txt', "w") as f:
    f.write(lines)
    f.close()

# Last bit of calculation to be displayed to the end user.
c1 = max_packet_size/1024
c2 = c1/1024
c3 = c2/1024
c4 = total_size/1024
c5 = c4/1024
c6 = c5/1024

# Print to the user the results
print(f'\nFile directory: {pic_path}')
print(f'\nMax packet size:\t{c3:>15,.2f} gb')
print(f'\nTotal size:\t\t{total_size:>15,} Bytes')
print(f'\t\t\t{c4:>15,.2f} kb')
print(f'\t\t\t{c5:>15,.2f} mb')
print(f'\t\t\t{c6:>15,.2f} gb')
print(f'\nTotal file packets:\t{file_packet_cnt:>15,}')
print(f'\nZip files created:\t{zip_cnt:>15,}')

# Elapse time stuff
t2 = time.perf_counter()
xtime = t2-t1
xtime_type = 'Seconds'

if xtime > 60:
    xtime = xtime / 60
    xtime_type = 'Minutes'

print(f'\nBackup complete. Elapse time: {xtime:.2f} {xtime_type}\n')
