#!/usr/bin/env python
# encoding: utf-8

'''
• See OPTION below to either use Label Size or Whole Glyph Body.
'''

# TODO:
#	add clipping path https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/#//apple_ref/doc/uid/20000339-SW27

import objc
from Foundation import *
from AppKit import *
import sys, os, re
import math
import traceback

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

#### OTIONS ++++++++++++++++++++++++++++++++++++++++++
#### #######++++++++++++++++++++++++++++++++++++++++++
# drawingOption = "Label Size"
drawingOption = "Label Size Descender"
# drawingOption = "Full Glyph Body"
#### #######++++++++++++++++++++++++++++++++++++++++++
#### #######++++++++++++++++++++++++++++++++++++++++++


alpha = .9
labelColorsDict = {
	0 : (0.93, 0.57, 0.47, alpha), # red
	1 : (0.98, 0.79, 0.51, alpha), # orange
	2 : (0.84, 0.76, 0.62, alpha), # brown
	3 : (0.98, 0.98, 0.51, alpha), # yellow
	4 : (0.80, 0.96, 0.63, alpha), # light green
	5 : (0.48, 0.76, 0.46, alpha), # dark green
	6 : (0.47, 0.82, 0.96, alpha), # light blue
	7 : (0.60, 0.61, 0.91, alpha), # dark blue
	8 : (0.71, 0.52, 0.89, alpha), # purple
	9 : (0.98, 0.63, 0.82, alpha), # magenta
	10 : (0.86, 0.86, 0.86, alpha), # light gray
	11 : (0.56, 0.56, 0.56, alpha), # charcoal
	9223372036854775807 : (1, 1, 1, 0), # not colored, white
}


GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class LabelColor ( NSObject, GlyphsReporterProtocol ):
	def init( self ):
		"""
		Put any initializations you want to make here.
		"""
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
		
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return "* Label Color"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		"""
		Use any combination of these to determine the modifier keys for your default shortcut:
			return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		Or:
			return 0
		... if you do not want to set a shortcut.
		"""
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def drawForegroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		Setting a color:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 1.0, 1.0, 1.0 ).set() # sets RGBA values between 0.0 and 1.0
			NSColor.redColor().set() # predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor, darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor, purpleColor, redColor, whiteColor, yellowColor
		Drawing a path:
			myPath = NSBezierPath.alloc().init()  # initialize a path object myPath
			myPath.appendBezierPath_( subpath )   # add subpath to myPath
			myPath.fill()   # fill myPath with the current NSColor
			myPath.stroke() # stroke myPath with the current NSColor
		To get an NSBezierPath from a GSPath, use the bezierPath() method:
			myPath.bezierPath().fill()
		You can apply that to a full layer at once:
			if len( myLayer.paths > 0 ):
				myLayer.bezierPath()       # all closed paths
				myLayer.openBezierPath()   # all open paths
		See:
		https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
		https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html
		"""
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )
	

	def BlockOutGlyph( self, Layer ):
		if drawingOption == "Label Size":
			pass
		elif drawingOption == "Full Glyph Body":
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1, 1, 1, 1 ).set()
			thisGlyphPath = Layer.copyDecomposedLayer().bezierPath()
			if thisGlyphPath:
				thisGlyphPath.fill()

	
	def LabelColor( self, Layer ):
		try:
			try:
				colorCode = Layer.parent.color
				thisColor = labelColorsDict[colorCode]
			except:
				# Glyphs 1.x or no layerColor:
				thisColor = (1, 1, 1, 0)

			try:
				layerColor = Layer.color()
			except:
				pass
			
			try:
				thisWidth = Layer.width
				thisGlyph = Layer.parent
				thisFont = thisGlyph.parent
				thisMaster = thisFont.selectedFontMaster
				thisDescender = thisMaster.descender
				thisXHeight = thisMaster.xHeight
				upm = thisFont.upm
				thisAngle = thisMaster.italicAngle

				
				NSColor.colorWithCalibratedRed_green_blue_alpha_( *thisColor ).set()


				### Italic Angle Stuff
				def angle(yPos):
					# rotation point is half of x-height
					offset = math.tan(math.radians(thisAngle)) * thisXHeight/2
					shift = math.tan(math.radians(thisAngle)) * yPos - offset
					return shift
				
				if drawingOption == "Label Size":
					rectangle = [0, 0, thisWidth, -40]
				elif drawingOption == "Label Size Descender":
					rectangle = [0, thisDescender, thisWidth, thisDescender-40]
					rectangleLeft = [0, thisDescender, thisWidth/2, thisDescender-40]
					rectangleRight = [thisWidth/2, thisDescender, thisWidth, thisDescender-40]
				elif drawingOption == "Full Glyph Body":
					ySize = upm+thisDescender
					rectangle = [0, thisDescender, thisWidth, ySize]
				


				if layerColor:				
					'''
					LEFT = Glyph-Color
					'''
					pathRectLeft = NSBezierPath.bezierPath()
					pathRectLeft.moveToPoint_( (rectangleLeft[0] + angle(rectangleLeft[1]), rectangleLeft[1]) )
					pathRectLeft.lineToPoint_( (rectangleLeft[0] + angle(rectangleLeft[3]), rectangleLeft[3]) )
					pathRectLeft.lineToPoint_( (rectangleLeft[2] + angle(rectangleLeft[3]), rectangleLeft[3]) )
					pathRectLeft.lineToPoint_( (rectangleLeft[2] + angle(rectangleLeft[1]), rectangleLeft[1]) )
					pathRectLeft.closePath()

					pathRectLeft.fill()

					'''
					RIGHT = Layer-Color
					'''
					pathRectRight = NSBezierPath.bezierPath()
					pathRectRight.moveToPoint_( (rectangleRight[0] + angle(rectangleRight[1]), rectangleRight[1]) )
					pathRectRight.lineToPoint_( (rectangleRight[0] + angle(rectangleRight[3]), rectangleRight[3]) )
					pathRectRight.lineToPoint_( (rectangleRight[2] + angle(rectangleRight[3]), rectangleRight[3]) )
					pathRectRight.lineToPoint_( (rectangleRight[2] + angle(rectangleRight[1]), rectangleRight[1]) )
					pathRectRight.closePath()

					thisLayerColor = layerColor.redComponent(), layerColor.greenComponent(), layerColor.blueComponent(), alpha #layerColor.alphaComponent()
					pathRectRight.setLineWidth_(5)
					NSColor.colorWithCalibratedRed_green_blue_alpha_( *thisLayerColor ).set()

					pathRectRight.fill()


				else:
					## using a bezier path instead of an NSRect for transforming ability
					pathRect = NSBezierPath.bezierPath()
					pathRect.moveToPoint_( (rectangle[0] + angle(rectangle[1]), rectangle[1]) )
					pathRect.lineToPoint_( (rectangle[0] + angle(rectangle[3]), rectangle[3]) )
					pathRect.lineToPoint_( (rectangle[2] + angle(rectangle[3]), rectangle[3]) )
					pathRect.lineToPoint_( (rectangle[2] + angle(rectangle[1]), rectangle[1]) )
					pathRect.closePath()

					pathRect.fill()					

			except:
				pass


		# except Exception as e:
		# 	self.logToConsole( "LabelColor: %s" % str(e) )
		except:
			self.logToConsole( "LabelColor: %s" % str(traceback.format_exc()) )
			
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			# pass
			self.LabelColor( Layer )
			# self.BlockOutGlyph( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths, but for inactive masters.
		"""
		try:
			pass
			self.LabelColor( Layer )
			# self.BlockOutGlyph( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def drawTextAtPoint( self, text, textPosition, fontSize=9.0, fontColor=NSColor.brownColor() ):
		"""
		Use self.drawTextAtPoint( "blabla", myNSPoint ) to display left-aligned text at myNSPoint.
		"""
		try:
			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 3 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except Exception as e:
			self.logToConsole( "drawTextAtPoint: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True

	
	def getHandleSize( self ):
		"""
		Returns the current handle size as set in user preferences.
		Use: self.getHandleSize() / self.getScale()
		to determine the right size for drawing on the canvas.
		"""
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_( "GSHandleSize" )
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0 # Regular
		except Exception as e:
			self.logToConsole( "getHandleSize: HandleSize defaulting to 7.0. %s" % str(e) )
			return 7.0

	def getScale( self ):
		"""
		self.getScale() returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same apparent pixel size.
		"""
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		print myLog
		NSLog( myLog )
