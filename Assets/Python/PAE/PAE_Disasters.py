# Disasters features and events

# Imports
from CvPythonExtensions import (CyGlobalContext, CyInterface, CyMap, CyGame,
																CyCamera, CyEngine, PlotTypes,
																CyTranslator, DirectionTypes,
																ColorTypes, CyPopupInfo, isWorldWonderClass,
																ButtonPopupTypes, plotXY, plotDirection)
import CvUtil

import PAE_City
import PAE_Unit

# Defines
gc = CyGlobalContext()

# Entrypoint


def doGenerateDisaster(iGameTurn):

		if iGameTurn == 0:
				return

		# doNebel()

		iTurnDisastersModulo = 80
		bApocalypse = False
		if gc.getPlayer(gc.getGame().getActivePlayer()).getName() == "Apocalypto":
				iTurnDisastersModulo = 20
				bApocalypse = True

		if gc.getGame().getGameTurnYear() > -600 and iGameTurn % 25 == 0:
				doNebel()

		# Teiler
		if gc.getGame().getGameTurnYear() > -400:
				iTeiler = 2
		else:
				iTeiler = 1

		# entweder Erdbeben, Comet, Meteore oder Vulkan

		# Katas erzeugen
		if iGameTurn % (iTurnDisastersModulo / iTeiler) == 0:
				iRand = CvUtil.myRandom(5, "doDisaster")
				if iRand == 0:
						doErdbeben(0, 0)
				elif iRand == 1:
						doVulkan(0, 0, 0)
				elif iRand == 2:
						doComet()
				else:
						doMeteorites()

		# Warnung aussenden
		elif (iGameTurn + 1) % (iTurnDisastersModulo / iTeiler) == 0:
				iBuilding1 = gc.getInfoTypeForString("BUILDINGCLASS_ORACLE")
				iBuilding2 = gc.getInfoTypeForString("BUILDINGCLASS_ORACLE2")
				iRange = gc.getMAX_PLAYERS()
				for i in range(iRange):
						loopPlayer = gc.getPlayer(i)
						if loopPlayer.isHuman():
								iChance = 0
								if loopPlayer.getBuildingClassCount(iBuilding1) > 0:
										iChance = 100
								elif loopPlayer.getBuildingClassCount(iBuilding2) > 0:
										iChance = 50
								if iChance > 0 and iChance > CvUtil.myRandom(100, "warning"):
										# Player gets warning message
										CyInterface().addMessage(i, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_ORACLE_WARNING", ("",)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		if bApocalypse:
				if iGameTurn % (85 / iTeiler) == 0:
						doSeesturm()
				if iGameTurn % (90 / iTeiler) == 0:
						doGrasshopper()
				if iGameTurn % (60 / iTeiler) == 0:
						doTornado()
		elif iGameTurn % (70 / iTeiler) == 0:
				iRand = CvUtil.myRandom(2, "Disaster")
				if iRand == 0:
						doSeesturm()
				elif iRand == 1:
						doGrasshopper()
				else:
						doTornado()

		if iGameTurn % (90 / iTeiler) == 0:
				doSandsturm()

		if iGameTurn % ((iTurnDisastersModulo / iTeiler) + 20) == 0:
				undoVulkan()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++ Naturkatastrophen / Disasters +++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def doSandsturm():

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		feat_desertstorm = gc.getInfoTypeForString("FEATURE_FALLOUT")
		terr_desert = gc.getInfoTypeForString("TERRAIN_DESERT")
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		# lImprovements = [
		#     gc.getInfoTypeForString("IMPROVEMENT_FORT"),
		#     gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
		#     gc.getInfoTypeForString("IMPROVEMENT_TURM2")
		# ]

		lDesert = []
		# Schritt 1: DesertPlots raussuchen
		for x in range(iMapW):
				for y in range(iMapH):
						loopPlot = gc.getMap().plot(x, y)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.getFeatureType() == iDarkIce:
										continue
								if loopPlot.getTerrainType() != terr_desert:
										continue
								if loopPlot.getFeatureType() != -1:
										continue
								if loopPlot.getImprovementType() != -1:
										continue
								if loopPlot.isPeak():
										continue
								if plotXY(loopPlot.getX(), loopPlot.getY(), 2, 0).getTerrainType() == terr_desert:
										# nur x-Koordinaten speichern
										lDesert.append(x)
										break

		# Schritt 2: Sandsturm setzen
		if lDesert:
				OwnerArray = []
				#  0 = WORLDSIZE_DUEL
				#  1 = WORLDSIZE_TINY
				#  2 = WORLDSIZE_SMALL
				#  3 = WORLDSIZE_STANDARD
				#  4 = WORLDSIZE_LARGE
				#  5 = WORLDSIZE_HUGE
				iMaxEffect = max(1, gc.getMap().getWorldSize() - 1)
				for _ in range(iMaxEffect):
						if lDesert:
								iRand = CvUtil.myRandom(len(lDesert), "doSandsturmGetRandomXCoord")
								iPlotX = lDesert[iRand]

								# Sandsturm 3 breit
								# entlang der x-Koordinate auf allen y Plots
								for x in range(3):
										for y in range(iMapH):
												loopPlot = plotXY(iPlotX, y, x, 0)
												if loopPlot is not None and not loopPlot.isNone():
														if loopPlot.getFeatureType() == iDarkIce:
																continue
														if loopPlot.getTerrainType() != terr_desert:
																continue
														if loopPlot.getFeatureType() != -1:
																continue
														if loopPlot.getImprovementType() != -1:
																continue
														if loopPlot.isPeak():
																continue

														loopPlot.setFeatureType(feat_desertstorm, 0)

														# Besitzer herausfinden
														if loopPlot.getOwner() not in OwnerArray:
																OwnerArray.append(loopPlot.getOwner())

								# Remove x-Koordinaten 3 Felder breit
								for i in range(-3, 4):
										j = iPlotX + i
										if j in lDesert:
												lDesert.remove(j)
						else:
								break

				# Sturmmeldung an die Plot-Besitzer
				for iOwner in OwnerArray:
						if iOwner != -1:
								if gc.getPlayer(iOwner).isHuman():
										CyInterface().addMessage(gc.getPlayer(iOwner).getID(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_DESERTSTORM", ("", )),
																						 None, 2, gc.getFeatureInfo(feat_desertstorm).getButton(), ColorTypes(7), -1, -1, False, False)


def doGrasshopper():

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		feat_grasshopper = gc.getInfoTypeForString("FEATURE_GRASSHOPPER")
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		lTerrain = [
				gc.getInfoTypeForString("TERRAIN_DESERT"),
				gc.getInfoTypeForString("TERRAIN_PLAINS")
		]

		lImprovements = [
				gc.getInfoTypeForString("IMPROVEMENT_FORT"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
				gc.getInfoTypeForString("IMPROVEMENT_TURM2"),
				gc.getInfoTypeForString("IMPROVEMENT_MINE"),
				gc.getInfoTypeForString("IMPROVEMENT_QUARRY")
		]

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMaxEffect = 0
		iMapSize = gc.getMap().getWorldSize()
		if iMapSize < 3:
				iMax = 1
		elif iMapSize < 5:
				iMax = 2
		else:
				iMax = 4

		# 10 Versuche max. 4 Heuschreckenplagen zu kreieren
		for _ in range(10):

				iRandX = CvUtil.myRandom(iMapW, "doGrasshopper1")
				iRandY = CvUtil.myRandom(iMapH, "doGrasshopper2")

				pPlot = gc.getMap().plot(iRandX, iRandY)
				if pPlot is not None and not pPlot.isNone():
						if pPlot.getFeatureType() == iDarkIce:
								continue
						if pPlot.getFeatureType() == -1 and not pPlot.isPeak() and pPlot.getTerrainType() in lTerrain:
								OwnerArray = []
								iMaxEffect += 1
								for i in range(3):
										for j in range(5):
												# An den aeusseren Grenzen etwas auflockern
												if j == 0 or j == 4:
														iSetStorm = CvUtil.myRandom(2, "doGrasshopper3")
												else:
														iSetStorm = 1
												# Sturm setzen
												if iSetStorm == 1:
														loopPlot = gc.getMap().plot(pPlot.getX() + i - 1, pPlot.getY() + j - 2)
														if loopPlot is not None and not loopPlot.isNone():
																if not loopPlot.isWater() and not loopPlot.isPeak() and loopPlot.getFeatureType() == -1 \
																				and loopPlot.getTerrainType() in lTerrain:
																		if loopPlot.getImprovementType() not in lImprovements:
																				loopPlot.setImprovementType(-1)
																		loopPlot.setFeatureType(feat_grasshopper, 0)
						# Besitzer herausfinden
														if loopPlot.getOwner() != -1 and loopPlot.getOwner() not in OwnerArray:
																OwnerArray.append(loopPlot.getOwner())

								# Sturmmeldung an die Plot-Besitzer
								iRange = len(OwnerArray)
								for i in range(iRange):
										if gc.getPlayer(OwnerArray[i]).isHuman():
												CyInterface().addMessage(gc.getPlayer(OwnerArray[i]).getID(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_GRASSHOPPERS",
																																																											 ("",)), None, 2, gc.getFeatureInfo(feat_grasshopper).getButton(), ColorTypes(7), iRandX, iRandY, True, True)

				# Maximal iMax Heuschreckenplagen
				if iMaxEffect == iMax:
						break


def doNebel():

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		feat_nebel = gc.getInfoTypeForString("FEATURE_NEBEL")

		lIce = [
				gc.getInfoTypeForString("FEATURE_ICE"),
				gc.getInfoTypeForString("FEATURE_DARK_ICE")
		]
		lOceans = [
				gc.getInfoTypeForString("TERRAIN_OCEAN"),
				gc.getInfoTypeForString("TERRAIN_DEEP_OCEAN")
		]

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMaxEffect = 0
		iMapSize = gc.getMap().getWorldSize()
		if iMapSize < 3:
				iMax = 1
		else:
				iMax = 3

		# 10 Versuche max. iMax Nebel zu kreieren
		for _ in range(10):
				iRandX = CvUtil.myRandom(iMapW, "doNebel1")
				iRandY = CvUtil.myRandom(iMapH, "doNebel2")

				pPlot = gc.getMap().plot(iRandX, iRandY)
				if pPlot is not None and not pPlot.isNone():
						if pPlot.getFeatureType() in lIce:
								continue
						if pPlot.getTerrainType() in lOceans:
								OwnerArray = []
								iMaxEffect += 1
								for i in range(10):
										for j in range(7):
												# An den aeusseren Grenzen etwas auflockern
												if i == 0 or i == 9 or j == 0 or j == 6:
														iSetStorm = CvUtil.myRandom(3, "doNebel3")
												elif i == 1 or i == 8 or j == 1 or j == 5:
														iSetStorm = CvUtil.myRandom(2, "doNebel4")
												else:
														iSetStorm = 1
												# Sturm setzen
												if iSetStorm == 1:
														loopPlot = gc.getMap().plot(pPlot.getX() + i - 1, pPlot.getY() + j - 2)
														if loopPlot is not None and not loopPlot.isNone():
																if loopPlot.getFeatureType() in lIce:
																		continue
																elif loopPlot.getTerrainType() in lOceans:
																		loopPlot.setFeatureType(-1, 0)  # Required for reset of visibility
																		loopPlot.setFeatureType(feat_nebel, (i+j) % 2)

																		# Nebel Variationen
																		num_remove = CyGame().getMapRandNum(8, "Nebelvariation")
																		for r in range(num_remove):
																				plane_name = "Plane%02d" % (CyGame().getMapRandNum(16, "Nebelvariation")+1)
																				loopPlot.setFeatureDummyVisibility(plane_name, False)
																		# tiefste Texturen (Kante an Meeresoberfläche)
																		loopPlot.setFeatureDummyVisibility("Plane07", False)
																		loopPlot.setFeatureDummyVisibility("Plane10", False)
																		# loopPlot.resetFeatureModel()

																		# Besitzer herausfinden
																		if loopPlot.getOwner() != -1 and loopPlot.getOwner() not in OwnerArray:
																				OwnerArray.append(loopPlot.getOwner())

								# Sturmmeldung an die Plot-Besitzer
								iRange = len(OwnerArray)
								for i in range(iRange):
										if gc.getPlayer(OwnerArray[i]).isHuman():
												CyInterface().addMessage(gc.getPlayer(OwnerArray[i]).getID(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_NEBEL",
																																																											 ("",)), None, 2, gc.getFeatureInfo(feat_nebel).getButton(), ColorTypes(14), iRandX, iRandY, True, True)

				# Maximal 3 Nebeldecken
				if iMaxEffect == iMax:
						break


def doSeesturm():

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		feat_seesturm = gc.getInfoTypeForString("FEATURE_SEESTURM")

		lIce = [
				gc.getInfoTypeForString("FEATURE_ICE"),
				gc.getInfoTypeForString("FEATURE_DARK_ICE")
		]
		lOceans = [
				gc.getInfoTypeForString("TERRAIN_COAST"),
				gc.getInfoTypeForString("TERRAIN_OCEAN"),
				gc.getInfoTypeForString("TERRAIN_DEEP_OCEAN")
		]

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMaxEffect = 0
		iMapSize = gc.getMap().getWorldSize()
		iMax = min(5, 1+round(iMapSize/2))

		#  if iMapSize == 0: iMax = 1
		#  elif iMapSize == 1: iMax = 2
		#  elif iMapSize == 2: iMax = 2
		#  elif iMapSize == 3: iMax = 3
		#  elif iMapSize == 4: iMax = 3
		#  elif iMapSize == 5: iMax = 4
		#  else: iMax = 5

		# 20 Versuche max. iMax Seestuerme zu kreieren
		for _ in range(20):
				# Maximal 5 Seestuerme
				if iMaxEffect == iMax:
						break

				iRandX = CvUtil.myRandom(iMapW, "doSeesturm1")
				iRandY = CvUtil.myRandom(iMapH, "doSeesturm2")

				pPlot = gc.getMap().plot(iRandX, iRandY)
				if pPlot is not None and not pPlot.isNone():

						if pPlot.getFeatureType() in lIce:
								continue

						if pPlot.getTerrainType() in lOceans:
								OwnerArray = []
								iMaxEffect += 1
								for i in range(8):
										for j in range(5):
												# An den aeusseren Grenzen etwas auflockern
												if i == 0 or i == 7 or j == 0 or j == 4:
														iSetStorm = CvUtil.myRandom(2, "doSeesturm3")
												else:
														iSetStorm = 1
												# Sturm setzen
												if iSetStorm == 1:
														loopPlot = gc.getMap().plot(pPlot.getX() + i - 1, pPlot.getY() + j - 2)
														if loopPlot is not None and not loopPlot.isNone():
																if loopPlot.getFeatureType() not in lIce and loopPlot.getTerrainType() in lOceans:
																		if loopPlot.getImprovementType() > -1:
																				loopPlot.setImprovementType(-1)
																				if loopPlot.getOwner() > -1:
																						if gc.getPlayer(loopPlot.getOwner()).isHuman():
																								CyInterface().addMessage(gc.getPlayer(loopPlot.getOwner()).getID(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_SEESTURM_FISCHERBOOT", ("",)),
																																				 None, 2, gc.getFeatureInfo(feat_seesturm).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)
																		loopPlot.setFeatureType(feat_seesturm, 0)
																		doKillUnits(pPlot, 10)
														# Besitzer herausfinden
														if loopPlot.getOwner() != -1 and loopPlot.getOwner() not in OwnerArray:
																OwnerArray.append(loopPlot.getOwner())

								# Sturmmeldung an die Plot-Besitzer
								iRange = len(OwnerArray)
								for i in range(iRange):
										if gc.getPlayer(OwnerArray[i]).isHuman():
												CyInterface().addMessage(gc.getPlayer(OwnerArray[i]).getID(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_SEESTURM",
																																																											 ("",)), None, 2, gc.getFeatureInfo(feat_seesturm).getButton(), ColorTypes(7), iRandX, iRandY, True, True)


def doTornado():
		iMaxEffect = 0

		feat_tornado = gc.getInfoTypeForString('FEATURE_TORNADO')
		feat_sturm = gc.getInfoTypeForString('FEATURE_STURM')
		feat_seesturm = gc.getInfoTypeForString('FEATURE_SEESTURM')

		feat_flood_plains = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
		feat_oasis = gc.getInfoTypeForString('FEATURE_OASIS')

		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMapSize = gc.getMap().getWorldSize()
		iMax = min(7, iMapSize+1)

		#if iMapSize == 0: iMax = 1
		# elif iMapSize == 1: iMax = 2
		# elif iMapSize == 2: iMax = 3
		# elif iMapSize == 3: iMax = 4
		# elif iMapSize == 4: iMax = 5
		# elif iMapSize == 5: iMax = 6
		# else: iMax = 7

		# 10 Versuche fuer max. iMax Tornados
		for _ in range(10):

				# Maximal iMax Effekte
				if iMaxEffect == iMax:
						break

				iMapW = gc.getMap().getGridWidth()
				iMapH = gc.getMap().getGridHeight()

				iRandX = CvUtil.myRandom(iMapW, "doTornado1")
				iRandY = CvUtil.myRandom(iMapH, "doTornado2")
				pPlot = gc.getMap().plot(iRandX, iRandY)
				if pPlot is not None and not pPlot.isNone():

						if pPlot.getFeatureType() == iDarkIce:
								continue

						if pPlot.isPeak():
								continue

						if pPlot.getFeatureType() != feat_flood_plains and pPlot.getFeatureType() != feat_oasis:
								iMaxEffect += 1
								if not pPlot.isCity():
										pPlot.setRouteType(-1)
								pPlot.setImprovementType(-1)
								pPlot.setFeatureType(feat_tornado, 0)

								iPlayer = pPlot.getOwner()
								if iPlayer != -1:
										pOwner = gc.getPlayer(iPlayer)

										if pPlot.isVisibleToWatchingHuman():
												CyCamera().JustLookAtPlot(pPlot)

										if pOwner.isHuman():
												popupInfo = CyPopupInfo()
												popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
												sText = CyTranslator().getText("TXT_KEY_DISASTER_TORNADO", ("", ))
												popupInfo.setText(sText)
												popupInfo.addPopup(iPlayer)
												CyInterface().addMessage(iPlayer, True, 12, sText, None, 2, gc.getFeatureInfo(feat_tornado).getButton(), ColorTypes(7), iRandX, iRandY, True, True)

										if pPlot.isCity():
												pCity = pPlot.getPlotCity()
												iPop_alt = pCity.getPopulation()
												iPop_neu = max(1, int(pCity.getPopulation() / 2))

												pCity.setPopulation(iPop_neu)
												if pPlot.isVisibleToWatchingHuman():
														if pOwner.isHuman():
																CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_DISASTER_TORNADO_CITY", (pCity.getName(), iPop_neu, iPop_alt)),
																												 None, 2, gc.getFeatureInfo(feat_tornado).getButton(), ColorTypes(7), iRandX, iRandY, True, True)
														else:
																CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_TORNADO_CITY_OTHER",
																																																													(pOwner.getCivilizationAdjective(2), pCity.getName())), None, 2, gc.getFeatureInfo(feat_tornado).getButton(), ColorTypes(2), iRandX, iRandY, True, True)
												# City, Wahrscheinlichkeit in %
												doDestroyCityBuildings(pCity, 25)
												doKillUnits(pPlot, 10)
												PAE_City.doCheckCityState(pCity)

								# rundherum Sturm kreieren
								for i in range(3):
										for j in range(3):
												loopPlot = gc.getMap().plot(iRandX - 1 + i, iRandY - 1 + j)
												if loopPlot is not None and not loopPlot.isNone():
														if loopPlot.getFeatureType() == iDarkIce:
																continue
														if loopPlot.getFeatureType() == -1 and not loopPlot.isPeak():
																if loopPlot.isWater():
																		loopPlot.setFeatureType(feat_seesturm, 0)
																else:
																		loopPlot.setFeatureType(feat_sturm, 0)


def doErdbeben(iX, iY):
		# Effekt
		earthquakeEffect = gc.getInfoTypeForString("EFFECT_RES_BOMB")
		bonusPlotArray = []

		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		# Effekt beim Vulkanausbruch
		if iX > 0 and iY > 0:
				CyEngine().triggerEffect(earthquakeEffect, gc.getMap().plot(iX, iY).getPoint())
		else:
				feat_erdbeben = gc.getInfoTypeForString('FEATURE_ERDBEBEN')
				feat_brand = gc.getInfoTypeForString('FEATURE_SMOKE')

				feat_flood_plains = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
				feat_oasis = gc.getInfoTypeForString('FEATURE_OASIS')
				feat_forest = gc.getInfoTypeForString('FEATURE_FOREST')
				feat_forest2 = gc.getInfoTypeForString('FEATURE_DICHTERWALD')
				feat_forest_burnt = gc.getInfoTypeForString('FEATURE_FOREST_BURNT')

				feat_ice = gc.getInfoTypeForString('FEATURE_ICE')
				terr_snow = gc.getInfoTypeForString('TERRAIN_SNOW')

				# Staerkegrad des Erdbebens 6 - 9
				# 6 - Radius 1: Modernisierungen 60%, Stadt: Gebaeude 15%, Units 10%
				# 7 - Radius 1: Modernisierungen 70%, Stadt: Gebaeude 30%, Units 30%, -2 Pop, Land: Units 10%
				# 8 - Radius 2: Modernisierungen 80%
				#               Radius 2: Stadt: Gebaeude 30%, Units 30%, Pop - 1/3, Land: Units 10%
				#               Epi + 1:  Stadt: Gebaeude 50%, Units 50%, Pop / 2,   Land: Units 20%
				# 9 - Radius 3: Modernisierungen 90%
				#               Epi + 1: Pop < 6: Stadt und Units 100%,
				#                        Pop > 5: 3/4 Pop weg, Gebaeude 80%, Wunder 50%, Units 80%
				#                        Land: Units 40%
				#               Radius 2: Pop / 2, Stadt:   Gebaeude 60%, Units 60%, Land: Units 30%
				#               Radius 3: Pop - 1/3, Stadt: Gebaeude 40%, Units 40%, Land: Units 20%
				iSkala = 6 + CvUtil.myRandom(4, "doErdbeben1")

				iMapW = gc.getMap().getGridWidth()
				iMapH = gc.getMap().getGridHeight()

				# Plot soll nicht ganz am Rand sein (Flunky: alle 4 Raender ausnehmen)
				iRandX = 3 + CvUtil.myRandom(iMapW - 6, "doErdbeben2")
				iRandY = 3 + CvUtil.myRandom(iMapH - 6, "doErdbeben3")
				pPlot = gc.getMap().plot(iRandX, iRandY)
				iPlayer = pPlot.getOwner()

				if pPlot is not None and not pPlot.isNone():

						doOracleShowsDisaster(iRandX, iRandY)

						if not pPlot.isWater() and pPlot.getFeatureType() != iDarkIce:
								if pPlot.isVisibleToWatchingHuman():
										CyCamera().JustLookAtPlot(pPlot)
								# ERDBEBEN 6, 7
								if iSkala < 8:
										if iPlayer != -1:
												if gc.getPlayer(iPlayer).isHuman():
														# Message: Ein gewaltiges Erdbeben der Staerke %d erschuettert Euer Land!
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_6_OR_7", (iSkala, 0)))
														popupInfo.addPopup(iPlayer)
														CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_6_OR_7", (iSkala, 0)),
																										 "AS2D_EARTHQUAKE", 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)

										for i in range(3):
												for j in range(3):
														loopPlot = gc.getMap().plot(iRandX - 1 + i, iRandY - 1 + j)
														if loopPlot is not None and not loopPlot.isNone():
																if loopPlot.getFeatureType() == iDarkIce:
																		continue
																if not loopPlot.isWater():
																		CyEngine().triggerEffect(earthquakeEffect, loopPlot.getPoint())

																# Plot fuer Bonus Resource checken
																# Vergabe unten
																if not loopPlot.isWater() and loopPlot.getBonusType(loopPlot.getOwner()) == -1 and not loopPlot.isPeak() and loopPlot.isHills():
																		bonusPlotArray.append(loopPlot)

																# Stadt
																if loopPlot.isCity():
																		pCity = loopPlot.getPlotCity()
																		pCity.setFood(0)
																		if iSkala == 6:
																				doDestroyCityBuildings(pCity, 15)
																				doKillUnits(loopPlot, 10)
																		else:
																				doDestroyCityBuildings(pCity, 30)
																				doKillUnits(loopPlot, 30)
																				iPopAlt = pCity.getPopulation()
																				iPopNeu = 1
																				if iPopAlt > 4:
																						iPopNeu = iPopAlt - 2
																				elif iPopAlt > 2:
																						iPopNeu = iPopAlt - 1

																				pCity.setPopulation(iPopNeu)

																				if iPopNeu and iPlayer != -1:
																						if gc.getPlayer(iPlayer).isHuman():
																								# Message: Die Bevoelkerung der Stadt %s sank von %alt auf %neu!
																								CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_CITY_SHRINKS_TO", (pCity.getName(), iPopAlt, iPopNeu)),
																																				 None, 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)

																		PAE_City.doCheckCityState(pCity)

																# Modernisierungen zerstoeren
																elif not loopPlot.isWater():
																		iRand = CvUtil.myRandom(10, "doErdbeben4")
																		if iSkala == 6:
																				iLimit = 6
																		else:
																				iLimit = 7
																				doKillUnits(loopPlot, 10)
																		if iRand < iLimit:
																				loopPlot.setRouteType(-1)
																				loopPlot.setImprovementType(-1)
																		# Brand setzen
																		if not loopPlot.isPeak() and loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_oasis:
																				if loopPlot.getFeatureType() == feat_forest or loopPlot.getFeatureType() == feat_forest2:
																						if CvUtil.myRandom(3, "doErdbeben5") == 1:
																								loopPlot.setFeatureType(feat_forest_burnt, 0)
																				elif loopPlot.getFeatureType() != feat_ice and loopPlot.getTerrainType() != terr_snow:
																						loopPlot.setFeatureType(feat_brand, 0)

								# ERDBEBEN 8
								elif iSkala == 8:

										if gc.getPlayer(gc.getGame().getActivePlayer()).isHuman():
												if pPlot.isVisibleToWatchingHuman():
														CyCamera().JustLookAtPlot(pPlot)
														# Message: Ein verheerendes Erdbeben der Staerke 8 erschuetterte das Land.
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_8", ("",)))
														popupInfo.addPopup(gc.getGame().getActivePlayer())
														CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_8", ("",)),
																										 "AS2D_EARTHQUAKE", 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
												else:
														# Message: Ein verheerendes Erdbeben der Staerke 8 erschuetterte ein fernes Land.
														CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_8_FAR_AWAY", ("",)),
																										 None, 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(12), pPlot.getX(), pPlot.getY(), True, True)

										for i in range(5):
												for j in range(5):
														loopPlot = gc.getMap().plot(iRandX - 2 + i, iRandY - 2 + j)
														if loopPlot is not None and not loopPlot.isNone():
																if loopPlot.getFeatureType() == iDarkIce:
																		continue
																if not loopPlot.isWater():
																		CyEngine().triggerEffect(earthquakeEffect, loopPlot.getPoint())

																# Plot fuer Bonus Resource checken
																# Vergabe unten
																if not loopPlot.isWater() and loopPlot.getBonusType(loopPlot.getOwner()) == -1 and not loopPlot.isPeak() and loopPlot.isHills():
																		bonusPlotArray.append(loopPlot)

																# Entfernung zum Epizentrum berechnen
																iBetrag = (iRandX - loopPlot.getX()) * (iRandX - loopPlot.getX()) + (iRandY - loopPlot.getY()) * (iRandY - loopPlot.getY())

																# Stadt
																if loopPlot.isCity():
																		pCity = loopPlot.getPlotCity()
																		iPopAlt = pCity.getPopulation()
																		if iBetrag < 2:
																				doDestroyCityBuildings(pCity, 50)
																				doKillUnits(loopPlot, 50)
																				iPopNeu = int(iPopAlt / 2)
																				if iPopNeu < 2:
																						iPopNeu = 1
																				pCity.setPopulation(iPopNeu)
																		else:
																				doDestroyCityBuildings(pCity, 30)
																				doKillUnits(loopPlot, 30)
																				iPopNeu = iPopAlt - int(iPopAlt / 3)
																				if iPopNeu < 2:
																						iPopNeu = 1
																				pCity.setPopulation(iPopNeu)
																		pCity.setFood(0)

																		if iPlayer != -1:
																				if gc.getPlayer(iPlayer).isHuman():
																						# Message: Die Bevoelkerung der Stadt %s sank von %alt auf %neu!
																						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_CITY_SHRINKS_TO", (pCity.getName(), iPopAlt, iPopNeu)),
																																		 None, 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)

																		PAE_City.doCheckCityState(pCity)

																# Modernisierungen zerstoeren
																elif not loopPlot.isWater():
																		iRand = CvUtil.myRandom(10, "doErdbeben6")
																		if iRand < 8:
																				loopPlot.setRouteType(-1)
																				loopPlot.setImprovementType(-1)
																		# Brand setzen
																		if not loopPlot.isPeak() and loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_oasis:
																				if loopPlot.getFeatureType() == feat_forest or loopPlot.getFeatureType() == feat_forest2:
																						if CvUtil.myRandom(2, "doErdbeben7") == 1:
																								loopPlot.setFeatureType(feat_forest_burnt, 0)
																				elif loopPlot.getFeatureType() != feat_ice and loopPlot.getTerrainType() != terr_snow:
																						loopPlot.setFeatureType(feat_brand, 0)
																		# Units killen
																		if iBetrag < 2:
																				doKillUnits(loopPlot, 20)
																		else:
																				doKillUnits(loopPlot, 10)

								# ERDBEBEN 9
								elif iSkala > 8:
										if gc.getPlayer(gc.getGame().getActivePlayer()).isHuman():
												if pPlot.isVisibleToWatchingHuman():
														CyCamera().JustLookAtPlot(pPlot)
														# Message: Ein katastrophales Erdbeben der Staerke 9 erschuetterte das Land.
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_9", ("",)))
														popupInfo.addPopup(gc.getGame().getActivePlayer())
														CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_9", ("",)),
																										 "AS2D_EARTHQUAKE", 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
												else:
														# Message: Ein verheerendes Erdbeben der Staerke 8 erschuetterte ein fernes Land.
														CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_9_FAR_AWAY", ("",)),
																										 None, 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(12), pPlot.getX(), pPlot.getY(), True, True)

										for i in range(7):
												for j in range(7):
														loopPlot = gc.getMap().plot(iRandX - 3 + i, iRandY - 3 + j)
														if loopPlot is not None and not loopPlot.isNone():
																if loopPlot.getFeatureType() == iDarkIce:
																		continue
																if not loopPlot.isWater():
																		CyEngine().triggerEffect(earthquakeEffect, loopPlot.getPoint())

																# Plot fuer Bonus Resource checken
																# Vergabe unten
																if not loopPlot.isWater() and loopPlot.getBonusType(loopPlot.getOwner()) == -1 and not loopPlot.isPeak() and loopPlot.isHills():
																		bonusPlotArray.append(loopPlot)

																# Entfernung zum Epizentrum berechnen
																iBetrag = (iRandX - loopPlot.getX()) * (iRandX - loopPlot.getX()) + (iRandY - loopPlot.getY()) * (iRandY - loopPlot.getY())

																# Stadt
																if loopPlot.isCity():
																		pCity = loopPlot.getPlotCity()
																		iPopAlt = pCity.getPopulation()
																		if iBetrag < 2:
																				if iPopAlt < 6:
																						doDestroyCityWonders(pCity, 100, feat_erdbeben)
																						doKillUnits(loopPlot, 100)
																						pCity.kill()
																						if gc.getPlayer(iPlayer).isHuman():
																								# Message: Die Stadt %s und dessen Bevoelkerung wurde in ihren Truemmern begraben....
																								CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_EARTHQUAKE_CITY_DESTROYED", (pCity.getName(),)),
																																				 "AS2D_EARTHQUAKE", 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)
																				else:
																						doDestroyCityWonders(pCity, 50, feat_erdbeben)
																						doDestroyCityBuildings(pCity, 80)
																						doKillUnits(loopPlot, 80)
																						iPopNeu = int(iPopAlt / 4)
																						iPopNeu = max(iPopNeu, 1)
																						pCity.setPopulation(iPopNeu)
																		elif iBetrag < 3:
																				doDestroyCityBuildings(pCity, 60)
																				doKillUnits(loopPlot, 60)
																				iPopNeu = int(iPopAlt / 2)
																				iPopNeu = max(iPopNeu, 1)
																				pCity.setPopulation(iPopNeu)
																		else:
																				doDestroyCityBuildings(pCity, 40)
																				doKillUnits(loopPlot, 40)
																				iPopNeu = iPopAlt - int(iPopAlt / 3)
																				iPopNeu = max(iPopNeu, 1)
																				pCity.setPopulation(iPopNeu)

																		if pCity and not pCity.isNone():
																				pCity.setFood(0)
																				PAE_City.doCheckCityState(pCity)
																				if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
																						# Message: Die Bevoelkerung der Stadt %s sank von %alt auf %neu!
																						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_CITY_SHRINKS_TO", (pCity.getName(), iPopAlt, iPopNeu)),
																																		 None, 2, gc.getFeatureInfo(feat_erdbeben).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)

																# Modernisierungen zerstoeren
																elif not loopPlot.isWater():
																		iRand = CvUtil.myRandom(100, "doErdbeben8")
																		if iRand < 90:
																				loopPlot.setRouteType(-1)
																				loopPlot.setImprovementType(-1)
																		# Brand setzen
																		if not loopPlot.isPeak() and loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_oasis:
																				if loopPlot.getFeatureType() == feat_forest or loopPlot.getFeatureType() == feat_forest2:
																						loopPlot.setFeatureType(feat_forest_burnt, 0)
																				elif loopPlot.getFeatureType() != feat_ice and loopPlot.getTerrainType() != terr_snow:
																						loopPlot.setFeatureType(feat_brand, 0)
																				# Units killen
																		if iBetrag < 2:
																				doKillUnits(loopPlot, 40)
																		elif iBetrag < 3:
																				doKillUnits(loopPlot, 30)
																		else:
																				doKillUnits(loopPlot, 20)

								# Vergabe einer Bonus Resource 20%
								if bonusPlotArray and CvUtil.myRandom(10, "doErdbeben9") < 2:
										lBonus = [
												gc.getInfoTypeForString("BONUS_GEMS"),
												gc.getInfoTypeForString("BONUS_COPPER"),
												gc.getInfoTypeForString("BONUS_IRON"),
												gc.getInfoTypeForString("BONUS_MARBLE"),
												gc.getInfoTypeForString("BONUS_STONE"),
												gc.getInfoTypeForString("BONUS_OBSIDIAN"),
												gc.getInfoTypeForString("BONUS_MAGNETIT"),
												gc.getInfoTypeForString("BONUS_ZINK"),
												gc.getInfoTypeForString("BONUS_ZINN"),
												gc.getInfoTypeForString("BONUS_COAL"),
												gc.getInfoTypeForString("BONUS_ELEKTRON"),
												gc.getInfoTypeForString("BONUS_GOLD"),
												gc.getInfoTypeForString("BONUS_SILVER"),
												gc.getInfoTypeForString("BONUS_SALT")
										]
										iRand = CvUtil.myRandom(len(lBonus), "doErdbeben10")
										iBonus = lBonus[iRand]

										iRandPlot = CvUtil.myRandom(len(bonusPlotArray), "doErdbeben11")
										pRandPlot = bonusPlotArray[iRandPlot]
										pRandPlot.setBonusType(iBonus)
										iOwner = pRandPlot.getOwner()
										if iOwner > -1 and gc.getPlayer(iOwner).isHuman():
												CyInterface().addMessage(iOwner, True, 10, CyTranslator().getText("TXT_KEY_NEW_BONUS", (gc.getBonusInfo(iBonus).getDescription(),)),
																								 None, 2, gc.getBonusInfo(iBonus).getButton(), ColorTypes(14), pRandPlot.getX(), pRandPlot.getY(), True, True)

								# Zusaetzliche Gefahren durch das Erdbeben

								# Vulkan
								if pPlot.isPeak() and iSkala > 7:
										doVulkan(iRandX, iRandY, iSkala)

						# Unterwassererdbeben
						elif iSkala > 8:

								# Testen ob es ein Ozean ist
								iNumWaterTiles = 0
								for i in range(5):
										for j in range(5):
												loopPlot = gc.getMap().plot(iRandX - 2 + i, iRandY - 2 + j)
												if loopPlot is not None and not loopPlot.isNone():
														if loopPlot.getFeatureType() == iDarkIce:
																continue
														if loopPlot.isWater():
																iNumWaterTiles += 1
								# Statt dem Erbeben wird ein Tsunami zum Leben erweckt
								if iNumWaterTiles > 9:
										doTsunami(iRandX, iRandY)


