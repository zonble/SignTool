from Foundation import *
from AppKit import *
import os, os.path

class STDropView(NSView):
	def initWithFrame_(self, frame):
		self = super(STDropView, self).initWithFrame_(frame)
		if self:
			self.registerForDraggedTypes_([NSFilenamesPboardType])
			self.image = None
			self.filename = None
			self.receivingFile = False
			self.delegate = None
		return self
	
	def drawRect_(self, rect):
		b = NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(self.bounds(), 10.0, 10.0)
		color = NSColor.yellowColor() if self.receivingFile \
			else NSColor.colorWithCalibratedHue_saturation_brightness_alpha_(0.0, 0.0, 1.0, 0.5)
		color.setFill()
		b.fill()
		if self.image:
			frame = NSMakeRect((self.bounds().size.width - 128) / 2 , (self.bounds().size.height - 128) / 2, 128, 128)
			self.image.drawInRect_fromRect_operation_fraction_(frame, NSZeroRect, NSCompositeSourceOver, 1.0)
		if self.filename:
			frame = NSMakeRect(10, 7, self.bounds().size.width - 20, 16)
			paragraphStyle = NSMutableParagraphStyle.alloc().init()
			paragraphStyle.setAlignment_(NSCenterTextAlignment)
			paragraphStyle.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
			attr = {NSFontAttributeName:NSFont.systemFontOfSize_(12),
				NSParagraphStyleAttributeName:paragraphStyle
			}
			attributedString = NSAttributedString.alloc().initWithString_attributes_(self.filename, attr)
			attributedString.drawInRect_(frame)

		NSColor.darkGrayColor().setStroke()
		b.stroke()
		
	def draggingEntered_(self, sender):
		self.receivingFile = True
		self.setNeedsDisplay_(True)
		if NSFilenamesPboardType in sender.draggingPasteboard().types():
			list = sender.draggingPasteboard().propertyListForType_(NSFilenamesPboardType)
			try:
				if len(list) > 1: return NSDragOperationNone
				if os.path.splitext(list[0])[1][1:] != "xcarchive": return NSDragOperationNone
				if os.path.isdir(os.path.abspath(list[0])) == False: return NSDragOperationNone
			except:
				pass
			return NSDragOperationGeneric
		return NSDragOperationNone

	def draggingExited_(self, sender):
		self.receivingFile = False
		self.setNeedsDisplay_(True)

	def performDragOperation_(self, sender):
		self.receivingFile = False
		self.setNeedsDisplay_(True)
		if NSFilenamesPboardType in sender.draggingPasteboard().types():
			list = sender.draggingPasteboard().propertyListForType_(NSFilenamesPboardType)
			try:
				if len(list) > 1: return NSDragOperationNone
				if os.path.splitext(list[0])[1][1:] != "xcarchive": return False
				if os.path.isdir(os.path.abspath(list[0])) == False: return False
				return self.delegate.dropView_didReceiveFile_(self, list[0])			
			except:
				pass
		return False