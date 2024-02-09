#!/usr/bin/python
# -*- coding: utf-8 -*-
###################
## ONEupdater E2 ##
###################

Picons1='Full (100x60) Dark On Reflection'
Picons2='13e 19e 23e 28e (100×60) Dark On Reflection'
Picons3='13e 19e 23e 28e (100×60) Dark On Transparent'
Picons4='13e 19e 23e 28e (100×60) Light On Transparent'
Picons5='Ziggo (100×60) Dark On Reflection'
Picons6='Ziggo (100×60) Dark On Transparent'
Picons7='Ziggo (100×60) Light On Transparent'
Picons8='13e 19e 23e 28e (220×132) Dark On Reflection'
Picons9='13e 19e 23e 28e (220×132) Dark On Transparent'
Picons10='13e 19e 23e 28e (220x132) Light On Transparent'
Picons11='Ziggo (220×132) Dark On Reflection'
Picons12='Ziggo (220×132) Dark On Transparent'
Picons13='Ziggo (220x132) Light On Transparent'
Picons_ipk='ONEupdaterE2_picons.ipk'

ziggo_100_dr='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-ziggo.100.*k.on.r.*ipk" | cut -d : -f 2,3'
ziggo_100_dt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-ziggo.100.*k.on.t.*ipk" | cut -d : -f 2,3'
ziggo_100_lt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-ziggo.100.*t.on.t.*ipk" | cut -d : -f 2,3'
sat4_100_dr='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-13.*100.*k.on.r.*ipk" | cut -d : -f 2,3'
sat4_100_dt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-13.*100.*k.on.t.*ipk" | cut -d : -f 2,3'
sat4_100_lt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-13.*100.*t.on.t.*ipk" | cut -d : -f 2,3'
ziggo_220_dr='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-ziggo.220.*k.on.r.*ipk" | cut -d : -f 2,3'
ziggo_220_dt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-ziggo.220.*k.on.t.*ipk" | cut -d : -f 2,3'
ziggo_220_lt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-ziggo.220.*t.on.t.*ipk" | cut -d : -f 2,3'
sat4_220_dr='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-13.*220.*k.on.r.*ipk" | cut -d : -f 2,3'
sat4_220_dt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-13.*220.*k.on.t.*ipk" | cut -d : -f 2,3'
sat4_220_lt='curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-13.*220.*t.on.t.*ipk" | cut -d : -f 2,3'
full_100_dr = 'curl -s https://api.github.com/repos/picons/picons/releases/latest | grep "browser_download_url.*srp-full.*ipk" | cut -d : -f 2,3'

