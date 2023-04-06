local function readWord(ramAddr)
  return emu.readWord(ramAddr, emu.memType.workRam)
end
local function readByte(ramAddr)
  return emu.read(ramAddr, emu.memType.workRam)
end

local projectileData = {
      {"1A4B Xpos", addr=0x1A4B, len=2},
      {"1A4B Xpos1", addr=0x1A4B, len=1},
      {"1A4C Xpos2", addr=0x1A4C, len=1},

      {"1AB7 Xspe", addr=0x1AB7, len=2},
      {"1AB7 Xspe1", addr=0x1AB7, len=1},
      {"1AB8 Xspe2", addr=0x1AB8, len=1},

      {"1AFF Xacc", addr=0x1AFF, len=2},
      {"1AFF Xacc1", addr=0x1AFF, len=1},
      {"1B00 Xacc2", addr=0x1B00, len=1},

      {"1A28 Xacc3", addr=0x1A28, len=1},

      {"1A93 Ypos", addr=0x1A93, len=2},
      {"1B6F Ysubp", addr=0x1B6F, len=2},
      {"1B23 Yacc1", addr=0x1B23, len=2},
      {"1ADB Yspe", addr=0x1ADB, len=2},

}

projectileData_history = {}
for i,info in pairs(projectileData) do
   projectileData_history[i] = 0
end

colors = {}
colors[0x22] = 0x00FF4040
colors[0x20] = 0x4040FF40
colors[0x1e] = 0x404040FF
colors[0x1c] = 0x40FFFF40
colors[0x1a] = 0x40FF4040
colors[0x18] = 0x4040FFFF
colors[0x16] = 0x40404088
colors[0x14] = 0x40888840

local X_OFF = 85
local Y_OFF = 9
local BG = 0x80000000
local FG = 0xFFFFFF

history_output = ""
output = ""

local function printProjectiles()
  local x,y=0,0
  local function printVar(var, value, color)
     emu.drawString(x+2, y+2, var .. ":", color, BG, 1)
     emu.drawString(x+2+(12*5), y+2, string.format("%x", value), color, BG, 1)
     output = output .. string.format("%s: %x\n", var, value)
  end

  output = ""
  for _, offset in ipairs({0x22}) do --, 0x20, 0x1e, 0x1c, 0x1a, 0x18, 0x16, 0x14}) do
     x = 0
     local color = colors[offset]
     for i,info in pairs(projectileData) do
        local var = info[1]
        local value = 0
        if info.len == 1 then
           value = readByte(info.addr+offset)
        else
           value = readWord(info.addr+offset)
        end
        printVar(var, value, color)
        if value ~= projectileData_history[i] then
           local diff = value - projectileData_history[i]
           if diff > 0 then
              emu.log(string.format("%s: old: %x new: %x diff: %x", var, projectileData_history[i], value, diff))
           else
              diff = -diff
              emu.log(string.format("%s: old: %x new: %x diff: -%x", var, projectileData_history[i], value, diff))
           end
        end
        projectileData_history[i] = value
        if i % 3 == 1 then
           x = X_OFF
        elseif i % 3 == 2 then
           x = 2*X_OFF
        else
           x = 0
           y = y + Y_OFF
        end
     end
     y = y+Y_OFF+2

     if output ~= history_output then
        emu.log(output)
        emu.log("\n")
        history_output = output
     end
  end
end

emu.addEventCallback(printProjectiles, emu.eventType.endFrame)
