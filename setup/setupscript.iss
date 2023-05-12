; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "EzEncryptor"
#define MyAppVersion "1.0"
#define MyAppPublisher "rush1dan"
#define MyAppURL "https://github.com/rush1dan/file-encryptor"
#define MyAppExeName "EzEncryptor.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{EE01C5BC-E725-476E-AD7C-DA5BBEB53CEE}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=yes
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=C:\PythonProjects\FileEnDecryptor\LICENSE.md
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=C:\EzEncryptorTest
OutputBaseFilename=ezencryptor_installer
SetupIconFile=C:\Users\origi\Desktop\SetupIconMain.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "C:\PythonProjects\FileEnDecryptor\dist\EzEncryptor\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\PythonProjects\FileEnDecryptor\dist\EzEncryptor\EncryptionShellExtension.dll"; DestDir: "{app}"; Flags: regserver
Source: "C:\PythonProjects\FileEnDecryptor\dist\EzEncryptor\DecryptionShellExtension.dll"; DestDir: "{app}"; Flags: regserver
Source: "C:\PythonProjects\FileEnDecryptor\dist\EzEncryptor\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"