def doVulkan(iX, iY, iSkala):

		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		# iX, iY und iSkala vom Feature Erbeben: iSkala 8 oder 9
		# Wenn das nicht gegeben ist, einen eigenen Vulkanausbruch erzeugen
		if iSkala == 0:
				iSkala = 8 + CvUtil.myRandom(2, "doVulkan1")

				iMapW = gc.getMap().getGridWidth()
				iMapH = gc.getMap().getGridHeight()

				# 10 Versuche einen Berg ausfindig zu machen
				for _ in range(10):
						# Plot soll nicht ganz am Rand sein (Flunky: alle 4 Raender ausnehmen)
						iRandX = 3 + CvUtil.myRandom(iMapW - 6, "doVulkan2")
						iRandY = 3 + CvUtil.myRandom(iMapH - 6, "doVulkan3")
						if gc.getMap().plot(iRandX, iRandY).isPeak():
								iX = iRandX
								iY = iRandY
								break

		if iX > 0 and iY > 0:

				doOracleShowsDisaster(iX, iY)

				pPlot = gc.getMap().plot(iX, iY)

				# terr_peak   = gc.getInfoTypeForString("TERRAIN_PEAK")
				terr_tundra = gc.getInfoTypeForString("TERRAIN_TUNDRA")
				terr_coast = gc.getInfoTypeForString("TERRAIN_COAST")
				feat_vulkan = gc.getInfoTypeForString("FEATURE_VOLCANO")
				feat_brand = gc.getInfoTypeForString("FEATURE_SMOKE")
				feat_saurer_regen = gc.getInfoTypeForString("FEATURE_SAURER_REGEN")

				feat_flood_plains = gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS")
				feat_oasis = gc.getInfoTypeForString('FEATURE_OASIS')

				feat_forest = gc.getInfoTypeForString('FEATURE_FOREST')
				feat_forest2 = gc.getInfoTypeForString('FEATURE_DICHTERWALD')
				feat_jungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
				feat_forest_burnt = gc.getInfoTypeForString('FEATURE_FOREST_BURNT')

				bonus_magnetit = gc.getInfoTypeForString("BONUS_MAGNETIT")
				bonus_obsidian = gc.getInfoTypeForString("BONUS_OBSIDIAN")
				bonusPlotArray = []

				if pPlot.isPeak():
						pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
						pPlot.setTerrainType(terr_tundra, 1, 1)

				pPlot.setFeatureType(feat_vulkan, 0)

				# Meldungen -----
				if gc.getPlayer(gc.getGame().getActivePlayer()).isHuman():
						# Staerke 1
						if iSkala == 8:
								if pPlot.isVisibleToWatchingHuman():
										CyCamera().JustLookAtPlot(pPlot)
										# Message: Ein verheerender Vulkanausbruch legt das Land in Schutt und Asche.
										popupInfo = CyPopupInfo()
										popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
										sText = CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_VOLCANO_1", ("",))
										popupInfo.setText(sText)
										popupInfo.addPopup(gc.getGame().getActivePlayer())
										CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, sText, "AS2D_EARTHQUAKE", 2, gc.getFeatureInfo(feat_vulkan).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)

						# Staerke 2
						else:
								if pPlot.isVisibleToWatchingHuman():
										CyCamera().JustLookAtPlot(pPlot)
										# Message: Ein katastrophaler Vulkanausbruch legt das Land in Schutt und Asche.
										popupInfo = CyPopupInfo()
										popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
										sText = CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_VOLCANO_2", ("",))
										popupInfo.setText(sText)
										popupInfo.addPopup(gc.getGame().getActivePlayer())
										CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, sText, "AS2D_EARTHQUAKE", 2, gc.getFeatureInfo(feat_vulkan).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
								else:
										# Message: Ein katastrophaler Vulkanausbruch legt ein fernes Land in Schutt und Asche.
										CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_VOLCANO_2_FAR_AWAY", ("",)),
																						 None, 2, gc.getFeatureInfo(feat_vulkan).getButton(), ColorTypes(12), pPlot.getX(), pPlot.getY(), True, True)

				# Staerke 1 (iSkala 8): 1 Plot Radius
				#   Stadt: Pop / 2, Gebaeude 50%, Units 50%
				#   Land:  Units 25%
				#   Feature: Sauerer Regen: Umkreis von 5 Plots

				# Staerke 2 (iSkala 9): 2 Plots Radius
				#   Radius 1:
				#     Stadt: Pop = 1/4, Gebaeude 75%, Units 75%
				#     Land:  Units 50%
				#   Radius 2:
				#     Stadt: Pop / 2, Gebaeude 50%, Units 50%
				#     Land:  Units 25%
				#   Feature: Sauerer Regen: Umkreis von 1 Plot, Ellipse nach Osten oder Westen: 15 Plots

				iRandX = iX
				iRandY = iY

				# Effekt
				earthquakeEffect = gc.getInfoTypeForString("EFFECT_RES_BOMB")
				volcanoEffect = gc.getInfoTypeForString("EFFECT_OMEN_HORSEMAN")
				CyEngine().triggerEffect(volcanoEffect, pPlot.getPoint())

				PlayerPopUpFood = []

				# Staerke 1
				if iSkala == 8:
						for i in range(3):
								for j in range(3):
										loopPlot = gc.getMap().plot(iRandX - 1 + i, iRandY - 1 + j)
										if loopPlot is not None and not loopPlot.isNone():
												if loopPlot.getFeatureType() == iDarkIce:
														continue
												if not loopPlot.isWater() and i != 1 and j != 1:
														CyEngine().triggerEffect(earthquakeEffect, loopPlot.getPoint())

												# Entfernung zum Epizentrum berechnen
												iBetrag = (iRandX - loopPlot.getX()) * (iRandX - loopPlot.getX()) + (iRandY - loopPlot.getY()) * (iRandY - loopPlot.getY())

												# Stadt
												if loopPlot.isCity():
														pCity = loopPlot.getPlotCity()
														iPlayer = pCity.getOwner()
														iPopAlt = pCity.getPopulation()

														doDestroyCityBuildings(pCity, 50)
														doKillUnits(loopPlot, 50)
														iPopNeu = int(iPopAlt / 2)
														if iPopNeu < 2:
																iPopNeu = 1
														pCity.setPopulation(iPopNeu)
														pCity.setFood(0)

														if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
																# Message: Die Bevoelkerung der Stadt %s sank von %alt auf %neu!
																CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_CITY_SHRINKS_TO", (pCity.getName(), iPopAlt, iPopNeu)),
																												 None, 2, gc.getFeatureInfo(feat_vulkan).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)

														PAE_City.doCheckCityState(pCity)

												# Modernisierungen zerstoeren
												else:
														loopPlot.setRouteType(-1)
														loopPlot.setImprovementType(-1)
														# Brand setzen
														if not loopPlot.isWater() and not loopPlot.isPeak():
																if loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_vulkan and loopPlot.getFeatureType() != feat_oasis:
																		if loopPlot.getFeatureType() == feat_forest or loopPlot.getFeatureType() == feat_forest2 or loopPlot.getFeatureType() == feat_jungle:
																				loopPlot.setFeatureType(feat_forest_burnt, 0)
																		else:
																				loopPlot.setFeatureType(feat_brand, 0)
														# Units killen
														doKillUnits(loopPlot, 25)

												# Plot fuer Bonus checken
												# Vergabe ganz unten
												if not loopPlot.isWater() and not loopPlot.isPeak() and loopPlot.getBonusType(loopPlot.getOwner()) == -1 and loopPlot.getBonusType(-1) == -1 and loopPlot.isHills():
														bonusPlotArray.append(loopPlot)

												# Dem Plot +1 Nahrung geben (25%)
												if not loopPlot.isWater() and not loopPlot.isCity() and not loopPlot.isPeak() and (i != 1 or j != 1):
														if loopPlot.getFeatureType != feat_vulkan and loopPlot.getTerrainType() != terr_tundra:
																if CvUtil.myRandom(4, "doVulkan4") == 1:
																		gc.getGame().setPlotExtraYield(iRandX - 2 + i, iRandY - 2 + j, 0, 1)  # x,y,YieldType,iChange
																		iOwner = loopPlot.getOwner()
																		if iOwner != -1 and gc.getPlayer(iOwner).isHuman():
																				CyInterface().addMessage(iOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_VOLCANO_FOOD", ("",)), None,
																																 2, gc.getFeatureInfo(feat_vulkan).getButton(), ColorTypes(8), loopPlot.getX(), loopPlot.getY(), True, True)
																				# fuer spaeteres popup
																				if iOwner not in PlayerPopUpFood:
																						PlayerPopUpFood.append(iOwner)

												# Verbreitbare Resi vernichten
												if loopPlot.getBonusType(loopPlot.getOwner()) > -1 or loopPlot.getBonusType(-1) > -1:
														doEraseBonusFromDisaster(loopPlot)

						# Sauerer Regen
						for i in range(7):
								for j in range(7):
										loopPlot = gc.getMap().plot(iRandX - 3 + i, iRandY - 3 + j)
										if loopPlot is not None and not loopPlot.isNone():
												if loopPlot.getFeatureType() == iDarkIce:
														continue
												# loopPlot.setRouteType(-1)
												if loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_oasis and loopPlot.getFeatureType() != feat_brand and loopPlot.getFeatureType() != feat_vulkan and not loopPlot.isPeak():
														if loopPlot.getFeatureType() != feat_forest_burnt:
																loopPlot.setFeatureType(feat_saurer_regen, 0)

				# Staerke 2
				else:
						for i in range(5):
								for j in range(5):
										loopPlot = gc.getMap().plot(iRandX - 2 + i, iRandY - 2 + j)
										if loopPlot is not None and not loopPlot.isNone():
												if loopPlot.getFeatureType() == iDarkIce:
														continue
												if not loopPlot.isWater() and i != 2 and j != 2:
														CyEngine().triggerEffect(earthquakeEffect, loopPlot.getPoint())

												# Entfernung zum Vulkan berechnen
												iBetrag = (iRandX - loopPlot.getX()) * (iRandX - loopPlot.getX()) + (iRandY - loopPlot.getY()) * (iRandY - loopPlot.getY())

												# Stadt
												if loopPlot.isCity():
														pCity = loopPlot.getPlotCity()
														iPlayer = pCity.getOwner()
														iPopAlt = pCity.getPopulation()

														if iBetrag < 2:
																doDestroyCityBuildings(pCity, 75)
																doKillUnits(loopPlot, 75)
																iPopNeu = int(iPopAlt / 4)
																if iPopNeu < 1:
																		iPopNeu = 1
																pCity.setPopulation(iPopNeu)
														else:
																doDestroyCityBuildings(pCity, 50)
																doKillUnits(loopPlot, 50)
																iPopNeu = iPopAlt - int(iPopAlt / 2)
																if iPopNeu < 1:
																		iPopNeu = 1
																pCity.setPopulation(iPopNeu)
														pCity.setFood(0)

														if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
																# Message: Die Bevoelkerung der Stadt %s sank von %alt auf %neu!
																CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_CITY_SHRINKS_TO", (pCity.getName(), iPopAlt, iPopNeu)),
																												 None, 2, gc.getFeatureInfo(feat_vulkan).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)

														PAE_City.doCheckCityState(pCity)

												# Modernisierungen zerstoeren
												else:
														loopPlot.setRouteType(-1)
														loopPlot.setImprovementType(-1)
														# Brand setzen
														if not loopPlot.isWater() and loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_vulkan and not loopPlot.isPeak() and loopPlot.getFeatureType() != feat_oasis:
																if loopPlot.getFeatureType() == feat_forest or loopPlot.getFeatureType() == feat_forest2 or loopPlot.getFeatureType() == feat_jungle:
																		loopPlot.setFeatureType(feat_forest_burnt, 0)
																else:
																		loopPlot.setFeatureType(feat_brand, 0)
														# Units killen
														if iBetrag < 2:
																doKillUnits(loopPlot, 50)
														else:
																doKillUnits(loopPlot, 25)

												# Plot fuer Bonus checken
												# Nur 1 Plot rund um den Vulkan
												# Vergabe ganz unten
												if i > 0 and i < 4 and j > 0 and j < 4:
														if not loopPlot.isWater() and not loopPlot.isPeak() and loopPlot.getBonusType(loopPlot.getOwner()) == -1 and loopPlot.getBonusType(-1) == -1 and loopPlot.isHills():
																bonusPlotArray.append(loopPlot)

												# Dem Plot +1 Nahrung geben (25%)
												if not loopPlot.isWater() and not loopPlot.isCity() and not loopPlot.isPeak() and (i != 2 or j != 2):
														if loopPlot.getFeatureType != feat_vulkan and loopPlot.getTerrainType() != terr_tundra:
																if CvUtil.myRandom(4, "doVulkan5") == 1:
																		gc.getGame().setPlotExtraYield(iRandX - 2 + i, iRandY - 2 + j, 0, 1)  # x,y,YieldType,iChange
																		iOwner = loopPlot.getOwner()
																		if iOwner != -1:
																				if gc.getPlayer(iOwner).isHuman():
																						CyInterface().addMessage(iOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_VOLCANO_FOOD", ("",)), None,
																																		 2, gc.getFeatureInfo(feat_vulkan).getButton(), ColorTypes(8), loopPlot.getX(), loopPlot.getY(), True, True)
																						# fuer spaeteres popup
																						if gc.getPlayer(iOwner).getID() not in PlayerPopUpFood:
																								PlayerPopUpFood.append(gc.getPlayer(iOwner).getID())

												# Verbreitbare Resi vernichten
												if loopPlot.getBonusType(loopPlot.getOwner()) > -1 or loopPlot.getBonusType(-1) > -1:
														doEraseBonusFromDisaster(loopPlot)

						# Sauerer Regen
						# Ellipse nach Osten oder Westen: 15 Plots
						iRand_W_O = CvUtil.myRandom(2, "doVulkan6")
						for i in range(20):
								for j in range(-5, 6):
										if iRand_W_O == 1:
												loopPlot = gc.getMap().plot(iRandX + i, iRandY + j)
										else:
												loopPlot = gc.getMap().plot(iRandX - i, iRandY + j)

										if loopPlot is not None and not loopPlot.isNone():
												iFeature = loopPlot.getFeatureType()
												if iFeature == iDarkIce:
														continue
												if iFeature != feat_flood_plains and iFeature != feat_oasis and iFeature != feat_vulkan and not loopPlot.isPeak():
														bDoIt = False
														if i > 4 and i < 15:
																bDoIt = True
														elif (i == 0 or i == 19) and abs(j) < 2:
																bDoIt = True
														elif (i == 1 or i == 18) and abs(j) < 3:
																bDoIt = True
														elif (i == 2 or i == 17) and abs(j) < 4:
																bDoIt = True
														elif (i == 3 or i == 16) and abs(j) < 5:
																bDoIt = True
														elif (i == 4 or i == 15) and abs(j) < 10:
																bDoIt = True
														if bDoIt:
																# loopPlot.setRouteType(-1)
																bSetRegen = False
																if iFeature == -1:
																		bSetRegen = True
																elif iFeature != feat_forest_burnt:
																		if iFeature == feat_forest or iFeature == feat_forest2 or iFeature == feat_jungle:
																				if CvUtil.myRandom(2, "doVulkan7") == 1:
																						bSetRegen = True

																if bSetRegen:
																		loopPlot.setFeatureType(feat_saurer_regen, 0)

						# Vulkan wird zu Wasser, wenn auf einer (Halb)Insel
						# Sprengt sich weg (somit keine Vulkan-Feature-Grafik notwendig)
						iNumWaterTiles = 0
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
								loopPlot = plotDirection(iRandX, iRandY, DirectionTypes(iI))
								if loopPlot is not None and not loopPlot.isNone():
										if loopPlot.isWater() and loopPlot.getFeatureType() != iDarkIce:
												iNumWaterTiles += 1
						# Statt dem Erbeben wird ein Tsunami zum Leben erweckt
						if iNumWaterTiles > 3:
								pPlot.setFeatureType(-1, 0)
								pPlot.setTerrainType(terr_coast, 1, 1)
								pPlot.setPlotType(PlotTypes.PLOT_OCEAN, True, True)
								doTsunami(iRandX, iRandY)

				# Message: PopUp wegen +1 Food
				for iPlayerPopUpFood in PlayerPopUpFood:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_VOLCANO_FOOD_POPUP", ("",)))
						popupInfo.addPopup(iPlayerPopUpFood)

				# Chance einer Magnetit und Obsidian Bonus Resource jeweils 50%
				iRange = len(bonusPlotArray)
				if iRange > 0:
						iRand = CvUtil.myRandom(3, "doVulkan8")
						iBonus = -1
						if iRand == 1:
								iBonus = bonus_magnetit
						elif iRand == 2:
								iBonus = bonus_obsidian

						if iBonus != -1:
								for iLoopPlot in range(iRange):
										iRand = CvUtil.myRandom(100, "doVulkan9")
										if iRand < 100 / (iLoopPlot+1):
												pLoopPlot = bonusPlotArray[iLoopPlot]
												pLoopPlot.setBonusType(iBonus)
												iOwner = pLoopPlot.getOwner()
												if iOwner > -1 and gc.getPlayer(iOwner).isHuman():
														CyInterface().addMessage(bonusPlotArray[iLoopPlot].getOwner(), True, 10, CyTranslator().getText("TXT_KEY_NEW_BONUS", (gc.getBonusInfo(iBonus).getDescription(),)), None, 2, gc.getBonusInfo(
																iBonus).getButton(), ColorTypes(14), bonusPlotArray[iLoopPlot].getX(), bonusPlotArray[iLoopPlot].getY(), True, True)


