#ident "@(#)$Format:DEVOP1:XAU/get_gold_price.ps1:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$session.Cookies.Add((New-Object System.Net.Cookie("dtCookie","v_4_srv_4_sn_8B04893EB88646AD8E7D76F5A81E7AC4_app-3Ac0d4ef991776b9df_1_ol_0_perc_100000_mul_1","/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("BIGipServer~BCEE~PS-1141LBP28","rd1141o00000000000000000000ffffc0a8162do80", "/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("TS012a5450","01166c61636f1eaa0b4ec0df16633c46713698785de6f416ecb7de61c75f5f539a28bfeb2f3c02430becbfedab7a4dc0f33e8851ac","/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("TS019193e9","01166c61631dd9270d3b97e228bbac62082ea34410dddab18d996ea1e32bbb59e3be3bd52a3faa134adb4768eeeb46a07c24d56cd6","/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("dtPC","4`$210847492_817h2vDEPMKRGVCALELWCVDFRKEMHCMRHRHFHC-0e0", "/","www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("rxvt","1767212647667|1767210651399", "/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("dtSa", "-", "/","www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("rxVisitor","1735820566471GVFEMETL7KBGACE09T59DR69LT8JU1IK", "/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("stg_last_interaction", "Wed, 31 Dec 2025 19:52:03 GMT", "/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("ppms_privacy_146e6c83-9e24-4651-81ea-c8e6a32ac132","{`"visitorId`":`"b0c248c0-92f1-4198-9c53-629f5ae09809`",`"domain`":{`"normalized`":`"www.spuerkeess.lu`",`"isWildcard`":false,`"pattern`":`"www.spuerkeess.lu`"},`"consents`":{`"analytics`":{`"status`":1,`"updatedAt`":`"2025-12-31T19:50:54.362Z`"}},`"staleCheckpoint`":`"2025-12-31T19:50:51.949Z`"}","/", "www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("_pk_id.146e6c83-9e24-4651-81ea-c8e6a32ac132.aeaa","8b819e0c290ab56e.1767210654.1.1767210654.1767210654.", "/","www.spuerkeess.lu")))
$session.Cookies.Add((New-Object System.Net.Cookie("_pk_ses.146e6c83-9e24-4651-81ea-c8e6a32ac132.aeaa","*", "/", "www.spuerkeess.lu")))
Invoke-WebRequest -UseBasicParsing -Uri "https://www.spuerkeess.lu/fr/particuliers/epargner-investir/metaux-precieux/?action=ajax" `
-Method "POST" `
-WebSession $session `
-UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0" `
-Headers @{
"Accept" = "*/*"
   "Accept-Language" = "en-US,en;q=0.5"
   "Accept-Encoding" = "gzip, deflate, br, zstd"
   "x-dtpc" = "4`$210847492_817h2vDEPMKRGVCALELWCVDFRKEMHCMRHRHFHC-0e0"
   "Origin" = "null"
   "Sec-GPC" = "1"
   "Sec-Fetch-Dest" = "empty"
   "Sec-Fetch-Mode" = "same-origin"
   "Sec-Fetch-Site" = "same-origin"
   "Priority" = "u=4"
   "Cache-Control" = "max-age=0"
} `
-ContentType "multipart/form-data; boundary=----geckoformboundary6d9578a73603c335d4569e03da7cb73b" `
-Body ([System.Text.Encoding]::UTF8.GetBytes("------geckoformboundary6d9578a73603c335d4569e03da7cb73b$([char]13)$([char]10)Content-Disposition:form-data;name=`"formKey`"$([char]13)$([char]10)$([char]13)$([char]10)precious.metal.filter$([char]13)$([char]10)------geckoformboundary6d9578a73603c335d4569e03da7cb73b$([char]13)$([char]10)Content-Disposition:form-data;name=`"types`"$([char]13)$([char]10)$([char]13)$([char]10)102,103,106,77,80,78,79,308,73,188,241,99,114,76,85,200$([char]13)$([char]10)------geckoformboundary6d9578a73603c335d4569e03da7cb73b$([char]13)$([char]10)Content-Disposition:form-data;name=`"precious-metal-list-page`"$([char]13)$([char]10)$([char]13)$([char]10)0$([char]13)$([char]10)------geckoformboundary6d9578a73603c335d4569e03da7cb73b$([char]13)$([char]10)Content-Disposition:form-data;
name=`"sorting`"$([char]13)$([char]10)$([char]13)$([char]10)bcee$([char]13)$([char]10)------geckoformboundary6d9578a73603c335d4569e03da7cb73b--$([char]13)$([char]10)"))
