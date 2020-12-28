VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   5925
   ClientLeft      =   3330
   ClientTop       =   2160
   ClientWidth     =   10350
   LinkTopic       =   "Form1"
   ScaleHeight     =   5925
   ScaleWidth      =   10350
   Begin VB.CommandButton cmdStoredProc 
      Caption         =   "sp_ado_c3_c4"
      Height          =   375
      Left            =   120
      TabIndex        =   11
      Top             =   1080
      Width           =   2055
   End
   Begin VB.CommandButton cmdStored2parmProc 
      Caption         =   "sp_ado_2parm"
      Height          =   375
      Left            =   120
      TabIndex        =   10
      Top             =   1800
      Width           =   2055
   End
   Begin VB.CommandButton cmdSpOutNum 
      Caption         =   "sp_ado_outnum_c3_c4"
      Height          =   375
      Left            =   120
      TabIndex        =   9
      Top             =   3960
      Width           =   2055
   End
   Begin VB.CommandButton cmdSpOutDate 
      Caption         =   "sp_ado_outdate_c3_c4"
      Height          =   375
      Left            =   120
      TabIndex        =   8
      Top             =   3240
      Width           =   2055
   End
   Begin VB.CommandButton cmdSpOutInt 
      Caption         =   "sp_ado_out_c3_c4"
      Height          =   375
      Left            =   120
      TabIndex        =   7
      Top             =   2520
      Width           =   2055
   End
   Begin VB.TextBox passWordTextBox 
      Height          =   285
      IMEMode         =   3  'DISABLE
      Left            =   1320
      PasswordChar    =   "*"
      TabIndex        =   1
      Top             =   480
      Width           =   1095
   End
   Begin VB.ListBox List1 
      BeginProperty DataFormat 
         Type            =   0
         Format          =   "0"
         HaveTrueFalseNull=   0
         FirstDayOfWeek  =   0
         FirstWeekOfYear =   0
         LCID            =   1033
         SubFormatType   =   0
      EndProperty
      Height          =   4935
      ItemData        =   "adoStoredProc.frx":0000
      Left            =   2520
      List            =   "adoStoredProc.frx":0002
      TabIndex        =   5
      Top             =   480
      Width           =   7695
   End
   Begin VB.CommandButton cmdExit 
      Caption         =   "Exit"
      Height          =   375
      Left            =   120
      TabIndex        =   3
      Top             =   5040
      Width           =   1455
   End
   Begin VB.TextBox userNameTextBox 
      Height          =   285
      Left            =   1320
      TabIndex        =   0
      Text            =   "sa"
      Top             =   90
      Width           =   1095
   End
   Begin VB.Label Label2 
      Alignment       =   1  'Right Justify
      Caption         =   "PWD:"
      Height          =   255
      Left            =   0
      TabIndex        =   6
      Top             =   480
      Width           =   1215
   End
   Begin VB.Label Label3 
      Caption         =   "Output:"
      Height          =   255
      Left            =   3120
      TabIndex        =   4
      Top             =   120
      Width           =   1095
   End
   Begin VB.Label Label1 
      Alignment       =   1  'Right Justify
      Caption         =   "ID:"
      Height          =   255
      Left            =   120
      TabIndex        =   2
      Top             =   120
      Width           =   1095
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Option Explicit
Private Sub cmdExit_Click()
On Error Resume Next
Unload Me
Set Form1 = Nothing
End Sub
' Demostrates calling a simple stored procedure.
' This stored procedure does a select c3, c4 on ado_table.
' It returns the row(s) that match the criteria of the input parameter sent
' to the ASE on the stored procedure execution
Private Sub cmdStoredProc_Click()

Dim sql As String
Dim lstr As String
Dim sybConnection As ADODB.Connection


Dim sybCommand As ADODB.Command     'ADO Command object - holds Parameter object
Dim sybParameter As ADODB.Parameter 'ADO Parameter object
Dim parmVal As String               'To hold parameter value in case we are doing something with it

Dim errLoop As ADODB.Error      'ADO Error object
Dim strError As String

Dim sybRecordset As ADODB.Recordset
Dim sybField As ADODB.Field

On Error GoTo ErrTrap

Set sybConnection = New ADODB.Connection
Set sybCommand = New ADODB.Command
Set sybParameter = sybCommand.CreateParameter

