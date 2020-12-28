VERSION 5.00
Begin VB.Form Form1 
   BackColor       =   &H00808000&
   Caption         =   "Form1"
   ClientHeight    =   5265
   ClientLeft      =   3330
   ClientTop       =   2160
   ClientWidth     =   10350
   LinkTopic       =   "Form1"
   ScaleHeight     =   5265
   ScaleWidth      =   10350
   Begin VB.CommandButton cmdTest 
      Caption         =   "select * from ado_table"
      Height          =   375
      Left            =   240
      TabIndex        =   7
      Top             =   2160
      Width           =   2055
   End
   Begin VB.TextBox passWordTextBox 
      Height          =   285
      IMEMode         =   3  'DISABLE
      Left            =   1320
      PasswordChar    =   "*"
      TabIndex        =   1
      Top             =   1560
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
      Height          =   2790
      ItemData        =   "select.frx":0000
      Left            =   2760
      List            =   "select.frx":0002
      TabIndex        =   5
      Top             =   720
      Width           =   6855
   End
   Begin VB.CommandButton cmdExit 
      Caption         =   "Exit"
      Height          =   375
      Left            =   480
      TabIndex        =   3
      Top             =   2880
      Width           =   1455
   End
   Begin VB.TextBox userNameTextBox 
      Height          =   285
      Left            =   1320
      TabIndex        =   0
      Text            =   "sa"
      Top             =   1080
      Width           =   1095
   End
   Begin VB.Label Label4 
      BackColor       =   &H00FFFF80&
      Caption         =   $"select.frx":0004
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   975
      Left            =   480
      TabIndex        =   9
      Top             =   4080
      Width           =   9135
   End
   Begin VB.Label SybSamps 
      BackColor       =   &H00FFFF80&
      Caption         =   "SybSamps - select_ado"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   13.5
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   735
      Left            =   120
      TabIndex        =   8
      Top             =   120
      Width           =   2295
   End
   Begin VB.Label Label2 
      Alignment       =   1  'Right Justify
      BackColor       =   &H00FFFF80&
      Caption         =   "PASSWORD:"
      Height          =   255
      Left            =   120
      TabIndex        =   6
      Top             =   1560
      Width           =   1095
   End
   Begin VB.Label Label3 
      BackColor       =   &H00FFFF80&
      Caption         =   "Output: Heading contains Columns names and ADO datatype"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   255
      Left            =   2520
      TabIndex        =   4
      Top             =   120
      Width           =   6975
   End
   Begin VB.Label Label1 
      Alignment       =   1  'Right Justify
      BackColor       =   &H00FFFF80&
      Caption         =   "USER ID:"
      Height          =   255
      Left            =   120
      TabIndex        =   2
      Top             =   1080
      Width           =   1095
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'SybSamps for ADO
'
Option Explicit
Private Sub cmdExit_Click()
On Error Resume Next
Unload Me
Set Form1 = Nothing
End Sub
Private Sub cmdTest_Click()

Dim sql As String       ' sql statement
Dim connStr As String   ' connection string
Dim lstr As String      ' String that contains record data
Dim fieldStr As String  ' field info string
Dim firstRow As Boolean ' true if on first Row - to be used to make field string
Dim tmpStr As String


Dim sybConn As ADODB.Connection 'ADO Connection object
Dim sybRst As ADODB.Recordset   'ADO Recordset object
Dim sybFld As ADODB.Field       'ADO Field object
Dim sybFld2 As ADODB.Field      'ADO Field Object to collect column info
Dim errLoop As ADODB.Error      'ADO Error object
Dim strError As String

On Error GoTo ErrTrap

Set sybConn = New ADODB.Connection
Set sybRst = New ADODB.Recordset

'Connection object information
sybConn.CursorLocation = adUseClient
sybConn.ConnectionTimeout = 10  'login timeout
'sybConn.CommandTimeout = 10    'query timeout

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'Sybase ASE ODBC Driver Connection string - uses DSN
sybConn.Open "DSN=ase4141;UID=sa;PWD=;", userNameTextBox.Text, passWordTextBox.Text

'Sybase ASE ODBC Driver Connection string - uses DSN-less method
' Attribute NA is NetworkAddress - hostname and port for the ASE server
'connStr = "DRIVER={Sybase ASE ODBC Driver};NA=pvero-pc,12500;DB=odbc;UID=sa;PWD=;"
'sybConn.Open connStr
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'Sybase ASE OLE DB Provider Connection string - uses Data Source
'sybConn.Open "Provider=Sybase.ASEOLEDBProvider.2;Data Source=ase125;Initial Catalog=odbc;User Id=sa;Password=;", userNameTextBox.Text, passWordTextBox.Text

