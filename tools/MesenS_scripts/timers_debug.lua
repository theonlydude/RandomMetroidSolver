
local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end

local function readIGT()
  local frames,seconds,minutes,hours = readWord(0x09DA),readWord(0x09DC),readWord(0x09DE),readWord(0x09E0)
  return frames + 60*seconds + 60*60*minutes + 60*60*60*hours
end

local statsRamAddr = 0x1fc00

local timerData = {
  {"RTA", addr=0x5B8, region=false},
  {"Total", addr=statsRamAddr, region=false},
  {"Ceres", addr=statsRamAddr+7*2},
  {"Crateria", addr=statsRamAddr+9*2},
  {"Green Brin", addr=statsRamAddr+11*2},
  {"Red Brin", addr=statsRamAddr+13*2},
  {"Wr. Ship", addr=statsRamAddr+15*2},
  {"Kraid", addr=statsRamAddr+17*2},
  {"Up Norf", addr=statsRamAddr+19*2},
  {"Croc", addr=statsRamAddr+21*2},
  {"Lo Norf", addr=statsRamAddr+23*2},
  {"West Mar", addr=statsRamAddr+25*2},
  {"East Mar", addr=statsRamAddr+27*2},
  {"Tourian", addr=statsRamAddr+29*2},
  {"Pause", addr=statsRamAddr+38*2},
  {"RTA Lag", addr=0x033a,region=false},
  {"Lag", addr=statsRamAddr+42*2,region=false},
  {"IGT",addr=readIGT,region=false}
}

local function readTime(ramAddr)
  local lo = readWord(ramAddr)
  local hi = readWord(ramAddr+2)
  return hi << 16 | lo
end

local function getTime(addrEntry)
  if type(addrEntry) == "function" then
    return addrEntry()
  else
    return readTime(addrEntry)
  end
end

local function getTimeStr(frames)
  local seconds = frames // 60
  frames = frames % 60
  local minutes = seconds // 60
  seconds = seconds % 60
  local hours = minutes // 60
  minutes = minutes % 60
  return string.format("%02d:%02d:%02d.%02d", hours, minutes, seconds, frames)
end

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printRTA()
  local x,y=0,0
  local function printTime(title, frames)
     emu.drawString(x+2, y+2, title .. ":", FG, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, getTimeStr(frames), FG, BG, 1)
  end
  local regionTotal=0
  for i,info in pairs(timerData) do
     local area = info[1]
     local frames = getTime(info.addr)
     printTime(area, frames)
     if i % 2 == 1 then
       x = X_OFF
     else
       x = 0
       y = y + Y_OFF
     end
     if info.region ~= false then
       regionTotal = regionTotal + frames
     end
  end
  printTime("Regions", regionTotal)
end

emu.addEventCallback(printRTA, emu.eventType.endFrame)