'sybConnection.ConnectionTimeout = 0
'sybConnection.Open "Provider=Sybase ASE OLE DB Provider;Data Source=oledb", userNameTextBox.Text, passWordTextBox.Text
sybConnection.Open "DSN=ase4149;UID=sa;PWD=;", userNameTextBox.Text, passWordTextBox.Text

' sql holds our stored procedure name
sql = "sp_ado_c3_c4"

' I use this place to make ADO Command object property settings
' and to associate this Command object to the ADO Connection object
sybCommand.CommandTimeout = 10
sybCommand.ActiveConnection = sybConnection
sybCommand.CommandType = adCmdStoredProc
sybCommand.CommandText = sql

' setup for the parameter
sybParameter.Name = "@inp"          ' Only useful here, on the client.  No named parameters are sent in TDS
sybParameter.Type = adInteger       ' Set the Type to the ADO data type as defined in the
' ado specification. Supported datatypes for Sybase are listed in the ADO reference
' guide at the www.datadirect-technologies.com webpage, however these are listed as
' oledb datatypes.  You need to corelate these to ADO types.

sybParameter.Direction = adParamInput ' designates the direction of the parameter

sybCommand.Parameters.Append sybParameter   ' associates this parameter with the Command object
sybCommand.Parameters(0).Value = 1          ' Set the value through the Command object

Set sybParameter = Nothing      ' We no longer need the parameter object so we clean
' it out now.

' This sample sproc returns a result set, so we use the ADO Recordset to
' hold the results.  This is why we do the "Set sybRecordset = " on the Execute
'sybCommand.Execute
Set sybRecordset = sybCommand.Execute()

' Since we have a result set we process this information
Do While Not sybRecordset.EOF
    lstr = ""
     For Each sybField In sybRecordset.Fields
        lstr = lstr & sybField.Value & ", "
    Next
    lstr = Left(lstr, Len(lstr) - 1)
    List1.AddItem lstr
    sybRecordset.MoveNext
Loop

' Cleanup the objects, close the connection
sybRecordset.Close
sybConnection.Close
Set sybRecordset = Nothing
Set sybCommand = Nothing
Set sybConnection = Nothing
Exit Sub

ErrTrap:
If Err.Number = 5 Then
    lstr = lstr & Err.Description & ","
    Resume Next
End If

For Each errLoop In sybConnection.Errors
      strError = "Error #" & errLoop.Number & vbCr & _
         "   " & errLoop.Description & vbCr & _
         "   (Source: " & errLoop.Source & ")" & vbCr & _
         "   (SQL State: " & errLoop.SQLState & ")" & vbCr & _
         "   (NativeError: " & errLoop.NativeError & ")" & vbCr
      Debug.Print strError
Next
MsgBox "There has been an error" & vbCrLf & Err.Description
End Sub

' This is similar to the previous code, but we add one more Input parameter.
' Also, this handles the return status, as an output parameter, sent back from the
' ASE.  This code demonstrates how to prepare the parameters and how to handle the
' result set and the return status value.

Private Sub cmdStored2parmProc_Click()

Dim sql As String
Dim lstr As String
Dim sybConnection As ADODB.Connection
Dim sybCommand As ADODB.Command
Dim sybParameter As ADODB.Parameter
'Dim sybParameter2 As ADODB.Parameter

Dim errLoop As ADODB.Error      'ADO Error object
Dim strError As String

Dim sybRecordset As ADODB.Recordset
Dim sybField As ADODB.Field

On Error GoTo ErrTrap

Set sybConnection = New ADODB.Connection
Set sybCommand = New ADODB.Command

'sybConnection.ConnectionTimeout = 0
'sybConnection.Open "Provider=Sybase ASE OLE DB Provider;Data Source=ase12_test;Initial Catalog=odbc;User Id=sa;Password=;", userNameTextBox.Text, passWordTextBox.Text
sybConnection.Open "DSN=ase4147;UID=sa;PWD=;", userNameTextBox.Text, passWordTextBox.Text

sql = "sp_ado_2parm"
' The following format is optional. ADO will do this for us when we specify the
' parameters that we are using.
'sql = "{? = call sp_ado_2parm(?, ?)}"

sybCommand.CommandTimeout = 10
sybCommand.ActiveConnection = sybConnection
sybCommand.CommandType = adCmdStoredProc
sybCommand.CommandText = sql

