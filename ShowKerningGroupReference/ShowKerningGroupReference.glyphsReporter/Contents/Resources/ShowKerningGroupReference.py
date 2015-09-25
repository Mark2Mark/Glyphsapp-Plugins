#!/usr/bin/env python
# encoding: utf-8

#########################################################
#
# 2015 Mark Frömberg
# aka DeutschMark
# www.markfromberg.com
#
# ToDo:
#		- make drawing for left and right a function
#
#########################################################

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class ShowKerningGroupReference ( NSObject, GlyphsReporterProtocol ):
	
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
			return "Kerning Group Reference"
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

		Glyph = Layer.parent
		Font = Glyph.parent
		thisMaster = Font.selectedFontMaster
		masters = Font.masters
		activeMasterIndex = masters.index(thisMaster)

		try:
			#NSColor.darkGrayColor().set()
			NSColor.colorWithCalibratedRed_green_blue_alpha_(0.8, 0, 0, .8).set()
			thisWidth = Layer.width
			xHeight = thisMaster.xHeight
			margin = 30
			scaler = .2

			######## MAKE THESE A FUNCTION!
			### LEFT
			if Layer.parent.leftKerningGroup:
				LKG = Layer.parent.leftKerningGroup
								
				LKGGlyph = Font.glyphForName_(LKG)
				LKGGlyphActiveMaster = LKGGlyph.layers[activeMasterIndex]
				LKGWidth = LKGGlyphActiveMaster.width * scaler
				self.drawKerningGroupReference( LKGGlyphActiveMaster, -LKGWidth-margin, xHeight/2 )

			### Right
			if Layer.parent.rightKerningGroup:
				RKG = Layer.parent.rightKerningGroup
								
				RKGGlyph = Font.glyphForName_(RKG)
				RKGGlyphActiveMaster = RKGGlyph.layers[activeMasterIndex]
				RKGWidth = RKGGlyphActiveMaster.width * scaler
				self.drawKerningGroupReference( RKGGlyphActiveMaster, thisWidth+margin, xHeight/2 )


		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )

	
	def drawKerningGroupReference( self, Layer, positionX, positionY ):

		Glyph = Layer.parent
		# draw path AND components:
		thisBezierPathWithComponent = Layer.copyDecomposedLayer().bezierPath()
		scale = NSAffineTransform.transform()
		scale.translateXBy_yBy_( positionX, positionY )
		scale.scaleBy_( .2 )
		
		thisBezierPathWithComponent.transformUsingAffineTransform_( scale )
		
		if thisBezierPathWithComponent:
			thisBezierPathWithComponent.fill()


	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )

	def drawBackgroundForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths,
		but for inactive glyphs in the Edit view.
		"""
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def drawTextAtPoint( self, text, textPosition, fontSize=14.0, fontColor=NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.2, 0.0, 0.3 ) ):
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
			textAlignment = 0 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except Exception as e:
			self.logToConsole( "drawTextAtPoint: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed in the Preview at the bottom.
		Remove the method or return True if you want to leave the Preview untouched.
		Return True to leave the Preview as it is and draw on top of it.
		Return False to disable the Preview and draw your own.
		In that case, don't forget to add Bezier methods like in drawForegroundForLayer_(),
		otherwise users will get an empty Preview.
		"""
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
		NSLog( myLog )