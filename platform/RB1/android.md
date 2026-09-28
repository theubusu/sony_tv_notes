# Android

The TV suprisingly comes with a built-in Android subsystem. This feature seems to be documented or pointed out absoultely nowhere.

In the base system it is only used for:
- Photo frame mode app
- Alpha clock app
- Open source licenses menu in settings

Note that this does not mean the TV runs android at its core. It does not. It runs Sony's CELinux and TV stack, and Android is ran as a sub-process (started/managed by `dtAndroid`) in a chroot on THE SAME kernel. That's why we can get access to useful information about the underlying core system from android context. But most access is blocked by additional security.

The android version it runs is 4.0.4. Model reports as `BRAVIA`. See the dump of `build.prop` in `info.txt` for more info about the build.

- Even though, if you plug in a USB keyboard/mouse into the TV, it will say "Device not supported", HID works completely fine in android.
- ADB is seemingly completely removed from the system. So we only have the limited permissions of app user.   
`<3>init: cannot find '/sbin/adbd', disabling 'adbd'`
- As described in `NAND.md`, the android data partition is only around ~110 MB in size. The root filesystem is squashfs, so it is read-only.
- I have managed to accidentally brick the android subsystem by messing with some SSH server app, the TV will show an error on boot along the lines of "Some apps may not be avaliable due to a system error, See iManual for more info". iManual prompts to factory reset the device in this case. That completely wiped the data partition and android was back up

## Running arbitrary Android activities
On boot, the TV downloads two files that describe the apps list present in the SEN menu from URLS:
- http://bravia.dl.playstation.net/bravia/WidgetBundles/AppDataSourceAddon_tmp/plugins/local/data/preset.json
- http://bravia.dl.playstation.net/bravia/WidgetBundles/AppDataSourceAddon_tmp/plugins/local/data/mapping_WW.json

Since they are downloaded over plain HTTP with no verification, you can run a proxy, and redirect the request to run a specified android activity

- Add the preset entry to the `mapping_WW.json` with your wanted activity like this (example for settings):
```json
"preset://andro_settings" : "aais-app://com.android.settings/.Settings"
```
- Add an entry in `preset.json` - this is the actual app entry, and make it point to your preset entry:
```json
{
    "filter" : "normal_2",
    "id" : "preset://andro_settings",
    "name"  : "Android Settings",
    "desc"  : "Open android settings",
    "thumb" : "http://10.42.42.1:6767/icon_settings.png",
    "category" : "",
    "countries" : ["ALL"]
}
```
- Now reboot the TV to make it pull the new apps list. The app will now appear in the SEN menu.

## Installing apps
To install an app:
- place an apk somewhere on a USB stick and connect it to the TV
- Launch the android browser  (hint: the preset url for it is `aais-app://com.android.browser/.BrowserActivity`)
- In the address bar, navigate to `file:///mnt/usb1/[path to the apk]`
- The package installer will show, it might also prompt you to enable unknown sources. Continue with the installation

The app is now installed. Note: It will now always appear in the SEN menu, even if the TV is offline, so you don't need to add it in the proxy.

## Android to Core communication/access
Android does not have access to the filesystem of the core OS. It runs under a chroot with additional anti-escape protections. The chroot also has limited access to device and proc nodes.

Android has access to the usb drive at `/mnt/usb1`

`com.sony.dtv.services` exposes basic non-interesting intents for app to use to send commands to the core OS:
```java
public class DTVIntent {
    public static final String ACTION_MODE_ANDROID = "com.sony.dtv.intent.action.ACTION_MODE_ANDROID"; //Focus to android
    public static final String ACTION_MODE_CORE = "com.sony.dtv.intent.action.ACTION_MODE_CORE"; //Focus to core
    public static final String ACTION_PACKAGE_SETTINGS = "com.sony.dtv.intent.action.PACKAGE_SETTINGS"; //Open "Scene Select" menu
    public static final String ACTION_PICTURE_SETTINGS = "com.sony.dtv.intent.action.PICTURE_SETTINGS"; //Open Picture settings
    public static final String ACTION_SHUTDOWN_COMPLETED = "com.sony.dtv.intent.action.ACTION_SHUTDOWN_COMPLETED"; //?
    public static final String ACTION_SOUND_SETTINGS = "com.sony.dtv.intent.action.SOUND_SETTINGS"; //Open sound settings
    public static final String ACTION_TERMINATE = "com.sony.dtv.intent.action.TERMINATE"; //Terminate app/android
    public static final String ACTION_WEB_BROWSER = "com.sony.dtv.intent.action.WEB_BROWSER";   //Open web browser
}
```
And some messages:
```java
public enum HVAMessageType {
    HVA_MESSAGE_INVALID(-1),
    HVA_ENABLE_HID(1),
    HVA_DISABLE_HID(2),
    HVA_HID_ATTACHED(3),
    HVA_GO_TO_SLEEP(4),
    HVA_GO_TO_WAKEUP(5),
    HVA_TERMINATE_ALL_APP(6),
    HVA_CHANGE_PROCESS_LIMIT(7),
    HVA_CHANGE_TV_MODE(8),
    HVA_LAUNCH_NEW_ACTIVITY(9),
    HVA_SHUTDOWN_ANDROID(10);
}
```

Photo frame app also utilizes the public web control interface at port 80 for some commands.