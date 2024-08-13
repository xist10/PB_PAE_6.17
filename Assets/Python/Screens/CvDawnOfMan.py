# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, CyGame, CyMap,
																CyGameTextMgr, WidgetTypes, PanelStyles,
																GenericButtonSizes, PopupStates,
																CyInterface, CyAudioGame,
																AttitudeTypes, ButtonStyles)
import CvUtil
if not CvUtil.isPitbossHost():
    from CvPythonExtensions import CyGInterfaceScreen

ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
gc = CyGlobalContext()


class CvDawnOfMan:
		"Dawn of man screen"

		def __init__(self, iScreenID):
				self.iScreenID = iScreenID

				self.X_SCREEN = 0
				self.Y_SCREEN = 0
				self.W_SCREEN = 1024
				self.H_SCREEN = 768

				self.W_TECH = 425
				self.H_TECH = 80

				self.W_MAIN_PANEL = 800  # Was 550

				self.H_MAIN_PANEL = 700

				self.X_MAIN_PANEL = (self.W_SCREEN/2) - (self.W_MAIN_PANEL/2)  # Was 250

				self.Y_MAIN_PANEL = 70

				self.iMarginSpace = 15

				self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
				self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
				self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
				self.H_HEADER_PANEL = int(self.H_MAIN_PANEL * 2 / 5)

				self.X_LEADER_ICON = self.X_HEADER_PANEL + self.iMarginSpace
				self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
				self.H_LEADER_ICON = self.H_HEADER_PANEL - (15 * 2)  # 140
				self.W_LEADER_ICON = int(self.H_LEADER_ICON / 1.272727)  # 110

				self.X_FANCY_ICON1 = self.X_HEADER_PANEL + 170
				self.X_FANCY_ICON2 = self.X_HEADER_PANEL + (self.W_MAIN_PANEL - 120)  # Was 430
				self.Y_FANCY_ICON = (self.Y_HEADER_PANEL + self.iMarginSpace + 6) - 6
				self.WH_FANCY_ICON = 64

				self.X_LEADER_TITLE_TEXT = (self.X_FANCY_ICON1+self.WH_FANCY_ICON)+((self.X_FANCY_ICON2 - (self.X_FANCY_ICON1+self.WH_FANCY_ICON))/2) - ((self.W_HEADER_PANEL / 3)/2)

				self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace + 6
				self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3
				self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 2

				self.X_STATS_TEXT = self.X_FANCY_ICON1  # + self.W_LEADER_ICON + (self.iMarginSpace * 2) + 5
				self.Y_STATS_TEXT = self.Y_LEADER_TITLE_TEXT + 75
				self.W_STATS_TEXT = int(self.W_HEADER_PANEL * (5 / 7.0)) + (self.iMarginSpace * 2)
				self.H_STATS_TEXT = int(self.H_HEADER_PANEL * (3 / 5.0)) - (self.iMarginSpace * 2)

				self.X_TEXT_PANEL = self.X_HEADER_PANEL
				self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.iMarginSpace - 10  # 10 is the fudge factor
				self.W_TEXT_PANEL = self.W_HEADER_PANEL
				self.H_TEXT_PANEL = self.H_MAIN_PANEL - self.H_HEADER_PANEL - (self.iMarginSpace * 3) + 10  # 10 is the fudge factor
				self.iTEXT_PANEL_MARGIN = 35

				self.W_EXIT = 120
				self.H_EXIT = 30

				self.X_EXIT = (self.W_SCREEN/2) - (self.W_EXIT/2)  # Was 460
				self.Y_EXIT = self.Y_MAIN_PANEL + 440

		def interfaceScreen(self):
				'Use a popup to display the opening text'
				if (CyGame().isPitbossHost()):
						return

				self.calculateSizesAndPositions()

				self.player = gc.getPlayer(gc.getGame().getActivePlayer())
				self.EXIT_TEXT = localText.getText("TXT_KEY_SCREEN_CONTINUE", ())

				# Create screen

				screen = CyGInterfaceScreen("CvDawnOfMan", self.iScreenID)
				screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
				screen.showWindowBackground(False)
				screen.setDimensions(self.X_SCREEN, screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
				screen.enableWorldSounds(False)

				# Create panels

				# Main
				szMainPanel = "DawnOfManMainPanel"
				screen.addPanel(szMainPanel, "", "", True, True,
												self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN)

				# Top
				szHeaderPanel = "DawnOfManHeaderPanel"
				screen.addPanel(szHeaderPanel, "", "", True, False,
												self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNTOP)

				# Bottom
				szTextPanel = "DawnOfManTextPanel"
				screen.addPanel(szTextPanel, "", "", True, True,
												self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM)

				# Add contents

				# Leaderhead graphic
				szLeaderPanel = "DawnOfManLeaderPanel"
				screen.addPanel(szLeaderPanel, "", "", True, False,
												self.X_LEADER_ICON - 3, self.Y_LEADER_ICON - 5, self.W_LEADER_ICON + 6, self.H_LEADER_ICON + 8, PanelStyles.PANEL_STYLE_DAWNTOP)
				screen.addLeaderheadGFC("LeaderHead", self.player.getLeaderType(), AttitudeTypes.ATTITUDE_PLEASED,
																self.X_LEADER_ICON + 5, self.Y_LEADER_ICON + 5, self.W_LEADER_ICON - 10, self.H_LEADER_ICON - 10, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Info/"Stats" text
				PlayersName = self.player.getNameKey()
				if PlayersName[:4] != "TXT_":
						szNameText = "<color=255,255,0,255>" + u"<font=3b>" + self.player.getNameKey().upper() + u"</font>"
				else:
						szNameText = "<color=255,255,0,255>" + u"<font=3b>" + gc.getLeaderHeadInfo(self.player.getLeaderType()).getDescription().upper() + u"</font>"
				szNameText += "\n- " + self.player.getCivilizationDescription(0) + " -\n"
				szNameText += u"<font=2>" + CyGameTextMgr().parseLeaderTraits(self.player.getLeaderType(), self.player.getCivilizationType(), True, False) + u"</font>"
				screen.addMultilineText("NameText", szNameText, self.X_LEADER_TITLE_TEXT, self.Y_LEADER_TITLE_TEXT, self.W_LEADER_TITLE_TEXT,
																self.H_LEADER_TITLE_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				screen.addMultilineText("HeaderText2", localText.getText("TXT_KEY_FREE_TECHS", ()) + ":", self.X_STATS_TEXT, self.Y_STATS_TEXT +
																15, self.W_STATS_TEXT, self.H_STATS_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				screen.addPanel("HeaderText3", "", "", False, True,
												self.X_STATS_TEXT, self.Y_STATS_TEXT+30, self.W_TECH, self.H_TECH, PanelStyles.PANEL_STYLE_EMPTY)

				for iTech in range(gc.getNumTechInfos()):
						if (gc.getCivilizationInfo(self.player.getCivilizationType()).isCivilizationFreeTechs(iTech)):
								screen.attachImageButton("HeaderText3", "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

				self.Text_BoxText = CyGameTextMgr().parseCivInfos(self.player.getCivilizationType(), True)

				screen.addMultilineText("HeaderText4", self.Text_BoxText, self.X_STATS_TEXT, self.Y_STATS_TEXT+30+self.H_TECH, self.W_STATS_TEXT -
																(self.iMarginSpace * 3), self.H_STATS_TEXT - (self.iMarginSpace * 4), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Fancy icon things
				screen.addDDSGFC("IconLeft", ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.player.getCivilizationType()).getArtDefineTag()).getButton(),
												 self.X_FANCY_ICON1, self.Y_FANCY_ICON, self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addDDSGFC("IconRight", ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.player.getCivilizationType()).getArtDefineTag()).getButton(),
												 self.X_FANCY_ICON2, self.Y_FANCY_ICON, self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# +++++ Special dawn of man texts for Szenario Maps in PAE ++++++++++++++++++++++++++++++++
				sScenarioName = CvUtil.getScriptData(CyMap().plot(0, 0), ["S", "t"])
				if sScenarioName == "FirstPunicWar":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_FIRST_PUNIC_WAR"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_FIRST_PUNIC_WAR"
				elif sScenarioName == "WarOfDiadochi":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_300"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_300"
				elif sScenarioName == "RiseOfEgypt":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_NIL"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_NIL"
				elif sScenarioName == "PeloponnesianWar":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_PELOPONNESIAN_WAR"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_PELOPONNESIAN_WAR"
				elif sScenarioName == "PeloponnesianWarKeinpferd":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_PELOPONNESIAN_WAR_KEINPFERD"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_PELOPONNESIAN_WAR_KEINPFERD"
				elif sScenarioName == "SchmelzEuro":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_ICE_AGE"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_ICE_AGE"
				elif sScenarioName == "SchmelzWelt":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_ICE_AGE"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_ICE_AGE2"
				elif sScenarioName == "LimesGermanicus":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_LIMES_GERMANICUS"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_LIMES_GERMANICUS"
				elif sScenarioName == "SmallLimesGermanicus":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_SMALL_LIMES_GERMANICUS"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_SMALL_LIMES_GERMANICUS"
				elif sScenarioName == "480BC":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_480BC"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_480BC"
				elif sScenarioName == "BarbaricumRiseOfGreekPoleis":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_BARBARICUM_RISE_OF_GREEK_POLEIS"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_BARBARICUM_RISE_OF_GREEK_POLEIS"
				elif sScenarioName == "RiseOfGreece":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_RISE_OF_GREECE"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_RISE_OF_GREECE"
				elif sScenarioName == "WarOfDiadochiJD":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_WAROFDIADOCHI_JD"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_WAROFDIADOCHI_JD"
				elif sScenarioName == "BarbaricumBritanniaMini":
						szDawnText1 = "Barbaricum Britannia"
						szDawnText2 = "TXT_KEY_SCENARIO_BARBARICUM_BRITANNIA_MINI"
				elif sScenarioName == "PAE_SECONDPUNICWAR_JD":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_SECONDPUNICWAR_JD_210BC"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_SECONDPUNICWAR_JD_210BC"
				elif sScenarioName == "SICILY_500BC":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_PAE_SICILY_500BC"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_PAE_SICILY_500BC"
				elif sScenarioName == "CivIIIRiseOfRome":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_PAE_CIVIII_RISEOFROME"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_PAE_CIVIII_RISEOFROME"
				elif sScenarioName == "EurasiaXXXLCivs":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_EURASIA_XXXL"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_EURASIA_XXXL"
				elif sScenarioName == "Western_Mediterranean":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_WESTERN_MED"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_WESTERN_MED"
				elif sScenarioName == "IberianConquest":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_IBERIAN_CONQUEST"
				elif sScenarioName == "BarbaricumRiseOfIndia":
						szDawnText1 = "TXT_KEY_BARBARICUM_RISE_OF_INDIA_TITLE"
						szDawnText2 = "TXT_KEY_BARBARICUM_RISE_OF_INDIA"
				elif sScenarioName == "GalliaEstOmnis":
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE_GALLIA_EST_OMNIS"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_GALLIA_EST_OMNIS"
				else:
						szDawnText1 = "TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE"
						szDawnText2 = "TXT_KEY_DAWN_OF_MAN_TEXT"

				# Main Body text
				szDawnTitle = u"<font=3>" + localText.getText(szDawnText1, ()).upper() + u"</font>"
				screen.setLabel("DawnTitle", "Background", szDawnTitle, CvUtil.FONT_CENTER_JUSTIFY,
												self.X_TEXT_PANEL + (self.W_TEXT_PANEL / 2), self.Y_TEXT_PANEL + 15, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				bodyString = localText.getText(szDawnText2, (CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn(), False), self.player.getCivilizationAdjectiveKey(), self.player.getNameKey()))
				screen.addMultilineText("BodyText", bodyString, self.X_TEXT_PANEL + self.iMarginSpace, self.Y_TEXT_PANEL + self.iMarginSpace + self.iTEXT_PANEL_MARGIN,
																self.W_TEXT_PANEL - (self.iMarginSpace * 2), self.H_TEXT_PANEL - (self.iMarginSpace * 2) - 75, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				screen.setButtonGFC("Exit", self.EXIT_TEXT, "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

				pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
				pLeaderHeadInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
				screen.setSoundId(CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0)))

		def handleInput(self, inputClass):
				return 0

		def update(self, fDelta):
				return

		def onClose(self):
				CyInterface().setSoundSelectionReady(True)
				return 0

		def calculateSizesAndPositions(self):
				self.X_SCREEN = 0
				self.Y_SCREEN = 0

				screen = CyGInterfaceScreen("CvDawnOfMan", self.iScreenID)

				self.W_SCREEN = screen.getXResolution()
				self.H_SCREEN = screen.getYResolution()

				self.W_TECH = 425
				self.H_TECH = 80

				self.W_MAIN_PANEL = 800  # Was 550

				self.H_MAIN_PANEL = 660
				self.X_MAIN_PANEL = (self.W_SCREEN/2) - (self.W_MAIN_PANEL/2)  # Was 250

				self.Y_MAIN_PANEL = 20

				self.iMarginSpace = 15

				self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
				self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
				self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
				self.H_HEADER_PANEL = int(self.H_MAIN_PANEL * (2.0 / 5.0)) + 60

				self.X_LEADER_ICON = self.X_HEADER_PANEL + self.iMarginSpace
				self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
				self.H_LEADER_ICON = self.H_HEADER_PANEL - (15 * 2)  # 140
				self.W_LEADER_ICON = int(self.H_LEADER_ICON / 1.272727)  # 110

				self.WH_FANCY_ICON = 64
				self.X_FANCY_ICON1 = self.X_LEADER_ICON + self.W_LEADER_ICON + self.iMarginSpace
				self.X_FANCY_ICON2 = self.X_LEADER_ICON + (self.W_HEADER_PANEL - (self.iMarginSpace * 2) - self.WH_FANCY_ICON)  # Was 430
				self.Y_FANCY_ICON = (self.Y_HEADER_PANEL + self.iMarginSpace + 6) - 6

				self.X_LEADER_TITLE_TEXT = (self.X_FANCY_ICON1+self.WH_FANCY_ICON)+((self.X_FANCY_ICON2 - (self.X_FANCY_ICON1+self.WH_FANCY_ICON))/2) - ((self.W_HEADER_PANEL / 3)/2)

				self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace + 6
				self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3
				self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 2

				self.X_STATS_TEXT = self.X_FANCY_ICON1  # + self.W_LEADER_ICON + (self.iMarginSpace * 2) + 5

				self.Y_STATS_TEXT = self.Y_LEADER_TITLE_TEXT + 60
				self.W_STATS_TEXT = int(self.W_HEADER_PANEL * (5 / 7.0)) + (self.iMarginSpace * 2)
				self.H_STATS_TEXT = int(self.H_HEADER_PANEL * (3 / 5.0)) - (self.iMarginSpace * 2)

				self.X_TEXT_PANEL = self.X_HEADER_PANEL
				self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.iMarginSpace - 10  # 10 is the fudge factor
				self.W_TEXT_PANEL = self.W_HEADER_PANEL
				self.H_TEXT_PANEL = 310
#                self.H_TEXT_PANEL = self.H_MAIN_PANEL - self.H_HEADER_PANEL - (self.iMarginSpace * 3) + 10 #10 is the fudge factor
				self.iTEXT_PANEL_MARGIN = 35

				self.W_EXIT = 120
				self.H_EXIT = 30

				self.X_EXIT = (self.W_SCREEN/2) - (self.W_EXIT/2)  # Was 460
				self.Y_EXIT = self.Y_TEXT_PANEL + self.H_TEXT_PANEL - (self.iMarginSpace * 3)
