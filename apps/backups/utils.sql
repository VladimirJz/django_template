select 
concat('INSERT INTO backups_backups(CreationDate,StartBackup,EndBackup,FileName,SizeMB,Size,Comments,Database_id,Job_id,Location_id,Status_id) VALUES (''',
CreationDate,''',''',convert(varchar(30),StartBackup ,121),''',''',convert(varchar(30),EndBackup ,121),''',''',FileName,''',',BackupSizeMB,',',BackupSize,',''',Comments,''',',1,',',1,',',LocationID,',',BackupStatusID,');')
from 
BACKUPS