def undoVulkan():
		terr_peak = gc.getInfoTypeForString("TERRAIN_PEAK")
		feat_vulkan = gc.getInfoTypeForString("FEATURE_VOLCANO")

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		for i in range(iMapW):
				for j in range(iMapH):
						pPlot = gc.getMap().plot(i, j)

						if pPlot.getFeatureType() == feat_vulkan:
								#iYield = pPlot.getYield(0)
								# if iYield > 0: gc.getGame().setPlotExtraYield(i, j, 0, -iYield) # x,y,YieldType,iChange
								# Reihenfolge einhalten! wichtig!!!
								pPlot.setFeatureType(-1, 0)
								pPlot.setTerrainType(terr_peak, 1, 1)
								pPlot.setPlotType(PlotTypes.PLOT_PEAK, True, True)

				# --------- Ende Vulkan / Volcano ------------


def doTsunami(iX, iY):
		feat_seuche = gc.getInfoTypeForString("FEATURE_SEUCHE")
		feat_saurer_regen = gc.getInfoTypeForString("FEATURE_SAURER_REGEN")

		feat_flood_plains = gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS")
		feat_oasis = gc.getInfoTypeForString('FEATURE_OASIS')
		feat_vulkan = gc.getInfoTypeForString("FEATURE_VOLCANO")
		feat_tsunami = gc.getInfoTypeForString("FEATURE_TSUNAMI")

		# iBuildingPalisade = gc.getInfoTypeForString('BUILDING_PALISADE')
		iBuildingWalls = gc.getInfoTypeForString('BUILDING_WALLS')
		iBuildingHW1 = gc.getInfoTypeForString('BUILDING_HIGH_WALLS')
		iBuildingHW2 = gc.getInfoTypeForString('BUILDING_CELTIC_DUN')
		iBuildingHW3 = gc.getInfoTypeForString('BUILDING_HIGH_WALLS_GRECO')

		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		# Der Tsunamieffekt muss im 2ten Wasserfeld vor der Kueste (Land) gestartet werden
		# Der Schaden soll bis einschliesslich 4 Landplots reingehen
		# Der Einschlag/Das Epizentrum darf maximal 3 Felder ausserhalb der Kueste (Land) sein, sonst unwirksam
		# Huegel und Berge stoppen den Schaden an weiteren Feldern
		# Plot 1: Stadt: Pop - 1/2, Units 15%, Gebaeude 10%, Mods + Streets
		# Plot 2: Stadt: Pop - 1/3, Units 10%, Gebaeude  5%, Mods + Streets
		#         Ausgenommen: Stadt auf Huegel mit Stadtmauer: Pop - 1/4, Units und Gebaeude 0%
		# Plot 3: Stadt: Pop - 1/4, Units  5%, Mods + Streets
		#         Ausgenommen: Stadt auf Huegel mit Stadtmauer: Sicher
		# Plot 4: Nur Modernisierungen
		# Stadtmauer 50%, Palisade 100% und Hohe Mauer 20% weg

		for iHimmelsrichtung in range(4):
				iDamageMaxPlots = 4
				bEffectDone = False
				bDoTsunami = False

				# 3 Plots dicke Flutkatastrophe
				for d in range(3):
						# Checken ob innerhalb von 10 Feldern Land ist
						for i in range(10):
								if iHimmelsrichtung == 0:
										loopPlot = CyMap().plot(iX - 1 + d, iY + i)  # Norden
								elif iHimmelsrichtung == 1:
										loopPlot = CyMap().plot(iX - 1 - d, iY - i)  # Sueden
								elif iHimmelsrichtung == 2:
										loopPlot = CyMap().plot(iX + i, iY - 1 + d)  # Osten
								elif iHimmelsrichtung == 3:
										loopPlot = CyMap().plot(iX - i, iY - 1 + d)  # Westen
								# Break und naechste Linie checken
								if loopPlot is None or loopPlot.isNone():
										break
								elif loopPlot.getFeatureType() == iDarkIce:
										break
								elif not loopPlot.isWater():
										bDoTsunami = True

				if not bDoTsunami:
						return

				for d in range(3):
						iDamagePlots = 0

						if iHimmelsrichtung == 0:
								iRange = iMapH - iY
						elif iHimmelsrichtung == 1:
								iRange = iY
						elif iHimmelsrichtung == 2:
								iRange = iMapW - iX
						elif iHimmelsrichtung == 3:
								iRange = iX

						for i in range(iRange):

								if iHimmelsrichtung == 0:
										loopPlot = CyMap().plot(iX - 1 + d, iY + i)
								elif iHimmelsrichtung == 1:
										loopPlot = CyMap().plot(iX - 1 + d, iY - i)
								elif iHimmelsrichtung == 2:
										loopPlot = CyMap().plot(iX + i, iY - 1 + d)
								elif iHimmelsrichtung == 3:
										loopPlot = CyMap().plot(iX - i, iY - 1 + d)

								# 0: Einschlag/Epizentrum
								# Ende bei Max Plots
								if iDamagePlots >= iDamageMaxPlots:
										break
								# Ende bei DarkIce
								if loopPlot.getFeatureType() == iDarkIce:
										break
								# Ende bei Berg oder aktivem Vulkan
								if loopPlot.isPeak() or loopPlot.getFeatureType() == feat_vulkan:
										break
								# Ende wenn es ein Landstrich ist
								if iDamagePlots > 0 and loopPlot.isWater():
										break

								# Land
								if i > 0 and not loopPlot.isWater():
										iDamagePlots += 1

										# Effekt
										if not bEffectDone and d == 1:
												if iHimmelsrichtung == 0:
														iEffect = gc.getInfoTypeForString("EFFECT_TSUNAMI_N")
														pEffectPlot = CyMap().plot(iX, iY + i - 2)
												elif iHimmelsrichtung == 1:
														iEffect = gc.getInfoTypeForString("EFFECT_TSUNAMI_S")
														pEffectPlot = CyMap().plot(iX, iY - i + 2)
												elif iHimmelsrichtung == 2:
														iEffect = gc.getInfoTypeForString("EFFECT_TSUNAMI_E")
														pEffectPlot = CyMap().plot(iX + i - 2, iY)
												elif iHimmelsrichtung == 3:
														iEffect = gc.getInfoTypeForString("EFFECT_TSUNAMI_W")
														pEffectPlot = CyMap().plot(iX - i + 2, iY)
												CyEngine().triggerEffect(iEffect, pEffectPlot.getPoint())
												bEffectDone = True

												doOracleShowsDisaster(pEffectPlot.getX(), pEffectPlot.getY())

												if gc.getPlayer(gc.getGame().getActivePlayer()).isHuman() and pEffectPlot.isVisibleToWatchingHuman():
														CyCamera().JustLookAtPlot(pEffectPlot)
														# Message: Eine gigantische Flutwelle trifft die Kueste und versetzt das Land in aergste Not!
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														sText = CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_TSUNAMI", ("",))
														popupInfo.setText(sText)
														popupInfo.addPopup(gc.getGame().getActivePlayer())
														CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, sText, "AS2D_TSUNAMI", 2, gc.getFeatureInfo(feat_tsunami).getButton(), ColorTypes(7), pEffectPlot.getX(), pEffectPlot.getY(), True, True)

										# Stadt
										if loopPlot.isCity():
												pCity = loopPlot.getPlotCity()
												iPlayer = pCity.getOwner()
												iPopAlt = pCity.getPopulation()
												iPopNeu = iPopAlt

												if iDamagePlots == 0:
														doDestroyCityBuildings(pCity, 10)
														doKillUnits(loopPlot, 15)
														iPopNeu = iPopAlt - int(iPopAlt / 2)
												elif iDamagePlots == 1:
														# Stadt mit Stadtmauern und Huegel
														if loopPlot.isHills() and (pCity.isHasBuilding(iBuildingWalls) or pCity.isHasBuilding(iBuildingHW1) or pCity.isHasBuilding(iBuildingHW2) or pCity.isHasBuilding(iBuildingHW3)):
																iPopNeu = iPopAlt - int(iPopAlt / 4)
														else:
																doDestroyCityBuildings(pCity, 5)
																doKillUnits(loopPlot, 10)
																iPopNeu = iPopAlt - int(iPopAlt / 3)
												elif iDamagePlots == 2:
														# Stadt mit Stadtmauern und Huegel
														if loopPlot.isHills() and (pCity.isHasBuilding(iBuildingWalls) or pCity.isHasBuilding(iBuildingHW1) or pCity.isHasBuilding(iBuildingHW2) or pCity.isHasBuilding(iBuildingHW3)):
																break
														else:
																doKillUnits(loopPlot, 5)
																iPopNeu = iPopAlt - int(iPopAlt / 4)
												pCity.setFood(0)

												# Stadtmauern zerstoeren
												doDestroyWalls(pCity)

												if iPopNeu != iPopAlt:
														iPopNeu = max(1, iPopNeu)
														pCity.setPopulation(iPopNeu)
														if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
																# Message: Die Bevoelkerung der Stadt %s sank von %alt auf %neu!
																CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_CITY_SHRINKS_TO", (pCity.getName(), iPopAlt, iPopNeu)),
																												 None, 2, gc.getFeatureInfo(feat_tsunami).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)

												PAE_City.doCheckCityState(pCity)

										# Land
										else:
												if iDamagePlots + 1 < iDamageMaxPlots:
														loopPlot.setRouteType(-1)
												loopPlot.setImprovementType(-1)
												if loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_saurer_regen and loopPlot.getFeatureType() != feat_oasis:
														loopPlot.setFeatureType(feat_seuche, 0)
												doKillUnits(loopPlot, 30)

										# Bei Huegel Tsunami stoppen
										if loopPlot.isHills():
												iDamagePlots = iDamageMaxPlots

