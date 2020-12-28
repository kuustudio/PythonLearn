VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   4890
   ClientLeft      =   3330
   ClientTop       =   2160
   ClientWidth     =   8070
   LinkTopic       =   "Form1"
   ScaleHeight     =   4890
   ScaleWidth      =   8070
   Begin VB.CommandButton cmdSPOutInt 
      Caption         =   "Execute stored procedure"
      Height          =   615
      Left            =   120
      TabIndex        =   7
      Top             =   960
      Width           =   2175
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
      Height          =   4155
      Left            =   2520
      TabIndex        =   5
      Top             =   480
      Width           =   5295
   End
   Begin VB.CommandButton cmdExit 
      Caption         =   "Exit"
      Height          =   375
      Left            =   120
      TabIndex        =   3
      Top             =   1800
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

' adoRsetOutputParm will demonstrate how to process a stored procedure
' that contains a ROW result set and an Output parameter

Private Sub cmdSPOutInt_Click()
Dim sql As String
Dim lstr As String

' for connection and command object
' command object also handles parameters for the execution
Dim sybConnection As ADODB.Connection
Dim sybCommand As ADODB.Command
Dim sybParameter As ADODB.Parameter

' Recordset and Field object handle the Records (rows)
' and fields (columns)
Dim sybRecordset As ADODB.Recordset
Dim sybField As ADODB.Field

On Error GoTo ErrTrap

Set sybConnection = New ADODB.Connection
Set sybCommand = New ADODB.Command
Set sybParameter = sybCommand.CreateParameter

' You could use Client Side cursors, which are provided by ODBC Driver, OLE DB
' Provider, or the MDAC itself in order to retrieve the output parameter before
' closing the Recordset.  By default the Sybase Connection will use Server Side cursor,
' which is either provided by the ASE itself using cursor mode or it will be
' handled by the client driver/provider.  In this case you must close the Recordset
' prior to retrieving the output parameter(s).  If you do not, then the output parameter
' vlaue will be whatever it was initialized as in this client application.
'sybConnection.CursorLocation = adUseClient

' Use this for ODBC connections
sybConnection.Open "DSN=ase4149;UID=sa;PWD=;", userNameTextBox.Text, passWordTextBox.Text

' Use this for OLE DB Connections
'sybConnection.Open "Provider=Sybase ASE OLE DB Provider; Data Source=ase125;User Id=sa;Password=;", userNameTextBox.Text, passWordTextBox.Text

sql = "sp_ado_out_c3_c4"

sybCommand.CommandTimeout = 10
sybCommand.ActiveConnection = sybConnection
sybCommand.CommandType = adCmdStoredProc
sybCommand.CommandText = sql

' setup for the parameter
sybParameter.Name = "@out"
sybParameter.Type = adInteger
' In this particular stored procedure the parameter @out is used as input parameter
' fisybRecordset, in order to provide a criteria for the SELECT statement, and then it is used
' as an output parameter for the return parameter value.  When you do this you must
' set the ADODB.Parameter object Direct to adParamInputOutput.  This is to ensure
' that the value will be sent up to the ASE.  If this is not done, that is you set
' Direction to adParamOutput, then a NULL value will be sent to the ASE.
sybParameter.Direction = adParamInputOutput

sybCommand.Parameters.Append sybParameter
sybCommand.Parameters(0).Value = 3
Set sybRecordset = sybCommand.Execute()

List1.AddItem "================================================="
List1.AddItem "Processing records (ROWs) in the Recordset Object"
List1.AddItem "================================================="

' This is here just so you can demonstrate what happens when you retrieve the Output
' parameter before processing the Recordset.  If you do this here you MUST use
' CursorLocation of adUseClient, or you will not be able to retrieve the value of the
' Output parameter as returned from the ASE.
'MsgBox "Output parameter before closing Recordset : " & sybCommand.Parameters(0).Value

' Processing loop for the Recordset
Do While Not sybRecordset.EOF
    lstr = ""
    For Each sybField In sybRecordset.Fields
        lstr = lstr & sybField.Value & ", "
    Next
    lstr = Left(lstr, Len(lstr) - 1)
    List1.AddItem lstr
    sybRecordset.MoveNext
Loop

' Must Close recordset before retreiving the output parameter.  This is how
' the ASE OLEDB Provider handles this.  BUT, if you use Client side cursors for
' the CursorLocation you can retrieve the parameter prior to closing the Recordset.
'MsgBox "Output parameter before closing Recordset : " & sybCommand.Parameters(0).Value

sybRecordset.Close

' Retreive output parm value
' Debug.Print will display values in the Immediate window.
' Use this for debugging purposes
'Debug.Print sybCommand.Parameters(0).Value
List1.AddItem "======================================="
List1.AddItem "Output parameter value : " & sybCommand.Parameters(0).Value
List1.AddItem "======================================="

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
MsgBox "There has been an error" & vbCrLf & Err.Description
End Sub

