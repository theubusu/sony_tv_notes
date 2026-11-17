# FMP-X5
Notes for FMP-X5 4K media player, based on RB2 hardware/software. Info should be mostly applicable to all players in series.

## Series comparasion

|               | FMP-X5        | FMP-X7        | FMP-X10       |
|---------------|---------      |---------      |-----------    |
|Destination    |Europe         |Japan          |America        |
|Built-in HDD   |-              |-              |O (1TB)        |
|Tuner          |-              |O              |-              |
|Wi-Fi          |-              |-              |O              |
|Video Player   |O              |O              |O              |
|Music Player   |-              |O              |O              |
|PKG            |`PKG2.059EUP`  |`PKG2.074JPP`  |`PKG2.071AAQ`  |

## HDMI
![picture](../../images/fmp-x5_hdmi_error.png)
The player needs to be connected to a HDCP 2.2 compatible HDMI port, otherwise it will not start up. It does not necessarily have to be a Sony TV, it worked on an LG TV, and a 4k DELL monitor.

## Firmware
Since Sony never released a downloadable firmware for this model, I didn't know the update ID. But I was able to guess it quite easily based on the fw of Japanese model, it's `sony_dtv0FA40A08A0A8_00413100`

By using TAR hack and nginx file described in `RB1/firmware.md`, I was able to access some of the internal files, like `/NAND/var/release.pkg.version`:
```
#: [Common Info]
PROTOTYPE=Release
IMAGE_TYPE=ENG-SCFADFLSLFVLV/ENG-SCPADPLSLPVLV
PACKAGE_TYPE=EU
BASELINE_TYPE=P
PACKAGE_PREFIX=14_RB2

#: [PKG Info]
PACKAGE_VERSION=PKG2.059EUP
CORETV_PACKAGE_VERSION=CM2.059EUP
ANDROID_PACKAGE_VERSION=AM2.059WW
DOWNLOAD_ENCRYPTION_MODELID=0x00413100
DOWNLOAD_VERSION=0859
UPDATE_ID=0x0FA40A08A0A8
JP_UPDATE_ID=0xFFFFFFFF
BR_UPDATE_ID=0xFFFFFFFF
DVB_UPDATE_ID=0x00413100
US_UPDATE_ID=0xFFFFFFFF
PACKAGE_NAME=14_RB2_00413100_V0859_PKG2.059EUP_SCFADFLSLFVLV
SYSTEM_PACKAGE_NAME=14_RB2_SYS2.059WW_S.fra
CORETV_PACKAGE_NAME=14_RB2_CM2.059EUP_CF_relnand.fra
ANDROID_PACKAGE_NAME=14_RB2_AM2.059WW_A_user.fra
VERSION_PACKAGE_NAME=14_RB2_00413100_V0859_VER2.059EUP_V.fra
VERSION_BASELINE=//14BOX/Panther/Exp/Release/TypeB-Release-GM10
VERSION_CHANGE_LIST=436883
ANDROID_DATA_PACKAGE_VERSION=AD2.059WW
ANDROID_DATA_PACKAGE_NAME=14_RB2_AD2.059WW_DF_user.fra
LYON_PACKAGE_VERSION=LM2.059LNQ
LYON_PACKAGE_NAME=14_RB2LN_LM2.059LNQ_LF_relnand.fra
LYON_SYSTEM_PACKAGE_NAME=14_RB2LN_SYS2.059WW_S.fra
LYON_VERSION_PACKAGE_NAME=14_RB2LN_00413100_V0859_VER2.059LNQ_V.fra
P4_SYNC_LABEL=@436883
ANDROID_CHANGE_LIST=436874
P4_SYNC_LABEL=@436883
```

But since ngnix runs as UID 500, access to many files is limited. As you can see on the above dump, the latest(?) version for X5 is `PKG2.059EUP`

