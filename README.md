# SignTool, a utility to help you re-sign your binary.

Xcode makes building your application and submit it to AppStore easy. After selecting "Archive" from the menu, Xode builds a release verison and signs your binary, what you need to do then is to just click on the "submit" button. However, sometimes you just need to re-sign your exising binary using another identity.

You can use a command line tool to do it, the command is "codesign -s IDENTIFY PATH_TO_YOUR_APP", but a GUI tool can make the task more friendly. That is why SignTool is built.

## How to use it?

1. Drag and drop your Xcode archive to SignTool's window.
2. Select a new identity for code signing.
3. Click on the "re-sign" button. Done!

Easy, right?
