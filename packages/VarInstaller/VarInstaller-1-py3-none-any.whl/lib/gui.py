from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import Frame as TkFrame
from tkinter.ttk import Button as PushButton
from tkinter.ttk import Style, Progressbar
from VarInstaller import *
from PIL import ImageTk
from PIL import Image as PILImage
import io, os, sys
from multiprocessing.dummy import Process

def getvar(name):
    lst = name.strip().split(";")
    newlist = []
    for i in lst:
        if i != "\n" or i != "":
            if i[:1] == "\n":
                newlist.append(i[1:])
            else:
                newlist.append(i)
    contlist = {}
    for i in newlist:
        content = i.split("=")
        contlist[content[0]] = content[-1]
    return contlist

def stringinsert(strdef, strin):
	index = 0
	while index != len(strdef):
		if strdef[index] == "%":
			return strdef[:index]+str(strin)+strdef[index+1:]
		else:
			index += 1

token = mktoken(10)
if LicenseFile != None:
	with open(LicenseFile, "r+") as l:
		LICENSE = l.read()
		l.close()
else:
	LICENSE = """GNU GENERAL PUBLIC LICENSE
Version 2, June 1991

Copyright (C) 1989, 1991 Free Software Foundation, Inc.  
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
Preamble
The licenses for most software are designed to take away your freedom to share and change it. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change free software--to make sure the software is free for all its users. This General Public License applies to most of the Free Software Foundation's software and to any other program whose authors commit to using it. (Some other Free Software Foundation software is covered by the GNU Lesser General Public License instead.) You can apply it to your programs, too.

When we speak of free software, we are referring to freedom, not price. Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for this service if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs; and that you know you can do these things.

To protect your rights, we need to make restrictions that forbid anyone to deny you these rights or to ask you to surrender the rights. These restrictions translate to certain responsibilities for you if you distribute copies of the software, or if you modify it.

For example, if you distribute copies of such a program, whether gratis or for a fee, you must give the recipients all the rights that you have. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights.

We protect your rights with two steps: (1) copyright the software, and (2) offer you this license which gives you legal permission to copy, distribute and/or modify the software.

Also, for each author's protection and ours, we want to make certain that everyone understands that there is no warranty for this free software. If the software is modified by someone else and passed on, we want its recipients to know that what they have is not the original, so that any problems introduced by others will not reflect on the original authors' reputations.

Finally, any free program is threatened constantly by software patents. We wish to avoid the danger that redistributors of a free program will individually obtain patent licenses, in effect making the program proprietary. To prevent this, we have made it clear that any patent must be licensed for everyone's free use or not licensed at all.

The precise terms and conditions for copying, distribution and modification follow.

TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
0. This License applies to any program or other work which contains a notice placed by the copyright holder saying it may be distributed under the terms of this General Public License. The "Program", below, refers to any such program or work, and a "work based on the Program" means either the Program or any derivative work under copyright law: that is to say, a work containing the Program or a portion of it, either verbatim or with modifications and/or translated into another language. (Hereinafter, translation is included without limitation in the term "modification".) Each licensee is addressed as "you".

Activities other than copying, distribution and modification are not covered by this License; they are outside its scope. The act of running the Program is not restricted, and the output from the Program is covered only if its contents constitute a work based on the Program (independent of having been made by running the Program). Whether that is true depends on what the Program does.

1. You may copy and distribute verbatim copies of the Program's source code as you receive it, in any medium, provided that you conspicuously and appropriately publish on each copy an appropriate copyright notice and disclaimer of warranty; keep intact all the notices that refer to this License and to the absence of any warranty; and give any other recipients of the Program a copy of this License along with the Program.

You may charge a fee for the physical act of transferring a copy, and you may at your option offer warranty protection in exchange for a fee.

2. You may modify your copy or copies of the Program or any portion of it, thus forming a work based on the Program, and copy and distribute such modifications or work under the terms of Section 1 above, provided that you also meet all of these conditions:

a) You must cause the modified files to carry prominent notices stating that you changed the files and the date of any change.
b) You must cause any work that you distribute or publish, that in whole or in part contains or is derived from the Program or any part thereof, to be licensed as a whole at no charge to all third parties under the terms of this License.
c) If the modified program normally reads commands interactively when run, you must cause it, when started running for such interactive use in the most ordinary way, to print or display an announcement including an appropriate copyright notice and a notice that there is no warranty (or else, saying that you provide a warranty) and that users may redistribute the program under these conditions, and telling the user how to view a copy of this License. (Exception: if the Program itself is interactive but does not normally print such an announcement, your work based on the Program is not required to print an announcement.)
These requirements apply to the modified work as a whole. If identifiable sections of that work are not derived from the Program, and can be reasonably considered independent and separate works in themselves, then this License, and its terms, do not apply to those sections when you distribute them as separate works. But when you distribute the same sections as part of a whole which is a work based on the Program, the distribution of the whole must be on the terms of this License, whose permissions for other licensees extend to the entire whole, and thus to each and every part regardless of who wrote it.

Thus, it is not the intent of this section to claim rights or contest your rights to work written entirely by you; rather, the intent is to exercise the right to control the distribution of derivative or collective works based on the Program.

In addition, mere aggregation of another work not based on the Program with the Program (or with a work based on the Program) on a volume of a storage or distribution medium does not bring the other work under the scope of this License.

3. You may copy and distribute the Program (or a work based on it, under Section 2) in object code or executable form under the terms of Sections 1 and 2 above provided that you also do one of the following:

a) Accompany it with the complete corresponding machine-readable source code, which must be distributed under the terms of Sections 1 and 2 above on a medium customarily used for software interchange; or,
b) Accompany it with a written offer, valid for at least three years, to give any third party, for a charge no more than your cost of physically performing source distribution, a complete machine-readable copy of the corresponding source code, to be distributed under the terms of Sections 1 and 2 above on a medium customarily used for software interchange; or,
c) Accompany it with the information you received as to the offer to distribute corresponding source code. (This alternative is allowed only for noncommercial distribution and only if you received the program in object code or executable form with such an offer, in accord with Subsection b above.)
The source code for a work means the preferred form of the work for making modifications to it. For an executable work, complete source code means all the source code for all modules it contains, plus any associated interface definition files, plus the scripts used to control compilation and installation of the executable. However, as a special exception, the source code distributed need not include anything that is normally distributed (in either source or binary form) with the major components (compiler, kernel, and so on) of the operating system on which the executable runs, unless that component itself accompanies the executable.

If distribution of executable or object code is made by offering access to copy from a designated place, then offering equivalent access to copy the source code from the same place counts as distribution of the source code, even though third parties are not compelled to copy the source along with the object code.

4. You may not copy, modify, sublicense, or distribute the Program except as expressly provided under this License. Any attempt otherwise to copy, modify, sublicense or distribute the Program is void, and will automatically terminate your rights under this License. However, parties who have received copies, or rights, from you under this License will not have their licenses terminated so long as such parties remain in full compliance.

5. You are not required to accept this License, since you have not signed it. However, nothing else grants you permission to modify or distribute the Program or its derivative works. These actions are prohibited by law if you do not accept this License. Therefore, by modifying or distributing the Program (or any work based on the Program), you indicate your acceptance of this License to do so, and all its terms and conditions for copying, distributing or modifying the Program or works based on it.

6. Each time you redistribute the Program (or any work based on the Program), the recipient automatically receives a license from the original licensor to copy, distribute or modify the Program subject to these terms and conditions. You may not impose any further restrictions on the recipients' exercise of the rights granted herein. You are not responsible for enforcing compliance by third parties to this License.

7. If, as a consequence of a court judgment or allegation of patent infringement or for any other reason (not limited to patent issues), conditions are imposed on you (whether by court order, agreement or otherwise) that contradict the conditions of this License, they do not excuse you from the conditions of this License. If you cannot distribute so as to satisfy simultaneously your obligations under this License and any other pertinent obligations, then as a consequence you may not distribute the Program at all. For example, if a patent license would not permit royalty-free redistribution of the Program by all those who receive copies directly or indirectly through you, then the only way you could satisfy both it and this License would be to refrain entirely from distribution of the Program.

If any portion of this section is held invalid or unenforceable under any particular circumstance, the balance of the section is intended to apply and the section as a whole is intended to apply in other circumstances.

It is not the purpose of this section to induce you to infringe any patents or other property right claims or to contest validity of any such claims; this section has the sole purpose of protecting the integrity of the free software distribution system, which is implemented by public license practices. Many people have made generous contributions to the wide range of software distributed through that system in reliance on consistent application of that system; it is up to the author/donor to decide if he or she is willing to distribute software through any other system and a licensee cannot impose that choice.

This section is intended to make thoroughly clear what is believed to be a consequence of the rest of this License.

8. If the distribution and/or use of the Program is restricted in certain countries either by patents or by copyrighted interfaces, the original copyright holder who places the Program under this License may add an explicit geographical distribution limitation excluding those countries, so that distribution is permitted only in or among countries not thus excluded. In such case, this License incorporates the limitation as if written in the body of this License.

9. The Free Software Foundation may publish revised and/or new versions of the General Public License from time to time. Such new versions will be similar in spirit to the present version, but may differ in detail to address new problems or concerns.

Each version is given a distinguishing version number. If the Program specifies a version number of this License which applies to it and "any later version", you have the option of following the terms and conditions either of that version or of any later version published by the Free Software Foundation. If the Program does not specify a version number of this License, you may choose any version ever published by the Free Software Foundation.

10. If you wish to incorporate parts of the Program into other free programs whose distribution conditions are different, write to the author to ask for permission. For software which is copyrighted by the Free Software Foundation, write to the Free Software Foundation; we sometimes make exceptions for this. Our decision will be guided by the two goals of preserving the free status of all derivatives of our free software and of promoting the sharing and reuse of software generally.

NO WARRANTY

11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

END OF TERMS AND CONDITIONS
How to Apply These Terms to Your New Programs
If you develop a new program, and you want it to be of the greatest possible use to the public, the best way to achieve this is to make it free software which everyone can redistribute and change under these terms.

To do so, attach the following notices to the program. It is safest to attach them to the start of each source file to most effectively convey the exclusion of warranty; and each file should have at least the "copyright" line and a pointer to where the full notice is found.

one line to give the program's name and an idea of what it does.
Copyright (C) yyyy  name of author

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
Also add information on how to contact you by electronic and paper mail.

If the program is interactive, make it output a short notice like this when it starts in an interactive mode:

Gnomovision version 69, Copyright (C) year name of author
Gnomovision comes with ABSOLUTELY NO WARRANTY; for details
type `show w'.  This is free software, and you are welcome
to redistribute it under certain conditions; type `show c' 
for details.
The hypothetical commands `show w' and `show c' should show the appropriate parts of the General Public License. Of course, the commands you use may be called something other than `show w' and `show c'; they could even be mouse-clicks or menu items--whatever suits your program.

You should also get your employer (if you work as a programmer) or your school, if any, to sign a "copyright disclaimer" for the program, if necessary. Here is a sample; alter the names:

Yoyodyne, Inc., hereby disclaims all copyright
interest in the program `Gnomovision'
(which makes passes at compilers) written 
by James Hacker.

signature of Ty Coon, 1 April 1989
Ty Coon, President of Vice
"""
class GitBar(RemoteProgress):
    def __init__(self, op_code, cur_count, max_count=None, message=''):
        progress["maximum"] = max_count
        progress["value"] = cur_count
        progress.update()

