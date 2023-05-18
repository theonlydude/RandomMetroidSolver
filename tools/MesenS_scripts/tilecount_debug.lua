
local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end

local function readByte(ramAddr)
  return emu.read(ramAddr, emu.memType.workRam)
end

local statsRamAddr = 0xd850

local tileCountData = {
  {"Total", addr=statsRamAddr+12, region=false, word=true},
  {"Ceres", addr=statsRamAddr},
  {"Crateria", addr=statsRamAddr+1},
  {"Green Brin", addr=statsRamAddr+2},
  {"Red Brin", addr=statsRamAddr+3},
  {"Wr. Ship", addr=statsRamAddr+4},
  {"Kraid", addr=statsRamAddr+5},
  {"Up Norf", addr=statsRamAddr+6},
  {"Croc", addr=statsRamAddr+7},
  {"Lo Norf", addr=statsRamAddr+8},
  {"West Mar", addr=statsRamAddr+9},
  {"East Mar", addr=statsRamAddr+10},
  {"Tourian", addr=statsRamAddr+11}
}

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printMapCompletion()
  local x,y=0,0
  local function printTileCount(title, count)
     emu.drawString(x+2, y+2, title .. ":", FG, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, tostring(count), FG, BG, 1)
  end
  local regionTotal=0
  for i,info in pairs(tileCountData) do
     local area = info[1]
     local count
     if info.word then
       count = readWord(info.addr)
     else
       count = readByte(info.addr)
     end
     printTileCount(area, count)
     if i % 2 == 1 then
       x = X_OFF
     else
       x = 0
       y = y + Y_OFF
     end
     if info.region ~= false then
       regionTotal = regionTotal + count
     end
  end
  printTileCount("Regions", regionTotal)
end

emu.addEventCallback(printMapCompletion, emu.eventType.endFrame)
