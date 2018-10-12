"""*********************************************************************
****FILE****
IT_OS_get_file_path_name(initial_dir="\\")
IT_OS_get_user_passwd(dir_filename)

****DATE TIME****
IT_OS_get_8_digit_GMT_date(delta_day)


****COMMUNICATION PROTOCOL****
IT_OS_SSH(host,port,user,pwd,command)
IT_OS_sftp_download(host,port,username,password,local,remote)
IT_OS_sftp_upload(host,port,username,password,local,remote)
Wind 20181010
*********************************************************************"""

'''****FILE*****'''

"""*********************************************************************
get_file_path_name enable user to select a file in dialog window
and return the file path and file name

Wind 20180924
*********************************************************************"""
def IT_OS_get_file_path_name(initial_dir="\\"):
	import time,os.path, os,shutil,tkinter.filedialog
	if initial_dir[0].isalpha()==False:#Not start like c:
		initial_dir=os.getcwd()+initial_dir
	root1=tkinter.Tk()
	root1.withdraw()
	full_name=tkinter.filedialog.askopenfilename(title="Choose File",\
	initialdir=(os.path.expanduser(initial_dir)))
	root1.destroy()
	file_path=os.path.split(full_name)[0]
	file_name=os.path.split(full_name)[1]
	return([file_path,file_name])

#print (IT_OS_get_file_path_name("\\file\\msu_report"))

"""*********************************************************************
IT_OS_get_user_passwd return first 2 words in specified file as username
and password.
protection for file does not exist, or the file is empty is not written
Wind 20181010
*********************************************************************"""
def IT_OS_get_user_passwd(dir_filename):
	import os
	if dir_filename[0].isalpha()==False:#Not start like c:
		dir_filename=os.getcwd()+dir_filename
	input=open(dir_filename)
	info=input.read().split(' ')
	input.close()
	# decide if the userinfo.txt is empty, if so, write one via show_login()
	#if len(info)==1:
	#	show_login()
	user= info[0]
	pwd=info[1]
	return([user,pwd])

#print (IT_OS_get_user_passwd('\\file\\userinfo.txt'))

'''****DATE TIME****'''

"""*********************************************************************
IT_OS_get_8_digit_GMT_date returns date in 8 digital format like 20181010
if need local time, replace gmttime with localtime in code
to get today, delta_day=0
to get yesterday, delta_day=-1

Wind 20181010
*********************************************************************"""
def IT_OS_get_8_digit_GMT_date(delta_day):
	import time

	year=str(time.gmtime(time.time()+24*60*60*delta_day).tm_year)
	month=str(time.gmtime(time.time()+24*60*60*delta_day).tm_mon)
	if len(month)==1:
		month="0"+month		
	day=str(time.gmtime(time.time()+24*60*60*delta_day).tm_mday)
	if len(day)==1:
		day="0"+day		
	timestamp=year+month+day
	return(timestamp)
	
#print(IT_OS_get_8_digit_GMT_date(-1))


'''***************COMMUNICATION PROTOCOL****************************************************************'''

def IT_OS_SSH(host,port,user,pwd,command):
	import paramiko
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=host,port=port, username=user, password=pwd)
	stdin, stdout, stderr = ssh.exec_command(command)
	res,err = stdout.read(),stderr.read()
	result = res if res else err
	dirresult=result.decode().rstrip().lstrip()
	return(dirresult)
	
#print(IT_OS_SSH('10.162.28.187',22,'g707414','????','netstat -an'))


"""*******************************************************************************************************
IT_OS_sftp_download(host,port,username,password,local,remote)
#host='10.162.28.182'
#port = 22 
#username='g707414'
#password='XXXXXX'
#local = 'C:\\sftptest\\test'#本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
#remote = '/home/g707414/'#远程文件或目录，与本地一致，当前为linux目录格式,取远程目录下所有文件
#remote = '/home/g707414/diameter-dsc.xml'#远程文件或目录，与本地一致，当前为linux目录格式

#sftp_upload(host,port,username,password,local,remote)#上传
#sftp_download(host,port,username,password,local,remote)#下载

Version: v1.0 2018.10.12

*******************************************************************************************************"""
def IT_OS_sftp_download(host,port,username,password,local,remote):
	import paramiko
	import os
	import platform
	import stat
	sf = paramiko.Transport((host,port))
	sf.connect(username = username,password = password)
	sftp = paramiko.SFTPClient.from_transport(sf)
	try:
		if os.path.isdir(local):#判断本地参数是目录还是文件
			print("dir is local")
			for f in sftp.listdir(remote):#遍历远程目录
				print(f)
				sftp.get(os.path.join(remote+f),os.path.join(local+f))#下载目录中文件
				#sftp.get('.kshrc',os.path.join(local+f))#下载目录中文件
		else:
			sftp.get(remote,local)#下载文件
	except Exception as e:
		print('download exception:',e)
	sf.close()
	

"""*******************************************************************************************************
IT_OS_sftp_upload(host,port,username,password,local,remote)
not tested yet
20181012
*******************************************************************************************************"""


def IT_OS_sftp_upload(host,port,username,password,local,remote):
	import paramiko
	import os
	import platform
	import stat
	sf = paramiko.Transport((host,port))
	sf.connect(username = username,password = password)
	sftp = paramiko.SFTPClient.from_transport(sf)
		try:
		if os.path.isdir(local):#判断本地参数是目录还是文件
			for f in os.listdir(local):#遍历本地目录
			sftp.put(os.path.join(local+f),os.path.join(remote+f))#上传目录中的文件
		else:
			sftp.put(local,remote)#上传文件
		except Exception as e:
			print('upload exception:',e)
	sf.close()
