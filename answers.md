#### 1. Create new location in GRASS GIS
New
GIS Data Directory: grassdata
Project Location: BadenWuerttemberg
Weiter
Read projection and datum terms from a georeferenced data file
Weiter
Georeferenced file: GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3.tif
Weiter und fertigstellen
Neu erstellte Location und PERMANENT-Mapset auswählen, dann Session starten

#### 2. Import data

##### 2.1 Motorways
`cd A2_GRASS_GIS\data`

`v.import motorways.shp`

##### 2.2 Administrative Districts of Baden-Württemberg
`v.in.ogr input=gadm28_adm2_germany.shp where="ID_1 =  1  AND  ENGTYPE_2 = 'District'" location=gadm`

`v.proj location=gadm mapset=PERMANENT input=gadm28_adm2_germany`

##### 2.3 Global Human Settlement Layer
Entfällt

#### 3. Calculate the total population of the districts

##### 3.1 Set the region
`g.region -p raster=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT vector=gadm28_adm2_germany@PERMANENT res=250`

##### 3.2 Rasterize the districts
`v.to.rast input=gadm28_adm2_germany@PERMANENT output=bw_raster use=attr attribute_column=OBJECTID`

##### 3.3 Calculate the population of each district
`r.stats.zonal base=bw_raster@PERMANENT cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT method=sum output=bw_raster_sum`

##### 3.4 Evaluate the population estimate
| Kreis  | Global Human Settlement Layer  |  offizielle Daten |
|---|---|---|
| Rhein-Neckar | 536.018 | 548.139 |
| Heidelberg | 154.588 | 159.975 |
| Mannheim | 290.401 | 309.090 |

Der Global Human Settlement Layer ist in Betrachtung der Tabelle realtiv genau. 


Datenquelle: Statista (2020): Einwohnerzahl der Land- und Stadtkreise in Baden-Württemberg 2019 (https://de.statista.com/statistik/daten/studie/1071004/umfrage/einwohnerzahl-der-kreise-in-baden-wuerttemberg/)

#### 4. Calculate total population living within 1km of motorways
- set region to motorways: `g.region -p vector=motorways@PERMANENT res=250`
- rasterize motorways: `v.to.rast input=motorways@PERMANENT output=motorways_rasterized use=v`
- get 1km motorways buffer: `r.buffer input=motorways_rasterized@PERMANENT output=motorways_rasterized_1km distances=1000`
- `r.stats.zonal base=motorways_rasterized_1km@PERMANENT cover=GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3@PERMANENT method=sum output=districts_bw_pop_motorways1km_sum`
- `r.stats input=districts_bw_pop_motorways1km_sum@PERMANENT`