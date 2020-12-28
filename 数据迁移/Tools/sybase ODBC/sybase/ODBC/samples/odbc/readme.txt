March 2003
Sybase ASE Visual Basic/ADO coding samples for use with
Sybase ASE ODBC Driver and Sybase ASE OLE DB Provider

Introduction:

These files are Visual Basic projects that use the ADO API to
demonstrate some simple concepts in writing ADO code and applying
it to applications that connect to Sybase ASE, using the Sybase
ASE ODBC Driver or the Sybase ASE OLE DB Provider. These samples
all use the 12.5 version of the products.

This file contains the descriptions of the various samples.  In
future EBF releases there will be more samples to demonstrate
various functionality and concepts using ADO.

It is assumed that the programmer has knowledge of Visual Basic
programming, and the use of the ADO API.  These samples have been
compiled with Visual Basic 6.0, using MDAC 2.70.

In order to use these samples you must first run the SQL script,
tab_ado_sproc.  This script contains t-sql that will create a test
table and some stored procedures, used to demonstrate stored procedure
calling, and handling results sets and parameters.  After running this
script you should run the stored procedure “sp_ado_insert”. By default
this will insert 10 rows into the table “ado_table”.  You may add more
by executing the stored procedure with a value larger than 10 for its
parameter.  

All the samples include the VB project files and the forms. There are
comments in each project that explain what is happening. Also, sample
connection strings are included for both the ODBC driver and the
OLE DB Provider.

These samples might be helpful in troubleshooting problems. It is even
possible to use them to reproduce a problem and then provide it to
Sybase Technical Support to assist in resolving product bugs. They
may also assist in developing more complex applications.

Samples:

The following sections explain each sample.
The format of the sections are:

Concept:  <VB Project name>
<Directory Location >

So for the first sample:
Concept is “select”
VB Project Name is “adoSelect.vbp”. This is what you open when you
start VB. Directory Location is %SYBASE%\OCS-12_5\sample\odbc\adoSelect

Select: adoSelect.vbp 
odbc\adoSelect

Demonstrates a SELECT statememt on the table “ado_table”. This table
contains an integer datatype, character datatype, numeric datatype and
datetime datetype. The sample also demonstrates how to gather some
metadata information such as column name and datatype through the ADO
field object. The code displays the data from the select statement. The
idea is to become familiar with the handling of the ADO RecordSet object.
The comments explain each section.
 

Stored Procedures and Input/Output parameters: adoStoredProcedure.vbp
odbc\adoStoredProcedure

Demonstrates 5 different stored procedures. The primary goal is to
demonstrate how to build a parameter list and how to handle various
Sybase ASE datatypes. A brief explanation is provided for each
SubRoutine. Each Sub is self-contained in that it contains its own
connection string and error handling routines. The names below refer
to the VB Sub name. The full name for StoredProc, for example, would be
"cmdStoredProc_Click(). These Subs correlate to the "buttons" that you
press on the Form, to execute the RPC call:

StoredProc : 
Demonstrates how to send one INPUT parameter and the response contains
a result set (for the ADO Recordset).

Stored2parmProc:
Similar to StoredProc, but there are 2 more parameters.  The first
parameter is used to demonstrate how to handle the Return Status from
the RPC call. The other parameter demonstrates how to setup a Character
type of parameter. In this case Sybase ASE "char" was used, correlating
to ADO "adChar".

SpOutInt:
This Sub demonstrates how to handle Output parameters. In this case the
Output parameter is of type "int".  In the ADO code,  this demonstrates
how to use the direction of "adParamInputOutput" to handle the data value.

SpOutDate: 
Similar to SpOutInt, but this uses the Sybase ASE "datatime" datatype. Of
particular importance is how this can use various DateTime formats for the
input data value.

SpOutNum: 
Similar to SpOutInt, but this uses Sybase ASE Numeric(10,2). The
significant piece to notice is how to setup the Precision and Scale for
the parameter data value.

Result Set and Output Parameter:
adoRsetOutputParm.vbp odbc\adoRsetOutputParm

Demonstrates how to retrieve an output parameter when the stored
procedure returns a result set and an output parameter value. Uses
stored procedure “sp_ado_out_c3_c4” for the stored procedure example.
What is very important here is that the Sybase ASE ODBC Driver and the
Sybase ASE OLE DB Provider can only retrieve the output parameter
value AFTER closing the Recordset when using the DEFAULT CursorLocation
of adUseServer.  If you set CursorLocation to adUseClient, then you will
be able to retrieve the output parameter value immediately after execution.
If there is no result set returned by the stored procedure you will be
able to retrieve the output parameter value immediately after execution.
