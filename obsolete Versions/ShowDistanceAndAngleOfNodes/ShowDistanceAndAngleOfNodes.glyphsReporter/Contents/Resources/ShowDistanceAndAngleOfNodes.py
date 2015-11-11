#!/usr/bin/env python
# encoding: utf-8

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# --> let me know if you have ideas for improving
# --> Mark Froemberg aka DeutschMark @ GitHub
# --> www.markfromberg.com
#
# - ToDo
#	- 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import objc
from Foundation import *
from AppKit import *
import sys, os, re
import math
# import cmath

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class ShowDistanceAndAngleOfNodes ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		try:
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
			return "* Distance & Angle"
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
		try:
			self.drawNodeDistanceText( Layer )
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )

	def drawCoveringBadge(self, x, y, width, height, radius, alpha):
		myPath = NSBezierPath.alloc().init()
		NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, .6, 1, alpha ).set()
		myRect = NSRect( ( x, y ), ( width, height ) )
		thisPath = NSBezierPath.bezierPathWithRoundedRect_cornerRadius_( myRect, radius )
		myPath.appendBezierPath_( thisPath )
		myPath.fill()
	
	def drawNodeDistanceText( self, Layer ):
		try:
			try:
				selection = Layer.selection
			except:
				selection = Layer.selection()
			if len(selection) == 2:
				x1, y1 = selection[0].x, selection[0].y
				x2, y2 = selection[1].x, selection[1].y
				t = 0.5 # MIDLLE
				xAverage = x1 + (x2-x1) * t
				yAverage = y1 + (y2-y1) * t
				dist = math.hypot(x2 - x1, y2 - y1)

				### BADGE
				badgeWidth = 11 * len(str(round(dist))) / self.getScale()
				badgeHeight = 23 / self.getScale()
				badgeRadius = 8 / self.getScale()
				
				### HACK TO KEEP THE TEXT IN ITS BADGE FOR ALL ZOOMS
				badgeAlpha = .75
				badgeFontColor = 1, 1, 1, 1
				if self.getScale() >= 6:
					shiftY = - 0.5
				if self.getScale() >= 15:
					badgeHeight = badgeHeight*1.5
					badgeWidth = badgeWidth*1.5
				if self.getScale() >= 20:
					shiftY = - 1
				if self.getScale() >= 25:
					badgeAlpha = 0
					badgeFontColor = 0, .5, 1, .75
				else:
					shiftY = 0


				'''
				ANGLE
				'''
				dx, dy = x2 - x1, y2 - y1
				rads = math.atan2( dy, dx )
				degs = math.degrees( rads )

				### CLEAN UP THE DIRECTIONS, LIMIT ANGLES BETWEEN 0 AND 180
				### SO THE SAME PERCIEVED ANGLE WILL HAVE THE SAME VALUE
				### IGNORING PATH DIRECTION
				if -180 < degs < -90:
					degs = degs+180
				elif degs == 180:
					degs = 0
				elif degs == -90:
					degs = 90

				### math.floor() to avoid jumpin position of badge & text
				self.drawCoveringBadge( math.floor(xAverage) - badgeWidth/2, math.floor(yAverage) - badgeHeight, badgeWidth, badgeHeight*2, badgeRadius, badgeAlpha)

				### is this one slowing down?
				self.drawTextAtPoint( u"%s\n%s°" % ( round(dist, 1), round(degs, 1) ), (math.floor(xAverage), math.floor(yAverage) + shiftY), fontSize=10.0, fontColor=NSColor.colorWithCalibratedRed_green_blue_alpha_( *badgeFontColor) )

			else:
				pass
		except Exception, e:
			self.logToConsole(e)
			pass

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
	
	def drawTextAtPoint( self, text, textPosition, fontSize=10.0, fontColor=NSColor.colorWithCalibratedRed_green_blue_alpha_( 1, 1, 1, 1 ) ):
		try:
			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 4 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
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
