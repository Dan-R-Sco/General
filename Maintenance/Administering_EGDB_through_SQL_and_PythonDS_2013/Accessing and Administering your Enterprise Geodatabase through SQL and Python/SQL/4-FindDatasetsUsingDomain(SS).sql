USE DS2013

DECLARE @DOMAIN NVARCHAR(MAX);
SET @DOMAIN = 'Employee';

SELECT
	ClassItems.Name AS 'Feature Class Name'
FROM

-- Find the "DomainInDataset" relationships.
(SELECT
	Relationships.OriginID AS ClassID,
	Relationships.DestID AS DomainID
 FROM
	GDB_ITEMRELATIONSHIPS AS Relationships
	INNER JOIN
	GDB_ITEMRELATIONSHIPTYPES AS RelationshipTypes
	ON Relationships.Type = RelationshipTypes.UUID
 WHERE RelationshipTypes.Name = 'DomainInDataset') AS DomainRelationships

-- Resolve the Domain UUID values.
INNER JOIN
GDB_ITEMS AS DomainItems
ON DomainRelationships.DomainID = DomainItems.UUID

-- Resolve the Class UUID values.
INNER JOIN
GDB_ITEMS AS ClassItems
ON DomainRelationships.ClassID = ClassItems.UUID

-- Filter the results so that only the specified domain is returned.
WHERE DomainItems.Name = @DOMAIN
