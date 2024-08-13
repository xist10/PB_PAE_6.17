# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, NotifyCode, AdvancedStartActionTypes,
																CyMessageControl, WidgetTypes, PanelStyles,
																CyInterface, InterfaceDirtyBits, CyGame,
																CommerceTypes, UnitClassTypes,
																ActivationTypes, PopupStates, GameOptionTypes,
																ButtonStyles, DomainTypes, YieldTypes)
import CvUtil
if not CvUtil.isPitbossHost():
    from CvPythonExtensions import CyGInterfaceScreen

# import ScreenInput
import CvScreenEnums
# import CvScreensInterface
import PAE_Lists as L

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range

PIXEL_INCREMENT = 7
BOX_INCREMENT_WIDTH = 33  # Used to be 33 #Should be a multiple of 3...
BOX_INCREMENT_HEIGHT = 9  # Should be a multiple of 3...
BOX_INCREMENT_Y_SPACING = 6  # Should be a multiple of 3...
BOX_INCREMENT_X_SPACING = 9  # Should be a multiple of 3...

TECH_BUTTON_SIZE = 49  # PAE: 49 bigger Techbutton  40 unten: y=12 statt 8 ?
TEXTURE_SIZE = 24
X_START = 6 + TECH_BUTTON_SIZE
X_INCREMENT = 27
Y_ROW = 32

