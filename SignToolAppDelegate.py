from Foundation import *
from AppKit import *
import os, os.path
import subprocess
import STDropView

class SignToolAppDelegate(NSObject):
	window = objc.IBOutlet()
	dropView = objc.IBOutlet()
	comboBox = objc.IBOutlet()
	resignButton = objc.IBOutlet()
	infoLabel = objc.IBOutlet()
	
	sheet = objc.IBOutlet()
	sheetCloseButton = objc.IBOutlet()
	sheetTextLabel = objc.IBOutlet()

	currentArchiveFilepath = None
	currentArchiveAppFilepath = None

	def awakeFromNib(self):
		self.infoLabel.setStringValue_("")
		self.window.setDelegate_(self)
		self.window.setDefaultButtonCell_(self.resignButton.cell())
		self.resignButton.setEnabled_(False)
		self.infoLabel.setFont_(NSFont.systemFontOfSize_(11))
		self.sheet.setDefaultButtonCell_(self.sheetCloseButton.cell())
		self.window.center()

	def applicationDidFinishLaunching_(self, sender):
		self.dropView.delegate = self
		lastUsedIndentity = NSUserDefaults.standardUserDefaults().stringForKey_("lastIdentity")
		if lastUsedIndentity == None:
			lastUsedIndentity = "iPhone Distribution"
			NSUserDefaults.standardUserDefaults().setObject_forKey_(lastUsedIndentity, "lastIdentity")
		self.comboBox.setStringValue_(lastUsedIndentity)
		self.comboBox.addItemsWithObjectValues_(["iPhone Distribution", "iPhone Developer"])

	def updateCodeSignInfo(self):
		cmd = "codesign --display --verbose=4 \"" + self.currentArchiveAppFilepath + "\""
		try:
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			lines = ""
			while True:
				line = p.stderr.readline()
				if not line: break
				line = line.strip()
				if len(line): lines += line + "\n"
			self.infoLabel.setStringValue_(lines)
		except:
			pass
			
	def handleOpenFile(self, inFile):
		appsFolder = os.path.join(inFile, "Products", "Applications")
		dirs = os.listdir(appsFolder)
		appDir = None
		for dir in dirs:
			if os.path.splitext(dir)[1][1:] == "app": appDir = dir; break
		if appDir == None:
			alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_("This is not a valid Xcode archive!", "OK", None, None, "We are not able to find an application bundle within the archive.")
			alert.runModal()
			return False

		self.currentArchiveFilepath = inFile
		self.currentArchiveAppFilepath = os.path.join(appsFolder, appDir)
		self.updateCodeSignInfo()
		self.resignButton.setEnabled_(True)
		
		image = NSWorkspace.sharedWorkspace().iconForFile_(inFile)
		filename = os.path.basename(inFile)
		self.dropView.image = image
		self.dropView.filename = filename
		self.dropView.setNeedsDisplay_(True)
		return True

	@objc.IBAction
	def open_(self, sender):
		panel = NSOpenPanel.openPanel()
		panel.setAllowedFileTypes_(["xcarchive"])
		panel.setCanChooseFiles_(True)
		panel.setCanChooseDirectories_(False)
		panel.setAllowsOtherFileTypes_(False)
		
		panel.beginSheetForDirectory_file_types_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
			os.path.expanduser("~/Library/Developer/Xcode/Archives"), None, ["xcarchive"], self.window,
			self, objc.selector(self.openPanelDidEnd_returnCode_contextInfo_, signature = 'v@:I'), None)

	def openPanelDidEnd_returnCode_contextInfo_(self, panel, returnCode, contextInfo):
		filenames = panel.filenames()
		if len(filenames) < 1: return
		self.handleOpenFile(filenames[0])

	@objc.IBAction
	def changeCodeSign_(self, sender):
		if not self.currentArchiveAppFilepath:
			alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_("You did not specify a Xcode archive bundle!", "OK", None, None, "Please select a Xcode archive and try again")
			alert.beginSheetModalForWindow_modalDelegate_didEndSelector_contextInfo_(self.window, None, None, None)
			return
		identity = self.comboBox.stringValue()
		if len(identity) == 0:
			alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_("You did not specify an identity!", "OK", None, None, "Please select an identity and try again")
			alert.beginSheetModalForWindow_modalDelegate_didEndSelector_contextInfo_(self.window, None, None, None)
			return

		self.sheetCloseButton.setEnabled_(False)
		self.sheetTextLabel.setStringValue_("")
		NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(self.sheet, self.window, None, None, None)
		self.sheet.orderFront_(self)

		cmd = "codesign -f -vv -s \"" + identity + "\" \"" + self.currentArchiveAppFilepath + "\""
		try:
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			lines = ""
			while True:
				line = p.stderr.readline()
				if not line: break
				line = line.strip()
				if len(line): lines += line + "\n"
				self.sheetTextLabel.setStringValue_(lines)
		except:
			pass
		self.updateCodeSignInfo()
		self.sheetCloseButton.setEnabled_(True)

	@objc.IBAction
	def closeSheet_(self, sender):
		NSApp.endSheet_(self.sheet)
		self.sheet.orderOut_(self)
		
	@objc.IBAction
	def openHomepage_(self, sender):
		url = NSURL.URLWithString_("https://github.com/zonble/SignTool")
		NSWorkspace.sharedWorkspace().openURL_(url)

	def dropView_didReceiveFile_(self, inDropView, inFile):
		return self.handleOpenFile(inFile)		
		
	def windowWillClose_(self, notification):
		NSApp.terminate_(self)
