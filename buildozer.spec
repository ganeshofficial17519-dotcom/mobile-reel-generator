[app]
title = Reel Generator
package.name = reelgenerator
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 🌟 FIXED: Explicitly pinning stable python and kivy versions here
requirements = python3==3.11.11,kivy==2.3.0,requests,edge-tts,asyncio,certifi,urllib3,idna,charset-normalizer

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.allow_backup = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
