local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end

local kraidData = {
      {"camera", addr=0x0941},
}

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF
local color = 0x30FF4040

local function printKraid()
  local x,y=0,0
  local function printVar(var, value, color)
     emu.drawString(x+2, y+2, var .. ":", color, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, value, color, BG, 1)
  end

  for i,info in pairs(kraidData) do
     local var = info[1]
     local value = readWord(info.addr)
     if info.func then
        value = info.func(value)
     else
        value = string.format("%x", value)
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
  y = y+(Y_OFF*2)
end

emu.addEventCallback(printKraid, emu.eventType.endFrame)