class CheckLang(Tk):
    def __init__(self, title, message):
        global combolang, AppLang
        super().__init__()
        self.details_expanded = False
        self.title(title)
        self.geometry('350x75')
        self.minsize(350, 75)
        self.maxsize(425, 250)
        self.resizable(False, False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.attributes('-toolwindow', True)
        name, var = getsyslang()
        ttk.Label(self, text=getvar(var).get("CheckLangMessage")).grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky='w')
        combolang = ttk.Combobox(self, values=AppLang)
        for i in AppLang:
        	if i == name:
        		combolang.current(AppLang.index(i))
        combolang.grid(row=1, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky='w')
        PushButton(self, text='OK', command=self.check).grid(row=1, column=1, sticky='e')
        # AppLang = combolang.get()
        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self.mainloop()

    def check(self):
        global AppLang
        AppLang = combolang.get()
        self.destroy()
class CommandBox(Tk):
    def __init__(self, command, message):
        global combolang, AppLang
        super().__init__()
        name, var = getsyslang()
        self.command = command
        self.details_expanded = False
        self.title("VarInstaller - "+getvar(var).get("Error"))
        self.geometry('350x75')
        self.minsize(350, 75)
        self.maxsize(425, 250)
        self.resizable(False, False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.attributes('-toolwindow', True)
        ttk.Label(self, text=getvar(var).get(message)).grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky='w')
        PushButton(self, text=getvar(var).get("OKButton"), command=self.destroy).grid(row=1, column=1, sticky='e')
        PushButton(self, text=getvar(var).get("OpenButton"), command=self.check).grid(row=1, column=2, sticky='e')
        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self.mainloop()

    def check(self):
    	subprocess.Popen(self.command)
    	self.destroy()
