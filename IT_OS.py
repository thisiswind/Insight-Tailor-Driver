"""*************************************************************************************************
====FILE
	IT_OS_get_file_path_name(initial_dir="\\")
	IT_OS_get_user_passwd(dir_filename)

====DATE TIME
	IT_OS_get_8_digit_GMT_date(delta_day)


====COMMUNICATION PROTOCOL
	IT_OS_SSH(host,port,user,pwd,command)
	IT_OS_sftp_download(host,port,username,password,local,remote)
	IT_OS_sftp_upload(host,port,username,password,local,remote)



Last Modified by:
Wind 20181010
*************************************************************************************************"""

"""====FILE**************************************************************************************"""

"""*************************************************************************************************
get_file_path_name enable windows user to locate and select a file in dialog window and return the
file path and file name as a list
initial_dir specified where the system start to browse, it can be eigher absolute director like
"C:\\DATA" or relative directory like "\\DATA"

Wind 20180924
*************************************************************************************************"""
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
#print (IT_OS_get_file_path_name("C:\\file\\msu_report"))

"""*************************************************************************************************
IT_OS_get_user_passwd return first 2 words in specified file as username and password.
if file does not exist or less than 2 words in the file, returns['empty','empty']
20181014 Wind
*************************************************************************************************"""
def IT_OS_get_user_passwd(dir_filename):
	import os,traceback
	if dir_filename[0].isalpha()==False:#Not start like c:
		dir_filename=os.getcwd()+dir_filename
	try:
		input=open(dir_filename)
		input.close()
	except:
		traceback.print_exc()
		return(['empty','empty'])	
	input=open(dir_filename)
	info=input.read().split(' ')
	input.close()
	if len(info)<2:
		print("Invalid format in "+dir_filename)
		print("Format shall be:username password")
		return(['empty','empty'])
	user= info[0]
	pwd=info[1]
	return([user,pwd])
#print (IT_OS_get_user_passwd('C:\\python_work\\userinfo.txt'))
#print (IT_OS_get_user_passwd('\\file\\userinfo.txt'))

"""*************************************************************************************************
IT_OS_get_user_passwd_with_dialog return first 2 words in specified file as username and password.
if file does not exist or less than 2 words in the file, dialog window will be opened to ask for
credential

20181014 Wind
*************************************************************************************************"""
def IT_OS_get_user_passwd_with_dialog(dir_filename):
	import os,tkinter,sys
	global user,pwd
	
	def show_login(dir_filename):
		global user
		global pwd
		def login():
			global user
			global pwd
			user=entryName.get()
			pwd=entryPwd.get()
			root.destroy()

		def cancel():
			global user
			global pwd
			user=""
			pwd=""
			root.destroy()
			sys.exit()

		root = tkinter.Tk()
		root.title("Enter your gid/pass to update file")
		root.geometry('330x170+500+200')
	
		labelName = tkinter.Label(root,text='Your Gid:',justify=tkinter.RIGHT,width=100)
		labelName.place(x=40, y=20, width=110, height=20)
	
		varName = tkinter.StringVar(root, value='')
		entryName = tkinter.Entry(root,width=80,textvariable=varName)
		entryName.place(x=170, y=20, width=100, height=20)
	
		labelPwd = tkinter.Label(root,text='Your Lan Password:',justify=tkinter.RIGHT,width=100)
		labelPwd.place(x=40, y=55, width=110, height=20)
	
		varPwd = tkinter.StringVar(root, value='')
		entryPwd = tkinter.Entry(root,show='*',width=80,textvariable=varPwd)
		entryPwd.place(x=170, y=55, width=100, height=20)
	
		buttonOk = tkinter.Button(root,text='Update File',command=login)
		buttonOk.place(x=80, y=100, width=80, height=20)
	
		buttonCancel = tkinter.Button(root,text='Cancel',command=cancel)
		buttonCancel.place(x=180, y=100, width=80, height=20)
		
		root.mainloop()
		output = open(dir_filename, 'w')
		if user!="" or pwd!="":
			output.write(user+' '+pwd)
		output.close()
	
	if dir_filename[0].isalpha()==False:#Not start like c:
		dir_filename=os.getcwd()+dir_filename
	try:
		input=open(dir_filename)
		input.close()
	except Exception as e:
		print('Exception:',e)
		show_login(dir_filename)
		
	input=open(dir_filename)
	info=input.read().split(' ')
	input.close()
	while len(info)<2:
		show_login(dir_filename)
		input=open(dir_filename)
		info=input.read().split(' ')
		input.close()
		
	user= info[0]
	pwd=info[1]
	return([user,pwd])
	
print (IT_OS_get_user_passwd_with_dialog('C:\\python_work\\userinfo.txt'))
		

"""====DATE TIME*********************************************************************************"""

"""*************************************************************************************************
IT_OS_get_8_digit_GMT_date returns date in 8 digital format like 20181010
if need local time, replace gmtime with localtime in code
to get today, delta_day=0
to get yesterday, delta_day=-1

Wind 20181010
*************************************************************************************************"""
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
	
#print(IT_OS_SSH('10.162.28.187',22,'g707414','%password','netstat -an'))


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
	import paramiko,os,platform,stat

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