# ----------- Ende Tsunami ------------


def doMeteorites():
		feat_meteor = gc.getInfoTypeForString('FEATURE_METEORS')
		feat_brand = gc.getInfoTypeForString('FEATURE_SMOKE')

		feat_flood_plains = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
		feat_oasis = gc.getInfoTypeForString('FEATURE_OASIS')

		feat_forest = gc.getInfoTypeForString('FEATURE_FOREST')
		feat_forest2 = gc.getInfoTypeForString('FEATURE_DICHTERWALD')
		feat_forest_burnt = gc.getInfoTypeForString('FEATURE_FOREST_BURNT')

		feat_ice = gc.getInfoTypeForString('FEATURE_ICE')
		terr_snow = gc.getInfoTypeForString('TERRAIN_SNOW')

		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		iImpType1 = gc.getInfoTypeForString("IMPROVEMENT_LUMBER_CAMP")

		bonus = [
				gc.getInfoTypeForString("BONUS_MAGNETIT"),
				gc.getInfoTypeForString("BONUS_OREICHALKOS"),
				gc.getInfoTypeForString("BONUS_IRON")
		]
		bonusPlotArray = []

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMaxEffect = 0
		iMapSize = gc.getMap().getWorldSize()
		iMax = max(1, min(12, 2*iMapSize))
		# if iMapSize == 0:
		# iMax = 1
		# elif iMapSize == 1:
		# iMax = 2
		# elif iMapSize == 2:
		# iMax = 4
		# elif iMapSize == 3:
		# iMax = 6
		# elif iMapSize == 4:
		# iMax = 8
		# elif iMapSize == 5:
		# iMax = 10
		# else:
		# iMax = 12

		# 20 Chancen fuer max. iMax Meteorstrikes
		for _ in range(20):
				# Maximal iMax Effekte
				if iMaxEffect == iMax:
						break

				iMapW = gc.getMap().getGridWidth()
				iMapH = gc.getMap().getGridHeight()

				iRandX = CvUtil.myRandom(iMapW, "doMeteorites1")
				iRandY = CvUtil.myRandom(iMapH, "doMeteorites2")
				pPlot = gc.getMap().plot(iRandX, iRandY)
				if pPlot is not None and not pPlot.isNone():
						if pPlot.getFeatureType() == iDarkIce:
								continue

						doOracleShowsDisaster(iRandX, iRandY)

						iMaxEffect += 1
						# Modernisierung und Strasse entfernen
						if not pPlot.isCity():
								pPlot.setRouteType(-1)
								pPlot.setImprovementType(-1)

						iPlayer = pPlot.getOwner()
						if pPlot.isVisibleToWatchingHuman():
								CyCamera().JustLookAtPlot(pPlot)
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_DISASTER_METEORITES", ("", )))
								popupInfo.addPopup(gc.getGame().getActivePlayer())
								CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_METEORITES", ("", )),
																				 "AS2D_METEORSTRIKE", 2, gc.getFeatureInfo(feat_meteor).getButton(), ColorTypes(7), iRandX, iRandY, True, True)

						# Effekt
						iEffect = gc.getInfoTypeForString("EFFECT_METEORS")
						CyEngine().triggerEffect(iEffect, pPlot.getPoint())

						# Stadt
						if pPlot.isCity():
								pCity = pPlot.getPlotCity()
								iPop_alt = pCity.getPopulation()
								iPop_neu = int(pCity.getPopulation() / 2)
								if iPop_neu < 2:
										iPop_neu = 1
								pCity.setPopulation(iPop_neu)
								pCity.setFood(0)
								if iPlayer != -1:
										if pPlot.isVisibleToWatchingHuman():
												if iPlayer == gc.getGame().getActivePlayer():
														CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_DISASTER_METEORITES_CITY", (pCity.getName(), iPop_neu, iPop_alt)),
																										 None, 2, gc.getFeatureInfo(feat_meteor).getButton(), ColorTypes(7), iRandX, iRandY, True, True)
												else:
														CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_METEORITES_CITY_OTHER", (gc.getPlayer(
																pCity.getOwner()).getCivilizationAdjective(2), pCity.getName())), None, 2, gc.getFeatureInfo(feat_meteor).getButton(), ColorTypes(2), iRandX, iRandY, True, True)

								# City, Wahrscheinlichkeit in %
								doKillUnits(pPlot, 10)
								doDestroyCityBuildings(pCity, 33)
								# Stadtmauern zerstoeren
								doDestroyWalls(pCity)
								PAE_City.doCheckCityState(pCity)

						# rundherum Brand generieren und dabei 50:50 Modernis und Strassen entfernen
						for i in range(3):
								for j in range(3):
										loopPlot = gc.getMap().plot(iRandX - 1 + i, iRandY - 1 + j)
										if loopPlot is not None and not loopPlot.isNone():
												if loopPlot.getFeatureType() == iDarkIce:
														continue
												elif loopPlot.getFeatureType() != feat_flood_plains and not loopPlot.isPeak() and not loopPlot.isWater() and loopPlot.getFeatureType() != feat_oasis:
														if loopPlot.getFeatureType() == feat_forest or loopPlot.getFeatureType() == feat_forest2:
																loopPlot.setFeatureType(feat_forest_burnt, 0)
														elif loopPlot.getFeatureType() != feat_ice and loopPlot.getTerrainType() != terr_snow:
																loopPlot.setFeatureType(feat_brand, 0)
														if loopPlot.getImprovementType() == iImpType1:
																loopPlot.setImprovementType(-1)

												if CvUtil.myRandom(2, "doMeteorites3") == 1 and not loopPlot.isCity():
														loopPlot.setRouteType(-1)
														loopPlot.setImprovementType(-1)
												doKillUnits(loopPlot, 20)

										# Plot fuer Magnetit/Oreichalkos Bonus checken
										if not loopPlot.isWater() and not loopPlot.isCity() and not loopPlot.isPeak() and loopPlot.getBonusType(loopPlot.getOwner()) == -1 and loopPlot.getBonusType(-1) == -1:
												bonusPlotArray.append(loopPlot)

										# Verbreitbare Resi vernichten
										if loopPlot.getBonusType(loopPlot.getOwner()) > -1 or loopPlot.getBonusType(-1) > -1:
												doEraseBonusFromDisaster(loopPlot)

		# Chance einer neuen Bonus Resource, 30%
		if bonusPlotArray:
				iRand = CvUtil.myRandom(9, "doMeteorites4_ChanceSetBonus")
				if iRand < 3:
						iRand = CvUtil.myRandom(len(bonus), "doMeteorites5_ChooseBonus")
						iNewBonus = bonus[iRand]
						iRandPlot = CvUtil.myRandom(len(bonusPlotArray), "doMeteorites6_ChooseBonusPlot")
						pRandPlot = bonusPlotArray[iRandPlot]
						pRandPlot.setBonusType(iNewBonus)
						iOwner = pRandPlot.getOwner()
						if iOwner > -1 and gc.getPlayer(iOwner).isHuman():
								CyInterface().addMessage(iOwner, True, 10, CyTranslator().getText("TXT_KEY_NEW_BONUS", (gc.getBonusInfo(iNewBonus).getDescription(), )),
																				 None, 2, gc.getBonusInfo(iNewBonus).getButton(), ColorTypes(14), pRandPlot.getX(), pRandPlot.getY(), True, True)