' set parameter object for Return Status
Set sybParameter = sybCommand.CreateParameter
sybParameter.Name = "RETURNVALUE"
sybParameter.Type = adInteger
' By setting this direction to adParamReturnValue, the connection will send the
' stored procedure in the correct format to handle this value. Prior to execution
' there is a Debug.Print that displays the command text. You will find it is in the format
' { ? = call sprocName(?, ?, ...) }
sybParameter.Direction = adParamReturnValue
sybCommand.Parameters.Append sybParameter

' It should not be necessary to set this value for the return status since it is treated
' as an output parameter.
'sybCommand.Parameters(0).Value = 99

' clear out sybParameter
Set sybParameter = Nothing

' setup parm object for next parameter
' There is another format for CreateParameter
' Set sybParameter = sybCommand.CreateParameter("@inp", adInteger, adParamInput, , 3)
' The args are parameter name, parameter datatype, direction, size and value.
' For adInteger the size is 4 bytes, and is not necessary to specify.
Set sybParameter = sybCommand.CreateParameter
' setup for the @inp parameter
sybParameter.Name = "@inp"
sybParameter.Type = adInteger
sybParameter.Direction = adParamInput

sybCommand.Parameters.Append sybParameter
' Be very careful when setting values in the Parameter array.
' If the ordinal is incorrect you will get errors, like invalid datatype
' errors and the command will not be sent to ASE. The Command object contains this array
' through its Parameters collection...
' sybCommand -> Parameters : parm[0], parm[1], parm[2]....
sybCommand.Parameters(1).Value = 3

' clear out sybParameter
Set sybParameter = Nothing
' setup for the next parameter
Set sybParameter = sybCommand.CreateParameter

' setup for the @inp2 parameter
sybParameter.Name = "@inp2"
sybParameter.Type = adChar
sybParameter.Direction = adParamInput
sybParameter.Size = 20

sybCommand.Parameters.Append sybParameter
sybCommand.Parameters(2).Value = "xyz"

' Use some debugs to track these items.
Debug.Print ("Return Value before sybRecordset exec : " & sybCommand.Parameters(0).Value)
Debug.Print ("Command Text : " & sybCommand.CommandText)
Set sybRecordset = sybCommand.Execute()

' Using simple logic to process the rows.
Do While Not sybRecordset.EOF
    lstr = ""
    For Each sybField In sybRecordset.Fields
        lstr = lstr & sybField.Value & ", "
    Next
    lstr = Left(lstr, Len(lstr) - 1)
    List1.AddItem lstr
    sybRecordset.MoveNext
Loop

' On the Sybase products we can only get the Return Status , an output parameter, after
' closing the Recordset, when using the default ADO CursorLocation of adUseServer.
' Look at the sample, adoRsetOutputParm, for more details on this behavior.
sybRecordset.Close

Debug.Print ("Return Value after sybRecordset close : " & sybCommand.Parameters(0).Value)

sybConnection.Close

Set sybParameter = Nothing
Set sybRecordset = Nothing
Set sybCommand = Nothing
Set sybConnection = Nothing
Exit Sub

ErrTrap:
If Err.Number = 5 Then
    lstr = lstr & Err.Description & ","
    Resume Next
End If

For Each errLoop In sybConnection.Errors
      strError = "Error #" & errLoop.Number & vbCr & _
         "   " & errLoop.Description & vbCr & _
         "   (Source: " & errLoop.Source & ")" & vbCr & _
         "   (SQL State: " & errLoop.SQLState & ")" & vbCr & _
         "   (NativeError: " & errLoop.NativeError & ")" & vbCr
      Debug.Print strError
Next
MsgBox "There has been an error" & vbCrLf & Err.Description
End Sub

' This will demonstrate the use of a parameter to provide INPUT to the stored procedure.
' Also, the same parameter will be used to pass back an Output value

Private Sub cmdSpOutInt_Click()

Dim sql As String
Dim lstr As String
Dim sybConnection As ADODB.Connection
Dim sybCommand As ADODB.Command
Dim sybParameter As ADODB.Parameter

Dim errLoop As ADODB.Error      'ADO Error object
Dim strError As String

Dim sybRecordset As ADODB.Recordset
Dim sybField As ADODB.Field

On Error GoTo ErrTrap

Set sybConnection = New ADODB.Connection
Set sybCommand = New ADODB.Command
Set sybParameter = sybCommand.CreateParameter