CIV_HAS_TECH = 0
CIV_IS_RESEARCHING = 1
CIV_NO_RESEARCH = 2
CIV_TECH_AVAILABLE = 3

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvTechChooser:
		"Tech Chooser Screen"

		def __init__(self):
				self.nWidgetCount = 0
				self.iCivSelected = 0
				self.aiCurrentState = []

				# Advanced Start
				self.m_iSelectedTech = -1
				self.m_bSelectedTechDirty = False
				self.m_bTechRecordsDirty = False

		def getScreen(self):
				return CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)

		def hideScreen(self):

				# Get the screen
				screen = self.getScreen()

				# Hide the screen
				screen.hideScreen()

		# Screen construction function
		def interfaceScreen(self):

				if CyGame().isPitbossHost():
						return

				# Create a new screen, called TechChooser, using the file CvTechChooser.py for input
				screen = self.getScreen()
				screen.setRenderInterfaceOnly(True)
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

				screen.hide("AddTechButton")
				screen.hide("ASPointsLabel")
				screen.hide("SelectedTechLabel")

				if CyGame().isDebugMode():
						screen.addDropDownBoxGFC("CivDropDown", 22, 12, 192, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT)
						screen.setActivation("CivDropDown", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
						for j in range(gc.getMAX_PLAYERS()):
								if (gc.getPlayer(j).isAlive()):
										screen.addPullDownString("CivDropDown", gc.getPlayer(j).getName(), j, j, False)
				else:
						screen.hide("CivDropDown")

				if screen.isPersistent() and self.iCivSelected == gc.getGame().getActivePlayer():
						self.updateTechRecords(False)
						return

				self.nWidgetCount = 0
				self.iCivSelected = gc.getGame().getActivePlayer()
				self.aiCurrentState = []
				screen.setPersistent(True)

				# Advanced Start
				if gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() >= 0:

						self.m_bSelectedTechDirty = True

						self.X_ADD_TECH_BUTTON = 10
						self.Y_ADD_TECH_BUTTON = 731
						self.W_ADD_TECH_BUTTON = 150
						self.H_ADD_TECH_BUTTON = 30
						self.X_ADVANCED_START_TEXT = self.X_ADD_TECH_BUTTON + self.W_ADD_TECH_BUTTON + 20

						szText = localText.getText("TXT_KEY_WB_AS_ADD_TECH", ())
						screen.setButtonGFC("AddTechButton", szText, "", self.X_ADD_TECH_BUTTON, self.Y_ADD_TECH_BUTTON, self.W_ADD_TECH_BUTTON,
																self.H_ADD_TECH_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
						screen.hide("AddTechButton")

# PAE - increased width - start
				if screen.getXResolution() > 1024:
						iWindowWidth = screen.getXResolution() - 60
						# iWindowWidth = screen.getXResolution()-50  # leider doch nicht zentriert
						# iWindowWidth = 1200  # 1200
				else:
						iWindowWidth = 1024
				# Here we set the background widget and exit button, and we show the screen
				screen.showWindowBackground(False)
				# screen.setDimensions(screen.centerX(0), screen.centerY(0), iWindowWidth, 768)
				screen.setDimensions((screen.getXResolution() - iWindowWidth) / 2, screen.centerY(0), iWindowWidth, 768)
# PAE - increased width - end

				screen.addPanel("TechTopPanel", u"", u"", True, False, 0, 0, iWindowWidth, 55, PanelStyles.PANEL_STYLE_TOPBAR)
				screen.addDDSGFC("TechBG", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 48, iWindowWidth, 672, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addPanel("TechBottomPanel", u"", u"", True, False, 0, 713, iWindowWidth, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR)
				screen.setText("TechChooserExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>",
											 CvUtil.FONT_RIGHT_JUSTIFY, iWindowWidth-30, 726, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
				screen.setActivation("TechChooserExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)

				# Header...
				szText = u"<font=4>"
				szText = szText + localText.getText("TXT_KEY_TECH_CHOOSER_TITLE", ()).upper()
				szText = szText + u"</font>"
				screen.setLabel("TechTitleHeader", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, (iWindowWidth / 2) - 10, 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Make the scrollable area for the city list...
				screen.addScrollPanel("TechList", u"", 0, 64, iWindowWidth, 626, PanelStyles.PANEL_STYLE_EXTERNAL)
				screen.setActivation("TechList", ActivationTypes.ACTIVATE_NORMAL)
				screen.hide("TechList")

				# Add the Highlight
				#screen.addDDSGFC( "TechHighlight", ArtFileMgr.getInterfaceArtInfo("TECH_HIGHLIGHT").getPath(), 0, 0, self.getXStart() + 6, 12 + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ), WidgetTypes.WIDGET_GENERAL, -1, -1 )
				#screen.hide( "TechHighlight" )

				# Place the tech blocks
				self.placeTechs()

				# Draw the arrows
				self.drawArrows()

				screen.moveToFront("CivDropDown")

				screen.moveToFront("AddTechButton")

		def placeTechs(self):
				global L

				iMaxX = 0
				iMaxY = 0

				# If we are the Pitboss, we don't want to put up an interface at all
				if CyGame().isPitbossHost():
						return

				# Get the screen
				screen = self.getScreen()


				# Go through all the techs
				for i in xrange(gc.getNumTechInfos()):

						# Create and place a tech in its proper location
						iX = 30 + ((gc.getTechInfo(i).getGridX() - 1) * ((BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH) * PIXEL_INCREMENT))
						iY = (gc.getTechInfo(i).getGridY() - 1) * (BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT) + 5
						szTechRecord = "TechRecord" + str(i)

						if (iMaxX < iX + self.getXStart()):
								iMaxX = iX + self.getXStart()
						if (iMaxY < iY + (BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT)):
								iMaxY = iY + (BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT)

						screen.attachPanelAt("TechList", szTechRecord, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX - 6, iY - 6,
																 self.getXStart() + 6, 12 + (BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT), WidgetTypes.WIDGET_TECH_TREE, i, -1)
						screen.setActivation(szTechRecord, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
						screen.hide(szTechRecord)

						# reset so that it offsets from the tech record's panel
						iX = 6
						iY = 6

						if gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i):
								screen.setPanelColor(szTechRecord, 85, 150, 87)
								self.aiCurrentState.append(CIV_HAS_TECH)
						elif gc.getPlayer(self.iCivSelected).getCurrentResearch() == i:
								screen.setPanelColor(szTechRecord, 104, 158, 165)
								self.aiCurrentState.append(CIV_IS_RESEARCHING)
						elif gc.getPlayer(self.iCivSelected).isResearchingTech(i):
								screen.setPanelColor(szTechRecord, 104, 158, 165)
								self.aiCurrentState.append(CIV_IS_RESEARCHING)
						elif gc.getPlayer(self.iCivSelected).canEverResearch(i):
								# Dieses Farbschema ist 2x in dieser Datei enthalten (ca. Zeile 1060)!!!
								iEra = gc.getTechInfo(i).getEra()
								if iEra == 4:
										screen.setPanelColor(szTechRecord, 170, 110, 50)  # braun
								elif iEra == 3:
										screen.setPanelColor(szTechRecord, 165, 30, 185)  # purpur
								elif iEra == 2:
										screen.setPanelColor(szTechRecord, 100, 104, 160)  # blau
								elif iEra == 1 or iEra == 5:
										screen.setPanelColor(szTechRecord, 255, 170, 0)  # orange
								else:
										screen.setPanelColor(szTechRecord, 140, 140, 140)  # grau
								self.aiCurrentState.append(CIV_NO_RESEARCH)
						else:
								screen.setPanelColor(szTechRecord, 206, 65, 69)
								self.aiCurrentState.append(CIV_TECH_AVAILABLE)

						szTechID = "TechID" + str(i)
						szTechString = "<font=1>"
						if (gc.getPlayer(self.iCivSelected).isResearchingTech(i)):
								szTechString = szTechString + str(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "
						szTechString += gc.getTechInfo(i).getDescription()
						szTechString = szTechString + "</font>"
						# PAE
						screen.setTextAt(szTechID, szTechRecord, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + TECH_BUTTON_SIZE, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1)
						screen.setActivation(szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)

						# PAE
						szTechButtonID = "TechButtonID" + str(i)
						screen.addDDSGFCAt(szTechButtonID, szTechRecord, gc.getTechInfo(i).getButton(), iX + 6, iY + 8, TECH_BUTTON_SIZE, TECH_BUTTON_SIZE, WidgetTypes.WIDGET_TECH_TREE, i, -1, False)

						self.addIconsToTechPanel(screen, i, X_START, iX, iY, szTechRecord)
						screen.show(szTechRecord)

				screen.setViewMin("TechList", iMaxX + 20, iMaxY + 20)
				screen.show("TechList")
				screen.setFocus("TechList")

		def addIconsToTechPanel(self, screen, i, fX, iX, iY, szTechRecord):
						fX = X_START

						j = 0
						k = 0

						# PAE - rank units, not buildable
						LDontShowTheseUnits = [
								gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"),
								gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"),
								gc.getInfoTypeForString("UNIT_HOPLIT_2"),
								gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"),
								gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS"),
								gc.getInfoTypeForString("UNIT_SPARTA_3"),
								gc.getInfoTypeForString("UNIT_HYPASPIST2"),
								gc.getInfoTypeForString("UNIT_HYPASPIST3"),
								gc.getInfoTypeForString("UNIT_PEZHETAIROI2"),
								gc.getInfoTypeForString("UNIT_PEZHETAIROI3"),
								gc.getInfoTypeForString("UNIT_PEZHETAIROI4"),
								gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"),
								gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"),
								gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2")
						]

						# Unlockable units
						for j in range(gc.getNumUnitClassInfos()):
								eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(j)
								if eLoopUnit != -1 and eLoopUnit not in LDontShowTheseUnits:
										if gc.getUnitInfo(eLoopUnit).getPrereqAndTech() == i:
												szUnitButton = "Unit" + str(j)
												screen.addDDSGFCAt(szUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + fX,
																					 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, True)
												fX += X_INCREMENT

						j = 0
						k = 0

						# Unlockable Buildings
						for j in xrange(gc.getNumBuildingClassInfos()):
								eLoopBuilding = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationBuildings(j)

								if eLoopBuilding != -1:
										if gc.getBuildingInfo(eLoopBuilding).getPrereqAndTech() == i:
												# PAE: Aqueduct for some CIVs only
												if eLoopBuilding == gc.getInfoTypeForString("BUILDING_AQUEDUCT"):
														if gc.getGame().getActiveCivilizationType() in L.LCivsWithAqueduct:
																szBuildingButton = "Building" + str(j)
																screen.addDDSGFCAt(szBuildingButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW,
																									 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, True)
																fX += X_INCREMENT
												else:
														szBuildingButton = "Building" + str(j)
														screen.addDDSGFCAt(szBuildingButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY + Y_ROW,
																							 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, True)
														fX += X_INCREMENT

						j = 0
						k = 0

						# Obsolete Buildings
						for j in xrange(gc.getNumBuildingClassInfos()):
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(self.iCivSelected).getCivilizationType()).getCivilizationBuildings(j)

								if eLoopBuilding != -1:
										if gc.getBuildingInfo(eLoopBuilding).getObsoleteTech() == i:
												# Add obsolete picture here...
												szObsoleteButton = "Obsolete" + str(j)
												szObsoleteX = "ObsoleteX" + str(j)
												screen.addDDSGFCAt(szObsoleteButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + fX, iY +
																					 Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False)
												screen.addDDSGFCAt(szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX +
																					 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False)
												fX += X_INCREMENT

						j = 0
						k = 0

						# Obsolete Bonuses
						for j in range(gc.getNumBonusInfos()):
								if (gc.getBonusInfo(j).getTechObsolete() == i):
										# Add obsolete picture here...
										szObsoleteButton = "ObsoleteBonus" + str(j)
										szObsoleteX = "ObsoleteXBonus" + str(j)
										screen.addDDSGFCAt(szObsoleteButton, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False)
										screen.addDDSGFCAt(szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX +
																			 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Obsolete Monastaries
						for j in range(gc.getNumSpecialBuildingInfos()):
								if (gc.getSpecialBuildingInfo(j).getObsoleteTech() == i):
										# Add obsolete picture here...
										szObsoleteSpecialButton = "ObsoleteSpecial" + str(j)
										szObsoleteSpecialX = "ObsoleteSpecialX" + str(j)
										screen.addDDSGFCAt(szObsoleteSpecialButton, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX,
																			 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False)
										screen.addDDSGFCAt(szObsoleteSpecialX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(),
																			 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Route movement change
						for j in range(gc.getNumRouteInfos()):
								if (gc.getRouteInfo(j).getTechMovementChange(i) != 0):
										szMoveButton = "Move" + str(j)
										screen.addDDSGFCAt(szMoveButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(),
																			 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MOVE_BONUS, i, -1, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Promotion Info
						for j in range(gc.getNumPromotionInfos()):
								if (gc.getPromotionInfo(j).getTechPrereq() == i):
										szPromotionButton = "Promotion" + str(j)
										screen.addDDSGFCAt(szPromotionButton, szTechRecord, gc.getPromotionInfo(j).getButton(), iX + fX, iY + Y_ROW,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, -1, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Free unit
						if (gc.getTechInfo(i).getFirstFreeUnitClass() != UnitClassTypes.NO_UNITCLASS):
								szFreeUnitButton = "FreeUnit" + str(i)

								eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(gc.getTechInfo(i).getFirstFreeUnitClass())
								if (eLoopUnit != -1):
										if (gc.getUnitInfo(eLoopUnit).getEspionagePoints() == 0 or not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)):
												screen.addDDSGFCAt(szFreeUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit),
																					 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_UNIT, eLoopUnit, i, False)
												fX += X_INCREMENT

						j = 0
						k = 0

						# Feature production modifier
						if (gc.getTechInfo(i).getFeatureProductionModifier() != 0):
								szFeatureProductionButton = "FeatureProduction" + str(i)
								screen.addDDSGFCAt(szFeatureProductionButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Worker speed
						if (gc.getTechInfo(i).getWorkerSpeedModifier() != 0):
								szWorkerModifierButton = "Worker" + str(i)
								screen.addDDSGFCAt(szWorkerModifierButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WORKER_SPEED").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WORKER_RATE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Trade Routes per City change
						if (gc.getTechInfo(i).getTradeRoutes() != 0):
								szTradeRouteButton = "TradeRoutes" + str(i)
								screen.addDDSGFCAt(szTradeRouteButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Health Rate bonus from this tech
						if (gc.getTechInfo(i).getHealth() != 0):
								szHealthRateButton = "HealthRate" + str(i)
								screen.addDDSGFCAt(szHealthRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HEALTH_RATE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Happiness Rate bonus from this tech
						if (gc.getTechInfo(i).getHappiness() != 0):
								szHappinessRateButton = "HappinessRate" + str(i)
								screen.addDDSGFCAt(szHappinessRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Free Techs
						if (gc.getTechInfo(i).getFirstFreeTechs() > 0):
								szFreeTechButton = "FreeTech" + str(i)
								screen.addDDSGFCAt(szFreeTechButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_TECH, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Line of Sight bonus
						if (gc.getTechInfo(i).isExtraWaterSeeFrom()):
								szLOSButton = "LOS" + str(i)
								screen.addDDSGFCAt(szLOSButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_LOS_BONUS, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Map Center Bonus
						if (gc.getTechInfo(i).isMapCentering()):
								szMapCenterButton = "MapCenter" + str(i)
								screen.addDDSGFCAt(szMapCenterButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_CENTER, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Map Reveal
						if (gc.getTechInfo(i).isMapVisible()):
								szMapRevealButton = "MapReveal" + str(i)
								screen.addDDSGFCAt(szMapRevealButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_REVEAL, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Map Trading
						if (gc.getTechInfo(i).isMapTrading() == True):
								szMapTradeButton = "MapTrade" + str(i)
								screen.addDDSGFCAt(szMapTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_TRADE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Tech Trading
						if (gc.getTechInfo(i).isTechTrading()):
								szTechTradeButton = "TechTrade" + str(i)
								screen.addDDSGFCAt(szTechTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_TRADE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Gold Trading
						if (gc.getTechInfo(i).isGoldTrading()):
								szGoldTradeButton = "GoldTrade" + str(i)
								screen.addDDSGFCAt(szGoldTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_GOLD_TRADE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Open Borders
						if (gc.getTechInfo(i).isOpenBordersTrading()):
								szOpenBordersButton = "OpenBorders" + str(i)
								screen.addDDSGFCAt(szOpenBordersButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Defensive Pact
						if (gc.getTechInfo(i).isDefensivePactTrading()):
								szDefensivePactButton = "DefensivePact" + str(i)
								screen.addDDSGFCAt(szDefensivePactButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Permanent Alliance
						if (gc.getTechInfo(i).isPermanentAllianceTrading()):
								szPermanentAllianceButton = "PermanentAlliance" + str(i)
								screen.addDDSGFCAt(szPermanentAllianceButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Vassal States
						if (gc.getTechInfo(i).isVassalStateTrading()):
								szVassalStateButton = "VassalState" + str(i)
								screen.addDDSGFCAt(szVassalStateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_VASSAL_STATE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Bridge Building
						if (gc.getTechInfo(i).isBridgeBuilding()):
								szBuildBridgeButton = "BuildBridge" + str(i)
								screen.addDDSGFCAt(szBuildBridgeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Irrigation unlocked
						if (gc.getTechInfo(i).isIrrigation()):
								szIrrigationButton = "Irrigation" + str(i)
								screen.addDDSGFCAt(szIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IRRIGATION, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Ignore Irrigation unlocked
						if (gc.getTechInfo(i).isIgnoreIrrigation()):
								szIgnoreIrrigationButton = "IgnoreIrrigation" + str(i)
								screen.addDDSGFCAt(szIgnoreIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Coastal Work unlocked
						if (gc.getTechInfo(i).isWaterWork()):
								szWaterWorkButton = "WaterWork" + str(i)
								screen.addDDSGFCAt(szWaterWorkButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WATER_WORK, i, -1, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Improvements
						# Limes
						lBuildInfos = []
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES1"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES3"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES4"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES5"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES6"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES7"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES8"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES9"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_1"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_2"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_3"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_4"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_5"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_6"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_7"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_8"))
						lBuildInfos.append(gc.getInfoTypeForString("BUILD_LIMES2_9"))
						for j in range(gc.getNumBuildInfos()):
								if j not in lBuildInfos:
										bTechFound = 0

										if gc.getBuildInfo(j).getTechPrereq() == -1:
												bTechFound = 0
												for k in range(gc.getNumFeatureInfos()):
														if gc.getBuildInfo(j).getFeatureTech(k) == i:
																bTechFound = 1
										else:
												if gc.getBuildInfo(j).getTechPrereq() == i:
														bTechFound = 1

										if bTechFound == 1:
												szImprovementButton = "Improvement" + str((i * 1000) + j)
												screen.addDDSGFCAt(szImprovementButton, szTechRecord, gc.getBuildInfo(j).getButton(), iX + fX, iY +
																					 Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, i, j, False)
												fX += X_INCREMENT

						j = 0
						k = 0

						# Domain Extra Moves
						for j in range(DomainTypes.NUM_DOMAIN_TYPES):
								if (gc.getTechInfo(i).getDomainExtraMoves(j) != 0):
										szDomainExtraMovesButton = "DomainExtraMoves" + str((i * 1000) + j)
										screen.addDDSGFCAt(szDomainExtraMovesButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(),
																			 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, i, j, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Adjustments
						for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
								if (gc.getTechInfo(i).isCommerceFlexible(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isCommerceFlexible(j))):
										szAdjustButton = "AdjustButton" + str((i * 1000) + j)
										if (j == CommerceTypes.COMMERCE_CULTURE):
												szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_CULTURE").getPath()
										elif (j == CommerceTypes.COMMERCE_ESPIONAGE):
												szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_ESPIONAGE").getPath()
										else:
												szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
										screen.addDDSGFCAt(szAdjustButton, szTechRecord, szFileName, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_ADJUST, i, j, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Terrain opens up as a trade route
						for j in range(gc.getNumTerrainInfos()):
								if (gc.getTechInfo(i).isTerrainTrade(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isTerrainTrade(j))):
										szTerrainTradeButton = "TerrainTradeButton" + str((i * 1000) + j)
										screen.addDDSGFCAt(szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(),
																			 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False)
										fX += X_INCREMENT

						j = gc.getNumTerrainInfos()
						if (gc.getTechInfo(i).isRiverTrade() and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isRiverTrade())):
								szTerrainTradeButton = "TerrainTradeButton" + str((i * 1000) + j)
								screen.addDDSGFCAt(szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False)
								fX += X_INCREMENT

						j = 0
						k = 0

						# Special buildings like monestaries
						for j in range(gc.getNumSpecialBuildingInfos()):
								if (gc.getSpecialBuildingInfo(j).getTechPrereq() == i):
										szSpecialBuilding = "SpecialBuildingButton" + str((i * 1000) + j)
										screen.addDDSGFCAt(szSpecialBuilding, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + fX, iY +
																			 Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, i, j, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Yield change
						for j in range(gc.getNumImprovementInfos()):
								bFound = False
								for k in range(YieldTypes.NUM_YIELD_TYPES):
										if (gc.getImprovementInfo(j).getTechYieldChanges(i, k)):
												if (bFound == False):
														szYieldChange = "YieldChangeButton" + str((i * 1000) + j)
														screen.addDDSGFCAt(szYieldChange, szTechRecord, gc.getImprovementInfo(j).getButton(), iX + fX, iY +
																							 Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, i, j, False)
														fX += X_INCREMENT
														bFound = True

						j = 0
						k = 0

						# Bonuses revealed
						for j in range(gc.getNumBonusInfos()):
								if (gc.getBonusInfo(j).getTechReveal() == i):
										szBonusReveal = "BonusRevealButton" + str((i * 1000) + j)
										screen.addDDSGFCAt(szBonusReveal, szTechRecord, gc.getBonusInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, i, j, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Civic options
						for j in range(gc.getNumCivicInfos()):
								if (gc.getCivicInfo(j).getTechPrereq() == i):
										szCivicReveal = "CivicRevealButton" + str((i * 1000) + j)
										screen.addDDSGFCAt(szCivicReveal, szTechRecord, gc.getCivicInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_CIVIC_REVEAL, i, j, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Projects possible
						for j in range(gc.getNumProjectInfos()):
								if (gc.getProjectInfo(j).getTechPrereq() == i):
										szProjectInfo = "ProjectInfoButton" + str((i * 1000) + j)
										screen.addDDSGFCAt(szProjectInfo, szTechRecord, gc.getProjectInfo(j).getButton(), iX + fX, iY + Y_ROW,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Processes possible
						for j in range(gc.getNumProcessInfos()):
								if (gc.getProcessInfo(j).getTechPrereq() == i):
										szProcessInfo = "ProcessInfoButton" + str((i * 1000) + j)
										screen.addDDSGFCAt(szProcessInfo, szTechRecord, gc.getProcessInfo(j).getButton(), iX + fX, iY + Y_ROW,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PROCESS_INFO, i, j, False)
										fX += X_INCREMENT

						j = 0
						k = 0

						# Religions unlocked
						for j in range(gc.getNumReligionInfos()):
								if (gc.getReligionInfo(j).getTechPrereq() == i):
										szFoundReligion = "FoundReligionButton" + str((i * 1000) + j)
										if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
												szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_POPUPBUTTON_RELIGION").getPath()
										else:
												szButton = gc.getReligionInfo(j).getButton()
										screen.addDDSGFCAt(szFoundReligion, szTechRecord, szButton, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, i, j, False)
										fX += X_INCREMENT
						j = 0

						# PAE: Kulte/Cults
						for j in range(gc.getNumCorporationInfos()):
								if (gc.getCorporationInfo(j).getTechPrereq() == i):
										szFoundCorporation = "FoundCorporationButton" + str((i * 1000) + j)
										screen.addDDSGFCAt(szFoundCorporation, szTechRecord, gc.getCorporationInfo(j).getButton(), iX + fX, iY +
																			 Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, i, j, False)
										fX += X_INCREMENT
						j = 0

						# Techs - PAE Special features made possible via python (eg. free units, unit formations, obsolete units, reservists)
						if i == gc.getInfoTypeForString("TECH_FRUCHTBARKEIT"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Corporations/button_unit_corp2.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_SENSE"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Corporations/button_unit_corp3.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_GLADIATOR"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Corporations/button_unit_corp5.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_NORDIC"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_nordic.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_CELTIC"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_celtic.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_SUMER"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_sumer.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_EGYPT"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_egypt.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_PHOEN"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_phoen.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_GREEK"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_greek.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_HINDU"):
								screen.addDDSGFCAt("", szTechRecord, ",Art/Interface/Buttons/Units/Missionary_Hindu.dds,Art/Interface/Buttons/Unit_Resource_Atlas.dds,4,3",
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_RELIGION_ROME"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_rome.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_DUALISMUS"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_zoro.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_DUALISMUS"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_missionar_zoro.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 2, False)
								fX += X_INCREMENT
						#elif i == gc.getInfoTypeForString("TECH_COLONIZATION"):
						#		screen.addDDSGFCAt("", szTechRecord, ",Art/Interface/Buttons/Units/Settler.dds,Art/Interface/Buttons/Unit_Resource_Atlas.dds,2,5", iX + fX,
						#											 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 676, 3, False)
						#		fX += X_INCREMENT

						# Siegestempel und -stelen
						elif i == gc.getInfoTypeForString("TECH_BUCHSTABEN"):
								screen.addDDSGFCAt("", szTechRecord, gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_SIEGESSTELE")).getButton(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 2, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_BELAGERUNG"):
								screen.addDDSGFCAt("", szTechRecord, gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL")).getButton(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 3, False)
								fX += X_INCREMENT

						elif i == gc.getInfoTypeForString("TECH_KRIEGERETHOS"):
								screen.addDDSGFCAt("", szTechRecord, gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL")).getButton(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 4, False)
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 4, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_GER_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 5, False)
								fX += X_INCREMENT

						# Unit Formations und Rang/Rank
						elif i == gc.getInfoTypeForString("TECH_BEWAFFNUNG3"):
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 6, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_BUERGERSOLDATEN"):
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_SUMER_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 7, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 8, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_BRANDSCHATZEN"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FOURAGE")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_ARMOR"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_SCHILDWALL")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_CLOSED_FORM"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_CLOSED_FORM")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_PHALANX"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PHALANX")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 9, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_PHALANX2"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_SCHIEF")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PHALANX2")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 10, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_SKIRMISH_TACTICS"):
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 11, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_BANKWESEN"):
								# Comission elite mercenaries
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_MERCENARIES_CITYBUTTON").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 15, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_MANIPEL"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_MANIPEL")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_TREFFEN"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_TREFFEN")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_FLANKENSCHUTZ")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_KAMPFHUNDE"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KEIL")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_MILIT_STRAT"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_ZANGENANGRIFF")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_LINOTHORAX"):
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_GREEK_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 12, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 13, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_MARIAN_REFORM"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KOHORTE")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ROM_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 14, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 15, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_STAUROGRAMM"):
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 16, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_TESTUDO"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_TESTUDO")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_PARTHERSCHUSS"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_PARTHER")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_KANTAKREIS"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_KANTAKREIS")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_GEOMETRIE2"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_GASSE")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_LOGIK"):
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_KEIL")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT
								iFormation = gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_ZANGE")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iFormation).getButton(), iX + fX, iY + Y_ROW,
																	 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iFormation, -1, False)
								fX += X_INCREMENT

						# Actions und Rang/Rank
						elif i == gc.getInfoTypeForString("TECH_HORSEBACK_RIDING"):
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_HUN")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 17, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_HORSEBACK_RIDING_2"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HORSE_DOWN").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 666, 666, False)
								fX += X_INCREMENT
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HORSE_UP").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 667, 667, False)
								fX += X_INCREMENT
								iPromotion = gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_1")
								screen.addDDSGFCAt("", szTechRecord, gc.getPromotionInfo(iPromotion).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 18, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_SYNKRETISMUS"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2BORDELL").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 668, 668, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_GLADIATOR"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_GLADIATOR").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 669, 669, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_DIONYSOS"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2THEATRE").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 670, 670, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_LITERATURE"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2SCHOOL").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 679, 679, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_MANUFAKTUREN"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2MANUFAKTUR_PROD").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 681, 681, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_WASSERRAD"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVE2BROTMANUFAKTUR").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 680, 680, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_ENSLAVEMENT"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_PALACE").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 692, 692, False)
								fX += X_INCREMENT
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_TEMPLE").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 693, 693, False)
								fX += X_INCREMENT
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SELL_SLAVES").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 694, 694, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_SOELDNERTUM"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SELL_UNITS").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 695, 100, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_FEUERWEHR"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_SLAVES_FEUERWEHR").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 696, 696, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_ARMOR"):
								screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_EDLE_RUESTUNG").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 699, -1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_AQUA"):
								eBonus = gc.getInfoTypeForString("BONUS_CRAB")
								screen.addDDSGFCAt("", szTechRecord, gc.getBonusInfo(eBonus).getButton(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False)
								fX += X_INCREMENT
								eBonus = gc.getInfoTypeForString("BONUS_CLAM")
								screen.addDDSGFCAt("", szTechRecord, gc.getBonusInfo(eBonus).getButton(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False)
								fX += X_INCREMENT
						#elif i == gc.getInfoTypeForString("TECH_KUESTE"):
						#		screen.addDDSGFCAt("", szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_PROMO_OIL").getPath(), iX +
						#											 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 701, -1, False)
						#		fX += X_INCREMENT

						# Reservisten
						elif i == gc.getInfoTypeForString("TECH_RESERVISTEN"):
								screen.addDDSGFCAt("", szTechRecord, ",Art/Interface/MainScreen/CityScreen/Great_Engineer.dds,Art/Interface/Buttons/Warlords_Atlas_2.dds,7,6",
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 724, -1, False)
								fX += X_INCREMENT
								# if gc.getGame().getActiveCivilizationType() in L.LGreeks or gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
								#    j = gc.getInfoTypeForString("UNIT_KLERUCHOI")
								#    screen.addDDSGFCAt( "", szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, j, -1, False )
								#    fX += X_INCREMENT
						# elif i == gc.getInfoTypeForString("TECH_BEWAFFNUNG5"):
						#    if gc.getGame().getActiveCivilizationType() in L.LNorthern or gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_IBERER"):
						#        j = gc.getInfoTypeForString("UNIT_SOLDURII")
						#        screen.addDDSGFCAt( "", szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, j, -1, False )
						#        fX += X_INCREMENT
						# elif i == gc.getInfoTypeForString("TECH_BERUFSSOLDATEN"):
						#    if gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ROME") or gc.getGame().getActiveCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
						#        j = gc.getInfoTypeForString("UNIT_LEGION_EVOCAT")
						#        screen.addDDSGFCAt( "", szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, j, -1, False )
						#        fX += X_INCREMENT

						# Sterberate von Sklaven
						elif i == gc.getInfoTypeForString("TECH_PATRONAT"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 16, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_MECHANIK"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 17, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_EISENPFLUG"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 18, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_MEDICINE3") or i == gc.getInfoTypeForString("TECH_ANATOMIE"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Units/button_slave.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 19, False)
								fX += X_INCREMENT

						# Auswanderer und Siedler können Dörfer zu Gemeinden vergrößern
						elif i == gc.getInfoTypeForString("TECH_HEILKUNDE"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Actions/button_action_slave2village.dds", iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 721, 21, False)
								fX += X_INCREMENT

						# Limes
						elif i == gc.getInfoTypeForString("TECH_LIMES"):
								# Special Wonder
								ListCivs = [
									gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"),
									gc.getInfoTypeForString("CIVILIZATION_BABYLON"),
									gc.getInfoTypeForString("CIVILIZATION_SUMERIA"),
									gc.getInfoTypeForString("CIVILIZATION_PERSIA"),
									gc.getInfoTypeForString("CIVILIZATION_PARTHER")
								]
								if gc.getPlayer(CyGame().getActivePlayer()).getCivilizationType() not in ListCivs:
										j = gc.getInfoTypeForString("BUILDING_GREAT_WALL_GORGAN")
										screen.addDDSGFCAt("", szTechRecord, gc.getBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, j, 1, True)
										fX += X_INCREMENT
								# Limes
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Buildings/button_building_hadrianswall.dds",
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 733, 1, False)
								fX += X_INCREMENT
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Buildings/button_building_limes.dds", iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 733, 0, False)
								fX += X_INCREMENT
						# Salae/Sold oder Dezimierung
						elif i == gc.getInfoTypeForString("TECH_CURRENCY"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Actions/button_action_salae.dds", iX + fX,
																	 iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 735, 1, False)
								fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_DEZIMATION"):
								screen.addDDSGFCAt("", szTechRecord, "Art/Interface/Buttons/Actions/button_action_dezimierung.dds", iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 735, 2, False)
								fX += X_INCREMENT
						# Obsolete units (Praetorianer)
						elif i == gc.getInfoTypeForString("TECH_GRENZHEER"):
								j = gc.getInfoTypeForString("UNIT_PRAETORIAN")
								szObsoleteSpecialButton = "ObsoleteUnit" + str(j)
								szObsoleteSpecialX = "ObsoleteUnitX" + str(j)
								screen.addDDSGFCAt(szObsoleteSpecialButton, szTechRecord, gc.getUnitInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, True)
								screen.addDDSGFCAt(szObsoleteSpecialX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, True)
								fX += X_INCREMENT
						# Obsolet Olympic Games
						elif i == gc.getInfoTypeForString("TECH_PAPSTTUM"):
								j = gc.getInfoTypeForString("PROJECT_OLYMPIC_GAMES")
								szObsoleteButton = "ObsoleteProject" + str(j)
								szObsoleteX = "ObsoleteProjectX" + str(j)
								screen.addDDSGFCAt(szObsoleteButton, szTechRecord, gc.getProjectInfo(j).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, False)
								screen.addDDSGFCAt(szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(),
																	 iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 754, j, False)
								fX += X_INCREMENT
						# Obsolete Ore Camp
						elif i == gc.getInfoTypeForString("TECH_BEWAFFNUNG2"):
								iImp = gc.getInfoTypeForString("IMPROVEMENT_ORE_CAMP")
								j = gc.getInfoTypeForString("BUILD_ORE_CAMP")
								szImprovementButton = "ObsoleteImprovement" + str((iImp * 1000) + j)
								szObsoleteX = "ObsoleteImprovementX" + str(j)
								screen.addDDSGFCAt(szImprovementButton, szTechRecord, gc.getBuildInfo(j).getButton(), iX + fX, iY +
																	 Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, i, j, False)
								screen.addDDSGFCAt(szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX +
																	 fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 749, 19, False)
								fX += X_INCREMENT

						# Special Wonders
						elif i == gc.getInfoTypeForString("TECH_MASONRY2"):
								if gc.getPlayer(CyGame().getActivePlayer()).getCivilizationType() != gc.getInfoTypeForString("CIVILIZATION_BRITEN"):
										j = gc.getInfoTypeForString("BUILDING_STONEHENGE")
										szBuildingButton = "Building" + str(j)
										screen.addDDSGFCAt(szBuildingButton, szTechRecord, gc.getBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, j, 1, True)
										fX += X_INCREMENT
						elif i == gc.getInfoTypeForString("TECH_WEHRTECHNIK"):
								if gc.getPlayer(CyGame().getActivePlayer()).getCivilizationType() != gc.getInfoTypeForString("CIVILIZATION_DAKER"):
										j = gc.getInfoTypeForString("BUILDING_WONDER_DAKER")
										szBuildingButton = "Building" + str(j)
										screen.addDDSGFCAt(szBuildingButton, szTechRecord, gc.getBuildingInfo(j).getButton(), iX + fX, iY + Y_ROW,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, j, 1, True)
										fX += X_INCREMENT
						# End -----------
						j = 0
						# PAE: Espionage Missions
						for j in range(gc.getNumEspionageMissionInfos()):
								if (gc.getEspionageMissionInfo(j).getTechPrereq() == i):
										szFoundEspionage = "FoundEspionageButton" + str((i * 1000) + j)
										szButton = ArtFileMgr.getInterfaceArtInfo("ESPIONAGE_BUTTON2").getPath()
										screen.addDDSGFCAt(szFoundEspionage, szTechRecord, szButton, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_GENERAL, 723, j, False)
										fX += X_INCREMENT
						j = 0

						# ------------------------

		# Will update the tech records based on color, researching, researched, queued, etc.

		def updateTechRecords(self, bForce):

				# If we are the Pitboss, we don't want to put up an interface at all
				if (CyGame().isPitbossHost()):
						return

				# Get the screen
				screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)

				abChanged = []
				bAnyChanged = 0

				# Go through all the techs
				for i in range(gc.getNumTechInfos()):

						abChanged.append(0)

						if (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i)):
								if (self.aiCurrentState[i] != CIV_HAS_TECH):
										self.aiCurrentState[i] = CIV_HAS_TECH
										abChanged[i] = 1
										bAnyChanged = 1
						elif (gc.getPlayer(self.iCivSelected).getCurrentResearch() == i):
								if (self.aiCurrentState[i] != CIV_IS_RESEARCHING):
										self.aiCurrentState[i] = CIV_IS_RESEARCHING
										abChanged[i] = 1
										bAnyChanged = 1
						elif (gc.getPlayer(self.iCivSelected).isResearchingTech(i)):
								if (self.aiCurrentState[i] != CIV_IS_RESEARCHING):
										self.aiCurrentState[i] = CIV_IS_RESEARCHING
										abChanged[i] = 1
										bAnyChanged = 1
						elif (gc.getPlayer(self.iCivSelected).canEverResearch(i)):
								if (self.aiCurrentState[i] != CIV_NO_RESEARCH):
										self.aiCurrentState[i] = CIV_NO_RESEARCH
										abChanged[i] = 1
										bAnyChanged = 1
						else:
								if (self.aiCurrentState[i] != CIV_TECH_AVAILABLE):
										self.aiCurrentState[i] = CIV_TECH_AVAILABLE
										abChanged[i] = 1
										bAnyChanged = 1

				for i in range(gc.getNumTechInfos()):

						if (abChanged[i] or bForce or (bAnyChanged and gc.getPlayer(self.iCivSelected).isResearchingTech(i))):
								# Create and place a tech in its proper location
								szTechRecord = "TechRecord" + str(i)
								szTechID = "TechID" + str(i)
								szTechString = "<font=1>"

								if (gc.getPlayer(self.iCivSelected).isResearchingTech(i)):
										szTechString = szTechString + unicode(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "  # noqa

								iX = 30 + ((gc.getTechInfo(i).getGridX() - 1) * ((BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH) * PIXEL_INCREMENT))
								iY = (gc.getTechInfo(i).getGridY() - 1) * (BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT) + 5

								szTechString += gc.getTechInfo(i).getDescription()
								if (gc.getPlayer(self.iCivSelected).isResearchingTech(i)):
										szTechString += " ("
										szTechString += str(gc.getPlayer(self.iCivSelected).getResearchTurnsLeft(i, (gc.getPlayer(self.iCivSelected).getCurrentResearch() == i)))
										szTechString += ")"
								szTechString = szTechString + "</font>"
								# PAE
								screen.setTextAt(szTechID, "TechList", szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + TECH_BUTTON_SIZE, iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1)
								screen.setActivation(szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)

								if (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i)):
										screen.setPanelColor(szTechRecord, 85, 150, 87)
								elif (gc.getPlayer(self.iCivSelected).getCurrentResearch() == i):
										screen.setPanelColor(szTechRecord, 104, 158, 165)
								elif (gc.getPlayer(self.iCivSelected).isResearchingTech(i)):
										screen.setPanelColor(szTechRecord, 104, 158, 165)
								elif (gc.getPlayer(self.iCivSelected).canEverResearch(i)):
										iEra = gc.getTechInfo(i).getEra()
										if iEra == 4:
												screen.setPanelColor(szTechRecord, 170, 110, 50)  # braun
										elif iEra == 3:
												screen.setPanelColor(szTechRecord, 165, 30, 185)  # purpur
										elif iEra == 2:
												screen.setPanelColor(szTechRecord, 100, 104, 160)  # blau
										elif iEra == 1:
												screen.setPanelColor(szTechRecord, 255, 170, 0)  # orange
										else:
												screen.setPanelColor(szTechRecord, 140, 140, 140)  # grau
								else:
										screen.setPanelColor(szTechRecord, 206, 65, 69)

		# Will draw the arrows
		def drawArrows(self):

				screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)

				# iLoop = 0
				self.nWidgetCount = 0

				ARROW_X = ArtFileMgr.getInterfaceArtInfo("ARROW_X").getPath()
				ARROW_Y = ArtFileMgr.getInterfaceArtInfo("ARROW_Y").getPath()
				ARROW_MXMY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXMY").getPath()
				ARROW_XY = ArtFileMgr.getInterfaceArtInfo("ARROW_XY").getPath()
				ARROW_MXY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXY").getPath()
				ARROW_XMY = ArtFileMgr.getInterfaceArtInfo("ARROW_XMY").getPath()
				ARROW_HEAD = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD").getPath()

				for i in range(gc.getNumTechInfos()):

						# bFirst = 1

						fX = (BOX_INCREMENT_WIDTH * PIXEL_INCREMENT) - 10  # - 8

						for j in range(gc.getNUM_AND_TECH_PREREQS()):

								eTech = gc.getTechInfo(i).getPrereqAndTechs(j)

								if (eTech > -1):

										fX = fX - X_INCREMENT

										iX = 30 + ((gc.getTechInfo(i).getGridX() - 1) * ((BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH) * PIXEL_INCREMENT))
										iY = (gc.getTechInfo(i).getGridY() - 1) * (BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT) + 5

										szTechPrereqID = "TechPrereqID" + str((i * 1000) + j)
										screen.addDDSGFCAt(szTechPrereqID, "TechList", gc.getTechInfo(eTech).getButton(), iX + fX, iY + 6,
																			 TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False)

										#szTechPrereqBorderID = "TechPrereqBorderID" + str((i * 1000) + j)
										#screen.addDDSGFCAt( szTechPrereqBorderID, "TechList", ArtFileMgr.getInterfaceArtInfo("TECH_TREE_BUTTON_BORDER").getPath(), iX + fX + 4, iY + 22, 32, 32, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

						j = 0

						for j in range(gc.getNUM_OR_TECH_PREREQS()):

								eTech = gc.getTechInfo(i).getPrereqOrTechs(j)

								if (eTech > -1):

										iX = 24 + ((gc.getTechInfo(eTech).getGridX() - 1) * ((BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH) * PIXEL_INCREMENT))
										iY = (gc.getTechInfo(eTech).getGridY() - 1) * (BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT) + 5

										# j is the pre-req, i is the tech...
										xDiff = gc.getTechInfo(i).getGridX() - gc.getTechInfo(eTech).getGridX()
										yDiff = gc.getTechInfo(i).getGridY() - gc.getTechInfo(eTech).getGridY()

										if (yDiff == 0):
												screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.getXStart(), iY +
																					 self.getYStart(3), self.getWidth(xDiff), 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
												screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getXStart() +
																					 self.getWidth(xDiff), iY + self.getYStart(3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
										elif (yDiff < 0):
												if (yDiff == -6):
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.getXStart(), iY +
																							 self.getYStart(1), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XY, iX + self.getXStart() + (self.getWidth(xDiff) / 2),
																							 iY + self.getYStart(1), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + self.getXStart() + (self.getWidth(xDiff) / 2), iY +
																							 self.getYStart(1) + 8 - self.getHeight(yDiff, 0), 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XMY, iX + self.getXStart() + (self.getWidth(xDiff) / 2),
																							 iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + self.getXStart() + (self.getWidth(xDiff) / 2), iY +
																							 self.getYStart(1) - self.getHeight(yDiff, 0), (self.getWidth(xDiff) / 2) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff),
																							 iY + self.getYStart(1) - self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
												elif (yDiff == -2 and xDiff == 2):
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.getXStart(), iY + self.getYStart(2),
																							 self.getWidth(xDiff) * 5 / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XY, iX + self.getXStart() + (self.getWidth(xDiff)
																							 * 5 / 6), iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + self.getXStart() + (self.getWidth(xDiff) * 5 / 6), iY +
																							 self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XMY, iX + self.getXStart() + (self.getWidth(xDiff) * 5 / 6),
																							 iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + self.getXStart() + (self.getWidth(xDiff) * 5 / 6), iY +
																							 self.getYStart(2) - self.getHeight(yDiff, 3), (self.getWidth(xDiff) / 6) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff),
																							 iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
												else:
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.getXStart(), iY +
																							 self.getYStart(2), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XY, iX + self.getXStart() + (self.getWidth(xDiff) / 2),
																							 iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + self.getXStart() + (self.getWidth(xDiff) / 2), iY +
																							 self.getYStart(2) + 8 - self.getHeight(yDiff, 3), 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_XMY, iX + self.getXStart() + (self.getWidth(xDiff) / 2),
																							 iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + self.getXStart() + (self.getWidth(xDiff) / 2), iY +
																							 self.getYStart(2) - self.getHeight(yDiff, 3), (self.getWidth(xDiff) / 2) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff),
																							 iY + self.getYStart(2) - self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
										elif (yDiff > 0):
												if (yDiff == 2 and xDiff == 2):
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.getXStart(), iY +
																							 self.getYStart(4), self.getWidth(xDiff) / 6, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXMY, iX + self.getXStart() +
																							 (self.getWidth(xDiff) / 6), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + self.getXStart() + (self.getWidth(xDiff) / 6),
																							 iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXY, iX + self.getXStart() + (self.getWidth(xDiff) / 6),
																							 iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + self.getXStart() + (self.getWidth(xDiff) / 6), iY +
																							 self.getYStart(4) + self.getHeight(yDiff, 3), (self.getWidth(xDiff) * 5 / 6) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff),
																							 iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
												elif (yDiff == 4 and xDiff == 1):
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.getXStart(), iY +
																							 self.getYStart(5), self.getWidth(xDiff) / 3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXMY, iX + self.getXStart() +
																							 (self.getWidth(xDiff) / 3), iY + self.getYStart(5), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + self.getXStart() + (self.getWidth(xDiff) / 3),
																							 iY + self.getYStart(5) + 8, 8, self.getHeight(yDiff, 0) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXY, iX + self.getXStart() + (self.getWidth(xDiff) / 3),
																							 iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + self.getXStart() + (self.getWidth(xDiff) / 3), iY +
																							 self.getYStart(5) + self.getHeight(yDiff, 0), (self.getWidth(xDiff) * 2 / 3) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff),
																							 iY + self.getYStart(5) + self.getHeight(yDiff, 0), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
												else:
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + self.getXStart(), iY +
																							 self.getYStart(4), self.getWidth(xDiff) / 2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXMY, iX + self.getXStart() +
																							 (self.getWidth(xDiff) / 2), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_Y, iX + self.getXStart() + (self.getWidth(xDiff) / 2),
																							 iY + self.getYStart(4) + 8, 8, self.getHeight(yDiff, 3) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_MXY, iX + self.getXStart() + (self.getWidth(xDiff) / 2),
																							 iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_X, iX + 8 + self.getXStart() + (self.getWidth(xDiff) / 2), iY +
																							 self.getYStart(4) + self.getHeight(yDiff, 3), (self.getWidth(xDiff) / 2) - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
														screen.addDDSGFCAt(self.getNextWidgetName(), "TechList", ARROW_HEAD, iX + self.getXStart() + self.getWidth(xDiff),
																							 iY + self.getYStart(4) + self.getHeight(yDiff, 3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

				return

		def TechRecord(self, inputClass):
				return 0

		# Clicked the parent?
		def ParentClick(self, inputClass):
				return 0

		def CivDropDown(self, inputClass):

				if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
						screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)
						iIndex = screen.getSelectedPullDownID("CivDropDown")
						self.iCivSelected = screen.getPullDownData("CivDropDown", iIndex)
						self.updateTechRecords(False)

		# Will handle the input for this screen...
		def handleInput(self, inputClass):

				# Get the screen
				screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)  # noqa

				# Advanced Start Stuff

				pPlayer = gc.getPlayer(self.iCivSelected)
				if (pPlayer.getAdvancedStartPoints() >= 0):

						# Add tech button
						if (inputClass.getFunctionName() == "AddTechButton"):
								if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, True) != -1):
										CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_TECH, self.iCivSelected, -1, -1, self.m_iSelectedTech, True)  # Action, Player, X, Y, Data, bAdd
										self.m_bTechRecordsDirty = True
										self.m_bSelectedTechDirty = True

						# Tech clicked on
						elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
								if (inputClass.getButtonType() == WidgetTypes.WIDGET_TECH_TREE):
										self.m_iSelectedTech = inputClass.getData1()
										self.updateSelectedTech()

				' Calls function mapped in TechChooserInputMap'
				# only get from the map if it has the key
				if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
						self.CivDropDown(inputClass)
						return 1
				return 0

		def getNextWidgetName(self):
				szName = "TechArrow" + str(self.nWidgetCount)
				self.nWidgetCount += 1
				return szName

		def getXStart(self):
				return (BOX_INCREMENT_WIDTH * PIXEL_INCREMENT)

		def getXSpacing(self):
				return (BOX_INCREMENT_X_SPACING * PIXEL_INCREMENT)

		def getYStart(self, iY):
				return int((((BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT) / 6.0) * iY) - PIXEL_INCREMENT)

		def getWidth(self, xDiff):
				return ((xDiff * self.getXSpacing()) + ((xDiff - 1) * self.getXStart()))

		def getHeight(self, yDiff, nFactor):
				return ((nFactor + ((abs(yDiff) - 1) * 6)) * PIXEL_INCREMENT)

		def update(self, fDelta):

				if (CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT)):
						CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, False)

						if (self.m_bSelectedTechDirty):
								self.m_bSelectedTechDirty = False
								self.updateSelectedTech()

						if (self.m_bTechRecordsDirty):
								self.m_bTechRecordsDirty = False
								self.updateTechRecords(True)

						if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() < 0):
								# hide the screen
								screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)
								screen.hide("AddTechButton")
								screen.hide("ASPointsLabel")
								screen.hide("SelectedTechLabel")

				return

		def updateSelectedTech(self):
				pPlayer = gc.getPlayer(CyGame().getActivePlayer())

				# Get the screen
				screen = CyGInterfaceScreen("TechChooser", CvScreenEnums.TECH_CHOOSER)

				szName = ""
				iCost = 0

				if (self.m_iSelectedTech != -1):
						szName = gc.getTechInfo(self.m_iSelectedTech).getDescription()
						iCost = gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartTechCost(self.m_iSelectedTech, True)

				if iCost > 0:
						szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_SELECTED_TECH_COST", (iCost, pPlayer.getAdvancedStartPoints())) + u"</font>"
						screen.setLabel("ASPointsLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT,
														self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				else:
						screen.hide("ASPointsLabel")

				szText = u"<font=4>"
				szText += localText.getText("TXT_KEY_WB_AS_SELECTED_TECH", (szName,))
				szText += u"</font>"
				screen.setLabel("SelectedTechLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT +
												250, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Want to add
				if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, True) != -1):
						screen.show("AddTechButton")
				else:
						screen.hide("AddTechButton")

		def onClose(self):
				pPlayer = gc.getPlayer(self.iCivSelected)
				if (pPlayer.getAdvancedStartPoints() >= 0):
						CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, True)
				return 0