def doComet():
		feat_comet = gc.getInfoTypeForString('FEATURE_COMET')
		feat_brand = gc.getInfoTypeForString('FEATURE_SMOKE')

		feat_flood_plains = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
		feat_oasis = gc.getInfoTypeForString('FEATURE_OASIS')

		feat_forest = gc.getInfoTypeForString('FEATURE_FOREST')
		feat_forest2 = gc.getInfoTypeForString('FEATURE_DICHTERWALD')
		feat_forest_burnt = gc.getInfoTypeForString('FEATURE_FOREST_BURNT')

		feat_ice = gc.getInfoTypeForString('FEATURE_ICE')
		terr_snow = gc.getInfoTypeForString('TERRAIN_SNOW')
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		iImpType1 = gc.getInfoTypeForString("IMPROVEMENT_LUMBER_CAMP")
		lVillages = []
		lVillages.append(gc.getInfoTypeForString("IMPROVEMENT_HAMLET"))
		lVillages.append(gc.getInfoTypeForString("IMPROVEMENT_VILLAGE"))
		lVillages.append(gc.getInfoTypeForString("IMPROVEMENT_TOWN"))

		bonus = [
				gc.getInfoTypeForString("BONUS_MAGNETIT"),
				gc.getInfoTypeForString("BONUS_OREICHALKOS"),
				gc.getInfoTypeForString("BONUS_IRON")
		]

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		iRangeMaxPlayers = gc.getMAX_PLAYERS()

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMapSize = gc.getMap().getWorldSize()
		if iMapSize < 3:
				iMax = 1
		elif iMapSize < 5:
				iMax = 2
		else:
				iMax = 3

		# iMax Kometen
		for _ in range(iMax):
				# Soll nicht ganz am Rand sein (Flunky: alle 4 Raender ausnehmen)
				iRandX = 3 + CvUtil.myRandom(iMapW - 6, "doComet1")
				iRandY = 3 + CvUtil.myRandom(iMapH - 6, "doComet2")
				pPlot = gc.getMap().plot(iRandX, iRandY)
				if pPlot is not None and not pPlot.isNone():
						if pPlot.getFeatureType() == iDarkIce:
								continue

						doOracleShowsDisaster(iRandX, iRandY)

						# Modernisierung und Strasse entfernen
						if not pPlot.isCity():
								pPlot.setRouteType(-1)
								pPlot.setImprovementType(-1)

						iPlayer = pPlot.getOwner()

						if pPlot.isVisibleToWatchingHuman():
								CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_COMET", ("",)),
																				 "AS2D_BOMBARD", 2, gc.getFeatureInfo(feat_comet).getButton(), ColorTypes(7), iRandX, iRandY, True, True)
								CyCamera().JustLookAtPlot(pPlot)

						# Effekt
						if pPlot.isWater():
								CyEngine().triggerEffect(gc.getInfoTypeForString("EFFECT_COMET_WATER"), pPlot.getPoint())
								# Loest Tsunami aus
								doTsunami(iRandX, iRandY)
						else:
								CyEngine().triggerEffect(gc.getInfoTypeForString("EFFECT_COMET"), pPlot.getPoint())
								# Stadt
								if pPlot.isCity():
										pCity = pPlot.getPlotCity()
										iPop_alt = pCity.getPopulation()
										iPop_neu = int(pCity.getPopulation() / 6)
										if iPop_neu < 2:
												iPop_neu = 1
										pCity.setPopulation(iPop_neu)
										pCity.setFood(0)

										# Messages
										for iPlayer2 in range(iRangeMaxPlayers):
												pSecondPlayer = gc.getPlayer(iPlayer2)
												iSecondPlayer = pSecondPlayer.getID()
												if pSecondPlayer.isHuman():
														iSecTeam = pSecondPlayer.getTeam()
														if pPlot.isVisible(iSecTeam, 0) and pSecondPlayer.isHuman():
																if iPlayer == iSecondPlayer:
																		popupInfo = CyPopupInfo()
																		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
																		sText = CyTranslator().getText("TXT_KEY_DISASTER_COMET_CITY", (pCity.getName(), iPop_neu, iPop_alt))
																		popupInfo.setText(sText)
																		popupInfo.addPopup(iPlayer)
																		CyInterface().addMessage(iPlayer, True, 12, sText, None, 2, gc.getFeatureInfo(feat_comet).getButton(), ColorTypes(7), iRandX, iRandY, True, True)
																elif iPlayer != -1:
																		# Message an alle
																		CyInterface().addMessage(iSecondPlayer, True, 12, CyTranslator().getText("TXT_KEY_DISASTER_COMET_CITY_OTHER", (gc.getPlayer(
																				iPlayer).getCivilizationAdjective(2), pCity.getName())), None, 2, gc.getFeatureInfo(feat_comet).getButton(), ColorTypes(2), iRandX, iRandY, True, True)

										# City, Wahrscheinlichkeit in %
										doKillUnits(pPlot, 100)
										doDestroyCityBuildings(pCity, 80)
										doDestroyCityWonders(pCity, 25, feat_comet)
										PAE_City.doCheckCityState(pCity)

								# rundherum Brand generieren und dabei 50:50 Modernis und Strassen entfernen
								for i in range(7):
										for j in range(7):
												loopPlot = gc.getMap().plot(iRandX - 3 + i, iRandY - 3 + j)
												if loopPlot is not None and not loopPlot.isNone():
														if loopPlot.getFeatureType() == iDarkIce:
																continue
														if loopPlot.getFeatureType() != feat_flood_plains and loopPlot.getFeatureType() != feat_oasis and not loopPlot.isPeak() and not loopPlot.isWater():
																if loopPlot.getFeatureType() == feat_forest or loopPlot.getFeatureType() == feat_forest2:
																		loopPlot.setFeatureType(feat_forest_burnt, 0)
																elif loopPlot.getFeatureType() != feat_ice and loopPlot.getTerrainType() != terr_snow:
																		loopPlot.setFeatureType(feat_brand, 0)
																if loopPlot.getImprovementType() == iImpType1:
																		loopPlot.setImprovementType(-1)

														if CvUtil.myRandom(2, "doComet3") == 1:
																if not loopPlot.isCity():
																		loopPlot.setRouteType(-1)
																		loopPlot.setImprovementType(-1)
														# Gemeinden und Doerfer -> Huetten/Cottages
														elif loopPlot.getImprovementType() in lVillages:
																loopPlot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_COTTAGE"))

														# Entfernung zum Einschlag berechnen
														iBetrag = (iRandX - loopPlot.getX()) * (iRandX - loopPlot.getX()) + (iRandY - loopPlot.getY()) * (iRandY - loopPlot.getY())
														if iBetrag == 1:
																doKillUnits(loopPlot, 50)
																if loopPlot.isCity():
																		doDestroyCityBuildings(loopPlot.getPlotCity(), 50)
														elif iBetrag == 2:
																doKillUnits(loopPlot, 25)
																if loopPlot.isCity():
																		doDestroyCityBuildings(loopPlot.getPlotCity(), 25)
														elif iBetrag == 3:
																doKillUnits(loopPlot, 10)
																if loopPlot.isCity():
																		doDestroyCityBuildings(loopPlot.getPlotCity(), 10)

												# Stadtmauern zerstoeren
												if loopPlot.isCity():
														doDestroyWalls(loopPlot.getPlotCity())

												# Verbreitbare Resi vernichten (nur Radius 2)
												if i > 0 and i < 6 and j > 1 and j < 6:
														if loopPlot.getBonusType(-1) != -1:
																doEraseBonusFromDisaster(loopPlot)

								# Chance einer neuen Bonus Resource fix auf pPlot, 50%
								if not pPlot.isWater() and not pPlot.isPeak() and pPlot.getBonusType(pPlot.getOwner()) == -1 and pPlot.getBonusType(-1) == -1:
										iRand = CvUtil.myRandom(2, "doComet4_ChanceOfBonus")
										if iRand == 0:
												iRand = CvUtil.myRandom(len(bonus), "doComet5_ChooseBonus")
												iNewBonus = bonus[iRand]
												pPlot.setBonusType(iNewBonus)
												iPlotOwner = pPlot.getOwner()
												if iPlotOwner != -1 and gc.getPlayer(iPlotOwner).isHuman():
														CyInterface().addMessage(iPlotOwner, True, 10, CyTranslator().getText("TXT_KEY_NEW_BONUS", (gc.getBonusInfo(iNewBonus).getDescription(),)),
																										 None, 2, gc.getBonusInfo(iNewBonus).getButton(), ColorTypes(14), pPlot.getX(), pPlot.getY(), True, True)

				# ------------------- Anfang Gebaeude, Wunder und Einheiten Damage  -----------------
				# iChance = Wahrscheinlichkeit, dass ein Gebaeude zerstoert wird


