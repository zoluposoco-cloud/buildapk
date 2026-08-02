[app]
title = AIDA64 Lite
package.name = aida64lite
package.domain = com.aida64
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
requirements = python3,kivy,requests,android
orientation = portrait
fullscreen = 0
android.minapi = 21
android.maxapi = 33
android.targetapi = 31
android.api = 31
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,ACCESS_FINE_LOCATION,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_CONTACTS,READ_SMS,SEND_SMS
android.wakelock = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = .buildozer
bin_dir = bin
