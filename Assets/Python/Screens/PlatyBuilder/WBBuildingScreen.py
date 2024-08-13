from CvPythonExtensions import (CyGlobalContext, CyGame,
																PanelStyles, CyTranslator, PopupStates,
																WidgetTypes, FontTypes, TableStyles,
																isLimitedWonderClass, isWorldWonderClass,
																isNationalWonderClass, isTeamWonderClass)
import CvUtil
if not CvUtil.isPitbossHost():
    from CvPythonExtensions import CyGInterfaceScreen

# import ScreenInput
import CvScreenEnums
import WBCityDataScreen
import WBCityEditScreen
import WBPlayerScreen
import WBTeamScreen
import WBPlotScreen
import WBEventScreen
import WBPlayerUnits
import WBReligionScreen
import WBCorporationScreen
import WBInfoScreen
import CvPlatyBuilderScreen
import CvEventManager

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range

gc = CyGlobalContext()

iChangeType = 2
iSelectedClass = 0
bApplyAll = False
iSelectedEra = -1

# changed for PAE


class WBBuildingScreen:

		def interfaceScreen(self, pCityX):
				screen = CyGInterfaceScreen("WBBuildingScreen", CvScreenEnums.WB_BUILDING)
				global pCity
				global iPlayer

				pCity = pCityX
				iPlayer = pCity.getOwner()

				screen.setRenderInterfaceOnly(True)
				screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN)
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

				screen.setLabel("BuildingHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY,
												screen.getXResolution() * 5/8 - 10, screen.getYResolution()/2, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabel("WonderHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()) + "</font>",
												CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() * 5/8 - 10, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_GRANT_AVAILABLE", ()) + "</color></font>"
				screen.setText("BuildingAvailable", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() * 5 /
											 8 - 10, screen.getYResolution()/2 + 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setText("WonderAvailable", "Background", sText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() * 5/8 - 10, 50, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setText("WBBuildingExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY,
											 screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

				iHeight = (screen.getYResolution() - 42 - 50) / 24 * 24 + 2
				iWidth = screen.getXResolution()/4 - 40
				screen.addTableControlGFC("CurrentCity", 1, 20, 80, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.setTableColumnHeader("CurrentCity", 0, "", iWidth)

				pPlayer = gc.getPlayer(iPlayer)
				(loopCity, pIter) = pPlayer.firstCity(False)
				while(loopCity):
						if not loopCity.isNone() and loopCity.getOwner() == pPlayer.getID():  # only valid cities
								iRow = screen.appendTableRow("CurrentCity")
								sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
								if loopCity.getID() == pCity.getID():
										sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
								screen.setTableText("CurrentCity", 0, iRow, "<font=3>" + sColor + loopCity.getName() + "</font></color>", gc.getCivilizationInfo(pCity.getCivilizationType()
																																																																								 ).getButton(), WidgetTypes.WIDGET_PYTHON, 7200 + iPlayer, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						(loopCity, pIter) = pPlayer.nextCity(pIter, False)

				# Era
				screen.addDropDownBoxGFC("TechEra", screen.getXResolution()/4, 20, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("TechEra", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), -1, -1, True)
				for i in xrange(gc.getNumEraInfos()):
						screen.addPullDownString("TechEra", gc.getEraInfo(i).getDescription(), i, i, i == iSelectedEra)

				screen.addDropDownBoxGFC("WonderClass", screen.getXResolution()/4, 50, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("WonderClass", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), 0, 0, iSelectedClass == 0)
				screen.addPullDownString("WonderClass", CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ()), 1, 1, iSelectedClass == 1)
				screen.addPullDownString("WonderClass", CyTranslator().getText("TXT_KEY_PEDIA_TEAM_WONDER", ()), 2, 2, iSelectedClass == 2)
				screen.addPullDownString("WonderClass", CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ()), 3, 3, iSelectedClass == 3)

				screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY_DATA", ()), 0, 0, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_CITY_DATA2", ()), 1, 1, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), 2, 2, True)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 3, 3, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 4, 4, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 8, 8, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 9, 9, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 5, 5, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ()), 6, 6, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ()), 7, 7, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

				sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()),)) + "</font>"
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if bApplyAll:
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				screen.setText("ApplyAll", "Background", sColor + sText + "</color>", CvUtil.FONT_LEFT_JUSTIFY, screen.getXResolution() /
											 4, screen.getYResolution()/2 + 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				screen.addDropDownBoxGFC("ChangeType", screen.getXResolution() - 170, 20, 150, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_MODIFY", ("",)), 2, 2, 2 == iChangeType)
				screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, 1 == iChangeType)
				screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, 0 == iChangeType)

				sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</color></font>"
				screen.setText("BuildingAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20,
											 screen.getYResolution()/2 + 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setText("WonderAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 20, 50, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				self.createTechList()
				self.sortBuildings()

		def sortBuildings(self):
				global lBuilding
				global lNational
				global lTeam
				global lWorld
				lBuilding = []
				lNational = []
				lTeam = []
				lWorld = []

				for i in xrange(gc.getNumBuildingInfos()):
						BuildingInfo = gc.getBuildingInfo(i)
						iClass = BuildingInfo.getBuildingClassType()
						if CvPlatyBuilderScreen.bHideInactive:
								if gc.getCivilizationInfo(pCity.getCivilizationType()).getCivilizationBuildings(iClass) != i:
										continue

						if iSelectedEra == -1 or BuildingInfo.getPrereqAndTech() in lTech:
								if isNationalWonderClass(iClass):
										lNational.append([BuildingInfo.getDescription(), i])
								elif isTeamWonderClass(iClass):
										lTeam.append([BuildingInfo.getDescription(), i])
								elif isWorldWonderClass(iClass):
										lWorld.append([BuildingInfo.getDescription(), i])
								else:
										lBuilding.append([BuildingInfo.getDescription(), i])
				lNational.sort()
				lTeam.sort()
				lWorld.sort()
				lBuilding.sort()
				self.placeBuildings()
				self.placeWonders()

		def placeWonders_BCP(self):
				screen = CyGInterfaceScreen("WBBuildingScreen", CvScreenEnums.WB_BUILDING)
				if iSelectedClass == 0:
						lWonders = lNational + lTeam + lWorld
				elif iSelectedClass == 1:
						lWonders = lNational
				elif iSelectedClass == 2:
						lWonders = lTeam
				else:
						lWonders = lWorld

				iWidth = screen.getXResolution() * 3/4 - 20
				iMaxRows = (screen.getYResolution()/2 - 80) / 24
				nColumns = max(1, min(iWidth/180, (len(lBuilding) + iMaxRows - 1)/iMaxRows))
				iHeight = iMaxRows * 24 + 2
				screen.addTableControlGFC("WBWonders", nColumns, screen.getXResolution()/4, 80, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				for i in xrange(nColumns):
						screen.setTableColumnHeader("WBWonders", i, "", iWidth/nColumns)

				nRows = (len(lWonders) + nColumns - 1) / nColumns
				for i in xrange(nRows):
						screen.appendTableRow("WBWonders")

				for iCount in xrange(len(lWonders)):
						item = lWonders[iCount]
						iRow = iCount % nRows
						iColumn = iCount / nRows
						ItemInfo = gc.getBuildingInfo(item[1])
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if pCity.getNumRealBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						elif pCity.isHasBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
						screen.setTableText("WBWonders", iColumn, iRow, "<font=3>" + sColor + item[0] + "</font></color>",
																ItemInfo.getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeBuildings_BCP(self):
				screen = CyGInterfaceScreen("WBBuildingScreen", CvScreenEnums.WB_BUILDING)
				iWidth = screen.getXResolution() * 3/4 - 20
				iMaxRows = (screen.getYResolution()/2 - 102) / 24
				nColumns = max(1, min(iWidth/180, (len(lBuilding) + iMaxRows - 1)/iMaxRows))
				iHeight = iMaxRows * 24 + 2
				screen.addTableControlGFC("WBBuilding", nColumns, screen.getXResolution()/4, screen.getYResolution()/2 + 60, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)

				# c1 = 0
				# c2 = 1
				for i in xrange(nColumns):
						screen.setTableColumnHeader("WBBuilding", i, "", iWidth/nColumns)

				nRows = len(lBuilding) / nColumns
				if len(lBuilding) % nColumns:
						nRows += 1
				for i in xrange(nRows):
						screen.appendTableRow("WBBuilding")

				for iCount in xrange(len(lBuilding)):
						item = lBuilding[iCount]
						iRow = iCount % nRows
						iColumn = iCount / nRows
						ItemInfo = gc.getBuildingInfo(item[1])
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if pCity.getNumRealBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						elif pCity.isHasBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
						screen.setTableText("WBBuilding", iColumn, iRow, "<font=3>" + sColor + item[0] + "</font></color>",
																ItemInfo.getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeWonders(self):
				screen = CyGInterfaceScreen("WBBuildingScreen", CvScreenEnums.WB_BUILDING)
				if iSelectedClass == 0:
						lWonders = lNational + lTeam + lWorld
				elif iSelectedClass == 1:
						lWonders = lNational
				elif iSelectedClass == 2:
						lWonders = lTeam
				else:
						lWonders = lWorld

				iWidth = screen.getXResolution() * 3/4 - 20
				iMaxRows = (screen.getYResolution()/2 - 80) / 24
				nColumns = 4
				iHeight = iMaxRows * 24 + 2
				screen.addTableControlGFC("WBWonders", nColumns*2, screen.getXResolution()/4, 80, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				c1 = 0
				c2 = 1
				for i in xrange(nColumns):
						screen.setTableColumnHeader("WBWonders", c1, "", iWidth/nColumns-33)
						screen.setTableColumnHeader("WBWonders", c2, "", 30)
						c1 = c1 + 2
						c2 = c2 + 2

				nRows = (len(lWonders) + nColumns - 1) / nColumns
				for i in xrange(nRows):
						screen.appendTableRow("WBWonders")

				for iCount in xrange(len(lWonders)):
						item = lWonders[iCount]
						iRow = iCount % nRows
						iColumn = iCount / nRows * 2
						ItemInfo = gc.getBuildingInfo(item[1])
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if pCity.getNumRealBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						elif pCity.isHasBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
						screen.setTableText("WBWonders", iColumn, iRow, "<font=3>" + sColor + item[0] + "</font></color>",
																ItemInfo.getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)

						button = ""
						if ItemInfo.getProductionCost() == -1:
								button = gc.getTechInfo(gc.getInfoTypeForString("TECH_NONE")).getButton()
						if pCity.canConstruct(item[1], 0, 0, 0):
								button = "Art/Interface/Buttons/General/CheckMark.dds"
						elif not pCity.isHasBuilding(item[1]) and gc.getGame().isBuildingEverActive(item[1]):
								button = gc.getTechInfo(gc.getInfoTypeForString("TECH_NONE")).getButton()

						screen.setTableText("WBWonders", iColumn+1, iRow, "", button, WidgetTypes.WIDGET_PYTHON, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		def placeBuildings(self):
				screen = CyGInterfaceScreen("WBBuildingScreen", CvScreenEnums.WB_BUILDING)
				iWidth = screen.getXResolution() * 3/4 - 20
				iMaxRows = (screen.getYResolution()/2 - 102) / 24
				nColumns = 4
				iHeight = iMaxRows * 24 + 2
				screen.addTableControlGFC("WBBuilding", nColumns*2, screen.getXResolution()/4, screen.getYResolution()/2 + 60, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)

				c1 = 0
				c2 = 1
				for i in xrange(nColumns):
						screen.setTableColumnHeader("WBBuilding", c1, "", iWidth/nColumns-33)
						screen.setTableColumnHeader("WBBuilding", c2, "", 30)
						c1 = c1 + 2
						c2 = c2 + 2

				nRows = (len(lBuilding) + nColumns - 1) / nColumns
				for i in xrange(nRows):
						screen.appendTableRow("WBBuilding")

				for iCount in xrange(len(lBuilding)):
						item = lBuilding[iCount]
						iRow = iCount % nRows
						iColumn = iCount / nRows * 2
						ItemInfo = gc.getBuildingInfo(item[1])
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if pCity.getNumRealBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						elif pCity.isHasBuilding(item[1]):
								sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
						screen.setTableText("WBBuilding", iColumn, iRow, "<font=3>" + sColor + item[0] + "</font></color>",
																ItemInfo.getButton(), WidgetTypes.WIDGET_HELP_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)

						button = ""
						if ItemInfo.getProductionCost() == -1:
								button = gc.getTechInfo(gc.getInfoTypeForString("TECH_NONE")).getButton()

								# Stadtstatus
								if item[1] == gc.getInfoTypeForString("BUILDING_SIEDLUNG"):
										if pCity.isHasBuilding(item[1]):
												button = "Art/Interface/Buttons/General/CheckMark.dds"
										else:
												button = "Art/Interface/PlotPicker/Warning.dds"
								elif item[1] == gc.getInfoTypeForString("BUILDING_KOLONIE"):
										if pCity.getPopulation() >= 3:
												if pCity.isHasBuilding(item[1]):
														button = "Art/Interface/Buttons/General/CheckMark.dds"
												else:
														button = "Art/Interface/PlotPicker/Warning.dds"
								elif item[1] == gc.getInfoTypeForString("BUILDING_STADT"):
										if pCity.getPopulation() >= 6:
												if pCity.isHasBuilding(item[1]):
														button = "Art/Interface/Buttons/General/CheckMark.dds"
												else:
														button = "Art/Interface/PlotPicker/Warning.dds"
								elif item[1] == gc.getInfoTypeForString("BUILDING_PROVINZ"):
										if pCity.getPopulation() >= 12:
												if pCity.isHasBuilding(item[1]):
														button = "Art/Interface/Buttons/General/CheckMark.dds"
												else:
														button = "Art/Interface/PlotPicker/Warning.dds"
								elif item[1] == gc.getInfoTypeForString("BUILDING_METROPOLE"):
										if pCity.getPopulation() >= 20:
												if pCity.isHasBuilding(item[1]):
														button = "Art/Interface/Buttons/General/CheckMark.dds"
												else:
														button = "Art/Interface/PlotPicker/Warning.dds"

						if pCity.canConstruct(item[1], 0, 0, 0):
								button = "Art/Interface/Buttons/General/CheckMark.dds"
						screen.setTableText("WBBuilding", iColumn+1, iRow, "", button, WidgetTypes.WIDGET_PYTHON, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		def handleInput(self, inputClass):
				screen = CyGInterfaceScreen("WBBuildingScreen", CvScreenEnums.WB_BUILDING)
				global bApplyAll
				global iSelectedClass
				global iChangeType
				global iSelectedEra

				if inputClass.getFunctionName() == "TechEra":
						iSelectedEra = inputClass.getData() - 1
						self.createTechList()
						self.sortBuildings()
						self.placeBuildings()
						self.placeWonders()

				if inputClass.getFunctionName() == "CurrentPage":
						iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
						if iIndex == 0:
								WBCityEditScreen.WBCityEditScreen().interfaceScreen(pCity)
						elif iIndex == 1:
								WBCityDataScreen.WBCityDataScreen().interfaceScreen(pCity)
						elif iIndex == 3:
								WBPlayerScreen.WBPlayerScreen().interfaceScreen(iPlayer)
						elif iIndex == 4:
								WBTeamScreen.WBTeamScreen().interfaceScreen(pCity.getTeam())
						elif iIndex == 5:
								WBPlayerUnits.WBPlayerUnits().interfaceScreen(iPlayer)
						elif iIndex == 6:
								WBPlotScreen.WBPlotScreen().interfaceScreen(pCity.plot())
						elif iIndex == 7:
								WBEventScreen.WBEventScreen().interfaceScreen(pCity.plot())
						elif iIndex == 8:
								WBReligionScreen.WBReligionScreen().interfaceScreen(iPlayer)
						elif iIndex == 9:
								WBCorporationScreen.WBCorporationScreen().interfaceScreen(iPlayer)
						elif iIndex == 11:
								WBInfoScreen.WBInfoScreen().interfaceScreen(iPlayer)

				elif inputClass.getFunctionName() == "ChangeType":
						iChangeType = screen.getPullDownData("ChangeType", screen.getSelectedPullDownID("ChangeType"))

				elif inputClass.getFunctionName() == "CurrentCity":
						self.interfaceScreen(gc.getPlayer(iPlayer).getCity(inputClass.getData2()))

				elif inputClass.getFunctionName() == "WBBuilding":
						bUpdate = self.editBuilding(inputClass.getData1(), gc.getPlayer(iPlayer), False, False)
						self.placeBuildings()
						if bUpdate:
								self.placeWonders()

				elif inputClass.getFunctionName() == "BuildingAvailable":
						bUpdate = False
						for item in lBuilding:
								bTemp = self.editBuilding(item[1], gc.getPlayer(iPlayer), True, False)
								bUpdate = bUpdate or bTemp
						self.placeBuildings()
						if bUpdate:
								self.placeWonders()

				elif inputClass.getFunctionName() == "BuildingAll":
						bUpdate = False
						for item in lBuilding:
								bTemp = self.editBuilding(item[1], gc.getPlayer(iPlayer), False, False)
								bUpdate = bUpdate or bTemp
						self.placeBuildings()
						if bUpdate:
								self.placeWonders()

				elif inputClass.getFunctionName() == "WonderClass":
						iSelectedClass = inputClass.getData()
						self.placeWonders()

				elif inputClass.getFunctionName() == "WBWonders":
						bUpdate = self.editBuilding(inputClass.getData1(), gc.getPlayer(iPlayer), False, True)
						self.placeWonders()
						if bUpdate:
								self.placeBuildings()

				elif inputClass.getFunctionName() == "WonderAvailable":
						bUpdate = False
						lList = lWorld
						if iSelectedClass == 0:
								lList = lNational + lTeam + lWorld
						elif iSelectedClass == 1:
								lList = lNational
						elif iSelectedClass == 2:
								lList = lTeam
						for item in lList:
								bTemp = self.editBuilding(item[1], gc.getPlayer(iPlayer), True, True)
								bUpdate = bUpdate or bTemp
						self.placeWonders()
						if bUpdate:
								self.placeBuildings()

				elif inputClass.getFunctionName() == "WonderAll":
						bUpdate = False
						lList = lWorld
						if iSelectedClass == 0:
								lList = lNational + lTeam + lWorld
						elif iSelectedClass == 1:
								lList = lNational
						elif iSelectedClass == 2:
								lList = lTeam
						for item in lList:
								bTemp = self.editBuilding(item[1], gc.getPlayer(iPlayer), False, True)
								bUpdate = bUpdate or bTemp
						self.placeWonders()
						if bUpdate:
								self.placeBuildings()

				elif inputClass.getFunctionName() == "ApplyAll":
						bApplyAll = not bApplyAll
						sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()),)) + "</font>"
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if bApplyAll:
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						screen.modifyString("ApplyAll", sColor + sText + "</color>", 0)
				return 1

		def editBuilding(self, item, pPlayerX, bAvailable, bWonder):
				ItemInfo = gc.getBuildingInfo(item)
				iType = iChangeType or bAvailable
				if bApplyAll and not bWonder:
						(loopCity, pIter) = pPlayerX.firstCity(False)
						while(loopCity):
								if not loopCity.isNone() and loopCity.getOwner() == pPlayerX.getID():  # only valid cities
										bModify = True
										if ItemInfo.isWater() and not loopCity.isCoastal(ItemInfo.getMinAreaSize()):
												bModify = False
										if ItemInfo.isRiver() and not loopCity.plot().isRiver():
												bModify = False
										if bAvailable:
												if ItemInfo.isCapital():
														bModify = False
												iHolyReligion = ItemInfo.getHolyCity()
												if iHolyReligion > -1 and not loopCity.isHolyCityByType(iHolyReligion):
														bModify = False
												if not loopCity.canConstruct(item, True, False, True):
														bModify = False
												#iBuilding = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(item)
												#if not loopCity.canConstruct(iBuilding, True, False, True): bModify = False
										if bModify:
												if iChangeType == 2 and not bAvailable:
														iType = not loopCity.getNumRealBuilding(item)
												self.doEffects(loopCity, item, iType)
								(loopCity, pIter) = pPlayerX.nextCity(pIter, False)
				else:
						if bAvailable:
								if ItemInfo.isCapital():
										return
								iHolyReligion = ItemInfo.getHolyCity()
								if iHolyReligion > -1 and not pCity.isHolyCityByType(iHolyReligion):
										return
								if not pCity.canConstruct(item, True, False, True):
										return
								#iBuilding = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(item)
								# if not pCity.canConstruct(iBuilding, True, False, True): return
						if iChangeType == 2 and not bAvailable:
								iType = not pCity.getNumRealBuilding(item)
						self.doEffects(pCity, item, iType)
				iFreeBuilding = ItemInfo.getFreeBuildingClass()
				if iFreeBuilding > -1:
						if bWonder != isLimitedWonderClass(iFreeBuilding):
								return True
				return False

		def createTechList(self):
				global lTech
				lTech = []
				for i in xrange(gc.getNumTechInfos()):
						ItemInfo = gc.getTechInfo(i)
						if iSelectedEra == -1 or iSelectedEra == ItemInfo.getEra():
								lTech.append(i)

		def doEffects(self, pCity, item, bAdd):
				bEffects = False
				if bAdd and CvPlatyBuilderScreen.bPython and pCity.getNumRealBuilding(item) == 0:
						bEffects = True
				pCity.setNumRealBuilding(item, bAdd)
				if bEffects:
						CvEventManager.CvEventManager().onBuildingBuilt([pCity, item])

		def update(self, fDelta):
				return 1