def doDestroyCityBuildings(pCity, iChance):
		if pCity.getNumBuildings() > 0:
				iOwner = pCity.getOwner()
				iRange = gc.getNumBuildingInfos()
				bDestroyed = False
				for iBuilding in range(iRange):
						if pCity.getNumRealBuilding(iBuilding):
								pBuilding = gc.getBuildingInfo(iBuilding)
								if not isWorldWonderClass(pBuilding.getBuildingClassType()):
										if CvUtil.myRandom(100, "destroyCityBuildings") < iChance:
												pCity.setNumRealBuilding(iBuilding, 0)
												bDestroyed = True
												pOwner = gc.getPlayer(iOwner)
												if pOwner.isHuman():
														CyInterface().addMessage(pOwner.getID(), True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BUILDING", (pCity.getName(),
																																																																						 pBuilding.getDescription())), None, 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
				PAE_City.doCheckCityState(pCity)
				PAE_City.doCheckTraitBuildings(pCity)
				PAE_City.doCheckGlobalTraitBuildings(iOwner)
				if bDestroyed and pCity.getProductionProcess() != -1:
						pCity.clearOrderQueue()

				# iChance = Wahrscheinlichkeit, dass ein Wunder zerstoert wird
				# iFeatureType = Art der Katastrophe


