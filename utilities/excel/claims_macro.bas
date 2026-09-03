Attribute VB_Name = "Module11"

Sub FormatValveClaims()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets(1)
    
    ws.Name = "SyteLine Data"
    
    
    ' Insert Report Due Date column
    Range("I:I").Insert
    Range("I1").Select
    ActiveCell.FormulaR1C1 = "Report Due Date"
    
    ' Insert Report Due Date column
    Range("D:D").Insert
    Range("D1").Select
    ActiveCell.FormulaR1C1 = "Valve Group"
    
    ' Insert Days Since Assigned column
    Range("Q1").Select
    ActiveCell.FormulaR1C1 = "Days Since Assigned"
    
    ' Insert Days Since Assigned column
    Range("R1").Select
    ActiveCell.FormulaR1C1 = "Days Since Approved"

    ' Insert Days Since Assigned column
    Range("S1").Select
    ActiveCell.FormulaR1C1 = "Days Since Quote Sent"

    Dim columnsToKeep As Variant
    columnsToKeep = Array("Evaluation Group", "CCR#", "User Name", "Valve Group", "Name", "Item", "Evaluation Status", "Create Date", "Assigned Date", "Report Due Date", "Approval Date", "Quote Send Date", "Quote Due Date", "Customer Response", "Evaluator's Comments ( Internal  Only)", "Description", "Days Since Assigned", "Days Since Approved", "Days Since Quote Sent")

    Dim lastCol As Long
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column

    Dim colIndex As Long
    For colIndex = lastCol To 1 Step -1
        Dim header As String
        header = ws.Cells(1, colIndex).Value

        Dim keep As Boolean
        keep = False

        Dim i As Long
        For i = LBound(columnsToKeep) To UBound(columnsToKeep)
            If header = columnsToKeep(i) Then
                keep = True
                Exit For
            End If
        Next i

        If Not keep Then
            ws.Columns(colIndex).Delete
        End If
    Next colIndex

    ' Reorder columns
    Dim targetCol As Long
    targetCol = 1
    For i = LBound(columnsToKeep) To UBound(columnsToKeep)
        For colIndex = targetCol To ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
            If ws.Cells(1, colIndex).Value = columnsToKeep(i) Then
                If colIndex <> targetCol Then
                    ws.Columns(colIndex).Cut
                    ws.Columns(targetCol).Insert Shift:=xlToRight
                End If
                Exit For
            End If
        Next colIndex
        targetCol = targetCol + 1
    Next i

    ' Create table
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    Dim tblRange As Range
    Set tblRange = ws.Range(ws.Cells(1, 1), ws.Cells(lastRow, UBound(columnsToKeep) + 1))

    Dim lo As ListObject
    Set lo = ws.ListObjects.Add(xlSrcRange, tblRange, , xlYes)
    lo.Name = "Valve_Claims"
    lo.TableStyle = "TableStyleLight9"

    ' Column indexes
    Dim evalCol As Long, assignCol As Long, approvalCol As Long, quoteDueCol As Long, reportDueDate As Long, quoteSendCol As Long
    evalCol = 0: assignCol = 0: approvalCol = 0: quoteDueCol = 0: reportDueDate = 0: quoteSendCol = 0
    For colIndex = 1 To UBound(columnsToKeep) + 1
        Select Case ws.Cells(1, colIndex).Value
            Case "Evaluation Group"
                ws.Columns(colIndex).ColumnWidth = 18
            Case "CCR#"
                ws.Columns(colIndex).ColumnWidth = 10
            Case "User Name"
                ws.Columns(colIndex).ColumnWidth = 13
            Case "Valve Group"
                ws.Columns(colIndex).ColumnWidth = 15
            Case "Name"
                ws.Columns(colIndex).ColumnWidth = 40
            Case "Item"
                ws.Columns(colIndex).ColumnWidth = 30
            Case "Evaluation Status"
                evalCol = colIndex
                ws.Columns(colIndex).ColumnWidth = 30
            Case "Create Date"
                ws.Columns(colIndex).ColumnWidth = 13
            Case "Assigned Date"
                assignCol = colIndex
                ws.Columns(colIndex).ColumnWidth = 16
            Case "Approval Date"
                approvalCol = colIndex
                ws.Columns(colIndex).ColumnWidth = 16
            Case "Quote Due Date"
                quoteDueCol = colIndex
                ws.Columns(colIndex).ColumnWidth = 17
            Case "Report Due Date"
                reportDueDate = colIndex
                ws.Columns(colIndex).ColumnWidth = 18
            Case "Quote Send Date"
                quoteSendCol = colIndex
                ws.Columns(colIndex).ColumnWidth = 18
            Case "Customer Response"
                ws.Columns(colIndex).ColumnWidth = 21
            Case "Evaluator's Comments ( Internal  Only)"
                ws.Columns(colIndex).ColumnWidth = 50
            Case "Description"
                ws.Columns(colIndex).ColumnWidth = 50
            Case "Days Since Assigned"
                ws.Columns(colIndex).ColumnWidth = 22
            Case "Days Since Approved"
                ws.Columns(colIndex).ColumnWidth = 22
            Case "Days Since Quote Sent"
                ws.Columns(colIndex).ColumnWidth = 22
        End Select
    Next colIndex
    
    ' Adding report due dates and red if overdue
    Dim rowIndex As Long
    For rowIndex = 2 To lastRow
        If IsDate(ws.Cells(rowIndex, assignCol).Value) Then
            ' Add 7 days to Assigned Date and write to Report Due Date
            ws.Cells(rowIndex, reportDueDate).Value = ws.Cells(rowIndex, assignCol).Value + 7

            ' Highlight if Report Due Date is overdue
            If ws.Cells(rowIndex, reportDueDate).Value <= Date Then
                If ws.Cells(rowIndex, evalCol).Value = "Assigned for Evaluation" Or ws.Cells(rowIndex, evalCol).Value = "Received" Then
                    ws.Cells(rowIndex, reportDueDate).Interior.Color = RGB(255, 0, 0)
                End If
            End If
        End If
    Next rowIndex

    

    ' Conditional formatting
    For rowIndex = 2 To lastRow
        If evalCol > 0 And approvalCol > 0 Then
            If ws.Cells(rowIndex, evalCol).Value = "Pending Repair" Then
                If IsDate(ws.Cells(rowIndex, approvalCol).Value) Then
                    If ws.Cells(rowIndex, approvalCol).Value <= Date - 7 Then
                        ws.Cells(rowIndex, approvalCol).Interior.Color = RGB(255, 0, 0)
                    End If
                End If
            End If
        End If

        If evalCol > 0 And quoteDueCol > 0 Then
            If ws.Cells(rowIndex, evalCol).Value = "Pending Quote Approval" Then
                If IsDate(ws.Cells(rowIndex, quoteDueCol).Value) Then
                    If ws.Cells(rowIndex, quoteDueCol).Value < Date Then
                        ws.Cells(rowIndex, quoteDueCol).Interior.Color = RGB(255, 0, 0)
                    End If
                End If
            End If
        End If
    Next rowIndex


    ' Add new headers dynamically'
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column

    ' Apply formulas using column names
    For rowIndex = 2 To lastRow
        ws.Cells(rowIndex, lastCol - 2).Formula = "=IF(ISBLANK(" & ws.Cells(rowIndex, assignCol).Address(False, False) & "),0,NETWORKDAYS(" & ws.Cells(rowIndex, assignCol).Address(False, False) & ",TODAY()))"
        ws.Cells(rowIndex, lastCol - 1).Formula = "=IF(ISBLANK(" & ws.Cells(rowIndex, approvalCol).Address(False, False) & "),0,NETWORKDAYS(" & ws.Cells(rowIndex, approvalCol).Address(False, False) & ",TODAY()))"
        ws.Cells(rowIndex, lastCol).Formula = "=IF(ISBLANK(" & ws.Cells(rowIndex, quoteSendCol).Address(False, False) & "),0,NETWORKDAYS(" & ws.Cells(rowIndex, quoteSendCol).Address(False, False) & ",TODAY()))"
    Next rowIndex


    ' Set row height for all rows
    ws.Cells.RowHeight = 15

    Range("A1").Select
    
        

    Dim emailWB As Workbook, emailWS As Worksheet
    Dim mainWS As Worksheet
    Dim emailFilePath As String
    Dim lastRowEmail As Long, lastRowMain As Long
    Dim userColMain As Long, valveColMain As Long
    Dim userColEmail As Long, valveColEmail As Long
    Dim r As Long
    Dim valveGroupDict As Object

    ' Path to SharePoint file
    emailFilePath = "https://1smc.sharepoint.com/sites/US-Team-UTC-ValveClaim/Shared%20Documents/Claim%20follow%20up/email.xlsx"

    ' Open email.xlsx
    Set emailWB = Workbooks.Open(emailFilePath)
    Set emailWS = emailWB.Sheets(1)

    ' Build dictionary: User Name -> Valve Group
    Set valveGroupDict = CreateObject("Scripting.Dictionary")

    ' Find last row in email.xlsx
    lastRowEmail = emailWS.Cells(emailWS.Rows.Count, 1).End(xlUp).Row

    ' Identify columns in email.xlsx
    userColEmail = 1 ' Assuming User Name is column A
    valveColEmail = 4 ' Assuming Valve Group is column D

    For i = 2 To lastRowEmail ' Skip header
        If Not IsEmpty(emailWS.Cells(i, userColEmail).Value) Then
            valveGroupDict(Trim(emailWS.Cells(i, userColEmail).Value)) = emailWS.Cells(i, valveColEmail).Value
        End If
    Next i

    ' Work on main sheet
    Set mainWS = ThisWorkbook.Sheets("Syteline Data")
    lastRowMain = mainWS.Cells(mainWS.Rows.Count, 1).End(xlUp).Row

    ' Identify columns in main sheet
    userColMain = 3 ' Column C for User Name
    valveColMain = 4 ' Column D for Valve Group

    ' Populate Valve Group
    For r = 2 To lastRowMain
        Dim userName As String
        userName = Trim(mainWS.Cells(r, userColMain).Value)
        If valveGroupDict.Exists(userName) Then
            mainWS.Cells(r, valveColMain).Value = valveGroupDict(userName)
        Else
            mainWS.Cells(r, valveColMain).Value = "" ' Leave blank if no match
        End If
    Next r

    ' Close email.xlsx
    emailWB.Close SaveChanges:=False
    
    Dim ptSheet As Worksheet
    Dim dataRange As Range
    Dim pCache As PivotCache
    Dim pt As PivotTable
    
    ' Set worksheet and data range
    Set dataRange = ws.Range("A:S") ' Adjust range as needed

    ' Add a new sheet for the Evaluator Count
    Set ptSheet = ThisWorkbook.Sheets.Add
    ptSheet.Name = "Evaluator Count"

    ' Create Pivot Cache
    Set pCache = ThisWorkbook.PivotCaches.Create( _
        SourceType:=xlDatabase, _
        SourceData:=dataRange)

    ' Create Pivot Table
    Set pt = pCache.CreatePivotTable( _
        TableDestination:=ptSheet.Range("A3"), _
        TableName:="UserItemPivot")

    ' Configure Pivot Table fields
    With pt
        .PivotFields("Evaluation Status").Orientation = xlColumnField
        .PivotFields("User Name").Orientation = xlRowField
        .AddDataField .PivotFields("Item"), "Valve Claims", xlCount
        .PivotFields("Valve Group").Orientation = xlPageField ' Adds Valve Group as a filter
        
        .ShowTableStyleRowStripes = True
        .ShowTableStyleColumnStripes = True
        .TableStyle2 = "PivotStyleMedium9" ' This style includes blue banding

    End With

    Range("A1").Select
    
    Dim sheetOrder As Variant

    ' Define your custom order here
    sheetOrder = Array("Syteline Data", "Evaluator Count")

    For i = LBound(sheetOrder) To UBound(sheetOrder)
        On Error Resume Next ' Skip if sheet name doesn't exist
        Set ws = Worksheets(sheetOrder(i))
        If Not ws Is Nothing Then
            ws.Move After:=Sheets(Sheets.Count)
            ws.Move Before:=Sheets(i + 1)
        End If
        Set ws = Nothing
        On Error GoTo 0
    Next i
    
    Sheets("Syteline Data").Select


    '====================================================
    ' Create Pending Quote Approval worksheet
    '====================================================

    Dim pendingWS As Worksheet
    Dim statusCol As Long
    Dim lastRowPending As Long
    Dim lastColPending As Long

    ' Delete sheet if it already exists
    On Error Resume Next
    Application.DisplayAlerts = False
    Worksheets("Pending Quote Appr").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0

    ' Copy the main data sheet
    Sheets("Syteline Data").Copy After:=Sheets(Sheets.Count)
    Set pendingWS = ActiveSheet
    pendingWS.Name = "Pending Quote Appr"
    
    ' =============================================
    
    ' Find Evaluation Status column
    statusCol = 0
    For colIndex = 1 To pendingWS.Cells(1, pendingWS.Columns.Count).End(xlToLeft).Column
        If pendingWS.Cells(1, colIndex).Value = "Evaluation Status" Then
            statusCol = colIndex
            Exit For
        End If
    Next colIndex

    If statusCol > 0 Then

        lastRowPending = pendingWS.Cells(pendingWS.Rows.Count, 1).End(xlUp).Row
        lastColPending = pendingWS.Cells(1, pendingWS.Columns.Count).End(xlToLeft).Column

        ' Apply filter
        pendingWS.Range(pendingWS.Cells(1, 1), _
                        pendingWS.Cells(lastRowPending, lastColPending)).AutoFilter _
                        Field:=statusCol, _
                        Criteria1:="Pending Quote Approval"

    End If
    
    ' =============================================
    
    ' Highlight Customer Response cells that contain a value
    Dim customerResponseCol As Long
    customerResponseCol = 0

    ' Find Customer Response column
    For colIndex = 1 To pendingWS.Cells(1, pendingWS.Columns.Count).End(xlToLeft).Column
        If pendingWS.Cells(1, colIndex).Value = "Customer Response" Then
            customerResponseCol = colIndex
            Exit For
        End If
    Next colIndex

    ' Highlight populated Customer Response cells
    If customerResponseCol > 0 Then
        For rowIndex = 2 To lastRowPending
            If Trim(pendingWS.Cells(rowIndex, customerResponseCol).Value & "") <> "" Then
                pendingWS.Cells(rowIndex, customerResponseCol).Interior.Color = RGB(198, 239, 206) ' Light green
            End If
        Next rowIndex
    End If


    '====================================================
    ' Create Pending Repair worksheet
    '====================================================

    Dim repairWS As Worksheet
    Dim repairStatusCol As Long
    Dim lastRowRepair As Long
    Dim lastColRepair As Long

    ' Delete sheet if it already exists
    On Error Resume Next
    Application.DisplayAlerts = False
    Worksheets("Pending Repair").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0

    ' Copy the main data sheet
    Sheets("Syteline Data").Copy After:=Sheets(Sheets.Count)
    Set repairWS = ActiveSheet
    repairWS.Name = "Pending Repair"

    ' Find Evaluation Status column
    repairStatusCol = 0

    For colIndex = 1 To repairWS.Cells(1, repairWS.Columns.Count).End(xlToLeft).Column
        If repairWS.Cells(1, colIndex).Value = "Evaluation Status" Then
            repairStatusCol = colIndex
            Exit For
        End If
    Next colIndex

    If repairStatusCol > 0 Then

        lastRowRepair = repairWS.Cells(repairWS.Rows.Count, 1).End(xlUp).Row
        lastColRepair = repairWS.Cells(1, repairWS.Columns.Count).End(xlToLeft).Column

        ' Apply filter
        repairWS.Range(repairWS.Cells(1, 1), _
                       repairWS.Cells(lastRowRepair, lastColRepair)).AutoFilter _
                       Field:=repairStatusCol, _
                       Criteria1:="Pending Repair"

    End If
    

    '====================================================
    ' Create Assigned for Eval worksheet
    '====================================================

    Dim assignedWS As Worksheet
    Dim assignedStatusCol As Long
    Dim lastRowAssigned As Long
    Dim lastColAssigned As Long

    ' Delete sheet if it already exists
    On Error Resume Next
    Application.DisplayAlerts = False
    Worksheets("Assigned for Eval").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0

    ' Copy the main data sheet
    Sheets("Syteline Data").Copy After:=Sheets(Sheets.Count)
    Set assignedWS = ActiveSheet
    assignedWS.Name = "Assigned for Eval"

    ' Find Evaluation Status column
    assignedStatusCol = 0

    For colIndex = 1 To assignedWS.Cells(1, assignedWS.Columns.Count).End(xlToLeft).Column
        If assignedWS.Cells(1, colIndex).Value = "Evaluation Status" Then
            assignedStatusCol = colIndex
            Exit For
        End If
    Next colIndex

    If assignedStatusCol > 0 Then

        lastRowAssigned = assignedWS.Cells(assignedWS.Rows.Count, 1).End(xlUp).Row
        lastColAssigned = assignedWS.Cells(1, assignedWS.Columns.Count).End(xlToLeft).Column

        ' Find Report Due Date column
        Dim reportDueColAssigned As Long
        reportDueColAssigned = 0

        For colIndex = 1 To lastColAssigned
            If assignedWS.Cells(1, colIndex).Value = "Report Due Date" Then
                reportDueColAssigned = colIndex
                Exit For
            End If
        Next colIndex

        With assignedWS.Range(assignedWS.Cells(1, 1), _
                              assignedWS.Cells(lastRowAssigned, lastColAssigned))

            ' Filter Assigned for Evaluation
            .AutoFilter Field:=assignedStatusCol, _
                        Criteria1:="Assigned for Evaluation"

            ' Filter overdue Report Due Dates
            If reportDueColAssigned > 0 Then
                .AutoFilter Field:=reportDueColAssigned, _
                            Criteria1:="<=" & CLng(Date)
            End If

        End With

    End If
    '====================================================
    ' Create Received worksheet
    '====================================================

    Dim receivedWS As Worksheet
    Dim receivedStatusCol As Long
    Dim receivedUserCol As Long
    Dim lastRowReceived As Long
    Dim lastColReceived As Long

    ' Delete sheet if it already exists
    On Error Resume Next
    Application.DisplayAlerts = False
    Worksheets("Received").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0

    ' Copy main data sheet
    Sheets("Syteline Data").Copy After:=Sheets(Sheets.Count)
    Set receivedWS = ActiveSheet
    receivedWS.Name = "Received"

    ' Find Evaluation Status and User Name columns
    receivedStatusCol = 0
    receivedUserCol = 0

    For colIndex = 1 To receivedWS.Cells(1, receivedWS.Columns.Count).End(xlToLeft).Column

        If receivedWS.Cells(1, colIndex).Value = "Evaluation Status" Then
            receivedStatusCol = colIndex
        End If

        If receivedWS.Cells(1, colIndex).Value = "User Name" Then
            receivedUserCol = colIndex
        End If

    Next colIndex

    If receivedStatusCol > 0 And receivedUserCol > 0 Then

        lastRowReceived = receivedWS.Cells(receivedWS.Rows.Count, 1).End(xlUp).Row
        lastColReceived = receivedWS.Cells(1, receivedWS.Columns.Count).End(xlToLeft).Column

        With receivedWS.Range(receivedWS.Cells(1, 1), _
                              receivedWS.Cells(lastRowReceived, lastColReceived))

            .AutoFilter Field:=receivedStatusCol, _
                        Criteria1:="Received"

            .AutoFilter Field:=receivedUserCol, _
                        Criteria1:="<>"

        End With

    End If
    
End Sub