class InstallerGUI:
	def __init__(self, repourl, *args, **kwargs):
		global ProgramFile
		if type(AppLang) == list:
			CheckLang("VarInstaller ", "message")
		if AppLang == "Russian":
			self.LangLib = Russian
		else:
			self.LangLib = English
		if os.path.basename(ProgramFile) == str(ProgramFile):
			ProgramFile = rf"{os.path.dirname(USERFILE)}\{ProgramFile}"
		self.repourl = repourl
		self.window = Tk(*args, **kwargs)
		self.window.geometry("980x400+60+50")
		self.window.minsize(780, 400)
		self.window.resizable(0,0)
		self.window.attributes('-toolwindow', True)
		self.window.title(stringinsert(getvar(self.LangLib).get("SetupWindowTitle"), AppName))
		self.conf_temp()
		self.start_page()
		self.window.protocol("WM_DELETE_WINDOW", self.askexit)
		self.window.iconbitmap(rf"{TEMP}\{token}\icon.ico")
		self.window.mainloop()
	def desktop_shortcut(self):
		try:
			if not os.path.isdir(self.ppath):
				os.makedirs(self.ppath)
			os.link(ProgramFile, rf"C:\Users\{USERNAME}\Desktop\{AppName}.lnk")
		except (PermissionError):
			showwarning("VarInstaller - "+getvar(self.LangLib).get("Warning"), message=getvar(self.LangLib).get("PermissionError"))
	def menu_dir(self):
		try:
			os.symlink(ProgramFile, rf"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\{AppName}")
		except (PermissionError, OSError):
			showwarning("VarInstaller - "+getvar(self.LangLib).get("Warning"), message=getvar(self.LangLib).get("PermissionError"))
	def conf_temp(self):
		self.SpaceNeed = SpaceNeed
		if not os.path.isdir(rf"{TEMP}\{token}"):
			os.makedirs(rf"{TEMP}\{token}")
		if ProgramImage != None:
			if os.path.isfile(ProgramImage):
				with open(ProgramImage, "rb") as img:
					Bytes = img.read()
					with open(rf"{LIBPATH}/bytes.py", "w+") as byte:
						byte.write(f"\nBytesImage = {Bytes}")
						byte.close()
					img.close()
		with open(rf"{TEMP}\{token}\program.bmp", "ab") as f:
			f.write(BytesImage)
			f.close()
		with open(rf"{TEMP}\{token}\icon.ico", "ab") as f:
			f.write(Icon)
			f.close()
	def iftrue(self, *args):
		if self.liagreeVar.get() != True:
			self.nextButton.configure(state=DISABLED)
		elif self.liagreeVar.get() == True:
			self.nextButton.configure(state=NORMAL)
	def clear(self):
		try:
			shutil.rmtree(rf"{TEMP}\{token}")
		except PermissionError:
			CommandBox(rf'explorer /select, "{TEMP}\{token}"', "TempPermissionError")
		except:
			CommandBox(rf'explorer /select, "{TEMP}\{token}"', "TempError")
	def askexit(self):
		message = askyesno(title=getvar(self.LangLib).get("ExitSetupTitle"), message=stringinsert(getvar(self.LangLib).get("ExitSetupMessage"), AppName))
		if message == True:
			self.window.destroy()
			self.clear()
	def enddestroy(self):
		self.window.destroy()
		self.pi_atrib()
		self.clear()
	def pi_atrib(self):
		cs = self.csVar.get()
		md = self.mdVar.get()
		vr = self.vrVar.get()
		rp = self.rpVar.get()
		if type(ProgramFile) == str:
			if not md:
				p = Process(target=self.menu_dir)
				p.start()
			if cs:
				p = Process(target=self.desktop_shortcut)
				p.start()
			if rp:
				p = Process(target=subprocess.Popen, args=(ProgramFile,))
				p.start()
		if type(Readme) == str:
			if vr:
				p = Process(target=os.system, args=(Readme,))
				p.start()
	def postinstall_page(self):
		self.csVar = BooleanVar()
		self.mdVar = BooleanVar()
		self.vrVar = BooleanVar()
		self.rpVar = BooleanVar()
		self.installLabel.destroy()
		progress.destroy()
		self.topFrame.destroy()
		self.mainFrame.destroy()
		self.nextButton.destroy()
		self.canselButton.destroy()
		if ProgramImage == None:
			if not os.path.isfile(rf"{TEMP}\{token}\program.bmp"):
				with open(rf"{TEMP}\{token}\program.bmp", "ab") as f:
					f.write(BytesImage)
					f.close()
			self.image = ImageTk.PhotoImage(file=rf"{TEMP}\{token}\program.bmp")
		else:
			self.image = ImageTk.PhotoImage(file=ProgramImage)
		if type(ProgramFile) == str:
			self.prgrmImage = Label(self.window, image=self.image)
			self.prgrmImage.pack(fill="both", side=LEFT, anchor=NW)
			self.createShortcut = Checkbutton(text=getvar(self.LangLib).get("WorkTable"), variable=self.csVar)
			self.createShortcut.pack()
			self.menuDir = Checkbutton(text=getvar(self.LangLib).get("MenuDir"), variable=self.mdVar)
			self.menuDir.pack()
			self.runProgram = Checkbutton(text=stringinsert(getvar(self.LangLib).get("RunProgram"), AppName), variable=self.rpVar)
			self.runProgram.pack()
		if type(Readme) == str:
			self.viewReadme = Checkbutton(text=getvar(self.LangLib).get("ViewReadme"), variable=self.vrVar)
			self.viewReadme.pack()
		self.okButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("OKButton"), command=self.enddestroy)
		self.okButton.pack(side=RIGHT, pady=7, padx=5)
	def install(self):
		try:
			Repo.clone_from("https://github.com/VVoProd/"+self.repourl, rf"{TEMP}\{token}\{self.repourl}", progress=GitBar)
			try:
				self.installLabel.configure(text=getvar(self.LangLib).get("InstallUnpack"))
				if not os.path.isdir(self.ppath):
					os.makedirs(self.ppath)
				self.installLabel.configure(text=getvar(self.LangLib).get("InstallMove"))
				progress["value"] = 0
				progress["maximum"] = 100
				for i in os.listdir(rf"{TEMP}\{token}"):
					if os.path.isdir(rf"{TEMP}\{token}\{i}"):
						for item in os.listdir(rf"{TEMP}\{token}\{i}"):
							try:
								shutil.move(rf"{TEMP}\{token}\{i}\{item}", rf"{TEMP}\{token}\{item}")
							except FileNotFoundError:
								pass
						os.rmdir(rf"{TEMP}\{token}\{i}")
					else:
						try:
							shutil.move(rf"{TEMP}\{token}\{i}", rf"{self.ppath}\{i}")
						except FileNotFoundError:
							pass
				for i in os.listdir(rf"{TEMP}\{token}"):
					try:
						if i != "program.bmp":
							shutil.move(rf"{TEMP}\{token}\{i}", rf"{self.ppath}\{i}")
							progress["value"] += 100/FileCounter
					except:
						pass
				self.installLabel.configure(text=stringinsert(getvar(self.LangLib).get("OKInstall"), AppName))
				progress["value"] = progress["maximum"]
				self.nextButton.configure(state=NORMAL)
			except PermissionError:
				showwarning("VarInstaller - "+getvar(self.LangLib).get("Warning"), message=getvar(self.LangLib).get("PermissionError"))
			except Exception as error:
				askagain = askretrycancel("VarInstaller - "+getvar(self.LangLib).get("Warning"), message="VarInstaller - "+getvar(self.LangLib).get("InstallError"))
				if askagain:
					self.install()
		except TimeoutError:
			showerror("VarInstaller - "+getvar(self.LangLib).get("Warning"), message="VarInstaller - "+getvar(self.LangLib).get("TimeOutError"))
			self.askexit()
		except:
			askagain = askretrycancel("VarInstaller - "+getvar(self.LangLib).get("Warning"), message="VarInstaller - "+getvar(self.LangLib).get("InstallError"))
			if askagain:
				self.install()
	def install_process(self):
		ReportCreationProcess = Process(target=self.install)
		ReportCreationProcess.start()
	def browse_file(self):
		self.path = askdirectory()
		self.pathEntry.delete(0, END)
		if self.path != "" and self.path != None:
			if self.path[-1] != "/":
				self.pathEntry.insert(0, rf"{self.path}/{AppName}/")
			else:
				self.pathEntry.insert(0, self.path+AppName+"/")
	def install_page(self):
		global progress
		self.pname = self.nameEntry.get()
		self.topLabel.destroy()
		self.textLabel.destroy()
		self.cancelButton.destroy()
		self.nextButton.destroy()
		self.nameEntry.destroy()
		self.spaceLabel.destroy()
		self.installLabel = Label(self.mainFrame, text=getvar(self.LangLib).get("InstallUnpack"))
		self.installLabel.pack(fill=X, padx=3, pady=3)
		progress = Progressbar(self.mainFrame, maximum=100)
		progress.pack(fill=X, padx=3, pady=3)
		self.window.after(100, self.install_process)
		self.canselButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("CanselButton"), state=DISABLED, command=self.askexit)
		self.canselButton.pack(side=RIGHT, pady=7, padx=5)
		self.nextButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("NextButton"), state=DISABLED, command=self.postinstall_page)
		self.nextButton.pack(side=RIGHT, pady=7, padx=5)
	def name_page(self):
		self.ppath = self.pathEntry.get()
		self.topLabel.destroy()
		self.textLabel.destroy()
		self.cancelButton.destroy()
		self.nextButton.destroy()
		self.pathEntry.destroy()
		self.browseButton.destroy()
		# self.sp
		self.spaceLabel.destroy()
		self.topLabel = Label(self.topFrame, text=getvar(self.LangLib).get("NameTitle"), font=(("Fixedsys"), 25))
		self.topLabel.pack(expand=1, anchor=NW, padx=10)
		self.textLabel = Label(self.mainFrame, text=getvar(self.LangLib).get("NameText"), font=(("Fixedsys"), 13))
		self.textLabel.pack(anchor=NW, padx=3, pady=5, side=TOP)
		self.nameEntry = Entry(self.mainFrame)
		self.nameEntry.insert(0, AppName)
		self.nameEntry.pack(side=TOP, padx=5, fill=X)
		self.spaceLabel = Label(self.mainFrame, text=stringinsert(getvar(self.LangLib).get("DiskSpaceMBLabel"), self.SpaceNeed))
		self.spaceLabel.pack(side=BOTTOM, fill=X)
		self.cancelButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("CanselButton"), command=self.askexit)
		self.cancelButton.pack(side=RIGHT, pady=7, padx=5)
		self.nextButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("InstallButton"), command=self.install_page)
		self.nextButton.pack(side=RIGHT, pady=7, padx=5)
	def dir_page(self):
		self.topLabel.destroy()
		self.textLabel.destroy()
		self.licenseText.destroy()
		self.yagree.destroy()
		self.nagree.destroy()
		self.cancelButton.destroy()
		self.nextButton.destroy()
		self.topLabel = Label(self.topFrame, text=getvar(self.LangLib).get("DirTitle"), font=(("Fixedsys"), 25))
		self.topLabel.pack(expand=1, anchor=NW, padx=10)
		self.textLabel = Label(self.mainFrame, text=stringinsert(getvar(self.LangLib).get("DirPTitle"), AppName), font=(("Fixedsys"), 13))
		self.textLabel.pack(anchor=NW, padx=3, pady=5, side=TOP)
		self.pathEntry = Entry(self.mainFrame)
		self.pathEntry.insert(0, rf"{PROGRAMPATH}/{AppName}")
		self.pathEntry.pack(side=TOP, padx=5, fill=X)
		self.browseButton = PushButton(self.mainFrame, text="Browse", command=self.browse_file)
		self.browseButton.pack(fill=X, side=TOP, padx=5)
		self.spaceLabel = Label(self.mainFrame, text=stringinsert(getvar(self.LangLib).get("DiskSpaceMBLabel"), self.SpaceNeed))
		self.spaceLabel.pack(side=BOTTOM, fill=X)
		self.cancelButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("CanselButton"), command=self.askexit)
		self.cancelButton.pack(side=RIGHT, pady=7, padx=5)
		self.nextButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("NextButton"), command=self.name_page)
		self.nextButton.pack(side=RIGHT, pady=7, padx=5)
	def license_page(self):
		self.topLabel.destroy()
		self.textLabel.destroy()
		self.prgrmImage.destroy()
		self.cancelButton.destroy()
		self.nextButton.destroy()
		self.itextLabel.destroy()
		self.topLabel = Label(self.topFrame, text=getvar(self.LangLib).get("AgreementTitle"), font=(("Fixedsys"), 25))
		self.topLabel.pack(expand=1, anchor=NW, padx=10, pady=20)
		self.textLabel = Label(self.mainFrame, text=getvar(self.LangLib).get("AgreementPTitle"))
		self.textLabel.pack(anchor=NW, pady=3)
		self.licenseText = Text(self.mainFrame)
		self.licenseText.insert(1.0, LICENSE)
		self.licenseText.configure(state=DISABLED)
		self.licenseText.pack(side=LEFT)
		self.liagreeVar = BooleanVar()
		self.liagreeVar.set(True)
		self.yagree = Radiobutton(self.mainFrame, text=getvar(self.LangLib).get("YAgreement"), var=self.liagreeVar, value=True)
		self.yagree.pack(anchor=SW)
		self.nagree = Radiobutton(self.mainFrame, text=getvar(self.LangLib).get("NAgreement"), var=self.liagreeVar, value=False)
		self.nagree.pack(anchor=SW)
		self.liagreeVar.trace("w", self.iftrue)
		self.cancelButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("CanselButton"), command=self.askexit)
		self.cancelButton.pack(side=RIGHT, pady=7, padx=5)
		self.nextButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("NextButton"), command=self.dir_page, state=DISABLED)
		self.nextButton.pack(side=RIGHT, pady=7, padx=5)
		self.iftrue()
	def start_page(self):
		self.image = ImageTk.PhotoImage(file=rf"{TEMP}\{token}\program.bmp")
		self.prgrmImage = Label(self.window, image=self.image)
		self.prgrmImage.pack(fill="both", side=LEFT)
		self.topFrame = TkFrame(self.window)
		self.topFrame.pack(fill=X,side=TOP, anchor=SW)
		self.mainFrame = TkFrame(self.window)
		self.botFrame = TkFrame(self.window, borderwidth=2, relief=RIDGE)
		self.botFrame.pack(fill=X, side=BOTTOM)
		self.mainFrame.pack(expand=1, fill="both")
		self.topLabel = Label(self.topFrame, text=stringinsert(getvar(self.LangLib).get("StartTitle"), AppName), font=(("Fixedsys"), 25))
		self.topLabel.pack(expand=1, anchor=NW)
		self.textLabel = Label(self.mainFrame, text=stringinsert(getvar(self.LangLib).get("StartText"), AppName))
		self.textLabel.pack(anchor=NW)
		self.itextLabel = Label(self.mainFrame, text=getvar(self.LangLib).get("IStartText"))
		self.itextLabel.pack(anchor=NW)
		self.cancelButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("CanselButton"), command=self.askexit)
		self.cancelButton.pack(side=RIGHT, pady=7, padx=5)
		self.nextButton = PushButton(self.botFrame, text=getvar(self.LangLib).get("NextButton"), command=self.license_page)
		self.nextButton.pack(side=RIGHT, pady=7, padx=5)