'sybConnection.ConnectionTimeout = 0
'sybConnection.Open "Provider=Sybase ASE OLE DB Provider;Data Source=ase12_test;Initial Catalog=odbc;User Id=sa;Password=;", userNameTextBox.Text, passWordTextBox.Text
sybConnection.Open "DSN=ase4147;UID=sa;PWD=;", userNameTextBox.Text, passWordTextBox.Text

sql = "sp_ado_out_c3_c4"

sybCommand.CommandTimeout = 10
sybCommand.ActiveConnection = sybConnection
sybCommand.CommandType = adCmdStoredProc
sybCommand.CommandText = sql

' setup for the parameter
sybParameter.Name = "@out"
sybParameter.Type = adInteger
' This will indicate that we are passing a value up to the ASE
' to be used in the stored procedure. Also, this parameter will be used
' to pass a value back to this application after the execution.
sybParameter.Direction = adParamInputOutput

sybCommand.Parameters.Append sybParameter
sybCommand.Parameters(0).Value = 5

Set sybRecordset = sybCommand.Execute()

Do While Not sybRecordset.EOF
    lstr = ""
    For Each sybField In sybRecordset.Fields
        lstr = lstr & sybField.Value & ", "
    Next
    lstr = Left(lstr, Len(lstr) - 1)
    List1.AddItem lstr
    sybRecordset.MoveNext
Loop

' Must Close recordset before retreiving the output parameter
sybRecordset.Close

' Retreive output parm value
Debug.Print ("Output parameter value : " & sybCommand.Parameters(0).Value)

sybConnection.Close

Set sybParameter = Nothing
Set sybRecordset = Nothing
Set sybCommand = Nothing
Set sybConnection = Nothing
Exit Sub

ErrTrap:
If Err.Number = 5 Then
    lstr = lstr & Err.Description & ","
    Resume Next
End If

For Each errLoop In sybConnection.Errors
      strError = "Error #" & errLoop.Number & vbCr & _
         "   " & errLoop.Description & vbCr & _
         "   (Source: " & errLoop.Source & ")" & vbCr & _
         "   (SQL State: " & errLoop.SQLState & ")" & vbCr & _
         "   (NativeError: " & errLoop.NativeError & ")" & vbCr
      Debug.Print strError
Next
MsgBox "There has been an error" & vbCrLf & Err.Description
End Sub

' Demonstrates passing datetime value as an input parameter and
' uses it also as an Output parameter. Returns row data as well.

Private Sub cmdSpOutDate_Click()
Dim sql As String
Dim lstr As String
Dim sybConnection As ADODB.Connection
Dim sybCommand As ADODB.Command
Dim sybParameter As ADODB.Parameter

Dim errLoop As ADODB.Error      'ADO Error object
Dim strError As String

Dim sybRecordset As ADODB.Recordset
Dim sybField As ADODB.Field

On Error GoTo ErrTrap

Set sybConnection = New ADODB.Connection
Set sybCommand = New ADODB.Command
Set sybParameter = sybCommand.CreateParameter

'sybConnection.ConnectionTimeout = 0
'sybConnection.Open "Provider=Sybase ASE OLE DB Provider;Data Source=ase125;Initial Catalog=odbc;User Id=sa;Password=;", userNameTextBox.Text, passWordTextBox.Text
sybConnection.Open "DSN=ase4147;UID=sa;PWD=;", userNameTextBox.Text, passWordTextBox.Text

sql = "sp_ado_outdate_c3_c4"

sybCommand.CommandTimeout = 10
sybCommand.ActiveConnection = sybConnection
sybCommand.CommandType = adCmdStoredProc
sybCommand.CommandText = sql

' setup for the parameter
sybParameter.Name = "@out"
sybParameter.Type = adDBTimeStamp
sybParameter.Precision = 26
'sybParameter.Size = 26
sybParameter.Direction = adParamInputOutput
'sybParameter.Direction = adParamOutput

sybCommand.Parameters.Append sybParameter
'sybCommand.Parameters(0).Value = Null
' These formats should work for the input value
sybCommand.Parameters(0).Value = "3/31/2003 3:16:00 PM"
'sybCommand.Parameters(0).Value = "Mar 31 2003 3:16 PM"
'sybCommand.Parameters(0).Value = "3/31/03 3:16:00 PM"
'sybCommand.Parameters(0).Value = "Mar 31 2003 15:16"
Set sybRecordset = sybCommand.Execute()