class TechChooserMaps:

		TechChooserInputMap = {
				'TechRecord': CvTechChooser().TechRecord,
				'TechID': CvTechChooser().ParentClick,
				'TechPane': CvTechChooser().ParentClick,
				'TechButtonID': CvTechChooser().ParentClick,
				'TechButtonBorder': CvTechChooser().ParentClick,
				'Unit': CvTechChooser().ParentClick,
				'Building': CvTechChooser().ParentClick,
				'Obsolete': CvTechChooser().ParentClick,
				'ObsoleteX': CvTechChooser().ParentClick,
				'Move': CvTechChooser().ParentClick,
				'FreeUnit': CvTechChooser().ParentClick,
				'FeatureProduction': CvTechChooser().ParentClick,
				'Worker': CvTechChooser().ParentClick,
				'TradeRoutes': CvTechChooser().ParentClick,
				'HealthRate': CvTechChooser().ParentClick,
				'HappinessRate': CvTechChooser().ParentClick,
				'FreeTech': CvTechChooser().ParentClick,
				'LOS': CvTechChooser().ParentClick,
				'MapCenter': CvTechChooser().ParentClick,
				'MapReveal': CvTechChooser().ParentClick,
				'MapTrade': CvTechChooser().ParentClick,
				'TechTrade': CvTechChooser().ParentClick,
				'OpenBorders': CvTechChooser().ParentClick,
				'BuildBridge': CvTechChooser().ParentClick,
				'Irrigation': CvTechChooser().ParentClick,
				'Improvement': CvTechChooser().ParentClick,
				'DomainExtraMoves': CvTechChooser().ParentClick,
				'AdjustButton': CvTechChooser().ParentClick,
				'TerrainTradeButton': CvTechChooser().ParentClick,
				'SpecialBuildingButton': CvTechChooser().ParentClick,
				'YieldChangeButton': CvTechChooser().ParentClick,
				'BonusRevealButton': CvTechChooser().ParentClick,
				'CivicRevealButton': CvTechChooser().ParentClick,
				'ProjectInfoButton': CvTechChooser().ParentClick,
				'ProcessInfoButton': CvTechChooser().ParentClick,
				'FoundReligionButton': CvTechChooser().ParentClick,
				'CivDropDown': CvTechChooser().CivDropDown,
		}
