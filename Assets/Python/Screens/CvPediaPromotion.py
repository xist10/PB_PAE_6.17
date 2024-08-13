# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, CyGameTextMgr,
																WidgetTypes, PanelStyles, GenericButtonSizes,
																TableStyles, CivilopediaPageTypes)
import CvUtil
# import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvPediaPromotion:
		"Civilopedia Screen for Promotions"

		def __init__(self, main):
				self.iPromotion = -1
				self.top = main

				self.BUTTON_SIZE = 46

				self.X_UNIT_PANE = 50
				self.Y_UNIT_PANE = 80
				self.W_UNIT_PANE = 250
				self.H_UNIT_PANE = 210

				self.X_ICON = 123
				self.Y_ICON = 135
				self.W_ICON = 100
				self.H_ICON = 100
				self.ICON_SIZE = 64

				self.X_PREREQ_PANE = 330
				self.Y_PREREQ_PANE = 60
				self.W_PREREQ_PANE = 420
				self.H_PREREQ_PANE = 110

				self.X_LEADS_TO_PANE = 330
				self.Y_LEADS_TO_PANE = 180
				self.W_LEADS_TO_PANE = self.W_PREREQ_PANE
				self.H_LEADS_TO_PANE = 110

				self.X_SPECIAL_PANE = 330
				self.Y_SPECIAL_PANE = 294
				self.W_SPECIAL_PANE = self.W_PREREQ_PANE
				self.H_SPECIAL_PANE = 380

				self.X_UNIT_GROUP_PANE = 50
				self.Y_UNIT_GROUP_PANE = 294
				self.W_UNIT_GROUP_PANE = 250
				self.H_UNIT_GROUP_PANE = 380
				self.DY_UNIT_GROUP_PANE = 25
