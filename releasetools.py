#
# Copyright (C) 2017 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import common
import re

def FullOTA_Assertions(info):
  AddModemAssertion(info)
  return

def FullOTA_InstallEnd(info):
  info.script.Mount("/vendor")
  RunCustomScript(info, "deunify.sh", "")
  info.script.Unmount("/vendor")
  return

def IncrementalOTA_Assertions(info):
  AddModemAssertion(info)
  return

def IncrementalOTA_InstallEnd(info):
  info.script.Mount("/vendor")
  RunCustomScript(info, "deunify.sh", "")
  info.script.Unmount("/vendor")
  return

def AddModemAssertion(info):
  android_info = info.input_zip.read("OTA/android-info.txt")
  m = re.search(r'require\s+version-modem\s*=\s*(.+)', android_info)
  if m:
    version = m.group(1).rstrip()
    if len(version) and '*' not in version:
      info.script.AppendExtra(('assert(leeco.verify_modem("%s") == "1");' % (version)))
  return

def RunCustomScript(info, name, arg):
  info.script.AppendExtra(('run_program("/tmp/install/bin/%s", "%s");' % (name, arg)))
  return
