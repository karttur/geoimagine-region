'''
Created on 16 Oct 2018

@author: thomasgumbricht
'''

import geoimagine.gis.mj_gis_v80 as mj_gis

class ProcessRegion:
    'class for all region management'   
    def __init__(self, process):
        self.process = process
        #direct to subprocess
        SNULLE
        if self.process.processid == 'linkdefaultregionstomodis':
            self.LinkDefaultRegionsToMODIS()
    
    def GetModisTilesDict(self):
        '''
        '''
        recs = self.session._SelectModisTileCoords({})
        modisTileD ={}
        for rec in recs:
            hvtile,h,v,minxsin,minysin,maxxsin,maxysin,ullat,ullon,lrlat,lrlon,urlat,urlon,lllat,lllon = rec
            llptL = ((ullon,ullat),(urlon,urlat),(lrlon,lrlat),(lllon,lllat))
            modtilegeom = mj_gis.Geometry()
            modtilegeom.PointsToPolygonGeom(llptL)
            west, south, east, north = modtilegeom.shapelyGeom.bounds
            modisTileD[hvtile] = {'hvtile':hvtile,'h':h,'v':v,'geom':modtilegeom,
                                  'west':west,'south':south,'east':east,'north':north}        
     
    def GetSystemDefRegions(self):
        '''
        '''
        #I need the layer for the region that is not in the regionsmodis table
        recs = self.regionSession._SelectAllDefRegions()
        for rec in recs:
            compQ = {'system': 'system'}
            inclL = [{'regiionid':rec[1]}]
            layerComp = self.regionSession._SelectCompAlt(compQ,inclL)
            #Create the layer
            STOPFORNOW
    
    def GetRegionVector(self,FPN):
        '''
        '''
             
    def LinkMODIS(self):
        '''
        session = SelectUser()
        userid = 'karttur'
        userData = session._SelectUserCreds(userid,'')
        if userData[2] < 10:
            exitstr = 'The user does not have sufficient rights for this process'
            exit(exitstr)  
        '''  
        #Open the db session for MODIS
        #sessionModis = ManageMODIS()
        #Open the session for sentinel
        #sessionLandsat = ManageLandsat()
        recs = self.session._SelectModisTileCoords({})
        modisTileD ={}
        for rec in recs:
            hvtile,h,v,minxsin,minysin,maxxsin,maxysin,ullat,ullon,lrlat,lrlon,urlat,urlon,lllat,lllon = rec
            llptL = ((ullon,ullat),(urlon,urlat),(lrlon,lrlat),(lllon,lllat))
            modtilegeom = mj_gis.Geometry()
            modtilegeom.PointsToPolygonGeom(llptL)
            west, south, east, north = modtilegeom.shapelyGeom.bounds
            modisTileD[hvtile] = {'hvtile':hvtile,'h':h,'v':v,'geom':modtilegeom,
                                  'west':west,'south':south,'east':east,'north':north}
        '''
            #Get all sentinel tiles falling inside the bounding box (nothing is omitted?)
            landsattiles = sessionLandsat._SearchTilesFromWSEN(west, south, east, north)
            #loop
            for landsattile in landsattiles:
                wrs,ldir,p,r,tilewest,tilesouth,tileeast,tilenorth,ullon,ullat,urlon,urlat,lrlon,lrlat,lllon,lllat, minx, miny, maxx, maxy = landsattile  
                llptL = ((ullon,ullat),(urlon,urlat),(lrlon,lrlat),(lllon,lllat))
                tilegeom = mj_gis.Geometry()
                tilegeom.PointsToPolygonGeom(llptL)
                prD = ConvertLandsatTilesToStr(p,r)
                #print ('llptL',prD['prstr'],wrs,ldir,llptL)
                #Get the overlap
                overlapGeom = tilegeom.ShapelyIntersection(modtilegeom)
                productoverlap = overlapGeom.area/tilegeom.shapelyGeom.area
    
                if productoverlap > 0:
                   
                    queryD = {'regionid':hvtile, 'regiontype':'sintile', 'prstr':prD['prstr'], 'dir':ldir, 'wrs':wrs, 'path':p, 'row':r}
                    #print ('query',queryD)
    
                    sessionLandsat._InsertSingleLandsatRegion(queryD)
        '''
        
    def LinkDefaultRegionsToMODIS(self):
        layerIn = self.PolygonLinkFile()
        datum = self.process.srcPeriod.datumL[0]
        satsys = 'MODIS'
        if satsys == 'MODIS': 
            recs = ConnRegions.SelectAllRegoinsMODIS()
        elif satsys == 'landsat':
            recs = ConnRegions.SelectAllRegoinsWrs()
        #set the link class and the wrs poly file
        linkwrs = mj_gis.LinkRegions(layerIn.FPN,'htile','vtile')
        for rec in recs:
            if rec[2].upper() == 'D':
                print 'rec',rec
                comp = ConnRegions.SelectRegionCompFromIdCat(rec[0],rec[1])
                if not len(comp) == 1:
                    print '    duplicates for',rec[0],rec[1]
                    for c in comp:
                        print '        ',c
                    continue
                source, product, folder, band, prefix, suffix, acqdatestr, regionid, regioncat, stratum = comp[0]
                #datum = AcqDate({'acqdatestr': acqdatestr, 'timestep': 'dummy'}) 
                #reset the datum to the db datum for the region
                datum = {'acqdatestr': acqdatestr, 'timestep': 'dummy'}  
                parentcatid = ConnRegions.SelectParentRegion(regioncat,regionid)
                if parentcatid == None:
                    exitstr = 'No parent found for region %s' %(regionid)
                    continue
                #parentid, parentcat = parentcatid
                parentid = parentcatid[0]
                mainpath = os.path.split(self.process.srcpath.mainpath)[0]
                csvFP = os.path.join(mainpath,'temp')
                if not os.path.exists(csvFP):
                    os.makedirs(csvFP)
                csvFPN = os.path.join(csvFP,'wrstemp.csv')
                mainpath = os.path.join(mainpath,'ROI')
                comp = Composition(source,product,folder,band,prefix,suffix, division = 'region',mainpath = mainpath)
                comp.SetExt('shp')

                regionLayer = ROILayer(comp, regionid, datum)

                regionLayer.SetRegionPath() 
                if os.path.isfile(regionLayer.FPN):
                    print '        extracting tile coverage for %s' %(regionLayer.FN)
                    #wrsLD = mj_gis.LinkRegionsToWRS(regionLayer.FPN, layerIn.FPN, 0.005)
                    #wrsLD = linkwrs.OverlayRegion(regionLayer.FPN, 0.005)
                    if stratum < 5:
                        #For subcontinental to global the smallest items are approximately 5 km
                        wrsLD = linkwrs.OverlayRegion(regionLayer.FPN, 0.05)
                    else:
                        #For countires and smaller the smallest items are approximately 0.5 km
                        wrsLD = linkwrs.OverlayRegion(regionLayer.FPN, 0.0005)
                    if not wrsLD:
                        continue
                    if len(wrsLD) == 0: 
                         
                        #if not wrs scene location is found (small island regions) rerun with full resolution     
                        wrsLD = linkwrs.OverlayRegion(regionLayer.FPN, False)
                        #wrsLD = mj_gis.LinkRegionsToWRS(regionLayer.FPN, layerIn.FPN, False)
                    print regionid, wrsLD 
                    if satsys == 'MODIS':
                        ConnRegions.InsertBULKRegionMODIS(csvFPN,wrsLD,regionid,'D')  
                    else:
                        MINGAL                        
                        ConnRegions.InsertBULKRegionWRS(csvFPN,wrsLD,regionid,'D',aD['wrs'])
                else:
                    exitstr = 'default region layer missing: %s' %(regionLayer.FPN)
                    print exitstr
                    sys.exit(exitstr)