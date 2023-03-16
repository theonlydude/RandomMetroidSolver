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

local enemyData = {
      {"F7A Xpos", addr=0x0F7A},
      {"F7E Ypos", addr=0x0F7E},
      {"F8A AI1", addr=0x0F8A},
      {"FB2 AI2", addr=0x0FB2},
      {"F92 IL", addr=0x0F92},
      {"F8E SM", addr=0x0F8E},
      {"FA8 var0", addr=0x0FA8},
      {"FAA var1", addr=0x0FAA},
      {"FAC var2", addr=0x0FAC},
      {"FAE var3", addr=0x0FAE},
      {"FB0 var4", addr=0x0FB0},
      {"FB2 var5", addr=0x0FB2},
      {"FB4 param1", addr=0x0FB4},
      {"FB6 param2", addr=0x0FB6},
      {"F86 prop", addr=0x0F86},
      {"F88 x prop", addr=0x0F88},
}

-- keep history of ai changes
enemys_history_ai = {}
enemys_history_ai[0x0] = 0x0
enemys_history_il = {}
enemys_history_il[0x0] = 0x0
enemys_history_sm = {}
enemys_history_sm[0x0] = 0x0
enemys_history_state = {}
enemys_history_state[0x0] = 0x0

enemys_colors = {}
enemys_colors[0x0] = 0x30FF4040

local X_OFF = 125
local Y_OFF = 10
local BG = 0x80000000
local FG = 0xFFFFFF

local function printEnemys()
  local x,y=0,0
  local function printVar(var, value, color)
     emu.drawString(x+2, y+2, var .. ":", color, BG, 1)
     emu.drawString(x+2+X_OFF//2, y+2, string.format("%x", value), color, BG, 1)
  end

  for _, offset in ipairs({0x0}) do
     local color = enemys_colors[offset]
     for i,info in pairs(enemyData) do
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

     -- get ai
     local ai = readWord(0x0FB2+offset)
     local il = readWord(0x0F92+offset)
     local sm = readWord(0x0F8E+offset)
     local state = readWord(0x0FB4+offset)

     -- compare with last one, log if different
     if(ai ~= enemys_history_ai[offset] or il ~= enemys_history_il[offset] or sm ~= enemys_history_sm[offset] or state ~= enemys_history_state[offset]) then
        emu.log(string.format("%x: ai: %x il: %x sm: %x state: %x", offset, ai, il, sm, state))
        enemys_history_ai[offset] = ai
        enemys_history_il[offset] = il
        enemys_history_sm[offset] = sm
        enemys_history_state[offset] = state
     end

     -- display colored box for each enemy
     local x = readWord(0x0F7A+offset)
     local y = readWord(0x0F7E+offset)

     -- camera
     local layer1x = readWord(0x0911)
     local layer1y = readWord(0x0915)

     emu.drawRectangle(x-layer1x, y-layer1y, 8, 8, color, true)
  end
end

emu.addEventCallback(printEnemys, emu.eventType.endFrame)
