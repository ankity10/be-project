import time,sys,shelve
import os.path

class file_class(object):

	def __init__(self):
		self.name=str
		self.content=str

	def create(self,file_name):
		self.inode_no=str(time.time())
		self.name=file_name
		self.content=""

	def copy(self,source,destination):
		src=open(source,"r")
		self.name=destination
		self.inode_no=str(time.time())
		self.content=src.read()

	def echo(self):
		print self.content



#f.create("b.txt")
io=shelve.open("textfs.sys",writeback=True)
print "COMMANDS:create,delete,echo,copy"
cmd=raw_input(">").split()

while(cmd[0]!="exit"):

	if cmd[0]=="create":
		if len(cmd)==1:
			print "Arguments incorrect. "
			print "Correct command: create filename"
		else:
			for i in range(1,len(cmd)):
				found=0
				for inode_no, obj in io.items():
					if obj.name==cmd[i]:
						found=1
						break
				if found:
					print "File "+cmd[i]+" already exists!"
				else:
					f=file_class()
					f.create(cmd[i])
					io[f.inode_no]=f
					print "File "+cmd[i]+" created!"
					io.sync()

	elif cmd[0]=="copy":
		if len(cmd)==3:
			found=0
			for inode_no, obj in io.items():
				if obj.name==cmd[2]:
					found=1
					break
			if found==1:
				print "File "+cmd[2]+" already exists!"
			else:
				if os.path.isfile(cmd[1]):	
					f=file_class()
					f.copy(cmd[1],cmd[2])
					io[f.inode_no]=f
					io.sync()
					print len(io.items())
				else:
					print "File "+cmd[1]+" doesn't exist!"

		else:
			print "Arguments incorrect. "
			print "Correct command: copy source destination"

	elif cmd[0]=="echo":
		if len(cmd)==2:
			found=0
			for inode_no,obj in io.items():
				if obj.name==cmd[1] :
					obj.echo()
					found=1
			if found==0:
				print "File not found"

		else:
			print "Arguments incorrect. "
			print "Correct command: echo filename"

	elif cmd[0]=="delete":
		if len(cmd)==2:	
			found=0
			for inode_no,obj in io.items():
				if obj.name==cmd[1]:
					del io[obj.inode_no]
					io.sync()

		else:
			print "Arguments incorrect. "
			print "Correct command: delete filename"

	elif cmd[0]=="ls":
		if len(cmd)==1:
			for inode_no,obj in io.items():
				print obj.name

		else:
			print "Arguments incorrect. "
			print "Correct command: ls"


	else:
		print "Invalid Command"

	cmd=raw_input(">").split()

io.sync()	
