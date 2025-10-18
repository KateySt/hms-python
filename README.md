1. Install Ubuntu on wsl
```
wsl --install -d Ubuntu-22.04
```
2. go to dir
```
cd /mnt/c/Users/User/Desktop/hws-python
```
3. venv 
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
4. script run
```
chmod +x create_new_file.sh
./create_new_file.sh
Enter file name: text.txt

chmod +x backup.sh
./backup.sh

SOURCE_DIR="/mnt/c/Users/User/Desktop/hws-python/bash-script" # Directory to backup
BACKUP_DIR="/mnt/c/Users/User/Desktop/hws-python/backup" # Destination for backups
```