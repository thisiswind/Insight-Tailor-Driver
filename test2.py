import tkinter
import tkinter.messagebox
import os
import os.path
import requests
import sys
from requests_ntlm import HttpNtlmAuth
import datetime,time
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
def IT_OS_get_user_passwd_with_dialog(credential_dir_filename=""):
	import os,os.path,tkinter,sys
	import tkinter.messagebox
	global user,pwd
	user=pwd=""
	
	def show_login():#populate global variable user,pwd
		global user
		global pwd
		def login():
			global user
			global pwd
			user=entryName.get()
			pwd=entryPwd.get()
			root.destroy()

		def cancel():
			global user,pwd
			user=pwd=""
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

	#start
	if credential_dir_filename=="":
		while user=="" or pwd=="":
			show_login()
		return([user,pwd])
	if credential_dir_filename!="":
		if credential_dir_filename[0].isalpha()==False:#Not start like c
			credential_dir_filename=os.getcwd()+credential_dir_filename
			print(credential_dir_filename)
		credential_dir=os.path.split(credential_dir_filename)[0]
		credential_filename=os.path.split(credential_dir_filename)[1]
		if not os.path.exists(credential_dir):
			root1=tkinter.Tk()
			root1.withdraw()
			tkinter.messagebox.showinfo('Credential file path error.',"Path "+credential_dir+" not exist")
			return(["",""])
		if not os.path.exists(credential_dir_filename):
			while user=="" or pwd=="":
				show_login()
			output = open(credential_dir_filename, 'w')
			output.write(user+' '+pwd)
			output.close()
			return([user,pwd])
			
		if os.path.exists(credential_dir_filename):
			input=open(credential_dir_filename)
			info=input.read().split(' ')
			input.close()
			if len(info)==2:
				user=info[0]
				pwd=info[1]
				return([user,pwd])
			if len(info)!=2:
				while user=="" or pwd=="":
					show_login()
				output = open(credential_dir_filename, 'w')
				output.write(user+' '+pwd)
				output.close()
				return([user,pwd])

"""*************************************************************************************************
IT_OS_fileupdate_from_sharepoint download file from sharepoint url if local file does not exist
or local file is older than file on sharepoint.
If user,pwd is not corrrect and credential_file_dir_name!="", it will delete credential_file_dir_name 
and call IT_OS_get_user_passwd_with_dialog(credential_file_dir_name) to reget user and pwd repeatedly
until credential is correct or ["",""] is returned by IT_OS_get_user_passwd_with_dialog(canceled)
If user,pwd is not corrrect and credential_file_dir_name==""
This function is developed by Greg and updated by Wind

20181017 Greg/Wind
*************************************************************************************************"""

def IT_OS_fileupdate_from_sharepoint(user,pwd,url1,output_file_name_path,credential_dir_filename=""):
	import tkinter,tkinter.messagebox,os,os.path,requests,sys,datetime,time
	from requests_ntlm import HttpNtlmAuth
	GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

	try:
		r1=requests.get(url1,auth=HttpNtlmAuth(user,pwd))
	except requests.exceptions.ConnectionError:
		print ('Connection error, URL address not found, please check URL.\n')
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', 'Connection error, URL address not found, please check URL.')
		sys.exit()
	except requests.exceptions.MissingSchema:
		print ('Invalid URL '+url1+' : No schema supplied. Perhaps you meant http://'+ url1+'?\n')
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning', 'Invalid URL '+url1+' : No schema supplied. Perhaps you meant http://'+ url1+'?\n')
		sys.exit()
	else:
		res1= r1.status_code
# process different HTTP reponse codes 
	if res1==404:
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning','No file in the URL, please double check URL.')
		print ('No file in the URL, please double check URL.\n\n')
		sys.exit()
		return()
	while res1==401:
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning','User name or password incorrect.')
		root1.destroy()

		if credential_dir_filename!="":
			if credential_dir_filename[0].isalpha()==False:#Not start like c
				credential_dir_filename=os.getcwd()+credential_dir_filename
			try:
				os.remove(credential_dir_filename)
			except:
				root1=tkinter.Tk()
				root1.withdraw()
				tkinter.messagebox.showwarning('Cannot locate credential_dir_filename',credential_dir_filename)
				root1.destroy()
				return()
		
		info=IT_OS_get_user_passwd_with_dialog(credential_dir_filename)
		user= info[0]
		pwd=info[1]
		if user=="" and pwd=="":#canceled
			return()
		r1=requests.get(url1,auth=HttpNtlmAuth(user,pwd))
		res1= r1.status_code


	if output_file_name_path[0].isalpha()==False:#Not start like c
		output_file_name_path=os.getcwd()+output_file_name_path
		
	output_file=os.path.split(output_file_name_path)[1]
	output_file_directory=os.path.split(output_file_name_path)[0]

	if not os.path.exists(output_file_directory):
		print ("The directory of "+output_file_directory+" dose not exist. Please double check the file directory name.\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showwarning('Warning',"The directory of " +output_file_directory+" dose not exist. Please double check the file directory name.")
		sys.exit()
		
# get url file modification time
	c1=r1.headers
	time1=datetime.datetime.strptime(c1 ['Last-Modified'], GMT_FORMAT)
	timeArray1 = time.strptime(str(time1), "%Y-%m-%d %H:%M:%S")
	url1timestamp = int(time.mktime(timeArray1))
	
# if the file in target directory does not exit, download file dircetly from url
	if not os.path.exists(output_file_name_path):		
		print (output_file+" dose not exist. Start downloading "+ output_file +" from provided URL1\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', output_file+" dose not exist. Start downloading "+ output_file +" from provided URL.")
		with open(output_file_name_path, "wb") as code:
			code.write(r1.content)
		print (output_file+" is downloaded successful\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', output_file+" is downloaded successful.")
		return (0)

# if file exits, get the local file's modification time
	output_filetimestamp=int(os.path.getmtime(output_file_name_path))
	#print ('file time')
	#print (output_filetimestamp)
# if local file is older than url file, start updating file
	if output_filetimestamp > url1timestamp:
		print ("The "+output_file +" in your local directory is the lastest version.\n")

	else:
		print ("A new version of " +output_file+" is found. Start downloading the new version of "+ output_file +" from provided URL.\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', "A new version of " +output_file+" is found. Start downloading the new version of "+ output_file +" from provided URL.")
		with open(output_file_name_path, "wb") as code:
			code.write(r1.content)
		print (output_file+" is updated successful.\n")
		root1=tkinter.Tk()
		root1.withdraw()
		tkinter.messagebox.showinfo('Information', output_file+" is updated successful.")




#IT_OS_fileupdate_from_sharepoint ('g707414','#Bisctac','http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/PeeringPolicy.csv','\\PeeringPolicy.csv','\\c.txt')
IT_OS_fileupdate_from_sharepoint ('g707414','#Bisctac','http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/PeeringPolicy.csv','\\PeeringPolicy.csv')