def doDestroyCityWonders(pCity, iChance, iFeatureType):
		if pCity.getNumBuildings() > 0:
				iOwner = pCity.getOwner()
				iFeature_Erdbeben = gc.getInfoTypeForString("FEATURE_ERDBEBEN")
				iFeature_Komet = gc.getInfoTypeForString("FEATURE_COMET")
				LDoNotDestroy = [
						gc.getInfoTypeForString("BUILDING_PYRAMID")
				]
				iRange = gc.getNumBuildingInfos()
				for iBuilding in range(iRange):
						if iBuilding not in LDoNotDestroy:
								pBuilding = gc.getBuildingInfo(iBuilding)
								if pCity.getNumBuilding(iBuilding) and isWorldWonderClass(pBuilding.getBuildingClassType()):
										if CvUtil.myRandom(100, "destroyWW") < iChance:
												pCity.setNumRealBuilding(iBuilding, 0)
												# Messages
												pOwner = gc.getPlayer(iOwner)
												iOwnerTeam = pOwner.getTeam()
												iRangeMaxPlayers = gc.getMAX_PLAYERS()
												for iAllPlayer in range(iRangeMaxPlayers):
														ThisPlayer = gc.getPlayer(iAllPlayer)
														iThisPlayer = ThisPlayer.getID()
														iThisTeam = ThisPlayer.getTeam()
														ThisTeam = gc.getTeam(iThisTeam)
														if ThisTeam.isHasMet(iOwnerTeam) and ThisPlayer.isHuman():
																if iFeatureType == iFeature_Erdbeben:
																		CyInterface().addMessage(iThisPlayer, True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_WONDER_ERDBEBEN", (pOwner.getCivilizationAdjective(
																				1), pCity.getName(), pBuilding.getDescription())), "AS2D_EARTHQUAKE", 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
																elif iFeatureType == iFeature_Komet:
																		CyInterface().addMessage(iThisPlayer, True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_WONDER_KOMET", (pOwner.getCivilizationAdjective(
																				1), pCity.getName(), pBuilding.getDescription())), "AS2D_PLAGUE", 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
																else:
																		CyInterface().addMessage(iThisPlayer, True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_WONDER", (pOwner.getCivilizationAdjective(
																				1), pCity.getName(), pBuilding.getDescription())), "AS2D_PLAGUE", 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

				# iChance = Wahrscheinlichkeit, dass eine Unit gekillt wird


