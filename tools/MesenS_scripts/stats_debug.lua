
local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end

local statsRamAddr = 0x1fc00

local statsData = {
  {"Doors", index=2},
  {"Uncharged", index=31},
  {"Charged", index=32},
  {"SBAs", index=33},
  {"Missiles", index=34},
  {"Supers", index=35},
  {"PBs", index=36},
  {"Bombs", index=37},
  {"Deaths", index=40},
  {"Resets", index=41}
}

local function getRamValue(index)
    return readWord(statsRamAddr+index*2)
end

local function getSramValue(index)
  local saveIndex = readWord(0x0952)
  local sramAddr = emu.readWord(0x81ef20+2*saveIndex, emu.memType.cpu)
  return emu.readWord(sramAddr+index*2, emu.memType.saveRam)
end

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printStats()
  local x,y=0,0
  local function printStat(title, ramVal, sramVal)
     emu.drawString(x+2, y+2, title .. ":", FG, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, ramVal, FG, BG, 1)
     emu.drawString(x+2+X_OFF//2+X_OFF//4, y+2, sramVal, FG, BG, 1)
  end
  for i,info in pairs(statsData) do
     local stat = info[1]
     printStat(stat, getRamValue(info.index), getSramValue(info.index))
     if i % 2 == 1 then
       x = X_OFF
     else
       x = 0
       y = y + Y_OFF
     end
  end
end

emu.addEventCallback(printStats, emu.eventType.endFrame)