Additional: nginx info (got by `/proc/self/exe` lol):
```
nginx version: nginx/1.2.9
configure arguments: --with-cc='ccache arm-sony-linux-gnueabi-thumb2-dev-gcc-4.5.1-08000002 -L/home/muroya/p4/14TV/Ryu/Exp/develop/output/develop_EU/integ/export/target/thumb2/sony/usr/sony/lib/ -losal -D_GNU_SOURCE' --crossbuild=Linux: --prefix=/devel/usr --error-log-path=/tmp/nginx/nginx.log --conf-path=/var/nginx/nginx.conf --with-ipv6 --without-http_charset_module --without-http_empty_gif_module --without-http_fastcgi_module --without-http_geo_module --without-http_gzip_module --without-http_map_module --without-http_memcached_module --without-http_referer_module --without-http_scgi_module --without-http_split_clients_module --without-http_ssi_module --without-http_upstream_ip_hash_module --without-http_userid_module --without-http_uwsgi_module --without-http_autoindex_module --without-http_auth_basic_module --without-http_limit_req_module --add-module=chunkin-nginx-module-0.23 --add-module=headers-more-nginx-module-0.21/
```
Not sure if nginx can be used for anything useful here

## Network update
The network update ID is `00605`, product: `Mediabox2G` (retrieved from `/tmp/mnt/ccf/iptv.nvm/bmmdata.tgz`)

Update is no longer served.

## Apps
![picture](../../images/fmp-x5_home_screen.png)
The home screen presents you with only 2 avaliable applications: Netflix and Video player.

Netflix starts to the login screen (seemingly modern version) and promptly crashes a second later.

The Video player runs on Android, and indeed it only allows you to play video files. USB only, no DLNA, also MKV files are not supported for some reason

Help -> Help Guide is supposed to launch the browser with the online E-manual, but it errors out "Internet browser will be closed due to internal error" by default.

It loads http://rd1.sony.net:80/help/hv/fmpx5/h_zz/. You can redirect this and fix the error by blocking communication to `xml.opera.com` and `certs.opera.com`, to load any page in the browser.

## Applicast
The player downloads an index from: https://applicast.ga.sony.net/WsIndexes/MB2_WW.xml

It is pretty empty and doesnt have anything useful/interesting. I tried modifing stuff to make video player launch another app, but it is no use, the video player launch is hardcoded in home menu: 
```js
F1BoxFooterArea.prototype.onMediaPlayerSelected = function()
{
    appLauncher.launch(
        'aapp://aais-app://com.sony.dtv.mediaplayer/com.sony.dtv.mediaplayer.MediaContentsBrowserActivity|MediaType=Video',
        function(isAccepted, result) {
            F1LOG.I('isAccepted: ' + isAccepted + ' result:' + result);
        });
};
```
If we load appdatasource from RB1, it will fail to launch because RB1's syntax is different. So that means appLauncher is updated. But it is signed so it cant be manipulated

## Hardware
![picture](../../images/fmp-x5_board_btm.jpg)
SAL-1001 board. Common for FMP-X5/X7/X10

The player is equipped with Ayu2 (CXD4741GB) and XVAD1 (Lyon, CXD4754GB). The same setup as in high-end RB2 tv.

There is 2xTHGBMAG5A1JBAIR eMMC, for Ayu2 and Lyon.

2Mb SPI-ROM MX25L2006EM1I-12G is used for eMMC boot.

SATA components/connectors are not present for FMP-X5.

There is an unpopulated USB3.0 connector CN4100. Looks to be unused on all variants.

### Notable connections
Not yet tested

|Connector      | FMP-X5        |
|---------------|---------      |
|CN3104         |Located next to SPI flash, has SPI interface "Writing connector at production". HDMI controller related.|
|CN4002         |DEBUG LOG FOR LYON AND FRC|
|CN4004         |MS for Lyon         |
|CN4005         |JTAG for Lyon #1       |
|CN4007         |JTAG for Lyon #2       |
|CN7001         |MS for Ayu2         |
|CN7301         |Main TL-EX1 debug connector with Ayu2 and Lyon console        |
|CN7310         |JTAG for Ayu2|

Lyon has two seperate JTAG connections, labeled "JTAG MIPS/ARM", and "JTAG ALLEGRO"

## Service menus
### Self Check Diagnosis
[RETURN], [DOWN], [PAUSE], [POWER]
![picture](../../images/fmp-x5_self_check_diagnosis.png)

### Service Adjustments Mode
[RETURN], [UP], [PAUSE], [POWER]
![picture](../../images/fmp-x5_service_adjustments_mode.png)

## Service manual
FMP-X5: https://elektrotanya.com/sony_fmp-x5_fmp-x5-1_4k-hd-mp_ver.1.0_rm.pdf/download.html

FMP-X10: https://elektrotanya.com/sony_fmp-x10_4k-hd-mp_ver.2.0_rm.pdf/download.html