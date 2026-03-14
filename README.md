# SignTool

> **⚠️ This project is archived and no longer maintained.** It is kept here for historical reference only.

SignTool is a macOS GUI utility for re-signing iOS application archives (.xcarchive files). It was created in **October 2011** to provide a friendlier alternative to using the `codesign` command-line tool directly.

Xcode makes building and submitting your application to the App Store easy. After selecting "Archive" from the menu, Xcode builds a release version and signs your binary, and all you need to do is click the "Submit" button. However, sometimes you need to re-sign an existing binary using a different identity — for example when distributing an archive to a third party or switching between development and distribution certificates. SignTool was built to make that task simple with a drag-and-drop interface.

## Technical Details

- **Language**: Python (via [PyObjC](https://pyobjc.readthedocs.io/)), with a thin Objective-C entry point (`main.m`)
- **Framework**: Cocoa/AppKit
- **Version**: 0.1
- **Bundle ID**: `net.zonble.SignTool`
- **Target platform**: macOS 10.5 (Leopard), 32-bit (ppc/i386)

### Project Structure

| File | Description |
|------|-------------|
| `main.m` | Objective-C entry point; sets up the Python environment and runs `main.py` |
| `main.py` | Python entry point; starts the Cocoa event loop via PyObjC |
| `SignToolAppDelegate.py` | Main application logic: handles file opening, displays signing info, and runs `codesign` |
| `STDropView.py` | Custom `NSView` subclass that accepts drag-and-drop of `.xcarchive` files |
| `English.lproj/MainMenu.xib` | Main window and menu UI layout |
| `Info.plist` | Application bundle metadata |
| `SignTool.xcodeproj` | Xcode project file |

## How to Build

1. Open `SignTool.xcodeproj` in Xcode.
2. Select **Product > Build** (or press `⌘B`).
3. The built `SignTool.app` will appear in the `build/` directory (or `~/Applications` for Release builds).

> **Note**: The project targets macOS 10.5 with a 32-bit architecture and requires the system Python framework (`/System/Library/Frameworks/Python.framework`) along with PyObjC. It was developed against Xcode 3 and the macOS 10.5 SDK. Building on modern macOS versions is not supported.

## How to Use

1. Drag and drop your Xcode archive (`.xcarchive`) onto SignTool's window, or use **File > Open** to browse for one.
2. The app will display the current code-signing information for the archive's application bundle.
3. Enter or select the signing identity you want to use (e.g. `iPhone Distribution` or `iPhone Developer`).
4. Click the **Re-sign** button.

The app invokes `codesign -f -vv -s "<identity>" "<path to .app>"` under the hood and displays the output.
