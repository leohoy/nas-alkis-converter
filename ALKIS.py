from osgeo import ogr
import os
import geopandas as gp
from sys import getsizeof

dictwhichfileiswhichclass={}
for filename in os.listdir('ALKIS'):
    if filename.endswith(".xml"):
        file1 = open('ALKIS/{}'.format(filename), "r+")
        data = file1.read()
        position1=data.find("AX_",200)
        position2=(data.find("&lt",position1))
        ALKIS=(data[position1+3:-1*((len(data))-position2)])
        if ALKIS in dictwhichfileiswhichclass:
            dictwhichfileiswhichclass[ALKIS].append(filename)
        else:
            dictwhichfileiswhichclass[ALKIS] = [filename]

print('done')
for key,value in dictwhichfileiswhichclass.items():
    dfline=gp.GeoDataFrame()
    dfcompoundcurve=gp.GeoDataFrame()
    dfpoly=gp.GeoDataFrame()
    dfmultipoly=gp.GeoDataFrame()
    dfpoint=gp.GeoDataFrame()
    dfmultipoint=gp.GeoDataFrame()
    dfcurvepoly=gp.GeoDataFrame()
    m=0
    for item in value:
        file = ogr.Open('ALKIS/{}'.format(item))
        for name in range(len(file)):
            shaper = file.GetLayer(name)
            drv = ogr.GetDriverByName('GeoJSON')
            feature = shaper.GetNextFeature()
            try:
                geometry = feature.GetGeometryRef()
                geometrytype = geometry.GetGeometryName()
            except:
                continue
            FileName="item.geojson"
            if os.path.exists(FileName):
                drv.DeleteDataSource(FileName)
            outDataSource = drv.CreateDataSource(FileName)
            outLayer = outDataSource.CopyLayer(shaper,'item')
            del shaper,drv,outDataSource,outLayer
            df2=gp.read_file("item.geojson")
            if geometrytype=='LINESTRING':
                dfline=dfline.append(df2)
                if getsizeof(dfline) > 104857600:
                    dfline.to_file('ALKIS/Shapefiles/{}{}line.shp'.format(key, m), driver='Shapefile')
                    dfline = gp.GeoDataFrame()
                    m += 1
            if geometrytype=='POLYGON':
                dfpoly=dfpoly.append(df2)
                if getsizeof(dfpoly) > 104857600:
                    dfpoly.to_file('ALKIS/Shapefiles/{}{}poly.shp'.format(key, m), driver='Shapefile')
                    dfpoly = gp.GeoDataFrame()
                    m += 1
            if geometrytype=='MULTIPOLYGON':
                dfmultipoly=dfmultipoly.append(df2)
                if getsizeof(dfmultipoly) > 104857600:
                    dfmultipoly.to_file('ALKIS/Shapefiles/{}{}multipoly.shp'.format(key, m), driver='Shapefile')
                    dfmultipoly = gp.GeoDataFrame()
                    m += 1
            if geometrytype=='CURVEPOLYGON':
                dfcurvepoly=dfcurvepoly.append(df2)
                if getsizeof(dfcurvepoly) > 104857600:
                    dfcurvepoly.to_file('ALKIS/Shapefiles/{}{}curvepoly.shp'.format(key, m), driver='Shapefile')
                    dfcurvepoly = gp.GeoDataFrame()
                    m += 1
            if geometrytype=='POINT':
                dfpoint=dfpoint.append(df2)
                if getsizeof(dfpoint)>104857600:
                    dfpoint.to_file('ALKIS/Shapefiles/{}{}point.shp'.format(key, m), driver='Shapefile')
                    dfpoint = gp.GeoDataFrame()
                    m += 1
            if geometrytype=='MULTIPOINT':
                dfmultipoint=dfmultipoint.append(df2)
                if getsizeof(dfmultipoint)>104857600:
                    dfmultipoint.to_file('ALKIS/Shapefiles/{}{}multipoint.shp'.format(key, m), driver='Shapefile')
                    dfmultipoint = gp.GeoDataFrame()
                    m += 1
            if geometrytype=='COMPOUNDCURVE':
                dfcompoundcurve=dfcompoundcurve.append(df2)
                if getsizeof(dfcompoundcurve)>104857600:
                    dfcompoundcurve.to_file('ALKIS/Shapefiles/{}{}compoundcurve.shp'.format(key, m), driver='Shapefile')
                    dfcompoundcurve = gp.GeoDataFrame()
                    m += 1
            geotypes=['LINESTRING','POLYGON','CURVEPOLYGON','POINT','MULTIPOINT','COMPOUNDCURVE','MULTIPOLYGON']
            if geometrytype not in geotypes:
                print(geometrytype)
                stop
    if len(dfline)!=0:
        dfline.to_file('ALKIS/Shapefiles/{}{}line.shp'.format(key, m), driver='Shapefile')
        dfline = gp.GeoDataFrame()
        m += 1
    if len(dfpoly) != 0:
        dfpoly.to_file('ALKIS/Shapefiles/{}{}poly.shp'.format(key, m), driver='Shapefile')
        dfpoly = gp.GeoDataFrame()
        m += 1
    if len(dfmultipoly) != 0:
        dfmultipoly.to_file('ALKIS/Shapefiles/{}{}multipoly.shp'.format(key, m), driver='Shapefile')
        dfmultipoly = gp.GeoDataFrame()
        m += 1
    if len(dfpoint) != 0:
        dfpoint.to_file('ALKIS/Shapefiles/{}{}point.shp'.format(key, m), driver='Shapefile')
        dfpoint = gp.GeoDataFrame()
        m += 1
    if len(dfpoint) != 0:
        dfmultipoint.to_file('ALKIS/Shapefiles/{}{}multipoint.shp'.format(key, m), driver='Shapefile')
        dfmultipoint = gp.GeoDataFrame()
        m += 1
    if len(dfcompoundcurve) != 0:
        dfcompoundcurve.to_file('ALKIS/Shapefiles/{}{}compoundcurve.shp'.format(key, m), driver='Shapefile')
        dfcompoundcurve = gp.GeoDataFrame()
        m += 1
    if len(dfcurvepoly) != 0:
        dfcurvepoly.to_file('ALKIS/Shapefiles/{}{}curvepoly.shp'.format(key, m), driver='Shapefile')
        dfcurvepoly = gp.GeoDataFrame()
        m += 1
    print(key)