'Sybase ASE OLE DB Provider Connection string that does not use Data Source
' Server Name is the ASE hostname
' Server Port Address is the ASE listening port
' Can use connStr = to the string below, then sybConn.Open connStr to make connection.
' This can be useful if you want to build some sort of pull down dialog box to select
' various connection strings.
'sybConn.Open "Provider=Sybase.ASEOLEDBProvider.2;Server Name=pvero-pc;Server Port Address=12500;Initial Catalog=odbc;User Id=sa;Password=;", userNameTextBox.Text, passWordTextBox.Text

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'Example of using the MSDASQL Provider to load the ODBC Driver...
'connStr = "Provider=MSDASQL;DRIVER={Sybase ASE ODBC Driver 4141};DB=odbc;UID=sa;PWD=;NetworkAddress=loki,1212;"
'sybConn.Open connStr

' Use this connection string for the DSN-less example below, just another way
' to build the connection.  Build the string, then setup various properties
' then use the Open method to make the connection.
'
'connStr = "DRIVER={Sybase ASE ODBC Driver 4128};DB=odbc;UID=sa;PWD=;ServerName=pvero-pc,12500;"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' USE FOR DSN-LESS CONNECTION
'With sybConn
'    .ConnectionString = connStr
'    .Provider = "MSDASQL"
' Valid Enums for the ADO Prompt property are:
' adPromptAlways = 1
' adPromptComplete = 2 - only if any values aren't complete...
' adPromptCompleteRequired = 3
' adPromptNever =4
'    .Properties("Prompt") = adPromptComplete
'    .Open connStr
'  End With
 ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'sybConn.Open connStr

' SQL Statement to send to ASE
sql = "select * from ado_table"

' This informs the Recordset object, sybRst to use Connection object sybConn.
' When the Recordset object is opened below, then the application uses sybConn
' to access the ASE database.
sybRst.ActiveConnection = sybConn

'If you want to limit records returned from ASE you can do it here with the
' MaxRecords Recordset property.
'sybRst.MaxRecords = 5

'This is where we open the Recordset object. Note that there are a variety of settings.
'Open recordset object: sql string (sql), connection object (sybConn), cursor type,
' lock type, option : in this case we send adCmdText
'sybRst.Open sql, sybConn, adOpenKeyset, adLockOptimistic, adCmdText
sybRst.Open sql, sybConn, adOpenStatic, adLockOptimistic, adCmdText
'sybRst.Open sql, sybConn, adOpenDynamic, adLockOptimistic, adCmdText
'sybRst.Open sql, sybConn, adOpenForwardOnly, adLockOptimistic, adCmdText

' Get Column Names - this is very crude and will not line up with the
' output below of the actual data, but it gives you an idea on how to gather this
' type of information
fieldStr = ""
List1.AddItem "=============================================="

For Each sybFld2 In sybRst.Fields
    fieldStr = fieldStr & sybFld2.Name & ", "           'column name
    fieldStr = fieldStr & sybFld2.Type & ",    "        'ADO datatype
    'fieldStr = fieldStr & sybFld2.Attributes & ","     'This returns the enumerated
                                                        'value of the Attributes
Next
fieldStr = Left(fieldStr, Len(fieldStr) - 1)
List1.AddItem fieldStr
List1.AddItem "=============================================="

' This loops over the sybRst object and will display the data values in each row
Do While Not sybRst.EOF
    lstr = ""
    For Each sybFld In sybRst.Fields
        lstr = lstr & sybFld.Value & ","
    Next
    lstr = Left(lstr, Len(lstr) - 1)
    List1.AddItem lstr
    sybRst.MoveNext
Loop
List1.AddItem "=============================================="


'Message Boxes are one way to get debug info.
'In this case we get the RecordCount from this select
MsgBox "RecordCount is " & sybRst.RecordCount
'Debug.Print will display the info in the Immediate Window down below
'Debug.Print "RecordCount is " & sybRst.RecordCount

'Housecleaning - close all ADO objects used
'field objects are destroyed when Recordset object is destroyed
sybRst.Close
sybConn.Close
Set sybRst = Nothing
Set sybConn = Nothing

Exit Sub

'Basic error handling when error is trapped
ErrTrap:
If Err.Number = 5 Then
    lstr = lstr & Err.Description & ","
    Resume Next
End If
'We get description of error, the ADO number and the Source
MsgBox "There has been an error" & vbCrLf & "  " & Err.Description & "  " & Err.Number & "  " & Err.Source
' Another method to collect error information
' Enumerate Errors collection and display
' properties of each Error object.
For Each errLoop In sybConn.Errors
      strError = "Error #" & errLoop.Number & vbCr & _
         "   " & errLoop.Description & vbCr & _
         "   (Source: " & errLoop.Source & ")" & vbCr & _
         "   (SQL State: " & errLoop.SQLState & ")" & vbCr & _
         "   (NativeError: " & errLoop.NativeError & ")" & vbCr
      'If errLoop.HelpFile = "" Then
      '   strError = strError & _
      '      "   No Help file available" & _
      '      vbCr & vbCr
      'Else
      '   strError = strError & _
      '      "   (HelpFile: " & errLoop.HelpFile & ")" & vbCr & _
      '      "   (HelpContext: " & errLoop.HelpContext & ")" & _
      '      vbCr & vbCr
      'End If
         

   Debug.Print strError
Next


End Sub

