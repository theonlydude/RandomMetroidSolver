local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
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
local function readROMByte(romAddr)
   return emu.read(snes_to_pc(romAddr), emu.memType.prgRom)
end

local function complement2int(value, mask)
   -- convert 2 complement negative int to negative int
   test_mask = (mask+1)>>1
   comp_mask = mask

   -- test if negative value
   if(value & test_mask ~= 0) then
      return -(((~value)+1) & comp_mask)
   else
      return value
   end
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
      {"FA8 AI", addr=0x0FA8},
      {"FAA var1", addr=0x0FAA},
      {"FAC var2", addr=0x0FAC},
      {"FAE var3", addr=0x0FAE},
      {"FB0 var4", addr=0x0FB0},
      {"FB2 var5", addr=0x0FB2},
      {"FB4 param1", addr=0x0FB4},
      {"FB6 param2", addr=0x0FB6},
      {"F86 prop", addr=0x0F86},
      {"F88 x prop", addr=0x0F88},
      {"direction", addr=0x7820},
      {"x1?", addr=0x202a},
      {"x2?", addr=0x2024},
      {"v1?", addr=0x7838}, -- reste a 78 tout le long, relatif a la queue
      {"v2?", addr=0x7802}, -- ridley vivant ou mort
      {"v4?", addr=0x7804},
      {"v5?", addr=0x7806},
      {"v6?", addr=0x7808},
      {"v7?", addr=0x7810}, -- positionne a 08 au debut
      {"v8?", addr=0x7812}, -- positionne a 08 au debut
      {"v9?", addr=0x2000}, -- positionne a 01 au debut
      {"v10?", addr=0x7838}, -- reste a 78 tout le long
      {"v11?", addr=0x783e}, -- check si 0 au debut de BAB7
      {"v12?", addr=0x7824}, -- utilisé pour recuperer 1/3/7/a a BB4#
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
     local ai = readWord(0x0FA8+offset)
     local il = readWord(0x0F92+offset)
     local sm = readWord(0x0F8E+offset)
     local state = readWord(0x0FB4+offset)

     -- compare with last one, log if different
     if(ai ~= enemys_history_ai[offset] or sm ~= enemys_history_sm[offset] or state ~= enemys_history_state[offset] or il ~= enemys_history_il[offset]) then
        emu.log(string.format("%x: ai: %x sm: %x state: %x il: %x", offset, ai, sm, state, il))
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

ext_colors = {}
ext_colors[0] = 0xC0FF40FF
ext_colors[1] = 0xC040FF40
ext_colors[2] = 0xC04040FF
ext_colors[3] = 0xC0FFFF40

local function drawSpriteMaps()
   local torizo_x = readWord(0x0F7A)
   local torizo_y = readWord(0x0F7E)

   -- camera
   local layer1x = readWord(0x0911)
   local layer1y = readWord(0x0915)

   -- torizos use extended spritemaps
   local extsm = readWord(0x0F8E) + 0xAA0000
   local num_ext = readROMWord(extsm)
   --emu.log(string.format("extsm: %x with %x parts", extsm, num_ext))

   for i=0,num_ext-1 do
      local x_ext = complement2int(readROMWord(extsm + 2 + i*8), 0xffff)
      local y_ext = complement2int(readROMWord(extsm + 2 + i*8 + 2), 0xffff)
      local sm = readROMWord(extsm + 2 + i*8 + 4) + 0xAA0000

      local num = readROMWord(sm)

      --emu.log(string.format("sm %d: %x with %x parts", i, sm, num))
      local color = ext_colors[i]
      emu.drawString(6*4*i, 200, string.format("%x", sm & 0xFFFF), color & 0x00FFFFFF, BG, 1)

      for j=0,num-1 do
         local w1 = readROMWord(sm + 2 + j*5)
         local b = readROMByte(sm + 2 + j*5 + 2)
         local w2 = readROMWord(sm + 2 + j*5 + 3)

         local x = complement2int(w1 & 0x1FF, 0x1ff)
         local y = complement2int(b, 0xff)
         local size = (w1 & 0x8000) >> 15
         if(size == 0) then
            size = 8
         else
            size = 16
         end
         --emu.log(string.format("%x %x %x: x: %d y: %d size: %d", w1, b, w2, x, y, size))
         emu.drawRectangle(torizo_x-layer1x+x_ext+x, torizo_y-layer1y+y_ext+y+8, size, size, color, false)
      end
   end
end

emu.addEventCallback(printEnemys, emu.eventType.endFrame)
--emu.addEventCallback(drawSpriteMaps, emu.eventType.endFrame)
