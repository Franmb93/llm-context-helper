#define MyAppName "Selector de Contexto para LLMs"
#define MyAppVersion "1.0"
#define MyAppPublisher "BetanzosDev"
#define MyAppURL "https://buymeacoffee.com/betanzosdev"
#define MyAppExeName "SelectorDeContexto.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{5DD70B5F-94A3-4E7A-8A1C-B5A987654321}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputBaseFilename=SelectorDeContexto_Setup
Compression=lzma
SolidCompression=yes
OutputDir=installer
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "INSTALL.md"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

[CustomMessages]
spanish.BuyMeACoffee=¿Te resulta útil esta aplicación? ¡Invítame a un café!
spanish.VisitWebsite=Visitar sitio web del desarrollador

[UninstallDelete]
Type: files; Name: "{app}\*.*"
Type: dirifempty; Name: "{app}"

[Messages]
spanish.WelcomeLabel2=Este asistente te guiará a través de la instalación de [name/ver] en tu computadora.%n%nSe recomienda cerrar todas las demás aplicaciones antes de continuar.
spanish.FinishedHeadingLabel=Completando la instalación de [name]
spanish.FinishedLabel=El asistente ha terminado de instalar [name] en tu computadora. La aplicación puede ser iniciada seleccionando el ícono creado.%n%nSi te resulta útil, considera invitar al desarrollador a un café.

[INI]
Filename: "{app}\support.url"; Section: "InternetShortcut"; Key: "URL"; String: "https://buymeacoffee.com/betanzosdev"
