USE DS2013

-- Get the code/value pairs for each coded value domain in the geodatabase.
SELECT
	ITEMS.Name AS "Name",
	codedValue.value('Code[1]', 'nvarchar(max)') AS "Code",
	codedValue.value('Name[1]', 'nvarchar(max)') AS "Value"
FROM
	GDB_ITEMS AS ITEMS INNER JOIN GDB_ITEMTYPES AS ITEMTYPES
	ON ITEMS.Type = ITEMTYPES.UUID
CROSS APPLY
	ITEMS.Definition.nodes('/GPCodedValueDomain2/CodedValues/CodedValue') AS CodedValues(codedValue)
WHERE
	ITEMTYPES.Name = 'Coded Value Domain'
