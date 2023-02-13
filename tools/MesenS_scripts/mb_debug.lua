local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end

--        $0F78: ID
--        $0F7A: X position
--        $0F7C: X subposition
--        $0F7E: Y position
--        $0F80: Y subposition
--        $0F82: X radius
--        $0F84: Y radius
--        $0F86: Properties (Special in SMILE)
--        $0F88: Extra properties (special GFX bitflag in SMILE)
--        $0F8A: AI handler
--        $0F8C: Health
--        $0F8E: Spritemap pointer
--        $0F90: Timer
--        $0F92: Initialisation parameter (Orientation in SMILE, Tilemaps in RF) / instruction list pointer
--        $0F94: Instruction timer
--        $0F96: Palette index
--        $0F98: VRAM tiles index
--        $0F9A: Layer
--        $0F9C: Flash timer
--        $0F9E: Frozen timer
--        $0FA0: Invincibility timer
--        $0FA2: Shake timer
--        $0FA4: Frame counter
--        $0FA6: Bank
--        $0FA8: AI variable, frequently function pointer
--        $0FAA: AI variable
--        $0FAC: AI variable
--        $0FAE: AI variable
--        $0FB0: AI variable
--        $0FB2: AI variable
--        $0FB4: Parameter 1 (Speed in SMILE)
--        $0FB6: Parameter 2 (Speed2 in SMILE)

local etecoonData = {
      {"Id", addr=0x0F78},
      {"subAI", addr=0x0FF0},
      {"Xpos", addr=0x0F7A},
      {"Ypos", addr=0x0F7E},
      {"AI1", addr=0x0FA8},
      {"AI2", addr=0x0FE8},
--      {"InstrList", addr=0x0F92},
      {"Spritemap", addr=0x0F8E},
      {"target X", addr=0x0FB2},
      {"scroll x", addr=0x0911},
      {"phase", addr=0x7800},
--      {"var0", addr=0x0FA8},
--      {"var1", addr=0x0FAA},
--      {"var2", addr=0x0FAC},
--      {"var3", addr=0x0FAE},
--      {"var4", addr=0x0FB0},
}

colors = {}
colors[0x000] = 0x30FF4040
colors[0x040] = 0x3040FF40
colors[0x080] = 0x304040FF
colors[0x0c0] = 0x30FFFF40
colors[0x100] = 0x30FF40FF
colors[0x140] = 0x3040FFFF
colors[0x280] = 0x307F4040
colors[0x2c0] = 0x30407F40
colors[0x200] = 0x3040407F
colors[0x240] = 0x307F7F40
colors[0x280] = 0x307F407F
colors[0x2c0] = 0x30407F7F

-- keep history of mb ai change
history = {}
history[0x00] = {ai = 0x0, subai = 0x0, x = 0x0}
history[0x40] = {ai = 0x0, subai = 0x0, x = 0x0}
history["neck"] = 0x0

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printMB()
  local x,y=0,0
  local function printVar(var, value, color)
     emu.drawString(x+2, y+2, var .. ":", color, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, string.format("%x", value), color, BG, 1)
  end

  for _, offset in ipairs({0x00, 0x40}) do --, 0x80, 0xc0, 0x100, 0x140, 0x180, 0x1c0, 0x200, 0x240, 0x280, 0x2c0}) do
     local color = colors[offset]
     for i,info in pairs(etecoonData) do
        local var = info[1]
        local value = readWord(info.addr+offset)
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

     -- get ai
     local ai = readWord(0x0FA8+offset)
     local subai = readWord(0x0FF0+offset)
     local x = readWord(0x0F7A+offset)

     -- compare with last one, log if different
     if(ai ~= history[offset]["ai"] or subai ~= history[offset]["subai"] or x ~= history[offset]["x"]) then
        emu.log(string.format("%x: ai: %x subai: %x x: %x", offset, ai, subai, x))
        history[offset]["ai"] = ai
        history[offset]["subai"] = subai
        history[offset]["x"] = x
     end

     local mbneckhitboxsegment4xpos = readWord(0x7E805C)
     if(history["neck"] ~= mbneckhitboxsegment4xpos) then
        emu.log(string.format("neck x before: %x after: %x", history["neck"], mbneckhitboxsegment4xpos))
        history["neck"] = mbneckhitboxsegment4xpos
     end

     -- display colored box for mb brain and body
     local x = readWord(0x0F7A+offset)
     local y = readWord(0x0F7E+offset)

     -- camera
     local layer1x = readWord(0x0911)
     local layer1y = readWord(0x0915)

     emu.drawRectangle(x-layer1x, y-layer1y, 8, 8, color, true)
  end
end

emu.addEventCallback(printMB, emu.eventType.endFrame)
