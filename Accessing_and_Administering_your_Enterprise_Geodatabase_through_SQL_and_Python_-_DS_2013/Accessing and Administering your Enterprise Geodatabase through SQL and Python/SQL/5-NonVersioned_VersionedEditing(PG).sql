------------------------------------------
-- Non Versioned Editing Demo
------------------------------------------

-- Insert polygon into the non-versioned buildings feature class

--Begin a new database transaction
BEGIN;

--Insert a new polygon, using a nested subquery to determine the SRID
INSERT INTO brent.building_nv 
VALUES (SDE.NEXT_ROWID('brent','building_nv'), NULL, NULL, 0, 0, 1, 'DS_2013',sde.st_geometry('POLYGON ((
6228101.972 2296615.908,
6228121.937 2296625.457,
6228121.937 2296667.124,
6228172.284 2296667.124,
6228172.352 2296635.924,
6228163.611 2296635.924,
6228163.611 2296613.354,
6228139.298 2296613.304,
6228139.346 2296607.614,
6228110.652 2296594.207,
6228101.972 2296615.908))', (Select Distinct sde.ST_SRID(SHAPE) from brent.building_nv)));

--Commit the open transaction
COMMIT;


-- DEMO CLEANUP - for deleting temporary polygons created by the script
--DELETE FROM brent.building_nv where PHASE = 'DS_2013';

------------------------------------------
-- Versioned Editing Demo
------------------------------------------

-- If using s PGSQL function would be able to test for isVersioned and isSimple 
-- IF SDE.IS_SIMPLE('brent','ParcelCentroid') AND SDE.IS_VERSIONED('brent','ParcelCentroid') THEN

--Open the version for editing 1 = open new state on the version
SELECT sde.sde_edit_version('brent.WorkOrder1701',1);

--Begin the database transaction
BEGIN;

--Insert values into the parcel Centroids versioned view to make versioned edits through SQL
INSERT INTO brent.parcelcentroid_evw (SHAPE, comments) VALUES (sde.st_geometry('POINT (6228143.478  2296635.225)',(Select Distinct sde.ST_SRID(SHAPE) from brent.ParcelCentroid)),'DS2013');

SELECT * FROM brent.parcelcentroid_evw

--Commit the database transaction
COMMIT;

--Close the version for editing 2 = close the open state on the version
SELECT sde.sde_edit_version('brent.WorkOrder1701',2);


-- DEMO CLEANUP - delete the versioned feature that was created in the demo
SELECT sde.sde_edit_version('brent.WorkOrder1701',1);
BEGIN;
DELETE from brent.parcelcentroid_evw where comments = 'DS2013'; 
COMMIT;
SELECT sde.sde_edit_version('brent.WorkOrder1701',2);

------------------------------------------
-- Query layer / view demo 
------------------------------------------

SELECT owners.apn as PARCELID, owners.grantor as OWNER, parcels.shape 
FROM brent.owners, brent.parcels, brent.prime 
WHERE prime.circuit = '1140' 
AND sde.ST_INTERSECTS(parcels.shape, sde.ST_BUFFER(prime.shape,25)) = true  
AND owners.apn = parcels.apn