Do While Not sybRecordset.EOF
    lstr = ""
    For Each sybField In sybRecordset.Fields
        lstr = lstr & sybField.Value & ", "
    Next
    lstr = Left(lstr, Len(lstr) - 1)
    List1.AddItem lstr
    sybRecordset.MoveNext
Loop
''''''''''''''''''''''''''''''''''''''''''''

sybRecordset.Close

'ret output
'List1.AddItem (sybCommand.Parameters(0).Value)

Debug.Print "parm = " & sybCommand.Parameters(0).Value

sybConnection.Close

Set sybParameter = Nothing
Set sybRecordset = Nothing
Set sybCommand = Nothing
Set sybConnection = Nothing
Exit Sub

ErrTrap:
If Err.Number = 5 Then
    lstr = lstr & Err.Description & ","
    Resume Next
End If

For Each errLoop In sybConnection.Errors
      strError = "Error #" & errLoop.Number & vbCr & _
         "   " & errLoop.Description & vbCr & _
         "   (Source: " & errLoop.Source & ")" & vbCr & _
         "   (SQL State: " & errLoop.SQLState & ")" & vbCr & _
         "   (NativeError: " & errLoop.NativeError & ")" & vbCr
      Debug.Print strError
Next
MsgBox "There has been an error" & vbCrLf & Err.Description
End Sub

Private Sub cmdSpOutNum_Click()
Dim sql As String
Dim lstr As String
Dim sybConnection As ADODB.Connection
Dim sybCommand As ADODB.Command
Dim sybParameter As ADODB.Parameter

Dim errLoop As ADODB.Error      'ADO Error object
Dim strError As String

Dim sybRecordset As ADODB.Recordset
Dim sybField As ADODB.Field

On Error GoTo ErrTrap

Set sybConnection = New ADODB.Connection
Set sybCommand = New ADODB.Command
Set sybParameter = sybCommand.CreateParameter

'sybConnection.ConnectionTimeout = 0
'sybConnection.Open "Provider=Sybase ASE OLE DB Provider;Data Source=ase125;Initial Catalog=odbc;User Id=sa;Password=;", userNameTextBox.Text, passWordTextBox.Text
sybConnection.Open "DSN=ase4147;UID=sa;PWD=;", userNameTextBox.Text, passWordTextBox.Text

' has row result set, then output parm
sql = "sp_ado_outnum_c3_c4"

sybCommand.CommandTimeout = 10
sybCommand.ActiveConnection = sybConnection
sybCommand.CommandType = adCmdStoredProc
sybCommand.CommandText = sql

' setup for the parameter
sybParameter.Name = "@out"
sybParameter.Type = adNumeric
' setup the Precision and Scale
sybParameter.Precision = 10
sybParameter.NumericScale = 2
sybParameter.Direction = adParamInputOutput

sybCommand.Parameters.Append sybParameter
'sybCommand.Parameters(0).Value = Null
sybCommand.Parameters(0).Value = 11111.11
'sybCommand.Parameters(0).Value = 0
'arithmetic overflow
'sybCommand.Parameters(0).Value = 999999999.99

Set sybRecordset = sybCommand.Execute()

Do While Not sybRecordset.EOF
    lstr = ""
    For Each sybField In sybRecordset.Fields
        lstr = lstr & sybField.Value & ", "
    Next
    lstr = Left(lstr, Len(lstr) - 1)
    List1.AddItem lstr
    sybRecordset.MoveNext
Loop


sybRecordset.Close

'ret output
List1.AddItem (sybCommand.Parameters(0).Value)

sybConnection.Close

Set sybParameter = Nothing
Set sybRecordset = Nothing
Set sybCommand = Nothing
Set sybConnection = Nothing
Exit Sub

ErrTrap:
If Err.Number = 5 Then
    lstr = lstr & Err.Description & ","
    Resume Next
End If

For Each errLoop In sybConnection.Errors
      strError = "Error #" & errLoop.Number & vbCr & _
         "   " & errLoop.Description & vbCr & _
         "   (Source: " & errLoop.Source & ")" & vbCr & _
         "   (SQL State: " & errLoop.SQLState & ")" & vbCr & _
         "   (NativeError: " & errLoop.NativeError & ")" & vbCr
      Debug.Print strError
Next
MsgBox "There has been an error" & vbCrLf & Err.Description
End Sub




