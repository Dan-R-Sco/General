USE DS2013

-- Join the Parcels feature class with the Employee coded value domain.
SELECT
	OBJECTID, PROPERTY_I, PARCEL_ID, ZONING_S--, Value 
FROM
	dbo.PARCELS LEFT OUTER JOIN
	(SELECT
		codedValue.value('Code[1]', 'nvarchar(max)') AS "Code",
		codedValue.value('Name[1]', 'nvarchar(max)') AS "Value"
	 FROM
		GDB_ITEMS AS ITEMS INNER JOIN GDB_ITEMTYPES AS ITEMTYPES
	 ON ITEMS.Type = ITEMTYPES.UUID
		CROSS APPLY
	 ITEMS.Definition.nodes('/GPCodedValueDomain2/CodedValues/CodedValue') AS CodedValues(codedValue)
	 WHERE
		ITEMTYPES.Name = 'Coded Value Domain' AND
		ITEMS.Name = 'ZoningCodes'
	) AS CodedValues
	ON parcels.ZONING_S = CodedValues.Code
