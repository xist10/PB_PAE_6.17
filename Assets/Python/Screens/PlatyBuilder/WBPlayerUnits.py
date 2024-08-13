from CvPythonExtensions import (CyGlobalContext, CyGame,
																PanelStyles, CyTranslator, PopupStates,
																WidgetTypes, FontTypes, TableStyles, PlayerTypes)
import CvUtil
if not CvUtil.isPitbossHost():
    from CvPythonExtensions import CyGInterfaceScreen

# import ScreenInput
import CvScreenEnums
import WBPlayerScreen
import WBTeamScreen
import WBProjectScreen
import WBTechScreen
import WBCityEditScreen
import WBUnitScreen
import WBInfoScreen
import CvPlatyBuilderScreen

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range

gc = CyGlobalContext()

iCityID = 0
iUnitID = 0


class WBPlayerUnits:

		def interfaceScreen(self, iPlayerX):
				screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
				global iPlayer
				global pPlayer
				global iTeam
				global pTeam
				global iMapWidth
				global iMapHeight
				iPlayer = iPlayerX
				pPlayer = gc.getPlayer(iPlayer)
				iTeam = pPlayer.getTeam()
				pTeam = gc.getTeam(iTeam)
				iMapWidth = screen.getXResolution()/4
				iMapHeight = iMapWidth * 3/4

				screen.setRenderInterfaceOnly(True)
				screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN)
				screen.setDimensions(0, 0, screen.getXResolution(), screen.getYResolution())
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
				screen.setText("WBExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY,
											 screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

				screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 0, 0, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 1, 1, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 3, 3, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 4, 4, True)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

				screen.addDropDownBoxGFC("CurrentPlayer", 20, 20, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in xrange(gc.getMAX_PLAYERS()):
						pPlayerX = gc.getPlayer(i)
						if pPlayerX.isEverAlive():
								sText = pPlayerX.getName()
								if not pPlayerX.isAlive():
										sText = "*" + sText
								screen.addPullDownString("CurrentPlayer", sText, i, i, i == iPlayer)

				screen.setImageButton("DeleteAllCities", "Art/Interface/Buttons/Actions/Delete.dds", screen.getXResolution()/2 - 35, 50 + iMapHeight, 28, 28, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabel("DeleteCitiesText", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY,
												screen.getXResolution()/2 - 35, 50 + iMapHeight, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButton("DeleteAllUnits", "Art/Interface/Buttons/Actions/Delete.dds", screen.getXResolution() - 45, 50 + iMapHeight, 28, 28, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabel("DeleteUnitsText", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY,
												screen.getXResolution() - 45, 50 + iMapHeight, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				self.setCityTable()
				self.setUnitTable()

		def setUnitTable(self):
				screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
				global iUnitID
				iY = 80 + iMapHeight
				iWidth = screen.getXResolution()/2 - 30
				iHeight = (screen.getYResolution() - iY - 42) / 24 * 24 + 2
				iColWidth = (iWidth - 48) / 10

				screen.addTableControlGFC("WBUnitList", 7, 10 + screen.getXResolution()/2, iY, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.setTableColumnHeader("WBUnitList", 0, "", 24)
				screen.setTableColumnHeader("WBUnitList", 1, "", 24)
				screen.setTableColumnHeader("WBUnitList", 2, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()), iColWidth * 4)
				screen.setTableColumnHeader("WBUnitList", 3, CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " ID", iColWidth * 2)
				screen.setTableColumnHeader("WBUnitList", 4, CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()), iColWidth * 2)
				screen.setTableColumnHeader("WBUnitList", 5, "X", iColWidth)
				screen.setTableColumnHeader("WBUnitList", 6, "Y", iColWidth)
				screen.enableSort("WBUnitList")

				(loopUnit, pIter) = pPlayer.firstUnit(False)
				while(loopUnit):
						iRow = screen.appendTableRow("WBUnitList")
						if pPlayer.getUnit(iUnitID).isNone():
								iUnitID = loopUnit.getID()
						screen.setTableText("WBUnitList", 0, iRow, "", "Art/Interface/Buttons/Actions/Delete.dds", WidgetTypes.WIDGET_PYTHON, 1031, loopUnit.getID(), CvUtil.FONT_CENTER_JUSTIFY)
						screen.setTableText("WBUnitList", 1, iRow, "", loopUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 1030, loopUnit.getID(), CvUtil.FONT_CENTER_JUSTIFY)
						screen.setTableText("WBUnitList", 2, iRow, "<font=3>" + loopUnit.getName() + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + iPlayer, loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableInt("WBUnitList", 3, iRow, "<font=3>" + str(loopUnit.getID()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + iPlayer, loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableInt("WBUnitList", 4, iRow, "<font=3>" + str(loopUnit.plot().getArea()) + "</font>", "",
															 WidgetTypes.WIDGET_PYTHON, 8300 + iPlayer, loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableInt("WBUnitList", 5, iRow, "<font=3>" + str(loopUnit.getX()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + iPlayer, loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableInt("WBUnitList", 6, iRow, "<font=3>" + str(loopUnit.getY()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8300 + iPlayer, loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						(loopUnit, pIter) = pPlayer.nextUnit(pIter, False)
				self.placeUnitMap()

		def setCityTable(self):
				screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
				global iCityID
				iY = 80 + iMapHeight
				iWidth = screen.getXResolution()/2 - 30
				iHeight = (screen.getYResolution() - iY - 42) / 24 * 24 + 2
				iColWidth = (iWidth - 48) / 10

				screen.addTableControlGFC("WBCityList", 7, 20, iY, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.setTableColumnHeader("WBCityList", 0, "", 24)
				screen.setTableColumnHeader("WBCityList", 1, "", 24)
				screen.setTableColumnHeader("WBCityList", 2, CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), iColWidth * 4)
				screen.setTableColumnHeader("WBCityList", 3, CyTranslator().getText("TXT_KEY_WB_CITY", ()) + " ID", iColWidth * 2)
				screen.setTableColumnHeader("WBCityList", 4, CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()), iColWidth * 2)
				screen.setTableColumnHeader("WBCityList", 5, "X", iColWidth)
				screen.setTableColumnHeader("WBCityList", 6, "Y", iColWidth)
				screen.enableSort("WBCityList")

				(loopCity, pIter) = pPlayer.firstCity(False)
				while(loopCity):
						if not loopCity.isNone() and loopCity.getOwner() == pPlayer.getID():  # only valid cities
								iRow = screen.appendTableRow("WBCityList")
								if pPlayer.getCity(iCityID).isNone():
										iCityID = loopCity.getID()
								screen.setTableText("WBCityList", 0, iRow, "", "Art/Interface/Buttons/Actions/Delete.dds", WidgetTypes.WIDGET_PYTHON, 1031, loopCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
								screen.setTableText("WBCityList", 1, iRow, "", gc.getCivilizationInfo(loopCity.getCivilizationType()).getButton(),
																		WidgetTypes.WIDGET_PYTHON, 1030, loopCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
								screen.setTableText("WBCityList", 2, iRow, "<font=3>" + loopCity.getName() + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + iPlayer, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableInt("WBCityList", 3, iRow, "<font=3>" + str(loopCity.getID()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + iPlayer, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableInt("WBCityList", 4, iRow, "<font=3>" + str(loopCity.plot().getArea()) + "</font>", "",
																	 WidgetTypes.WIDGET_PYTHON, 7200 + iPlayer, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableInt("WBCityList", 5, iRow, "<font=3>" + str(loopCity.getX()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + iPlayer, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableInt("WBCityList", 6, iRow, "<font=3>" + str(loopCity.getY()) + "</font>", "", WidgetTypes.WIDGET_PYTHON, 7200 + iPlayer, loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						(loopCity, pIter) = pPlayer.nextCity(pIter, False)
				self.placeCityMap()

		def placeCityMap(self):
				screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
				pCity = pPlayer.getCity(iCityID)
				if pCity.isNone():
						return
				screen.setLabel("GoToCity", "Background", "<font=4b>" + pCity.getName() + "</font>", CvUtil.FONT_CENTER_JUSTIFY,
												screen.getXResolution()/4, 50, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addPlotGraphicGFC("CityView", screen.getXResolution()/4 - iMapWidth/2, 80, iMapWidth, iMapHeight, pCity.plot(), 350, False, WidgetTypes.WIDGET_GENERAL, -1, -1)

		def placeUnitMap(self):
				screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
				pUnit = pPlayer.getUnit(iUnitID)
				if pUnit.isNone():
						return
				screen.setLabel("GoToUnit", "Background", "<font=4b>" + pUnit.getName() + "</font>", CvUtil.FONT_CENTER_JUSTIFY,
												screen.getXResolution()*3/4, 50, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addPlotGraphicGFC("UnitView", screen.getXResolution() * 3/4 - iMapWidth/2, 80, iMapWidth, iMapHeight, pUnit.plot(), 350, True, WidgetTypes.WIDGET_GENERAL, -1, -1)

		def handleInput(self, inputClass):
				screen = CyGInterfaceScreen("WBPlayerUnits", CvScreenEnums.WB_UNITLIST)
				global iCityID
				global iUnitID
				if inputClass.getFunctionName() == "CurrentPage":
						iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
						if iIndex == 0:
								WBPlayerScreen.WBPlayerScreen().interfaceScreen(iPlayer)
						elif iIndex == 1:
								WBTeamScreen.WBTeamScreen().interfaceScreen(iTeam)
						elif iIndex == 2:
								WBProjectScreen.WBProjectScreen().interfaceScreen(iTeam)
						elif iIndex == 3:
								WBTechScreen.WBTechScreen().interfaceScreen(iTeam)
						elif iIndex == 11:
								WBInfoScreen.WBInfoScreen().interfaceScreen(iPlayer)

				elif inputClass.getFunctionName() == "CurrentPlayer":
						iIndex = screen.getPullDownData("CurrentPlayer", screen.getSelectedPullDownID("CurrentPlayer"))
						iCityID = 0
						iUnitID = 0
						self.interfaceScreen(iIndex)

				elif inputClass.getFunctionName() == "WBCityList":
						iCityID = inputClass.getData2()
						if inputClass.getData1() == 1030:
								WBCityEditScreen.WBCityEditScreen().interfaceScreen(pPlayer.getCity(iCityID))
						elif inputClass.getData1() == 1031:
								pPlayer.getCity(iCityID).kill()
								self.setCityTable()
						else:
								self.placeCityMap()

				elif inputClass.getFunctionName() == "DeleteAllCities":
						pPlayer.killCities()
						self.setCityTable()

				elif inputClass.getFunctionName() == "WBUnitList":
						iUnitID = inputClass.getData2()
						if inputClass.getData1() == 1030:
								WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).interfaceScreen(pPlayer.getUnit(iUnitID))
						elif inputClass.getData1() == 1031:
								pPlayer.getUnit(iUnitID).kill(False, PlayerTypes.NO_PLAYER)
								self.setUnitTable()
						else:
								self.placeUnitMap()

				elif inputClass.getFunctionName() == "DeleteAllUnits":
						pPlayer.killUnits()
						self.setUnitTable()
				return

		def update(self, fDelta):
				return 1
