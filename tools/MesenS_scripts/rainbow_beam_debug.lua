local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end

-- $7E:8022: Mother Brain rainbow beam angle. Units of pi/80h radians, 0 = down, increasing = anti-clockwise
-- 
-- $7E:8026: Mother Brain rainbow beam angular width. Units of pi/8000h radians. Increased by 180h up to C00h during rainbow beam
-- 
-- $7E:8034: Mother Brain rainbow beam right edge angle. Units of pi/80h radians, 0 = down, increasing = anti-clockwise
-- $7E:8036: Mother Brain rainbow beam left edge angle. Units of pi/80h radians, 0 = down, increasing = anti-clockwise
-- $7E:8038: Mother Brain rainbow beam right edge origin X position. Initialised to ([Mother Brain's brain X position] + Eh) * 100h
-- $7E:803A: Mother Brain rainbow beam origin Y position. Initialised to [Mother Brain's brain Y position] + 5
-- $7E:803C: Mother Brain rainbow beam left edge origin X position. Initialised to ([Mother Brain's brain X position] + Eh) * 100h
-- $7E:803E: Mother Brain rainbow beam origin Y position. Same as $803A. Used when beam is aimed right, $803A is used otherwise. Initialised to [Mother Brain's brain Y position] + 5


local beamData = {
--      {"angle", addr=0x7e8022}, -- always displays 0
      {"angular width", addr=0x7e8026},
--      {"right edge angle", addr=0x7e8034}, -- always displays 0
--      {"left edge angle", addr=0x7e8036}, -- always displays 0
      {"right edge orig x pos", addr=0x7e8038},
--      {"orig y pos", addr=0x7e803a}, -- always displays 0
      {"left edge orig x pos", addr=0x7e803c},
--      {"orig y pos", addr=0x7e803e}, -- always displays 0
}

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printBeam()
  local x,y=0,0
  local function printVar(var, value, color)
     emu.drawString(x+2, y+2, var .. ":", color, BG, 1)
     emu.drawString(x+2+X_OFF, y+2, string.format("%x", value), color, BG, 1)
  end

  local color = 0xFFFFFF
  for i,info in pairs(beamData) do
     local var = info[1]
     local value = readWord(info.addr)
     printVar(var, value, color)
     y = y + Y_OFF
  end
end

local function displayQuadrant()
   local samusX = readWord(0x0AF6)
   local samusY = readWord(0x0AFA)
   local mbX = readWord(0x0FBA)-0x10
   local mbY = readWord(0x0FBE)+10
   local tanAngle = (mbX-samusX) / (mbY-samusY)
   local angle = math.atan(tanAngle)
   -- get same angle value than in-game
   if samusY < mbY then
      if samusX < mbX then
         angle = angle - math.pi
      else
         angle = angle + math.pi
      end
   end
   local angleDeg = 180*angle/math.pi
   emu.log(string.format("tanAngle: %f angle: %f angleDeg: %f", tanAngle, angle, angleDeg))

   -- camera
   local layer1x = readWord(0x0911)
   local layer1y = readWord(0x0915)
   mbX = mbX - layer1x
   mbY = mbY - layer1y
   emu.drawLine(mbX, mbY, samusX-layer1x, samusY-layer1y, 0xFF0000)

   -- angle width / 2 in degrees
   local angleWidth = 8.43
   -- display quadrant
   if angleDeg > angleWidth and angleDeg < 90 - angleWidth then
      -- down right
      emu.drawRectangle(mbX+0x20-8, mbY+0x20-8, 16, 16, 0x00FF00, true)
   elseif (angleDeg < 0 and angleDeg > -angleWidth) or (angleDeg > 0 and angleDeg < angleWidth) then
      -- down
      emu.drawRectangle(mbX-8, mbY+0x20-8, 16, 16, 0x00FF00, true)
   elseif angleDeg < 0 and angleDeg > -90 + angleWidth then
      -- down left
      emu.drawRectangle(mbX-0x20-8, mbY+0x20-8, 16, 16, 0x00FF00, true)
   elseif angleDeg < 0 and angleDeg > -90 - angleWidth then
      -- left
      emu.drawRectangle(mbX-0x20-8, mbY-8, 16, 16, 0x00FF00, true)
   elseif angleDeg < 0 and angleDeg > -180 + angleWidth then
      -- top left
      emu.drawRectangle(mbX-0x20-8, mbY-0x20-8, 16, 16, 0x00FF00, true)
   elseif angleDeg < 0 and angleDeg < -180 then
      -- top
      emu.drawRectangle(mbX-8, mbY-0x20-8, 16, 16, 0x00FF00, true)
   elseif angleDeg > 90+angleWidth and angleDeg < 180-angleWidth then
      -- top right
      emu.drawRectangle(mbX+0x20-8, mbY-0x20-8, 16, 16, 0x00FF00, true)
   elseif angleDeg > 90-angleWidth and angleDeg < 90+angleWidth then
      -- right
      emu.drawRectangle(mbX+0x20-8, mbY-8, 16, 16, 0x00FF00, true)
   end
end

emu.addEventCallback(printBeam, emu.eventType.endFrame)
emu.addEventCallback(displayQuadrant, emu.eventType.endFrame)