#    self.ITEMS_MARGIN = 18
#    self.ITEMS_SEPARATION = 2

		# Screen construction function
		def interfaceScreen(self, iPromotion):

				self.iPromotion = iPromotion

				self.top.deleteAllWidgets()

				screen = self.top.getScreen()

				bNotActive = (not screen.isActive())
				if bNotActive:
						self.top.setPediaCommonWidgets()

				# Header...
				szHeader = u"<font=4b>" + gc.getPromotionInfo(self.iPromotion).getDescription().upper() + u"</font>"
				szHeaderId = self.top.getNextWidgetName()
				screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Top
				screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU,
											 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION, -1)

				if self.top.iLastScreen != CvScreenEnums.PEDIA_PROMOTION or bNotActive:
						self.placeLinks(True)
						self.top.iLastScreen = CvScreenEnums.PEDIA_PROMOTION
				else:
						self.placeLinks(False)

				# Icon
				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
												self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
												self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
				screen.addDDSGFC(self.top.getNextWidgetName(), gc.getPromotionInfo(self.iPromotion).getButton(),
												 self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
#    screen.addDDSGFC(self.top.getNextWidgetName(), gc.getPromotionInfo(self.iPromotion).getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_GENERAL, self.iPromotion, -1 )

				# Place Required promotions
				self.placePrereqs()

				# Place Allowing promotions
				self.placeLeadsTo()

				# Place the Special abilities block
				self.placeSpecial()

				self.placeUnitGroups()

		# Place prereqs...

		def placePrereqs(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True,
												self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				ePromo = gc.getPromotionInfo(self.iPromotion).getPrereqPromotion()
				if (ePromo > -1):
						screen.attachImageButton(panelName, "", gc.getPromotionInfo(ePromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromo, 1, False)

				ePromoOr1 = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion1()
				ePromoOr2 = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion2()
				if (ePromoOr1 > -1):
						if (ePromo > -1):
								screen.attachLabel(panelName, "", localText.getText("TXT_KEY_AND", ()))

								if (ePromoOr2 > -1):
										screen.attachLabel(panelName, "", "(")

						screen.attachImageButton(panelName, "", gc.getPromotionInfo(ePromoOr1).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromoOr1, 1, False)

						if (ePromoOr2 > -1):
								screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
								screen.attachImageButton(panelName, "", gc.getPromotionInfo(ePromoOr2).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
																				 WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromoOr2, 1, False)

								if (ePromo > -1):
										screen.attachLabel(panelName, "", ")")

				# PAE Unit Rang Promos
				if "_RANG_" in gc.getPromotionInfo(self.iPromotion).getType():
						lFirst = [
								gc.getInfoTypeForString("PROMOTION_RANG_ROM_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_GER_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_HUN"),
								gc.getInfoTypeForString("PROMOTION_RANG_GREEK_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_1"),
								gc.getInfoTypeForString("PROMOTION_RANG_SUMER_1")
						]
						if self.iPromotion not in lFirst:
								str_text = gc.getPromotionInfo(self.iPromotion).getType()[:-2]
								str_zahl = gc.getPromotionInfo(self.iPromotion).getType()[-2:]
								if "_" in str_zahl:
										str_zahl = str_zahl[1:]
										str_text = str_text + "_"
								iPromo = gc.getInfoTypeForString(str_text + str(int(str_zahl) - 1))
								screen.attachImageButton(panelName, "", gc.getPromotionInfo(iPromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromo, 1, False)

				eTech = gc.getPromotionInfo(self.iPromotion).getTechPrereq()
				if (eTech > -1):
						screen.attachImageButton(panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, eTech, 1, False)

				eReligion = gc.getPromotionInfo(self.iPromotion).getStateReligionPrereq()
				if (eReligion > -1):
						screen.attachImageButton(panelName, "", gc.getReligionInfo(eReligion).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, eReligion, 1, False)

		# Place Leads To...

		def placeLeadsTo(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_LEADS_TO", ()), "", False, True,
												self.X_LEADS_TO_PANE, self.Y_LEADS_TO_PANE, self.W_LEADS_TO_PANE, self.H_LEADS_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				for j in range(gc.getNumPromotionInfos()):
						# iPrereq = gc.getPromotionInfo(j).getPrereqPromotion()
						if (gc.getPromotionInfo(j).getPrereqPromotion() == self.iPromotion or gc.getPromotionInfo(j).getPrereqOrPromotion1() == self.iPromotion or gc.getPromotionInfo(j).getPrereqOrPromotion2() == self.iPromotion):
								screen.attachImageButton(panelName, "", gc.getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, 1, False)

				# PAE Unit Rang Promos
				if "_RANG_" in gc.getPromotionInfo(self.iPromotion).getType():
						lLast = [
								gc.getInfoTypeForString("PROMOTION_RANG_ROM_15"),
								gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_5"),
								gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_15"),
								gc.getInfoTypeForString("PROMOTION_RANG_GER_3"),
								gc.getInfoTypeForString("PROMOTION_RANG_HUN"),
								gc.getInfoTypeForString("PROMOTION_RANG_GREEK_12"),
								gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_10"),
								gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_10"),
								gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_10"),
								gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_15"),
								gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_10"),
								gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_6"),
								gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_12"),
								gc.getInfoTypeForString("PROMOTION_RANG_SUMER_10")
						]
						if self.iPromotion not in lLast:
								str_text = gc.getPromotionInfo(self.iPromotion).getType()[:-2]
								str_zahl = gc.getPromotionInfo(self.iPromotion).getType()[-2:]
								if "_" in str_zahl:
										str_zahl = str_zahl[1:]
										str_text = str_text + "_"
								iPromo = gc.getInfoTypeForString(str_text + str(int(str_zahl) + 1))
								screen.attachImageButton(panelName, "", gc.getPromotionInfo(iPromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromo, 1, False)

		def placeSpecial(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False,
												self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				listName = self.top.getNextWidgetName()

				szSpecialText = CyGameTextMgr().getPromotionHelp(self.iPromotion, True)[1:]
				screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE -
																10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeUnitGroups(self):
				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_PROMOTION_UNITS", ()), "", True, True,
												self.X_UNIT_GROUP_PANE, self.Y_UNIT_GROUP_PANE, self.W_UNIT_GROUP_PANE, self.H_UNIT_GROUP_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				szTable = self.top.getNextWidgetName()
				screen.addTableControlGFC(szTable, 1,
																	self.X_UNIT_GROUP_PANE + 10, self.Y_UNIT_GROUP_PANE + 40, self.W_UNIT_GROUP_PANE - 20, self.H_UNIT_GROUP_PANE - 50, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)

				i = 0
				for iI in range(gc.getNumUnitCombatInfos()):
						if (0 != gc.getPromotionInfo(self.iPromotion).getUnitCombat(iI)):
								iRow = screen.appendTableRow(szTable)  # noqa
								screen.setTableText(szTable, 0, i, u"<font=2>" + gc.getUnitCombatInfo(iI).getDescription() + u"</font>",
																		gc.getUnitCombatInfo(iI).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iI, -1, CvUtil.FONT_LEFT_JUSTIFY)
								i += 1

		def placeLinks(self, bRedraw):

				screen = self.top.getScreen()

				if bRedraw:
						screen.clearListBoxGFC(self.top.LIST_ID)

				# sort techs alphabetically
				# listSorted=[(0,0)]*gc.getNumPromotionInfos()
				# for j in range(gc.getNumPromotionInfos()):
				#  listSorted[j] = (gc.getPromotionInfo(j).getDescription(), j)
				# listSorted.sort()

				listSorted = self.getPromoSortedList(self.getPromoType(self.iPromotion))

				i = 0
				iSelected = 0
				# for iI in range(gc.getNumPromotionInfos()):
				for iI in range(len(listSorted)):
						if (not gc.getPromotionInfo(listSorted[iI][1]).isGraphicalOnly()):
								if bRedraw:
										screen.appendListBoxStringNoUpdate(self.top.LIST_ID, listSorted[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, listSorted[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY)
								if listSorted[iI][1] == self.iPromotion:
										iSelected = i
								i += 1

				if bRedraw:
						screen.updateListBox(self.top.LIST_ID)

				screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

		def getPromoType(self, iPromotion):
				if "_FORM_" in gc.getPromotionInfo(iPromotion).getType():
						return 1
				if "_RANG_" in gc.getPromotionInfo(iPromotion).getType():
						return 2
				# Regular promo
				return 0

		# iType
		# 0: normal
		# 1: Formationen
		# 2: Rangsystem
		def getPromoSortedList(self, iType):
				listPromos = []
				iCount = 0

				for iPromo in range(gc.getNumPromotionInfos()):
						if (iType == 0 and "_FORM_" not in gc.getPromotionInfo(iPromo).getType() and "_RANG_" not in gc.getPromotionInfo(iPromo).getType()):
								listPromos.append(iPromo)
								iCount += 1
						elif (iType == 1 and "_FORM_" in gc.getPromotionInfo(iPromo).getType()):
								listPromos.append(iPromo)
								iCount += 1
						elif (iType == 2 and "_RANG_" in gc.getPromotionInfo(iPromo).getType()):
								listPromos.append(iPromo)
								iCount += 1

				listSorted = [(0, 0)] * iCount
				iI = 0
				for iPromo in listPromos:
						listSorted[iI] = (gc.getPromotionInfo(iPromo).getDescription(), iPromo)
						iI += 1
				if iType == 0 or iType == 1:
						listSorted.sort()
				return listSorted

		# Will handle the input for this screen...
		def handleInput(self, inputClass):
				return 0
