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
# from Foundation import *
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
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		try:
			return "* Kerning Group Reference"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	

	def drawForegroundForLayer_( self, Layer ):

		Glyph = Layer.parent
		Font = Glyph.parent
		masters = Font.masters		
		thisMaster = Font.selectedFontMaster
		activeMasterIndex = masters.index(thisMaster)
		direction = Font.tabs[-1].writingDirection() ### <-- crash issue at Line Break?

		def position( self, KGWidth):
			distance = 120
			# self.leftPosition = -KGWidth - margin, xHeight/2
			self.leftPosition = -distance - margin, xHeight/2
			# self.rightPosition = thisWidth + margin, xHeight/2
			self.rightPosition = thisWidth + margin+10 + distance - KGWidth, xHeight/2

		def switcher( A, B, KGGlyphActiveMaster ):
			if direction == 0:
				self.drawKerningGroupReference( KGGlyphActiveMaster, *A )
			if direction == 1:
				self.drawKerningGroupReference( KGGlyphActiveMaster, *B )

		try:
			# NSColor.colorWithCalibratedRed_green_blue_alpha_(0.8, 0, 0, .8).set()
			thisWidth = Layer.width
			xHeight = thisMaster.xHeight
			margin = 30
			scaler = .2
			R, G, B = 0, 0.5, 0.5
			floatLimit = 0.04
			

			### LEFT
			if Layer.parent.leftKerningGroup:
				LKG = Layer.parent.leftKerningGroup

				try:
					LKGGlyph = Font.glyphForName_(LKG)

					###
					LKGGlyphs = []
					for glyph in Font.glyphs:
						if glyph.leftKerningGroup == LKG:
							LKGGlyphs.append(Font.glyphForName_(glyph.name))
					# self.logToConsole(LKGGlyphs)
					###

					# self.LKGGlyphActiveMaster = LKGGlyph.layers[activeMasterIndex]
					# LKGWidth = self.LKGGlyphActiveMaster.width * scaler
					# position( self, LKGWidth )
					# switcher( self.leftPosition, self.rightPosition, self.LKGGlyphActiveMaster )
					for gL in LKGGlyphs:
						leftAlpha = .8/len(LKGGlyphs)
						if leftAlpha < floatLimit:
							leftAlpha = floatLimit
						# self.logToConsole(leftAlpha)
						# NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0.5, 0.5, leftAlpha).set()
						NSColor.colorWithCalibratedRed_green_blue_alpha_(R, G, B, leftAlpha).set()
						self.LKGGlyphActiveMaster = gL.layers[activeMasterIndex]
						LKGWidth = self.LKGGlyphActiveMaster.width * scaler
						position( self, LKGWidth )
						switcher( self.leftPosition, self.rightPosition, self.LKGGlyphActiveMaster )
					# LKGGlyphsNames = "\n".join([str(x.name) for x in LKGGlyphs])
					# self.drawTextAtPoint(str(LKGGlyphsNames), (0, 0))						
				except:
					pass


			### Right
			if Layer.parent.rightKerningGroup:
				RKG = Layer.parent.rightKerningGroup
				try:
					RKGGlyph = Font.glyphForName_(RKG)

					###
					RKGGlyphs = []
					for glyph in Font.glyphs:
						if glyph.rightKerningGroup == RKG:
							RKGGlyphs.append(Font.glyphForName_(glyph.name))
					# self.logToConsole(RKGGlyphs)
					###

					# self.RKGGlyphActiveMaster = RKGGlyph.layers[activeMasterIndex]
					# RKGWidth = self.RKGGlyphActiveMaster.width * scaler
					# position( self, RKGWidth )
					# switcher( self.rightPosition, self.leftPosition, self.RKGGlyphActiveMaster )
					for gR in RKGGlyphs:
						rightAlpha = .8/len(RKGGlyphs)
						if rightAlpha < floatLimit:
							rightAlpha = floatLimit						
						NSColor.colorWithCalibratedRed_green_blue_alpha_(R, G, B, rightAlpha).set()
						self.RKGGlyphActiveMaster = gR.layers[activeMasterIndex]
						RKGWidth = self.RKGGlyphActiveMaster.width * scaler
						position( self, RKGWidth )
						switcher( self.rightPosition, self.leftPosition, self.RKGGlyphActiveMaster )
						# self.drawTextAtPoint("\n".join(RKGGlyphs), (0, 0))
					# RKGGlyphsNames = "\n".join([str(x.name) for x in RKGGlyphs])
					# self.drawTextAtPoint(str(RKGGlyphsNames), (0, 0))
				except:
					pass

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
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )

	def drawBackgroundForInactiveLayer_( self, Layer ):
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def drawTextAtPoint( self, text, textPosition, fontSize=6.0, fontColor=NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.2, 0.0, 0.3 ) ):
		try:
			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 6 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except Exception as e:
			self.logToConsole( "drawTextAtPoint: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True
	
	def getHandleSize( self ):
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
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
