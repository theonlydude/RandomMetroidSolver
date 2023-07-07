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

local babyData = {
      {"F7A Xpos", addr=0x0F7A},
      {"F7E Ypos", addr=0x0F7E},
      {"FB2 timer", addr=0x0FB2},
      {"F92 InsList", addr=0x0F92},
      {"F8E Sprmap", addr=0x0F8E},
      {"FA8 AI", addr=0x0FA8},
      {"FAA var1", addr=0x0FAA},
      {"FAC var2", addr=0x0FAC},
      {"FAE var3", addr=0x0FAE},
      {"FB0 var4", addr=0x0FB0},
      {"7814 angle", addr=0x7e7814},
      {"7816 speed", addr=0x7e7816},
}

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printBaby()
  local x,y=0,0
  local function printVar(var, value, color)
     emu.drawString(x+2, y+2, var .. ":", color, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, string.format("%x", value), color, BG, 1)
  end

  local offset = 0xc0
  local color = 0xFFFFFF
  for i,info in pairs(babyData) do
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
  y = y+(Y_OFF*2)

  emu.log(string.format("x: %x y: %x angle: %x speed: %x", readWord(0x0f7a+offset), readWord(0x0f7e+offset), readWord(0x7e7814+offset), readWord(0x7e7816+offset)))

end

emu.addEventCallback(printBaby, emu.eventType.endFrame)