def doKillUnits(pPlot, iChance):
		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit is not None:
						iRand = CvUtil.myRandom(100, "doKillUnits")
						if iRand < iChance:
								# Wenn ein General draufgeht hat das Auswirkungen
								if pUnit.getLeaderUnitType() > -1:
										PAE_Unit.doDyingGeneral(pUnit)
								iOwner = pUnit.getOwner()
								if iOwner != -1 and gc.getPlayer(iOwner).isHuman():
										# Message: Eure Einheit %s hat diese schreckliche Naturgewalt nicht ueberlebt!
										CyInterface().addMessage(iOwner, True, 8, CyTranslator().getText("TXT_KEY_MESSAGE_DISASTER_UNIT_KILLED", (pUnit.getName(), 0)),
																						 "AS2D_PLAGUE", 2, pUnit.getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
								# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
								pUnit.kill(True, -1)  # RAMK_CTD
						else:
								pUnit.setDamage(60, -1)
								pUnit.setImmobileTimer(1)

# Stadtmauern zerstoeren


def doDestroyWalls(pCity):
		iPlayer = pCity.getOwner()
		iBuildingPalisade = gc.getInfoTypeForString('BUILDING_PALISADE')
		iBuildingWalls = gc.getInfoTypeForString('BUILDING_WALLS')
		iBuildingHW1 = gc.getInfoTypeForString('BUILDING_HIGH_WALLS')
		iBuildingHW2 = gc.getInfoTypeForString('BUILDING_CELTIC_DUN')
		iBuildingHW3 = gc.getInfoTypeForString('BUILDING_HIGH_WALLS_GRECO')
		bDestroyed = False

		iChance = CvUtil.myRandom(100, "destroy_HW1")
		if pCity.isHasBuilding(iBuildingHW1) and iChance < 25:
				bDestroyed = True
				pBuilding = gc.getBuildingInfo(iBuildingHW1)
				pCity.setNumRealBuilding(iBuildingHW1, 0)
				if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
						CyInterface().addMessage(gc.getPlayer(iPlayer).getID(), True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BUILDING",
																																																		(pCity.getName(), pBuilding.getDescription())), None, 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
		elif pCity.isHasBuilding(iBuildingHW2) and iChance < 25:
				bDestroyed = True
				pBuilding = gc.getBuildingInfo(iBuildingHW2)
				pCity.setNumRealBuilding(iBuildingHW2, 0)
				if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
						CyInterface().addMessage(gc.getPlayer(iPlayer).getID(), True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BUILDING",
																																																		(pCity.getName(), pBuilding.getDescription())), None, 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
		elif pCity.isHasBuilding(iBuildingHW3) and iChance < 25:
				bDestroyed = True
				pBuilding = gc.getBuildingInfo(iBuildingHW3)
				pCity.setNumRealBuilding(iBuildingHW3, 0)
				if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
						CyInterface().addMessage(gc.getPlayer(iPlayer).getID(), True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BUILDING",
																																																		(pCity.getName(), pBuilding.getDescription())), None, 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

		if pCity.isHasBuilding(iBuildingWalls):
				if (bDestroyed and iChance < 15) or (not bDestroyed and iChance < 50):
						bDestroyed = True
						pBuilding = gc.getBuildingInfo(iBuildingWalls)
						pCity.setNumRealBuilding(iBuildingWalls, 0)
						if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
								CyInterface().addMessage(gc.getPlayer(iPlayer).getID(), True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BUILDING",
																																																				(pCity.getName(), pBuilding.getDescription())), None, 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

		if pCity.isHasBuilding(iBuildingPalisade):
				if (bDestroyed and iChance < 15) or not bDestroyed:
						pBuilding = gc.getBuildingInfo(iBuildingPalisade)
						pCity.setNumRealBuilding(iBuildingPalisade, 0)
						if iPlayer != -1 and gc.getPlayer(iPlayer).isHuman():
								CyInterface().addMessage(gc.getPlayer(iPlayer).getID(), True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BUILDING",
																																																				(pCity.getName(), pBuilding.getDescription())), None, 2, pBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

		if bDestroyed and pCity.getProductionProcess() != -1:
				pCity.clearOrderQueue()

# Naturkatastrophen vernichten verbreitbare Bonusresourcen
# Nur bei Vulkan, Meteoriten und Kometen


def doEraseBonusFromDisaster(pPlot):
		# Inits (von doBonusCityGetPlot)
		lGetreide = [
				gc.getInfoTypeForString("BONUS_WHEAT"),
				gc.getInfoTypeForString("BONUS_GERSTE"),
				gc.getInfoTypeForString("BONUS_HAFER"),
				gc.getInfoTypeForString("BONUS_ROGGEN"),
				gc.getInfoTypeForString("BONUS_HIRSE"),
				gc.getInfoTypeForString("BONUS_RICE")
		]
		lVieh1 = [
				gc.getInfoTypeForString("BONUS_COW"),
				gc.getInfoTypeForString("BONUS_PIG"),
				gc.getInfoTypeForString("BONUS_SHEEP")
		]
		lSpice = [
				gc.getInfoTypeForString("BONUS_OLIVES"),
				gc.getInfoTypeForString("BONUS_DATTELN")
		]
		lTier1 = [
				gc.getInfoTypeForString("BONUS_CAMEL")
		]

		# known bonus or unknown bonus(?)
		iPlayer = pPlot.getOwner()
		iBonus = pPlot.getBonusType(iPlayer)
		if iBonus == -1:
				iBonus = pPlot.getBonusType(-1)

		elif iBonus in lGetreide or iBonus in lVieh1 or iBonus in lSpice or iBonus in lTier1:
				pPlot.setBonusType(-1)
				pPlot.setImprovementType(-1)
				if iPlayer > -1 and gc.getPlayer(iPlayer).isHuman():
						if iBonus in lGetreide:
								CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BONUS1", (gc.getBonusInfo(iBonus).getDescription(),)),
																				 None, 2, gc.getBonusInfo(iBonus).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
						elif iBonus in lVieh1 or iBonus in lTier1:
								CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BONUS2", (gc.getBonusInfo(iBonus).getDescription(),)),
																				 None, 2, gc.getBonusInfo(iBonus).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
						elif iBonus in lSpice:
								CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_DISASTER_DESTROYED_BONUS3", (gc.getBonusInfo(iBonus).getDescription(),)),
																				 None, 2, gc.getBonusInfo(iBonus).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)

# CIV mit dem Orakel von Delphi darf die Stelle grau sehen


def doOracleShowsDisaster(iX, iY):
		iBuilding = gc.getInfoTypeForString("BUILDINGCLASS_ORACLE")
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
				pPlayer = gc.getPlayer(i)
				if pPlayer.isHuman():
						if pPlayer.getBuildingClassCount(iBuilding) > 0:
								iTeam = pPlayer.getTeam()
								for x in range(-1, 2):
										for y in range(-1, 2):
												loopPlot = plotXY(iX, iY, x, y)
												if loopPlot is not None and not loopPlot.isNone():
														if not loopPlot.isVisible(iTeam, 0):
																# setRevealed (TeamType eTeam, BOOL bNewValue, BOOL bTerrainOnly, TeamType eFromTeam)
																loopPlot.setRevealed(iTeam, 0, 1, -1)
								return

# ++++++++++++++++++ ENDE Naturkatastrophen / Disasters +++++++++++++++++++++++++++++
