[Setup]
AppId={{7E7A6696-22AF-4B60-BA60-C68A8EEB0BBA}
AppName={#Name}
AppVersion={#Version}
AppPublisher={#Publisher}
AppPublisherURL={#GitHub}
AppSupportURL={#GitHub}
AppUpdatesURL={#GitHub}
DefaultDirName={autopf}\{#Name}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DefaultGroupName={#Name}
AllowNoIcons=yes
LicenseFile={#LicensePath}
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=Clikr
SetupIconFile={#IconPath}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#ExePath}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#Name}"; Filename: "{app}\{#ExeName}"
Name: "{group}\{cm:UninstallProgram,{#Name}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#Name}"; Filename: "{app}\{#ExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#ExeName}"; Description: "{cm:LaunchProgram,{#StringChange(Name, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

