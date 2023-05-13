local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end
local function readByte(ramAddr)
  return emu.read(ramAddr, emu.memType.workRam)
end

local function snes_to_pc(B)
      local B_1 = B >> 16
      local B_2 = B & 0xFFFF
      -- return 0 if invalid LoROM address
      if(B_1 < 0x80 or B_1 > 0xFFFFFF or B_2 < 0x8000) then
         return 0
      end
      local A_1 = (B_1 - 0x80) >> 1
      -- if B_1 is even, remove most significant bit
      local A_2 = B_2
      if( (B_1 & 1) == 0 ) then
         A_2 = B_2 & 0x7FFF
      end
      --emu.log(string.format("b: %x b1: %x b2: %x a1: %x a2: %x", B, B_1, B_2, A_1, A_2))
      return (A_1 << 16) | A_2
end

local function readROMWord(romAddr)
   -- readWord for prgRom is bugged
   local addr = snes_to_pc(romAddr)
   local l = emu.read(addr, emu.memType.prgRom)
   local h = emu.read(addr+1, emu.memType.prgRom)
   return l + (h << 8)
end

--    $0A1C: Samus pose
--    $0A1E: Samus pose X direction
--    $0A1F: Samus movement type
--    $0A96: Samus animation frame

local samusData = {
   {"Pose", addr=0x0a1c, len=2},
   {"Pose X dir", addr=0x0A1E, len=1},
   {"Move type", addr=0x0A1F, len=1},
   {"Anim frame", addr=0x0A96, len=2},
}

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printSamus()
  local x,y=0,0
  local function printVar(var, value, color)
     emu.drawString(x+2, y+2, var .. ":", color, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, string.format("%x", value), color, BG, 1)
  end

  local color = 0x30FF4040
  for i,info in pairs(samusData) do
     local var = info[1]
     local value = 0
     if info.len == 1 then
        value = readByte(info.addr)
     else
        value = readWord(info.addr)
     end

     printVar(var, value, color)
     if i % 2 == 1 then
        x = X_OFF
     else
        x = 0
        y = y + Y_OFF
     end
  end

  x = 0
  local samusPose = readWord(0x0a1c)
  local animFrame = readWord(0x0a96)

  -- A = [$92:9263 + [Samus pose] * 2] + [Samus animation frame] (Samus spritemap table index - top half)
  local ptrTop = readROMWord(0x929263 + samusPose*2)
  ptrTop = ptrTop + animFrame

  printVar("ptrTop", ptrTop, color)
  y = y + Y_OFF

  -- A = [$92:945D + [Samus pose] * 2] + [Samus animation frame] (Samus spritemap table index - bottom half)
  local ptrBot = readROMWord(0x92945d + samusPose*2)
  ptrBot = ptrBot + animFrame

  printVar("ptrBot", ptrBot, color)
  y = y + Y_OFF

  -- ;;; $8189AE: Add Samus spritemap to OAM ;;;
  -- Y = [$808D + [A] * 2] (address of spritemap)
  local spritemapTop = readROMWord(0x92808D + ptrTop*2)
  local spritemapBot = readROMWord(0x92808D + ptrBot*2)

  printVar("spritemapTop", spritemapTop, color)
  y = y + Y_OFF
  printVar("spritemapBot", spritemapBot, color)
  y = y + Y_OFF
end

emu.addEventCallback(printSamus, emu.eventType.endFrame)
