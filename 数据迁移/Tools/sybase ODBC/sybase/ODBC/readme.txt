
     readme.txt 

     Sybase ASE ODBC Driver, TDS Version
     Microsoft Windows 9x, NT, 2000, ME, XP
     Version 4.20.0067 (12.5.1/P-EBF11786 ESD #02/04.20.0067)
     March 2004

CONTENTS

Sybase ASE ODBC Driver, TDS Version
Problems Fixed
Installation Instructions
Driver Options
Notes and Known Problems
Installed Files
Technical Support



    Sybase ASE ODBC Driver, TDS Version

IMPORTANT:  You must have at least version 2.60 of the Microsoft Data 
Access Components (MDAC) installed to use the Sybase ASE ODBC Driver 4.20.0067.
The current version at the time of DataDirect Technologies's original release
of this driver was 2.7.  You can download a utility that determines the version
of your currently installed MDAC from the following Microsoft site:

http://www.microsoft.com/data  (Just follow the links for MDAC)

You can download the latest MDAC from the Microsoft site:

http://www.microsoft.com/data

This Driver is ODBC 3.51 compliant.  If you are using MDAC 2.10 and
MDAC 2.50, and encounter problems, please upgrade to the current 
MDAC level and test for resolution.  If problem persists please 
contact Sybase Technical Support.


IMPORTANT NOTE:

*********************************************************************
***  PLEASE NOTE - The following is a known issue, and has been   ***
***  addressed by the following Sybase ASE releases:              ***
***                                                               ***
***     Sybase ASE 12.0.0.7 IR (Interim Release)                  ***
***     Sybase ASE 12.5.0.3 IR (Interim Release)                  ***
***                                                               ***
***  Currently, multiple components in an MTS/DTC application     ***
***  (using OLE-DB or ODBC via the XA interface) cannot share     ***
***  the same 'lock space' on ASE. These applications may hang    ***
***  if they have multiple components or connections attempting   ***
***  to access the same data simultaneously; even within a        ***
***  single MTS/DTC transaction.                                  ***
***  This problem does NOT affect ASE on NT using the Native-OLE  ***
***  distributed transaction interface, nor will it affect        ***
***  components that access separate data and do not need to      ***
***  share locks.                                                 ***
***  This problem is caused by the way MTS/DTC generates XA       ***
***  transaction Ids and these issues are being addressed under   ***
***  CR 259265.                                                   ***
*********************************************************************



     Problems Fixed

---------------------------------------------------------
IMPORTANT NOTE for 12.5.1 SDK GA and 12.5 ESD#14 version:

EBF 11529 ESD #14 from the 12.5.0 SDK is the same build as the ODBC build
in the 12.5.1 SDK GA version.  You will see this below as both releases 
contain driver version 4.20.0015.
---------------------------------------------------------

Version 4.20.0067 (12.5.1/P-EBF11786 ESD #02/04.20.0067)
-------------------------------------------------------
346310: ODBC:  When executing a stored procedure with or without 
"EXEC" keyword, and application is using a query timeout (such 
as CommandTimeout in ADO application, or using QueryTimeout 
in ODBC API SQLSetStmtAttr call), when the timeout occurs, 
SQLExecDirect() returns SQL_SUCCESS.  The message and SQL_ERROR 
return code was retrieved during SQLFetch().  This has been corrected 
so that the execute returns SQL_ERROR on the SQLExecDirect() API call.

342554: ODBC: E_FAIL status with AddNew() and CursorLocation set 
to adUseClient in a Visual Basic ADO applciation.  This is resolved 
by using the WorkArounds2=16 connection attribute.  You can add this 
to the ADO connections string as "WA2=16".  Another alternative is 
to add the "WorkArounds2=16" for the DSN as found in the registry 
under ODBC.INI.  

343251: ODBC: No updates were allowed on disconnected ADO Recordset 
from a stored procedure call, after upgrading to the 4.20 driver build.  
Application would recieve the error "-2147217887 : Multiple-step 
operation generated errors. Check each status value." To prevent this 
from happening, a new connection option is required, 
ReportUnknownForUpdatable, which is False (0) by default.  When 
set to TRUE (1), this option will always return SQL_ATTR_READWRITE_UNKNOWN 
for the SQL_DESC_UPDATABLE field of the result column descriptors.  
This will only apply to stored procedure result sets.

341065: ODBC: TDS ODBC Driver doesn't connect to an Asymmetric Secondary ASE 
in a HA setup.

341137: ODBC: Set identity_insert tab ON causes SQL_ERROR on execution 
of stored procedure.  Now it returns SQL_SUCCESS_WITH_INFO.

347201: ODBC: ODBC does not receive all Extended Error Data messages 
from PRINT statements in a stored procedure.

344287: ODBC: Table import in Access 2000/2002/2003 hangs with 
Select Method=Direct.

338334: ODBC: Unable to display and input Traditional Chinese (Big5) 
characters correctly due to Big5 characters were incorrectly mapped 
into unicode when using datatype SQL_C_WCHAR. 
-------------------------------------------------------

Version 4.20.0035 (12.5.1/P-EBF11410 ESD #01/04.20.0035)
------------------------------------------------------
CR 337129: ODBC: ASE varchar was treated the same as char value 
when ODBC was connected to ASE via Open Server gateway such as 
Open Switch, and ASE was at version 12.0.  The varchar data was 
being padded so the data displayed was "full length" of the varchar 
column as defined on ASE.  The padding no longer occurs.

CR 338504: ODBC: The ASE install master script set incorrect values, that are 
not within the ODBC 3.X specification. To correct this problem now, you can 
modify the system tables as follows:

sp_configure 'allow updates to system tables', 1
go
update sybsystemprocs..spt_datatype_info set data_type=-9 
where type_name='univarchar'
go
update sybsystemprocs..spt_datatype_info set data_type=-8 
where type_name='unichar'
go
sp_configure 'allow updates to system tables', 0
go

CR 325693 is logged to track this issue and to investigate a permanent 
solution to the situation.

CR 317043: ODBC: SQLFreeStmt(SQL_CLOSE) does not deallocate the ASE cursor.

CR 330322: ODBC: MS Access -7776 error with import table on 1.2 GHz PC, 
due to a
datetime column.

Version 4.20.0015 (12.5.1/P/04.20.0015)
------------------------------------------------------

CR 317873: When using Interfaces File, the driver was not
updating the "LogonID" value in the registry, in the
HKEY_LOCAL_USER\Software\ODBC\ODBC.INI section, under the specified DSN.

CR 323627: A hang occurred when calling SQLCancel if SM=0
(SelectMethod = Cursor).

CR 326555: NetworkAddress was put into the ConnectStringOut when the
UseInterfacesFile check box was checked, and it should not have been.

DEF0000166  NA: When using not null in Create Table statement, data was
not returned correctly.

CR 324645: Crash occurred when executing a stored procedure
against an OpenServer.

CR 319004: By customer request, removed an existing error message
from the error messages the driver returns when attempting to connect 
with an invalid UID and/or Server information.

------------------------------------------------------

Version 4.20.0015 (12.5.0/P-EBF11529 ESD#14/04.20.0015)
-------------------------------------------------------
CR 317873: ODBC: When using Interfaces File, the driver was not updating 
the "LogonID" value in the registry, in the 
HKEY_LOCAL_USER\Software\ODBC\ODBC.INI section, under the specified DSN.

CR 319004: ODBC: Login failure messages return in different order and 
are truncated. Therefore, by customer request, removed an existing error 
message from the error messages the driver returns when attempting to 
connect with an invalid UID and/or Server information.

CR 323627: ODBC: ADO property (Commmand object) CommandTimeout was 
not working prior to this release.

CR 324645: ODBC: Applications may crash with corrupted memory when 
processing results from stored procedures that access remote OpenServer 
applications.
--------------------------------------------------------

Version 4.20.0010 (12.5.0/P-EBF11434 ESD#13/04.20.0010)
------------------------------------------------------
CR 323821:  ODBC: Running query in MS Access 2002 on Windows XP that loops over 
the execution and returns large result set can result in memory access error 
resulting in an application crash.
------------------------------------------------------

Version 4.20.0006 (12.5.0/P-EBF11210 ESD#12/04.20.0006)
------------------------------------------------------
CR 314726: ODBC: Output parameter not displayed when raiserror is involved 
in a stored procedure.

CR 291178: ODBC: Support for Password Encryption, as found in the Client 
Library based ODBC Drivers.

CR 301187: ODBC: Driver fails for SQLBindCol with SQL_C_NUMERIC for a 
particular number when it had 17 digits. However since the ODBC 
specification limits maximum digits of Numeric values to 16, any value 
greater than 16 will now fail with a numeric overflow error message.  
For exmaple, this query will fail: 
select convert(numeric(17,0), 10000000000000001) with error message: 
"Numeric overflow. Error in column 1."
-------------------------------------------------------

Version 4.10.0049 (12.5.0/P-EBF11113 ESD#11/04.10.0049)
-------------------------------------------------------
CR 303369: ODBC: Fractional truncation on NUMERIC datatypes when the data 
is involved in a stored procedure/insert.

CR 304589: ODBC: The host_id() ASE function was returning value in 
hexidecimal format, when in earlier releases of ODBC driver the data 
returned in decimal format.

CR 307251: ODBC: SQLExecDirect() returns SQL_ERROR on stored procedure call 
that sends message through a PRINT T-SQL statement. Now it returns 
SQL_SUCCESS_WITH_INFO.

CR 307874: ODBC: GPF when using Parameter set size.

CR 312953: ODBC: Numeric parameters preceded by char parameters would display 
as char datatypes when the metadata information for the parameters was 
not provided in an ADO application.  What happend was the ODBC Driver 
would call SQLProcedureColumns to gather datatype information, but was 
not indicating NUMERIC for the NUMERIC datatypes.  It would indicate 
their types as CHAR.

CR 314065: ODBC: Using the "execute" keyword to execute stored procedures 
in ADO or ODBC applications causes the CommandTimeout to fail.  Instead 
of timing out the driver will cause an infinite loop based on the timeout 
value.
-------------------------------------------------------

Version 4.10.0041 (12.5.0/P-EBF10969/04.10.0041)
------------------------------------------------
CR 300563: ODBC: Unable to connect to ASE using interfaces file through MS
Excel application.

CR 288181: ODBC: Connection behavior using MS Access with attribute DRIVER
fails to link table MS Access can not handle DSN-less connections.
Work around is to use DNS connections.
------------------------------------------------

Version 4.10.0040 (12.5.0/P-EBF10929/04.10.0040)
------------------------------------------------
CR 292372: ODBC: client connection cannot fail over when ASE HA is on NT

CR 296436: ODBC: Stored procedure with a raiserror returned a warning
(SQL_SUCCESS_WITH_INFO) instead of SQL_ERROR on execute.

CR 295709: ODBC: Unable to get a message returned from a raiserror that was
inside a trigger.

CR 295867: ODBC:  LDAP feature does not unbind the url session. When request
is made to retrieve the SybaseAddress the connection from ODBC driver to
ldap server remains OPEN until the odbc application terminates. The session
now UNBINDs immediately after request to provide information has occurred.

CR 297342: ODBC: Error 2601, "Attempt to insert duplicate key row in object
'tableName' with unique index 'indexName'", was a warning with the
ctlib-based driver and was returned as an error with the TDS-based driver.

CR 298282: ODBC: Stored procedures did not return empty result sets.

CR 299893: ODBC: Stored procedures executed as language commands returned
errors as separate result sets instead of in the same result set. For example,
if using the proc_role() function in a stored procedure, and if you pass an
invalid role as a parameter, you received one message about the invalid role.
You did not receive the other message indicating that you do not have the right
role.
------------------------------------------------

Version 4.10.0028 (12.5.0/P-EBF10719/04.10.0028)
------------------------------------------------
CR 293132: On connecting to an Open Server application the ODBC Driver 
would cause "Catastrophic Failure" in an ADO application.  It was discovered 
the failure occurred on the API call, SQLGetInfo, when retrieving the value 
for the SQL_DATABASE_NAME attribute.  This problem is now resolved, but it 
is REQUIRED to include the database name in the connection string.  This 
is required when using Open Server applications such as Sybase OpenSwitch 
only when the Open Server application is connecting to Sybase ASE. 
 
CR 295539: Default parameters are not supported by the ODBC Driver since 
ASE does not provide this information in the Catalog Stored Proceudures. 
Instead, if you try to use default parameters you will receive this error 
message: "Default parameters are not supported by this database."

CR 295783: Odbc driver would close the network socket after TDS_LOGOUT, 
without waiting for the TDS_DONE acknowledgement from the ASE. This could 
potentially cause "1608" network errors to appear in the Sybase ASE error 
log. This has been resolved.

CR 296725: The ODBC driver now supports using the Sybase OCS SQL.INI 
interfaces file for ASE server name resolution, providing a lookup for 
hostname and port number for connectivity.  To utilize this feature just 
bypass adding the Network Address in the DSN configuration. Go to the 
section in the General Tab titled "Use Interface File for Connection 
Information (Optional)".  Enter the full path and filename of the SQL.INI 
interfaces file for the field labeled "Interfaces File", like 
"C:\SYBASE\INI\SQL.INI". Enter the ASE Server name as found in the SQL.INI 
file in the field for "Server Name".  When you attempt to connect, the 
ODBC Driver will get the Hostname and Port number for the ASE Server, 
and use that information to make the connection. When using a connection 
string you can use the attributes "InterfacesFile" and 
"InterfacesFileServerName" in place of "NetworkAddress".  
------------------------------------------------------------------------

Version 4.10.0020 (12.5.0/P-EBF10572/04.10.0020)
-----------------------------------------------
CR 292810: Using DAO and sending "sp_addlogin" resulted in error 3146.

CR 288132: With MS Access 2000 users this error sometimes appeared when 
building a query: "Invalid precision value.  Error in parameter 1." This 
problem no longer occurs.  You need to set WorkArounds2=32768.

CR 269659: With "Set nocount on", empty result sets from stored procedures 
were not returning column info.
------------------------------------------------------------------------

Version 4.10.0010 (12.5.0/P-EBF10515/04.10.0010)
-----------------------------------------------
CR 259957: Raiserror messages were not displaying from stored procedure calls.
In some cases SQL_ERROR was not returning on the API call executing the stored
procedure.

CR 266325: When calling stored procedures in an ADO application that used both
adParamReturnValue (for Return Status) and adParamOutput (for Output parameters)
type of parameters, the OUTPUT parameter value(s) did not display in the 
application.

CR 273206: In an ADO application, when updating records, using a CursorLocation
set to adUseClient, the following errors would occur when using the indicated
MDAC version:
MDAC 2.6: "Insufficient base table information for updating or refreshing."
MDAC 2.7: "Data Provider or other service returned an E_FAIL status."
To resolve the problem you must use "WorkArounds2=24" in the ODBC connection
string.

CR 273652: In an RDO application a hang would occur when handling a result set
with more than 99 rows upon the second time of execution.

CR 276224: The ODBC driver would allow an "Application Name" of more than 30
characters, which contradicted the TDS specification (maximum application name
is 30 chars).  This would have undesireable effects such as ASE stack traces
or crashes. Now the ODBC driver will truncate an Application Name that contains
more than 30 characters to a length of 30 characters.

CR 278603: Application hang or GPF on API calls SQLProcedureColumns or 
SQLExecDirect when the ASE was no longer accessible from the client.  Now 
client receives a message about the terminated connection.

CR 287731: A table with a Primary Key consisting of varchar, int, datetime 
and including 2 additional fields of text, datetime will fail when opened in 
MS Access after linking to the table.  When opened data references display 
#DELETED instead of the actual data in the table.

CR 287840: With 4.10.0000 (EBF 9970) ODBC Driver, showplan results were 
returned as SQL_ERROR instead of SQL_SUCCESS_WITH_INFO.  Also the order 
of the message text was incorrect.
------------------------------------------------------------------------

Version 4.10.0000 (12.5.0/P-EBF9970/04.10.0000)
-----------------------------------------------
Sybase ASE ODBC Driver fully supports LDAP and SSL features.
For more information, please read driver's help file.
------------------------------------------------------------------------

Version 4.00.0003 (12.5.0/P-EBF9923/04.00.0003)
-----------------------------------------------
Sybase ASE ODBC Driver fully support HA Failover feature.

CR 261284: With Chinese characters, an error occurred with WHERE 
clause : "Unclosed quote before the character string 
'%<2 chinese characters>'.  This has been resolved.
------------------------------------------------------------------------

Version 4.00.0001 (12.5.0/P-EBF9720/04.00.0001)
-----------------------------------------------
CR 257623: In some instances SQLDescribeCol() API call fails with 
"Prepared statement not a cursor-specification".  This problem has been 
resolved.

CR 257070: Microsoft Access 2000 users would receive (-7748) error when 
importing/linking tables that had at least one unique, non-clustered index.
Problem was with SQLStatistics API call, in the MS Access implementation 
(sp_statistics), which is now resolved by entering "WorkArounds2 = 8192" 
in ODBC DSN connection string.  This was not a Bug in the ODBC Driver.
------------------------------------------------------------------------

Version 3.70.0020 (12.5.0/P/03.70.0020)
---------------------------------------
CR 235380: Client did not process attention acknowledgement from ASE
when client was executing an RPC event.

CR 234993: TDS_LOGOUT packet was sent incorrectly.

CR 234802: Unable to change default packet size. Error message was :
[MERANT][ODBC Sybase ASE driver]Network Error: 9; Read from the netowrk 
socket failed.  Now changing to legal values works.  Currently DataDirect 
Technologies is fixing case where this parameter is set to (-1) and (0).

CR 215347: File DSN works independently of User and System Data Sources.
------------------------------------------------------------------------


     Installation Instructions



     Driver Options

Sybase has included non-standard options for the drivers that
enable you to take full advantage of packaged ODBC-enabled applications
requiring non-standard or extended behavior.

To use these options, we recommend that you create a separate data
source for each application.  Using the registry editor (REGEDIT on
Windows 9x and Windows NT 4.0, and REGEDT32 on Windows NT 3.5x), open the
ODBC.INI section in the registry.  In the section for the data source
you created, add the string value WorkArounds (or WorkArounds2) with a
value of n (for example, WorkArounds=n).  The value n is the cumulative value
of all options added together.

Note that each of these options has potential side effects related to
its use.  An option should only be used to address the specific problem for
which it was designed.  For example, WorkArounds=2 causes the driver to report
that database qualifiers are not supported, even when they are.  As a result,
applications that use qualifiers may not perform properly when this option is
enabled.

WorkArounds=1.  If an ODBC driver reports that its
SQL_CURSOR_COMMIT_BEHAVIOR or SQL_CURSOR_ROLLBACK_BEHAVIOR is 0, then
return 1 instead and force statements to be prepared again by the
driver.

WorkArounds=2.  Some applications cannot handle database qualifiers.
If this option is on, the driver reports that qualifiers are not
supported.

WorkArounds=4.  Some applications require two connections to
a database system.  Since some database systems support only one
connection, the second connection attempt fails.  Turning this option
on causes our drivers to detect this condition and have the two ODBC
connections share a single physical connection to the database system.

WorkArounds=8.  If an ODBC driver cannot deduce the number of rows
affected by an INSERT, UPDATE, or DELETE, it may return -1 in
SQLRowCount.  Some products cannot handle this.  Turning this option on
causes the driver to return 1 instead.

WorkArounds=16.  For SQLStatistics, if an ODBC driver reports
an INDEX_QUALIFIER that contains a period, some applications raise a
"tablename is not a valid name" error.  Turning this option on causes
the driver to return no INDEX_QUALIFIER.

WorkArounds=32.  Turning this option on enables users of flat-file
drivers to abort a long-running query by pressing the ESC key.

WorkArounds=64.  This option results in a column name of C<position>
where <position> is the ordinal position in the result set.  For
example, "SELECT col1, col2+col3 FROM table1" produces the column names
"col1" and C2.  SQLColAttributes/SQL_COLUMN_NAME returns <empty string>
for result columns that are expressions.  Use this option for
applications that cannot handle <empty string> column names.

WorkArounds=256.  Forces SQLGetInfo/SQL_ACTIVE_CONNECTIONS to be
returned as 1.

WorkArounds=513.  To prevent ROWID results, this option forces the
SQLSpecialColumns function to return a unique index as returned from
SQLStatistics.

WorkArounds=2048.  Microsoft Access performs more efficiently when
the output connection string of SQLDriverConnect returns DATABASE=
instead of DB= for some data sources. This option forces DATABASE= to
be returned.

WorkArounds=65536.  This option strips trailing zeros from decimal
results, which prevents Microsoft Access from issuing an error when
decimal columns containing trailing zeros are included in the unique
index.

WorkArounds=131072.  This option turns all occurrences of the double
quote character ("") into the grave character (`). Some applications
always quote identifiers with double quotes. Double quoting causes
problems for data sources that do not return
SQLGetInfo/SQL_IDENTIFIER_QUOTE_CHAR = <double quote>.

WorkArounds=524288.  The Microsoft Foundation Classes (MFC) bind all
SQL_DECIMAL parameters with a fixed precision and scale, which causes
truncation errors.  Set this option to force the maximum
precision/scalesettings.

WorkArounds=1048576.  Some applications incorrectly specify a precision
of 0 for character types when the value will be SQL_NULL_DATA.  This
option overrides the specified precision and sets the precision to 256.

WorkArounds=2097152.  Some applications incorrectly specify a precision
of -1 for character types.  This option overrides the specified
precision and sets the precision to 2000.

WorkArounds=4194304.  For PowerBuilder users, this option converts all
catalog function arguments to upper case unless they are quoted.

WorkArounds=536870912.  This option allows for re-binding parameters
after calling SQLExecute for prepared statements.

WorkArounds=1073741824.  Microsoft Access assumes that ORDER BY columns
do not have to be in the SELECT list.  This workaround addresses that
mistaken assumption for data sources such as Informix and OpenIngres.

WorkArounds2=2.  Some applications incorrectly specify the
ColumnSize/DecimalDigits when binding timestamp parameters.  This
workaround causes the driver to ignore the ColumnSize/DecimalDigits specified by
the application and use the database defaults instead.

WorkArounds2=4.  Microsoft Access uses the most recent native type
mapping, as returned by SQLGetTypeInfo, for a given SQL type.  This workaround
reverses the order in which types are returned, so that Access will use the most
appropriate native type.

WorkArounds2=8.  This workaround causes base to add the bindoffset in
the ARD to the pointers returned by SQLParamData.  This is to work around a
MSDASQL problem.

WorkArounds2=16.  This workaround causes the drivers to ignore calls to
SQLFreeStmt(RESET_PARAMS) and only return success without taking other
action. It also causes parameter validation not to use the bind offset when
validating the charoctetlength buffer. This is to work around a MSDASQL problem.

WorkArounds2=24.  If you are using a Connect ODBC flat file driver,
such as dBase, under MSDASQL, you must use this workaround for the driver to
operate properly.

WorkArounds2=32.  Microsoft Access requires "DSN" to be included in a
connection string. This workaround appends "DSN=" to a connection string, if it
is not already included.

WorkArounds2=128.  Some applications will open extra connections if
SQLGetInfo(SQL_ACTIVE_STATEMENTS) does not return 0. This workaround
causes SQLGetInfo(SQL_ACTIVE_STATEMENTS) to return 0 to avoid the overhead of
these extra connections.

WorkArounds2=256. Workaround for MSDASQL. Causes the drivers to return 
Buffer Size for Long Data on calls to SQLGetData with a buffer size of 
0 on columns whose SQL type is SQL_LONGVARCHAR or SQL_LONGVARBINARY. 
Applications should always set this workaround when using MSDASQL and 
retrieving long data.

WorkArounds2=512. Workaround for Microsoft Query 2000. Causes the 
flat-file drivers to return old literal prefixes and suffixes for 
date, time, and timestamp data types. Query 2000 does not correctly 
handle the ODBC escapes that are currently returned as literal prefix 
and literal suffix.

WorkArounds2=1024. Workaround for ADO. ADO incorrectly interprets the 
SQLGetInfo(SQL_MULT_RESULT_SETS) to mean that the last result set 
returned from a stored procedure is the output parameters for the 
stored procedure. Setting this workaround causes the driver to return 
"N" for this SQLGetInfo call.

WorkArounds2=2048. Workaround for the ODBC cursor library. ODBC 3.x 
applications which use the ODBC cursor library will get errors on 
bindings for SQL_DATE, SQL_TIME, and SQL_TIMESTAMP columns. The cursor 
library incorrectly rebinds these columns with the ODBC 2.x type 
defines. The workaround causes the Connect ODBC drivers to accept 
these 2.x SQL types as valid.

WorkArounds2=4096. The ODBC Driver Manager incorrectly translates 
lengths of empty strings when a Unicode-enabled application uses a 
non-Unicode driver. This workaround causes the Connect ODBC drivers 
to internally adjust the length of empty strings. Use this workaround 
only if your application is Unicode enabled.

WorkArounds2=8192. Workaround for Microsoft Access 2000 when it calls 
SQLStatisticsW and SQLGetData for column number 10. Microsoft Access 
only asks for the data as a two-byte SQL_C_WCHAR, which is insufficient 
buffer to store the UCS2 character and the null terminator. Thus, 
the driver returns a warning, "01004 Data truncated", and returns a 
null character to Microsoft Access. Microsoft Access then passes 
error -7748. Setting this workaround causes Microsoft Access to not 
pass the error -7748.

Microsoft Access and Visual Basic Users
---------------------------------------
We recommend that users of Microsoft Access and Visual Basic
add the value pair WorkArounds=25 (1+8+16) for each data source they
use with Access and Visual Basic.  For data sources that support a
single connection, add the line WorkArounds=29 (1+4+8+16).


     Notes and Known Problems
Problem with unichar and univarchar datatypes with SQLGetTypeInfo
-----------------------------------------------------------------
In the system tables that contain metadata information for the Sybase ASE, there are 
incorrect data_type fields for the two ASE 12.5 datatypes, unichar and univarchar, 
in the table, spt_datatype_info.  This table stores values that are returned from the 
ODBC API call, SQLGetTypeInfo.  This metadata contains a listing of data types supported 
by the ASE.  The information provides a mapping to the data type name and the SQL type 
name used by the Sybase ASE ODBC Driver, for applications that require this information.

The SQL type names that correspond to unichar and univarchar are as follows, along with 
their proper data_type field value and currently existing field value:

SQL_WCHAR corresponds to unichar, and is defined as (-8). Currently it is set to 1.
SQL_WVARHCAR corresponds to univarchar, and is defined as (-9).  Currently it is set to 35.

The ASE install master script set incorrect values, that are not within the ODBC 3.X specification.
To correct this problem now, you can modify the system tables as follows:

sp_configure 'allow updates to system tables', 1
go
update sybsystemprocs..spt_datatype_info set data_type=-9 where type_name='univarchar'
go
update sybsystemprocs..spt_datatype_info set data_type=-8 where type_name='unichar'
go
sp_configure 'allow updates to system tables', 0
go

CR 325693 is logged to track this issue and to investigate a permanent solution to the situation.


ODBC Driver Manager
-------------------
Sybase ASE ODBC Drivers 12.5 require the 3.51 version of the ODBC Driver
Manager (ODBC32.DLL and ODBCCP32.DLL). Because the ODBC 3.51 Driver
Manager is compatible with 2.x compliant drivers, all 2.x versions of the Driver
Manager should be removed from your access path to ensure application stability.
Failing to remove older versions of the Driver Manager may
result in application errors and abnormal terminations.

SQLColAttribute(s)
------------------
The column attributes 1001 and 1002, which were assigned as Sybase
specific attributes, were inadvertently used as system attributes by
the Microsoft 3.0 ODBC implementation. Applications using those
attributes should now use 1901 and 1902 respectively.

SQL_C_NUMERIC
-------------
Because of inconsistencies in the ODBC specification, users attempting
to use SQL_C_NUMERIC parameters should set the precision and scale
values of the corresponding structure and the descriptor fields in the
APD.

Static Cursors with Long Columns
--------------------------------
When ODBC Application uses Static Cursors the default buffer length for 
long columns (text and image) is 4K.  This parameter is not configurable 
in the ODBC Administrator.  To change the value you need to do the following:
In the WindowsNT ( or Windows 9X ) registry go to the DSN folder , in 
HKEY_LOCAL_MACHINE\Software\ODBC\ODBC.INI for System DSNs, or in 
HKEY_CURRENT_USER\Software\ODBC\ODBC.INI for User DSNs and enter this 
attribute: "StaticCursorLongColBuffLen" and set the value in bytes.

Stored Procedures and Cursors
-----------------------------
A problem is encountered when using multiple stored procedures on multiple 
hstatements (HSTMTs) in cursor mode of the driver (SelectMethod=0). Sybase
doesn't allow stored procs to be executed on cursors unless there is a single 
statement in the procedure. ODBC doesn't have a way to detect the number of 
statements in the stored proc, therefore it cannot support this scenario and 
returns the error message:
"[MERANT][ODBC Sybase driver] Sybase does not allow more than one active 
statement when retrieving results without a cursor." 
The reason for this is because the ODBC Driver switches SelectMethod=1, or 
Direct mode.  When in Direct Mode only 1 active HSTMT is allowed per ODBC
connection.  In order to make this scenario work,  set the DSN to SelectMethod=1
and the ODBC driver will be able to handle this.


Catalog Stored Procedures (CSPs)
--------------------------------
You may experience a problem using catalog stored procedures when running the
driver with Sybase Adaptive Server 11.5 or 11.9.2.  Contact Sybase Technical
Support for information about fixes.  Included with currently released ODBC
Products is a file named "sycsp11.sql".  This script should be installed on
your ASE 11.X.  The ASE 12.X includes these changes, so it is not necessary to
install the scripts.  To install the scripts:

     isql -Usa -P<password> -S<ASE_Server_Name> -isycsp11.sql

*** NOTE *** Do not run the SYCSP11.SQL script on ASE 12.5.  Only install on 
ASE 12.0 as directed by Technical Support.  The current release of ASE 12.0
EBF has the updated CSPs.  Use the CSPs from the EBF install master script. 
If problems are still encountered contact Sybase Technical Support. For ASE 
12.5 please use the most current install master script from the 12.5.X release.

Statements containing COMPUTE BY clause
---------------------------------------
The Sybase driver supports statements containing COMPUTE BY clauses. The
results of the COMPUTE BY clause are handled as a separate result set. Use
SQLMoreResults to process the additional result set.

Using Sybase SQL.INI Interfaces file for connectivity
-----------------------------------------------------
Starting with EBF 10719, 4.10.0028, the ODBC driver now supports using the Sybase OCS SQL.INI interfaces 
file for ASE server name resolution, providing a lookup for hostname and port number for connectivity.
To utilize this feature just bypass adding the Network Address in the DSN configuration. Go
to the section in the General Tab titled "Use Interface File for Connection Information (Optional)".
Enter the full path and filename of the SQL.INI interfaces file for the field labeled "Interfaces File",
like "C:\SYBASE\INI\SQL.INI". Enter the ASE Server name as found in the SQL.INI file in the field 
for "Server Name".  When you attempt to connect, the ODBC Driver will get the Hostname and Port number 
for the ASE Server, and use that information to make the connection.

     Installed Files

The following files are included in the EBF zip file:

ODBC DLLs and other files:

readme.txt       This file.
syodase.dll      Sybase ASE ODBC Driver
syodaser.dll     Sybase ASE ODBC Driver Resource DLL
syodases.dll     Sybase ASE ODBC Driver Setup DLL
syodbas.dll      Sybase ASE ODBC Driver Base DLL
syodbasr.dll     Sybase ASE ODBC Driver BASE Resource DLL
syodutl.dll      Sybase ASE ODBC Driver Utility DLL
syodutlr.dll     Sybase ASE ODBC Driver Utility Resource DLL
syodbc.lic       Sybase ASE ODBC Driver License file
syodldap.dll     Sybase ASE ODBC Driver LDAP DLL
syodssl.dll      Sybase ASE ODBC Driver SSL DLL
syodicu.dll	 Sybase ASE ODBC Driver International Components for Unicode
/samples	 Sample programs
/help		 Help files in html format


****  Windows 2000 Users  ****

*** IMPORTANT!!!!!!!! ****
If you are using Windows 2000 DO NOT INSTALL MDAC 2.1 or 2.5 since
Windows 2000 already includes MDAC 2.6.  This product is certified for
use on Windows 2000.

For information on the files that are installed when you install the
MDAC runtime components, please see the following Microsoft
web site:

http://www.microsoft.com/data/MDAC21info/manifest_intro.htm

For current updates to the MDAC modules, please see the following Microsoft
web site:

http://www.microsoft.com/data

     Technical Support
-----------------------

Please report problems to Sybase Technical Support
(1-800-8SYBASE or 1-800-879-2273) or via your
conventional method (ie. web)


