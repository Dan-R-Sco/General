USE DS2013
DECLARE @CONTAINER NVARCHAR(MAX);
DECLARE @CONTAINER_TYPE NVARCHAR(MAX);
SET @CONTAINER = 'DS2013.dbo.Landbase';
SET @CONTAINER_TYPE = 'Feature Dataset';

-- Find all contained datasets.
SELECT
	DEST_ITEMS.Name AS "Name",
	DEST_TYPES.Name AS "Type"
FROM
	-- Gets the unique ID of the container...
	((((SELECT UUID, Type FROM dbo.GDB_ITEMS WHERE Name = @CONTAINER) AS SRC_ITEMS
	INNER JOIN
	(SELECT UUID FROM GDB_ITEMTYPES WHERE Name = @CONTAINER_TYPE) AS SRC_TYPES
	ON SRC_ITEMS.Type = SRC_TYPES.UUID)
	
	-- Gets the UUIDs of datasets with relationships to the container...
	INNER JOIN
	GDB_ITEMRELATIONSHIPS AS RELATIONSHIPS
	ON SRC_ITEMS.UUID = RELATIONSHIPS.OriginID)
	
	-- Resolve the names of the destination datasets...
	INNER JOIN
	GDB_ITEMS AS DEST_ITEMS
	ON RELATIONSHIPS.DestID = DEST_ITEMS.UUID)
	
	-- And get the datasets' types as human-readable strings...
	INNER JOIN
	GDB_ITEMTYPES AS DEST_TYPES
	ON DEST_ITEMS.Type = DEST_TYPES.UUID
