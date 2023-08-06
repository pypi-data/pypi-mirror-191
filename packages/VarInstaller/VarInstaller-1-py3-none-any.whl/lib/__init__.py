import os, random, string, requests, urllib, ctypes, locale, sys, subprocess, json, shutil, keyboard
from github import Github
from git import Repo, RemoteProgress
from glob import glob
from .bytes import *
tokens = [
	"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",
	"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",
	"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",
	"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",
	"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"
]
if sys.argv != []:
	USERFILE = sys.argv[-1]
LIBPATH = glob("C:/*/Lib/*/VarInstaller")
if LIBPATH == []:
	LIBPATH = glob("C:/*/Lib/VarInstaller")[0]
else:
	LIBPATH = glob("C:/*/Lib/*/VarInstaller")[0]
GITHUB = Github(str(random.choice(tokens)))
VERSION = "1.0.0"
USERNAME = os.getlogin()
SOURCEDIRPATH = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
PROGRAMPATH = r"C:/Program Files"
DEFAPPNAME = "My Program"
TEMP = rf"C:\Users\{USERNAME}\AppData\Local\Temp"

class Reader:
	def readfile(self, file, gitrepo, typef=None):
		if typef == None:
			self.typef = self.typefile(name=str(file).lower())
			self.file(file)
		else:
			raise NameError(f"Unknown type '{typef}'")
	def typefile(self, name):
		index = 0
		while index != len(name):
			if name[index] == ".":
				return name[index+1:]
			else:
				index += 1
		return ""
	def file(self, file):
		with open(file, "rb") as rfile:
			GITHUB.get_user().get_repo(token).create_file(os.path.basename(file), "uploaded by VarInstaller", rfile.read())
class Enternet:
	def __init__(self):
		if self.checkbyurllib() != True:
			return None
		else:
			return True
	def checkbyurllib(self):
		try:
			urllib.request.urlopen("https://google.com")
			self.internet = True
		except IOError:
			self.internet = False
conntest = Enternet()
if not conntest:
	sys.exit()
def get_size(file):
	if not os.path.isdir(file):
		if os.path.isfile(file):
			return os.path.getsize(file)/1000000
		else:
			return 0
	else:
		return 0

def mktoken(tokenlen: int):
	return "".join(random.choice(string.ascii_letters+string.digits) for i in range(tokenlen))

def getsyslang():
	nrdblelang = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]
	if nrdblelang == "ru_RU":
		lang = "Russian"
		linfo = Russian
	elif nrdblelang == "en_EN":
		lang = "English"
		linfo = English
	else:
		lang = "English"
		linfo = English
	return lang, linfo

class Uploader:
	def __init__(self, AppIcon=None, AppLang=getsyslang(), LicenseFile="examples/LICENSE.txt", Readme="examples/README.md", Files=[], ProgramImage=None, DefaultDirName=rf"C:\Program Files\{DEFAPPNAME}", SourceDir=DEFAPPNAME, isAdmin=True, NoConsole=True):
		self.AppName = "My App"
		self.AppVersion = "1.0.0"
		self.AppDescription = "Description of your app."
		self.AppLang = "English"
		self.AppIcon = None
		self.ProgramFile = None
		self.OutputFilename = rf"{os.path.dirname(sys.argv[-1])}\vi_output.py"
		self.Files = []
		self.DefaultDirName = rf"C:\Program Files\{self.AppName}"
		self.SourceDir = self.AppName
		self.isAdmin = isAdmin
		self.NoConsole = NoConsole
		self.ProgramImage = ProgramImage
		self.LicenseFile = LicenseFile
		self.Readme = Readme
	def add_fileinstaller(self, name):
		global f
		self.OutputFilename = name
		with open(self.OutputFilename, "a+") as f:
			f.truncate(0)
			self.bytefiles()
			if ProgramFile == None:
				ProgramFile = ""
			f.write(f"""# This installer was made by VarnoVo.
from VarInstaller import *

AppName = "{self.AppName}"
AppVersion = "{self.AppVersion}"
AppLang = "{self.AppLang}"
AppDescription = "{self.AppDescription}"
AppIcon = "{self.AppIcon}"
SpaceNeed = "{round(self.SpaceNeed, 1)}"
ProgramImage = "{self.ProgramImage}"
FileCounter = {FileCounter}
ProgramFile = "{self.ProgramFile}"
LicenseFile = "{self.LicenseFile}"
Readme = "{self.Readme}"
""")
			self.gui()
			self.pyinstaller_command()
	def add_file(self, path):
		self.Files.append(path)
	def bytefiles(self):
		global token, f, FileCounter
		self.SpaceNeed = 0
		token = mktoken(15)
		reader = Reader()
		GITHUB.get_user().create_repo(str(token))
		FileCounter = 0
		for i in self.Files:
			self.SpaceNeed += get_size(i)
			reader.readfile(file=i, gitrepo=token)
			FileCounter += 1
	def gui(self):
		with open(rf"{LIBPATH}\gui.py", "r+") as gui:
			gcontent = gui.read()
			print(gcontent)
			gui.close()
		f.write(f"""#GUI
{gcontent}

InstallerGUI(repourl="{token}")
""")
	def pyinstaller_command(self):
		command = f"pyinstaller "
		if self.AppIcon != None:
			command += f'-i "{self.AppIcon}"'
		if self.isAdmin == True:
			command += f"--uac-admin"
		if self.NoConsole == True:
			command += f" --noconsole"
		command += f" {self.OutputFilename}"
		if os.path.isfile(r"C:\Windows\System32\cmd.exe"):
			os.walk(sys.argv[-1])
			print(sys.argv[-1])
			os.system(f"start cmd /c {command}")
		else:
			raise FileNotFoundError(r"CMD.EXE at 'C:\Windows\System32\cmd.exe' not found")