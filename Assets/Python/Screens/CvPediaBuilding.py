# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Edited by pie (pierre@voak.at), Austria 2016
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, GenericButtonSizes, FontSymbols,
																WidgetTypes, PanelStyles, CyGame, TableStyles,
																CommerceTypes, YieldTypes, CyGameTextMgr,
																isNationalWonderClass, isTeamWonderClass,
																isWorldWonderClass, isTechRequiredForBuilding,
																CivilopediaPageTypes)
import CvUtil
# import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvPediaBuilding:
		"Civilopedia Screen for Buildings"

		def __init__(self, main):
				self.iBuilding = -1
				self.bLastBuildingType = False
				self.top = main

				self.BUTTON_SIZE = 46

				self.X_BUILDING_PANE = 10
				self.Y_BUILDING_PANE = 57
				self.W_BUILDING_PANE = 405
				self.H_BUILDING_PANE = 200

				self.X_BUILDING_ANIMATION = 421
				self.Y_BUILDING_ANIMATION = 65
				self.W_BUILDING_ANIMATION = 365
				self.H_BUILDING_ANIMATION = 191
				self.X_ROTATION_BUILDING_ANIMATION = -20
				self.Z_ROTATION_BUILDING_ANIMATION = 30
				self.SCALE_ANIMATION = 1.0

				self.X_STATS_PANE = 157
				self.Y_STATS_PANE = 100
				self.W_STATS_PANE = 250
				self.H_STATS_PANE = 200

				self.X_ICON = 40
				self.Y_ICON = 90
				self.W_ICON = 100
				self.H_ICON = 100
				self.ICON_SIZE = 64

				self.X_PREREQ_PANE = 10
				self.Y_PREREQ_PANE = 257
				self.W_PREREQ_PANE = 405
				self.H_PREREQ_PANE = 100

				self.X_SPECIAL_PANE = 10
				self.Y_SPECIAL_PANE = 365
				self.W_SPECIAL_PANE = 405
				self.H_SPECIAL_PANE = 345

				self.X_HISTORY_PANE = 420
				self.Y_HISTORY_PANE = 257
				self.W_HISTORY_PANE = 366
				self.H_HISTORY_PANE = 453

		# Screen construction function
		def interfaceScreen(self, iBuilding):

				self.iBuilding = iBuilding

				self.top.deleteAllWidgets()

				screen = self.top.getScreen()

				bNotActive = (not screen.isActive())
				if bNotActive:  # or self.top.iLastScreen != CvScreenEnums.PEDIA_BUILDING: # PAE different Link menu height
						self.top.setPediaCommonWidgets()

				# Header...
				szHeader = u"<font=4b>" + gc.getBuildingInfo(self.iBuilding).getDescription().upper() + u"</font>"
				szHeaderId = self.top.getNextWidgetName()
				screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0,
												FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, iBuilding)

				# Top
				if self.getBuildingType(iBuilding):
						link = CivilopediaPageTypes.CIVILOPEDIA_PAGE_WONDER
				else:
						link = CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING
				screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY,
											 self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, link, -1)

				if self.top.iLastScreen != CvScreenEnums.PEDIA_BUILDING or bNotActive or self.bLastBuildingType != self.getBuildingType(self.iBuilding):
						self.placeLinks(True)
						self.top.iLastScreen = CvScreenEnums.PEDIA_BUILDING
				else:
						self.placeLinks(False)
				self.bLastBuildingType = self.getBuildingType(self.iBuilding)

				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				# Icon
				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
				screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBuildingInfo(self.iBuilding).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE /
												 2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Unit animation
				screen.addBuildingGraphicGFC(self.top.getNextWidgetName(), self.iBuilding, self.X_BUILDING_ANIMATION, self.Y_BUILDING_ANIMATION, self.W_BUILDING_ANIMATION,
																		 self.H_BUILDING_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BUILDING_ANIMATION, self.Z_ROTATION_BUILDING_ANIMATION, self.SCALE_ANIMATION, True)

				self.placeStats()

				self.placeRequires()

				self.placeSpecial()

				self.placeHistory()

		# Place happiness/health/commerce/great people modifiers

		def placeStats(self):

				screen = self.top.getScreen()

				buildingInfo = gc.getBuildingInfo(self.iBuilding)

				panelName = self.top.getNextWidgetName()

				if buildingInfo.getGreatPeopleRateChange() != 0:
						y = self.Y_STATS_PANE - 30
				else:
						y = self.Y_STATS_PANE

				screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, y, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
				screen.enableSelect(panelName, False)

				if (isWorldWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
						iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxGlobalInstances()
						szBuildingType = localText.getText("TXT_KEY_PEDIA_WORLD_WONDER", ())
						if (iMaxInstances > 1):
								szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
								screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				if (isTeamWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
						iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxTeamInstances()
						szBuildingType = localText.getText("TXT_KEY_PEDIA_TEAM_WONDER", ())
						if (iMaxInstances > 1):
								szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
								screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				if (isNationalWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
						iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxPlayerInstances()
						szBuildingType = localText.getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ())
						if (iMaxInstances > 1):
								szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
								screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				if (buildingInfo.getProductionCost() > 0):
						if self.top.iActivePlayer == -1:
								szCost = localText.getText("TXT_KEY_PEDIA_COST", ((buildingInfo.getProductionCost() * gc.getDefineINT("BUILDING_PRODUCTION_PERCENT"))/100,))
						else:
								szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getPlayer(self.top.iActivePlayer).getBuildingProductionNeeded(self.iBuilding),))
						screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() +
																							 u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				for k in range(YieldTypes.NUM_YIELD_TYPES):
						if (buildingInfo.getYieldChange(k) != 0):
								if (buildingInfo.getYieldChange(k) > 0):
										szSign = "+"
								else:
										szSign = ""

								szYield = gc.getYieldInfo(k).getDescription() + ": "

								szText1 = szYield.upper() + szSign + str(buildingInfo.getYieldChange(k))
								szText2 = szText1 + (u"%c" % (gc.getYieldInfo(k).getChar()))
								screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText2 + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				for k in range(CommerceTypes.NUM_COMMERCE_TYPES):

						iTotalCommerce = buildingInfo.getObsoleteSafeCommerceChange(k) + buildingInfo.getCommerceChange(k)
						if (iTotalCommerce != 0):
								if (iTotalCommerce > 0):
										szSign = "+"
								else:
										szSign = ""

								szCommerce = gc.getCommerceInfo(k).getDescription() + ": "

								szText1 = szCommerce.upper() + szSign + str(iTotalCommerce)
								szText2 = szText1 + (u"%c" % (gc.getCommerceInfo(k).getChar()))
								screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText2 + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				iHappiness = buildingInfo.getHappiness()
				if self.top.iActivePlayer != -1:
						if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
								iHappiness += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHappiness(self.iBuilding)

				if (iHappiness > 0):
						szText = localText.getText("TXT_KEY_PEDIA_HAPPY", (iHappiness,)).upper()
						screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) +
																							 u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				elif (iHappiness < 0):
						szText = localText.getText("TXT_KEY_PEDIA_UNHAPPY", (-iHappiness,)).upper()
						screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) +
																							 u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				iHealth = buildingInfo.getHealth()
				if self.top.iActivePlayer != -1:
						if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
								iHealth += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHealth(self.iBuilding)

				if (iHealth > 0):
						szText = localText.getText("TXT_KEY_PEDIA_HEALTHY", (iHealth,)).upper()
						screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) +
																							 u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				elif (iHealth < 0):
						szText = localText.getText("TXT_KEY_PEDIA_UNHEALTHY", (-iHealth,)).upper()
						screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) +
																							 u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				if (buildingInfo.getGreatPeopleRateChange() != 0):
						szText = localText.getText("TXT_KEY_PEDIA_GREAT_PEOPLE", (buildingInfo.getGreatPeopleRateChange(),)).upper()
						screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR) +
																							 u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				# PAE: Conquest Probabilty
				szText = localText.getText("TXT_KEY_PEDIA_CONQUER", ()).upper() + u": " + str(buildingInfo.getConquestProbability()) + u"%"
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				screen.updateListBox(panelName)

		# Place prereqs (techs, resources)
		def placeRequires(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True,
												self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE+10, PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				# add tech buttons
				for iPrereq in range(gc.getNumTechInfos()):
						if isTechRequiredForBuilding(iPrereq, self.iBuilding):
								screen.attachImageButton(panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False)

				# add req buildings
				for iPrereq in range(gc.getNumBuildingInfos()):
						if gc.getBuildingInfo(self.iBuilding).isBuildingClassNeededInCity(gc.getBuildingInfo(iPrereq).getBuildingClassType()):
								screen.attachImageButton(panelName, "", gc.getBuildingInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPrereq, -1, False)

				# add resource buttons
				iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqAndBonus()
				if (iPrereq >= 0):
						screen.attachImageButton(panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False)

				for k in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
						iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqOrBonuses(k)
						if (iPrereq >= 0):
								screen.attachImageButton(panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False)

				iCorporation = gc.getBuildingInfo(self.iBuilding).getFoundsCorporation()
				bFirst = True
				if (iCorporation >= 0):
						for k in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
								iPrereq = gc.getCorporationInfo(iCorporation).getPrereqBonus(k)
								if (iPrereq >= 0):
										if not bFirst:
												screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
										else:
												bFirst = False
										screen.attachImageButton(panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False)

				# add religion button
				iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqReligion()
				if (iPrereq >= 0):
						screen.attachImageButton(panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, -1, False)

				# PAE - add corporation button
				iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqCorporation()
				if (iPrereq >= 0):
						screen.attachImageButton(panelName, "", gc.getCorporationInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, iPrereq, -1, False)

		# Place Special abilities

		def placeSpecial(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False,
												self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				listName = self.top.getNextWidgetName()

				szSpecialText = ""

				# PAE - Part of Victory type
				iBuildingClassType = gc.getBuildingInfo(self.iBuilding).getBuildingClassType()
				for iLoopVC in range(gc.getNumVictoryInfos()):
						victory = gc.getVictoryInfo(iLoopVC)
						if (gc.getBuildingClassInfo(iBuildingClassType).getVictoryThreshold(iLoopVC) > 0):
								szSpecialText = localText.getText("TXT_KEY_BUILDING_PART_OF_VICTORY", (victory.getDescription(),)) + localText.getText("[NEWLINE]", ())

				# PAE - negative food storage
				if gc.getBuildingInfo(self.iBuilding).getFoodKept() < 0:
						szSpecialText = localText.getText("TXT_KEY_BUILDING_STORES_FOOD2", (gc.getBuildingInfo(self.iBuilding).getFoodKept(),)) + localText.getText("[NEWLINE]", ())

				szSpecialText += CyGameTextMgr().getBuildingHelp(self.iBuilding, True, False, False, None)[1:]
				screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE -
																10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeHistory(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True,
												self.X_HISTORY_PANE, self.Y_HISTORY_PANE,
												self.W_HISTORY_PANE, self.H_HISTORY_PANE,
												PanelStyles.PANEL_STYLE_BLUE50)

				textName = self.top.getNextWidgetName()
				szText = u""
				if len(gc.getBuildingInfo(self.iBuilding).getStrategy()) > 0:
						szText += localText.getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
						szText += gc.getBuildingInfo(self.iBuilding).getStrategy()
						szText += u"\n\n"
				szText += localText.getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
				szText += gc.getBuildingInfo(self.iBuilding).getCivilopedia()
				screen.addMultilineText(textName, szText, self.X_HISTORY_PANE + 10, self.Y_HISTORY_PANE + 40,
																self.W_HISTORY_PANE - 10, self.H_HISTORY_PANE - 55, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeLinks(self, bRedraw):

				screen = self.top.getScreen()

				if bRedraw:
						screen.clearListBoxGFC(self.top.LIST_ID)

				listSorted = self.getBuildingSortedList(self.getBuildingType(self.iBuilding))

				iSelected = 0
				i = 0
				A = ""
				for iI in range(len(listSorted)):
						if (not gc.getBuildingInfo(listSorted[iI][1]).isGraphicalOnly()):
								if (not gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") or not gc.getGame().isFinalInitialized() or gc.getGame().isBuildingEverActive(listSorted[iI][1])):

										# Buchstabe
										B = listSorted[iI][0][:1]
										if A != B:
												A = B
												i += 1  # Zeile in der linken Navi
												# Buchstabe anzeigen
												if bRedraw:
														screen.appendListBoxStringNoUpdate(self.top.LIST_ID, u"<font=2>[" + A + u"]</font>", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

										# Name anzeigen
										if bRedraw:
												screen.appendListBoxStringNoUpdate(self.top.LIST_ID, listSorted[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, listSorted[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY)
										if listSorted[iI][1] == self.iBuilding:
												iSelected = i
										i += 1

				if bRedraw:
						screen.updateListBox(self.top.LIST_ID)

				screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

		# BTS Standard
		"""
		def getBuildingType(self, iBuilding):
			if (isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
				return True

			if (isTeamWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
				return True

			if (isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
				return True

			# Regular building
			return False
			
		def getBuildingSortedList(self, bWonder):
			listBuildings = []
			iCount = 0
			for iBuilding in range(gc.getNumBuildingInfos()):
				if (self.getBuildingType(iBuilding) == bWonder and not gc.getBuildingInfo(iBuilding).isGraphicalOnly()):
					listBuildings.append(iBuilding)
					iCount += 1
			
			listSorted = [(0,0)] * iCount
			iI = 0
			for iBuilding in listBuildings:
				listSorted[iI] = (gc.getBuildingInfo(iBuilding).getDescription(), iBuilding)
				iI += 1
			listSorted.sort()
			return listSorted
		"""
		# ---------------

		# PAE
		def getBuildingType(self, iBuilding):
				if (isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
						return 1

				if (isTeamWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
						return 1

				if (isNationalWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
						return 2

				# Special Building
				#lBuildingClasses = self.getStandardBuildings()
				#if iBuilding not in lBuildingClasses:
				#		return 3

				# Regular building
				return 0

		# iTyp: 0=normal, 1=wonder, 2=national, 3=special
		def getBuildingSortedList(self, iTyp):
				listBuildings = []
				iCount = 0

				#lBuildingClasses = []
				#if iTyp == 0 or iTyp == 3:
				#		lBuildingClasses = self.getStandardBuildings()

				for iBuilding in range(gc.getNumBuildingInfos()):
						if not gc.getBuildingInfo(iBuilding).isGraphicalOnly() and gc.getBuildingInfo(iBuilding).getArtDefineTag() != "ART_DEF_BUILDING_FAKE":
								if (iTyp == 0 and self.getBuildingType(iBuilding) == 0 or #and iBuilding in lBuildingClasses or
										iTyp == 1 and self.getBuildingType(iBuilding) == 1 or
										iTyp == 2 and self.getBuildingType(iBuilding) == 2
										#iTyp == 3 and self.getBuildingType(iBuilding) == 3
										):
										listBuildings.append(iBuilding)
										iCount += 1

				listSorted = [(0, 0)] * iCount
				iI = 0
				for iBuilding in listBuildings:
						listSorted[iI] = (gc.getBuildingInfo(iBuilding).getDescription(), iBuilding)
						iI += 1
				listSorted.sort()
				return listSorted

		def getStandardBuildings(self):
				list = []
				for i in range(gc.getNumBuildingClassInfos()):
						iBuilding = gc.getBuildingClassInfo(i).getDefaultBuildingIndex()
						if iBuilding != -1 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0:
								list.append(iBuilding)
				return list


		# Will handle the input for this screen...

		def handleInput(self, inputClass):
				return 0
