' =============================================================================
' DEMO 5 — ORIGINAL VBA MACRO: Premium Rating Calculator
' =============================================================================
' This is a typical VBA macro found in an actuarial team's Excel workbook.
' It calculates auto insurance premiums based on rating factors.
'
' PRESENTER NOTES:
' - Open this file in VS Code and ask Copilot Chat: "Explain this VBA code"
' - Then ask: "Convert this to Python"
' - Show how Copilot preserves the business logic while modernizing the code
' - Compare the output with premium_calc.py (the "answer key")
' =============================================================================

Option Explicit

Public Const BASE_RATE As Double = 800

Function GetAgeFactor(driverAge As Integer) As Double
    Select Case driverAge
        Case Is < 21
            GetAgeFactor = 2.1
        Case 21 To 25
            GetAgeFactor = 1.6
        Case 26 To 35
            GetAgeFactor = 1.1
        Case 36 To 45
            GetAgeFactor = 1.0
        Case 46 To 55
            GetAgeFactor = 0.95
        Case 56 To 65
            GetAgeFactor = 1.0
        Case Is > 65
            GetAgeFactor = 1.2
        Case Else
            GetAgeFactor = 1.0
    End Select
End Function

Function GetStateFactor(state As String) As Double
    Select Case UCase(state)
        Case "FL"
            GetStateFactor = 1.3
        Case "NY"
            GetStateFactor = 1.25
        Case "CA"
            GetStateFactor = 1.2
        Case "MI"
            GetStateFactor = 1.15
        Case "TX"
            GetStateFactor = 1.1
        Case "GA"
            GetStateFactor = 1.08
        Case "PA", "IL"
            GetStateFactor = 1.05
        Case "NC"
            GetStateFactor = 1.0
        Case "OH"
            GetStateFactor = 0.95
        Case Else
            GetStateFactor = 1.0
    End Select
End Function

Function GetCreditFactor(creditTier As String) As Double
    Select Case UCase(creditTier)
        Case "EXCELLENT"
            GetCreditFactor = 0.85
        Case "GOOD"
            GetCreditFactor = 1.0
        Case "FAIR"
            GetCreditFactor = 1.15
        Case "POOR"
            GetCreditFactor = 1.4
        Case Else
            GetCreditFactor = 1.0
    End Select
End Function

Function GetVehicleAgeFactor(vehicleAge As Integer) As Double
    If vehicleAge <= 2 Then
        GetVehicleAgeFactor = 1.15
    ElseIf vehicleAge <= 5 Then
        GetVehicleAgeFactor = 1.05
    ElseIf vehicleAge <= 10 Then
        GetVehicleAgeFactor = 1.0
    ElseIf vehicleAge <= 15 Then
        GetVehicleAgeFactor = 0.9
    Else
        GetVehicleAgeFactor = 0.8
    End If
End Function

Sub CalculatePremiums()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("PolicyData")
    
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    ws.Range("F1").Value = "AgeFactor"
    ws.Range("G1").Value = "StateFactor"
    ws.Range("H1").Value = "CreditFactor"
    ws.Range("I1").Value = "VehicleFactor"
    ws.Range("J1").Value = "CalculatedPremium"
    
    Dim i As Long
    For i = 2 To lastRow
        Dim ageFact As Double
        Dim stateFact As Double
        Dim creditFact As Double
        Dim vehicleFact As Double
        Dim premium As Double
        
        ageFact = GetAgeFactor(CInt(ws.Cells(i, 2).Value))
        stateFact = GetStateFactor(CStr(ws.Cells(i, 3).Value))
        creditFact = GetCreditFactor(CStr(ws.Cells(i, 4).Value))
        vehicleFact = GetVehicleAgeFactor(CInt(ws.Cells(i, 5).Value))
        
        premium = BASE_RATE * ageFact * stateFact * creditFact * vehicleFact
        If premium < 300 Then premium = 300
        
        ws.Cells(i, 6).Value = ageFact
        ws.Cells(i, 7).Value = stateFact
        ws.Cells(i, 8).Value = creditFact
        ws.Cells(i, 9).Value = vehicleFact
        ws.Cells(i, 10).Value = Round(premium, 2)
    Next i
    
    MsgBox "Premium calculation complete for " & (lastRow - 1) & " policies.", vbInformation
End Sub
