// auto tracker
var socket;
// device type
var device;
// try to reconnect for snes classic
var reconnectInProgress = false;
var retryCount = 0;
var retryMax = 30;
// timeout to restart the auto tracker
var retryTimeout;
// timeout to peek data
var timeout;
// timeout duration in ms
var waitingTime = 1000;
// timeout to increment RTA
var incrRTA;
// time when the timeout has been set
var incrRTAstart = 0;
var rawTimeFrames = 0;
var RTAwaitingTime = 50;

// first you open the socket,
// then you list the available devices,
// then you attach to the device and ask info to confirm attachment,
// then you can ask for data (main loop)
var stateEnum = {
    "opening": 1,
    "listing": 2,
    "infoing": 3,
    "looping": 4
}
var curState = 0;

// handle fragmented data reception
var askedDataSize = 0;
var receivedDataSize = 0;
var receivedData = [];
var transfertStart = 0;

// current and previous step data, uint8array
var stateArraySize = 0;
var currentState = undefined;
// data offsets in the state
var stateDataOffsets = {};
// to know if something changed
var previousStateChksum = 0;
// bit masks to apply on state to extract data we use
var stateBitMasks = undefined;

// array for each data we get
var itemsData = undefined;
var bossData = undefined;
var mapData = undefined;
var samusData = undefined;
let eventsData = undefined;
let inventoryData = undefined;

// different data that we ask
var dataEnum = {
    "state": 1,
    "map": 2,
    "curMap": 3,
    "samus": 4,
    "items": 5,
    "boss": 6,
    "events": 7,
    "inventory": 8
}
// 1. state:
// $0998: Game state
// $05D1: Debug. Debug mode. Set to [$80:8004] during boot / soft reset
// in-game timer:
// $05B8: NMI counter (RTA timer)
// $05BA: Lag counter (RTA timer)
// SRAM timer after game's end:
// define current_save_slot    $7e0952
// define stats_sram_slot0     $701400
// define stats_sram_slot1     $701700
// define stats_sram_slot2     $701a00

// 2. map:
// used for area/boss transitions - doors - nothing
// CD52 -> D351: map tiles for: Crateria + Brinstar + Norfair + Wrecked Ship + Maridia + Tourian

// 3. curmap:
// 07F7..08F6: map tiles for current area

// 4. samus:
// $0AF6: Samus X position (inside current room)
// $0AFA: Samus Y position (inside current room)
// 
// $079B: Room pointer
// $079F: Area index
// $07A1: Room X co-ordinate (on map)
// $07A3: Room Y co-ordinate (on map)

// 5. items
// $7E:D870..AF: Item bit array. $90h..AF are unused. See "Item PLMs.asm"
// loc id is used to index in it

// 6. boss
// $7E:D828..2F: Boss bits. Indexed by area
//     1: Area boss (Kraid, Phantoon, Draygon, both Ridleys)
//     2: Area mini-boss (Spore Spawn, Botwoon, Crocomire, Mother Brain)
//     4: Area torizo (Bomb Torizo, Golden Torizo)
// Area index
//     0: Crateria
//     1: Brinstar
//     2: Norfair
//     3: Wrecked Ship
//     4: Maridia
//     5: Tourian
//     6: Ceres
//     7: Debug

// 7. events
// $7E:D820..39

// 8. Inventory
// $7#:09A4..AA
// $7#:09C4..D6
var dataToAsk = {
    1: [{"address": "F50998", "size": 0x2},
        {"address": "F505D1", "size": 0x2},
        {"address": "F505B8", "size": 0x4},
        {"address": "F50952", "size": 0x2},
        {"address": "E01400", "size": 0x4},
        {"address": "E01700", "size": 0x4},
        {"address": "E01A00", "size": 0x4}],
    2: [{"address": "F5CD52", "size": 0x600}],
    3: [{"address": "F507F7", "size": 0x100}],
    4: [{"address": "F50AF6", "size": 0x2},
        {"address": "F50AFA", "size": 0x2},
        {"address": "F5079B", "size": 0x0a}],
    5: [{"address": "F5D870", "size": 0x20}],
    6: [{"address": "F5D828", "size": 0x8}],
    7: [{"address": "F5D820", "size": 0x20}],
    8: [{"address": "F509A4", "size": 0x6},
        {"address": "F509C4", "size": 0x12}]
}
// use an array listing the data to retrieve, the chain is init at auto tracker start
var dataToAskChain = [];
// the current position in the chain
var dataToAskStep = 0;

// state
var stateDataEnum = {
    "state": 0,
    "debug": 2,
    "rta1": 4,
    "rta2": 6,
    "saveSlot": 8,
    "sramStats": 0xa
}

// maps
var mapOffsetEnum = {
    "curMap": 0,
    "Crateria": 0,
    "Brinstar": 0x100,
    "Norfair": 0x200,
    "WreckedShip": 0x300,
    "Maridia": 0x400,
    "Tourian": 0x500
}

// samus
var samusEnum = {
    "x": 0,
    "y": 2,
    "roomPointer": 4,
    "roomIndex": 6,
    "areaIndex": 8,
    "roomX": 10,
    "roomY": 12
}

// areas
var areaEnum = {
    0: "Crateria",
    1: "Brinstar",
    2: "Norfair",
    3: "WreckedShip",
    4: "Maridia",
    5: "Tourian",
    6: "Ceres",
    7: "Debug"
}

// bit masks for all datas
var areaAccessPoints = {{response.write(areaAccessPoints, escape=False)}};
var bossAccessPoints = {{response.write(bossAccessPoints, escape=False)}};
var escapeAccessPoints = {{response.write(escapeAccessPoints, escape=False)}};
var bossBitMasks = {{response.write(bossBitMasks, escape=False)}};
var nothingScreens = {{response.write(nothingScreens, escape=False)}};
var doorsScreen = {{response.write(doorsScreen, escape=False)}};
var eventsBitMasks = {};
let inventoryBitMasks = {{response.write(inventoryBitMasks, escape=False)}};

// in js dict keys are strings
var itemsBitMasks = {
    0x00: 0xFF,
    0x01: 0xFF,
    0x02: 0xFF,
    0x03: 0xFF,
    0x04: 0xFF,
    0x05: 0xFF,
    0x06: 0xFF,
    0x07: 0xFF,
    0x08: 0xFF,
    0x09: 0xFF,
    0x0A: 0xFF,
    0x10: 0xFF,
    0x11: 0xFF,
    0x12: 0xFF,
    0x13: 0xFF
}

function resetLog() {
    document.getElementById("logAutoTracker").value = "";
}

function appendLog(msg) {
    console.log(msg);
    var txtArea = document.getElementById("logAutoTracker");
    txtArea.value +=  msg + '\r\n';

    // auto scroll to bottom
    txtArea.scrollTop = txtArea.scrollHeight;
}

function setAutoTrackerIcon(icon) {
  var names = ["statusOK", "statusKO", "statusLoad", "statusNA"];
  for(var i=0; i<names.length; i++) {
    if(names[i] == icon){
      document.getElementById(names[i]).style.display = "block";
    } else {
      document.getElementById(names[i]).style.display = "none";
    }
  }
}

function displayStopButton() {
    document.getElementById("stopAutoTracker").style.display = "block";
    document.getElementById("startAutoTracker").style.display = "none";
}

function displayStartButton() {
    document.getElementById("startAutoTracker").style.display = "block";
    document.getElementById("stopAutoTracker").style.display = "none";
}

function startAutoTracker() {
    if(interfaceIsFrozen()) {
        return;
    }

    if(mode == 'race') {
        alert("Auto Tracker is disabled with race protected seeds");
        return;
    }

    // in case a snes classic retry was in progress
    if(retryTimeout != undefined) {
        clearTimeout(retryTimeout);
        retryTimeout = undefined;
    }

    resetLog();
    appendLog("\r\n\u2026 Starting Auto Tracker");
    // open websocket
    var url = 'ws://localhost:8080';
    socket = new WebSocket(url);
    socket.onopen = socketOnOpen;
    socket.onmessage = socketOnMessage;
    socket.onclose = socketOnClose;
    socket.onerror = socketOnError;

    // update state
    curState = stateEnum.opening;
    autoTrackInProgress = true;

    // update interface
    displayStopButton();
    setAutoTrackerIcon("statusLoad");
}

function closeSocket() {
    socket.close(1000);

    // update state
    curState = stateEnum.closing;

    // update interface
    setAutoTrackerIcon("statusLoad");
    setSamusIcon()
}

function stopAutoTracker() {
    if(loaded == false || webServInProgress == true || init == false || autoTrackInProgress == false) {
        return;
    }

    appendLog("\u2026 Stopping Auto Tracker");
    closeSocket();

    // update interface
    displayStartButton();
}

function socketOnOpen(e) {
    appendLog("\u2705 Connection established");
    // appendLog(" bufferedAmount: "+socket.bufferedAmount);
// Constant 	Value
// WebSocket.CONNECTING 	0
// WebSocket.OPEN 	1
// WebSocket.CLOSING 	2
// WebSocket.CLOSED 	3
    // appendLog(" readyState: "+socket.readyState);

    appendLog("\u2026 Asking Device List");
    sendAutoTrackerMessage({
        "Opcode" : "DeviceList",
        "Space" : "SNES"
    }, stateEnum.listing);
}

function socketOnMessage(event) {
    if(curState == stateEnum.looping) {
        socketOnLoopMessage(event);
    } else {
        socketOnInitMessage(event);
    }
}

function socketOnInitMessage(event) {
    console.log(`event.data: ${event.data}`);
    var data = JSON.parse(event.data);
    var results = data["Results"];
    // appendLog(`Data received: ${results}`);
    setAutoTrackerIcon("statusOK");

    if(curState == stateEnum.listing) {
        if(results.length == 0) {
            appendLog("\u274C no device found");
            closeSocket();
        } else if(results.length > 1) {
            appendLog("\u274C too many devices found, please connect only one");
            closeSocket();
        } else {
            var deviceToAttach = results;
            appendLog(`\u2705 device found: ${deviceToAttach}`);

            appendLog("\u2026 Attaching to Device");
            sendAutoTrackerMessage({
                "Opcode" : "Attach",
                "Space" : "SNES",
                "Operands" : deviceToAttach
            }, stateEnum.infoing);

            // tell qusb our app name
            appendLog("\u2026 Send VARIA app name");
            sendAutoTrackerMessage({
                "Opcode" : "Name",
                "Space" : "SNES",
                "Operands": ["VARIA Tracker"]
            }, stateEnum.infoing);

            // send info command to validate attaching, we can send it right away as there's a queue in qusb
            appendLog("\u2026 Getting Device Info");
            sendAutoTrackerMessage({
                "Opcode" : "Info",
                "Space" : "SNES"
            }, stateEnum.infoing);

        }
    } else if(curState == stateEnum.infoing) {
        appendLog(`\u2705 info received: ${results}`);
        appendLog(`\u2705 device attached`);

        // keep device type, results is an array, device type is in 2nd position
        device = results[1];
        console.log(`device: [${device}]`);

        // reset snes classic retries
        retryCount = 0;
        reconnectInProgress = false;

        // start loop, update state
        curState = stateEnum.looping;

        // ask socket to return an arraybuffer instead of a blob
        socket.binaryType = "arraybuffer";

        // display initial time
        document.getElementById("rtaTimer").innerHTML = "00'00'00''00";
        document.getElementById("rtaTimerDiv").style.display = "block";

        // first data retrieval
        initDataChain();
        askForData();
    } else {
        appendLog(`\u274C unknown receiving state ${curState}`);
        closeSocket();
    }
}

function socketOnLoopMessage(event) {
    setAutoTrackerIcon("statusOK");
    handleData(event.data);
}

function socketOnClose(event) {
    if(event.wasClean) {
        appendLog(`\u2705 Connection closed cleanly`);
        console.log(`socketOnClose clean: code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        appendLog('\u274C Connection died');
        console.log(`socketOnClose not clean: code=${event.code} reason=${event.reason}`);
    }
    setAutoTrackerIcon("statusNA");
    cleanup(event.wasClean);
}

function socketOnError(error) {
    appendLog("\u274C Connection error");

    // update state & interface
    setAutoTrackerIcon("statusKO");
    cleanup(false);
}

function cleanup(cleanExit) {
    // stop running timeout
    clearTimeout(timeout);

    // update state & interface
    cleanupBuffer();
    curState = stateEnum.closed;
    autoTrackInProgress = false;
    displayStartButton();
    setSamusIcon()
    // RTA
    document.getElementById("rtaTimerDiv").style.display = "none";
    disableRTAFake();

    // if the device is an SNES Classic try to reconnect in 1s,
    // as reseting the game on it will close the connection to the auto tracker
    if(reconnectInProgress == true || (cleanExit == false && retryCount < retryMax && device == "SNES Classic")) {
        reconnectInProgress = true;
        // sometimes socketOnClose and socketOnError are called, just arm the retry timer once
        if(retryTimeout == undefined) {
            appendLog(`will try to reconnect to SNES Classic in 1s ${retryCount}/${retryMax}`);
            retryTimeout = setTimeout(startAutoTracker, waitingTime);
            retryCount += 1;
        }
    } else {
        // use the device variable to know if we were connected to a device before
        device = undefined;

        // as autotracker now read inventory from memory we've lost the ordering of collecting items with
        // the locations so unvisite all locations
        ajaxCall({action: "clear", scope: "item"}, "upload");
    }
}

// called to request datas from qusb
function askForData() {
    // check current state
    if(curState != stateEnum.looping) {
        appendLog(`\u274C Wrong state: ${curState}`);
        closeSocket();
    } else {
        var metadata = dataToAsk[dataToAskChain[dataToAskStep]];
        askedDataSize = 0;
        var ranges = [];

        for(var i=0; i<metadata.length; i++) {
            askedDataSize += metadata[i].size;
            ranges.push(metadata[i].address);
            ranges.push(metadata[i].size.toString(16));
        }

        console.log(`\u2026 Asking ${askedDataSize} bytes of Data`);

        transfertStart = Date.now();
        sendAutoTrackerMessage({
            "Opcode" : "GetAddress",
            "Space" : "SNES",
            "Operands": ranges
        }, stateEnum.looping);
        setAutoTrackerIcon("statusLoad");
    }
}

function readWord(array, addr) {
    return (array[addr+1]<<8) + array[addr];
}

function getGameStateName(gameStateCode) {
    switch(gameStateCode) {
        case '0': return "Reset/start";
        case '1': return "Opening. Cinematic";
        case '2': return "Game options menu";
        case '3': return "Nothing (RTS)";
        case '4': return "Save game menus";
        case '5': return "Loading game map view";
        case '6': return "Loading game data";
        case '7': return "Setting game up after loading the game";
        case '8': return "Main gameplay";
        case '9': return "Hit a door block";
        case 'a': return "Loading next room";
        case 'b': return "Loading next room";
        case 'c': return "Pausing, normal gameplay but darkening";
        case 'd': return "Pausing, loading pause screen";
        case 'e': return "Paused, loading pause screen";
        case 'f': return "Paused, map and item screens";
        case '10': return "Unpausing, loading normal gameplay";
        case '11': return "Unpausing, loading normal gameplay";
        case '12': return "Unpausing, normal gameplay but brightening";
        case '13': return "Samus ran out of health";
        case '14': return "Samus ran out of health, black out surroundings";
        case '15': return "Samus ran out of health, black out surroundings";
        case '16': return "Samus ran out of health, starting death animation";
        case '17': return "Samus ran out of health, flashing";
        case '18': return "Samus ran out of health, explosion";
        case '19': return "Samus ran out of health, black out (also cut to by time up death)";
        case '1a': return "Game over screen";
        case '1b': return "Reserve tanks auto";
        case '1c': return "Unused. Does JMP ($0DEA) ($0DEA is never set to a pointer)";
        case '1d': return "Debug game over menu (end/continue)";
        case '1e': return "Intro. Cinematic. Set up entirely new game with cutscenes";
        case '1f': return "Set up new game. Post-intro";
        case '20': return "Made it to Ceres elevator";
        case '21': return "Blackout from Ceres";
        case '22': return "Ceres goes boom, Samus goes to Zebes. Cinematic";
        case '23': return "Time up";
        case '24': return "Whiting out from time up";
        case '25': return "Ceres goes boom with Samus. Cinematic";
        case '26': return "Samus escapes from Zebes. Transition from main gameplay to ending and credits";
        case '27': return "Ending and credits. Cinematic";
        case '28': return "Transition to demo";
        case '29': return "Transition to demo";
        case '2a': return "Playing demo";
        case '2b': return "Transition from demo";
        case '2c': return "Transition from demo";
        default: return `Unkown game state (${gameStateCode})`;
    }
}

function displayRTA(frames) {
    // 60 frame per second
    var timeSeconds = Math.floor(frames / 60);
    var remainFrames = frames % 60;
    var hours   = Math.floor(timeSeconds / 3600);
    var minutes = Math.floor((timeSeconds - (hours * 3600)) / 60);
    var seconds = timeSeconds - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    if (remainFrames < 10) {remainFrames = "0"+remainFrames;}

    document.getElementById("rtaTimer").innerHTML = `${hours}'${minutes}'${seconds}''${remainFrames}`;
}

function disableRTAFake() {
    if(incrRTA != undefined) {
        clearTimeout(incrRTA);
        incrRTA = undefined;
    }
}

function updateRTAFake() {
    var diffms = new Date() - incrRTAstart;
    // 60 frames per seconds
    rawTimeFrames += Math.floor(diffms / (1000/60));
    displayRTA(rawTimeFrames);
    incrRTAstart = new Date();
    incrRTA = setTimeout(updateRTAFake, RTAwaitingTime);
}

function updateRTA(frames, armFakeTimer) {
    displayRTA(frames);
    disableRTAFake();

    if(armFakeTimer) {
        // arm a timer to increase displayed RTA between two data retrieval
        rawTimeFrames = frames;
        incrRTAstart = new Date();
        incrRTA = setTimeout(updateRTAFake, RTAwaitingTime);
    }
}

// managed data returned by qusb
function handleData(data) {
    var chunk = new Uint8Array(data);
    var chunkSize = chunk.length
    receivedDataSize += chunkSize;
    receivedData.push(chunk);
    console.log(`\u2026 get: ${chunkSize} (${receivedDataSize}/${askedDataSize})`);

    if(receivedDataSize >= askedDataSize) {
        if(dataToAskChain[dataToAskStep] == dataEnum.state) {
            var duration = Date.now() - transfertStart;
            console.log(`\u2705 State data received in ${duration}ms`);

            var stateData = concatArrays(dataEnum.state);

            // biggest valid game state
            var maxGameState = 0x2c;
            var mainGameplayState = 0x08;
            var gameOverState = 0x1a;
            var creditState = 0x27;

            var gameState = readWord(stateData, stateDataEnum.state);
            var gameStateName = getGameStateName(gameState.toString(16));
            // appendLog(`\u2026 Game state: ${gameStateName}`);

            var debugMode = readWord(stateData, stateDataEnum.debug);
            // appendLog(`\u2026 Debug Mode: ${debugMode}`);

            // check if game is running and is metroid
            if(debugMode == 0 && gameState <= maxGameState) {
                // handle RTA
                if(gameState >= mainGameplayState && gameState <= gameOverState) {
                    var w0 = readWord(stateData, stateDataEnum.rta1);
                    var w1 = readWord(stateData, stateDataEnum.rta2);
                    var rawTimeFrames = w1 << 16 | w0;
                    updateRTA(rawTimeFrames, true);
                } else if(gameState == creditState) {
                    // during the credits the last RTA has been copied to SRAM
                    var save = readWord(stateData, stateDataEnum.saveSlot);
                    var offset = stateDataEnum.sramStats + save * 0x4;
                    var w0 = readWord(stateData, offset);
                    var w1 = readWord(stateData, offset+2);
                    var rawTimeFrames = w1 << 16 | w0;
                    updateRTA(rawTimeFrames, false);
                } else {
                    // if the user reset, stop incrementing the RTA
                    disableRTAFake();
                }

                if(gameState == mainGameplayState) {
                    appendLog(`\u2705 Gameplay state: ${gameStateName}`);
                    askNextData();
                } else {
                    appendLog(`\u231B State: ${gameStateName}`);
                    resetNextDataChain();
                }
            } else {
                appendLog("\u231B Super Metroid is not running");
                resetNextDataChain();
            }
        } else if(dataToAskChain[dataToAskStep] == dataEnum.map) {
            var duration = Date.now() - transfertStart;
            console.log(`\u2705 Map data received in ${duration}ms`);

            // concatenate all arrays
            mapData = concatArrays(dataEnum.map);

            askNextData();
        } else if(dataToAskChain[dataToAskStep] == dataEnum.curMap) {
            var duration = Date.now() - transfertStart;
            console.log(`\u2705 Current Map data received in ${duration}ms`);

            // concatenate all arrays
            var curMapData = concatArrays(dataEnum.curMap);

            // replace current map data in map data
            var areaIndex = readWord(samusData, samusEnum.areaIndex);
            var tourianAreaIndex = 5;
            if(areaIndex <= tourianAreaIndex) {
                var mapOffset = mapOffsetEnum[areaEnum[areaIndex]];
                var mapSize = 0x100;

                for(var i=0; i<mapSize; i++) {
                    mapData[mapOffset+i] = curMapData[i];
                }
            }

            askNextData();
        } else if(dataToAskChain[dataToAskStep] == dataEnum.samus) {
            var duration = Date.now() - transfertStart;
            console.log(`\u2705 Samus data received in ${duration}ms`);

            // concatenate all arrays
            samusData = concatArrays(dataEnum.samus);

            // extract data we need
            var samusX = readWord(samusData, samusEnum.x);
            var samusY = readWord(samusData, samusEnum.y);
            var roomPointer = readWord(samusData, samusEnum.roomPointer).toString(16);
            var x = Math.floor(samusX / 0x100);
            var y = Math.floor(samusY / 0x100);
            setSamusIcon(roomPointer, x, y);

            newAP = getNewAP(roomPointer, x, y);

            // uncomment to display current samus position in map in console
            // compute (byte, bit) index in map data for current samus screen
            // Let
            //     x = [room X co-ordinate] + [$12] / 100h
            //     y = [room Y co-ordinate] + [$18] / 100h
            // Then
            //     $07FB + (y + (x & 20h)) * 4 + (x & 1Fh) / 8 |= 80h >> (x & 7)
            var areaIndex = readWord(samusData, samusEnum.areaIndex);
            var roomX = readWord(samusData, samusEnum.roomX);
            var roomY = readWord(samusData, samusEnum.roomY);
            var x = roomX + Math.floor(samusX / 0x100);
            var y = roomY + Math.floor(samusY / 0x100);
            var byteIndex = (y + (x & 0x20)) * 4 + Math.floor((x & 0x1F) / 8);
            // first line of map is unused, so add 4 to ignore it (8 bytes per lines, but 4 in each page)
            byteIndex += 4;
            var bitMask = 0x80 >> (x & 7);
            console.log(`cur byteIndex: ${byteIndex} bitMask: ${bitMask} room: ${roomPointer} area: ${areaEnum[areaIndex]}`);

            askNextData();
        } else if(dataToAskChain[dataToAskStep] == dataEnum.items) {
            var duration = Date.now() - transfertStart;
            console.log(`\u2705 Items data received in ${duration}ms`);

            // concatenate all arrays
            itemsData = concatArrays(dataEnum.items);

            askNextData();
        } else if(dataToAskChain[dataToAskStep] == dataEnum.boss) {
            var duration = Date.now() - transfertStart;
            console.log(`\u2705 Boss data received in ${duration}ms`);

            // concatenate all arrays
            bossData = concatArrays(dataEnum.boss);

            askNextData();
        } else if(dataToAskChain[dataToAskStep] == dataEnum.events) {
            var duration = Date.now() - transfertStart;
            console.log(`\u2705 Events data received in ${duration}ms`);

            // concatenate all arrays
            eventsData = concatArrays(dataEnum.events);

            askNextData();
        } else if (dataToAskChain[dataToAskStep] === dataEnum.inventory) {
            let duration = Date.now() - transfertStart;
            console.log(`\u2705 Inventory data received in ${duration}ms`);

            // concatenate all arrays
            inventoryData = concatArrays(dataEnum.inventory);

            askNextData();
        }
    }
}

function getDataSize(dataType) {
    var metadata = dataToAsk[dataType];
    var dataSize = 0;
    for(var i=0; i<metadata.length; i++) {
        dataSize += metadata[i].size;
    }
    return dataSize;
}

function concatArrays(dataType) {
    if(receivedData.length == 1) {
        return receivedData[0];
    } else {
        dataSize = getDataSize(dataType);

        var data = new Uint8Array(dataSize);
        var curPos = 0;

        for(var i=0; i<receivedData.length; i++) {
            data.set(receivedData[i], curPos);
            curPos += receivedData[i].length;
        }

        return data;
    }
}

var newAP = "";
function getNewAP(roomPointer, x, y) {
    // when samus enters a new graph area update the current access point
    newAP = lastAP;
    if(roomPointer in rooms && 'graphArea' in rooms[logic][roomPointer]) {
        var curGraphArea = apsGraphArea[lastAP];
        if(curGraphArea != rooms[logic][roomPointer]['graphArea']) {
            newAP = rooms[logic][roomPointer]['nearestAP'];
            if(newAP == multipleAPs) {
                // there's multiple APs in the room, choose the nearest one from samus position
                newAP = rooms[logic][roomPointer]['screens'][y][x];
            }
        }
    }
    return newAP;
}

function getMapDisplayCoord(byteIndex, bitMask) {
    // http://patrickjohnston.org/bank/90#fA8A6
    //
    // Map tiles explored (for current area). One bit per room.
    // Laid out like a 64x32 1bpp VRAM tilemap:
    //   2x1 pages of 32x32 map tiles (80h bytes per page, 4 bytes per row, 1 bit per tile),
    //   each byte is 8 map tiles where the most significant bit is the leftmost tile.
    //
    // Let
    //     x = [room X co-ordinate] + [$12] / 100h
    //     y = [room Y co-ordinate] + [$18] / 100h
    // Then
    //     $07FB + (y + (x & 20h)) * 4 + (x & 1Fh) / 8 |= 80h >> (x & 7)
    // are we in the first or second page

    // squares we are drawing
    var width = 8;
    var height = 8;

    var y = (byteIndex < 128) ? byteIndex : byteIndex - 128;
    // each line in a page is 4 bytes.
    // our squares are 8 pixels high.
    y = (y >> 2) * height;
    // are we in the first or second page
    var baseX = (byteIndex < 128) ? 0 : 4;
    // each bit is a square on the map, so 8 squares per byte
    baseX = (baseX + (byteIndex % 4)) * 8 * width;
    var j = Math.log2(bitMask);
    var x = baseX + (7 - j) * width;

    return [x, y];
}

function cleanupBuffer() {
    askedDataSize = 0;
    receivedDataSize = 0;
    receivedData = [];
}

function initDataChain() {
    // always ask for game state first
    dataToAskChain = [dataEnum.state];

    stateDataOffsets = {};
    var curOffset = 0;

    // ask item locs & boss
    dataToAskChain.push(dataEnum.items);
    stateDataOffsets[dataEnum.items] = curOffset;
    curOffset += getDataSize(dataEnum.items);

    dataToAskChain.push(dataEnum.boss);
    stateDataOffsets[dataEnum.boss] = curOffset;
    curOffset += getDataSize(dataEnum.boss);

    // ask samus position to know the current map area
    dataToAskChain.push(dataEnum.samus);

    // ask for events
    dataToAskChain.push(dataEnum.events);
    stateDataOffsets[dataEnum.events] = curOffset;
    curOffset += getDataSize(dataEnum.events);

    // ask for inventory
    dataToAskChain.push(dataEnum.inventory);
    stateDataOffsets[dataEnum.inventory] = curOffset;
    curOffset += getDataSize(dataEnum.inventory);

    // ask optional map data
    if(area || boss || doorsRando || hasNothing || escapeRando) {
        dataToAskChain.push(dataEnum.map);
        stateDataOffsets[dataEnum.map] = curOffset;
        curOffset += getDataSize(dataEnum.map);

        dataToAskChain.push(dataEnum.curMap);
    }

    // start at the beginning of the chain
    dataToAskStep = 0;

    // instantiate state/mask arrays (arrays are initialized with zeros)
    stateArraySize = curOffset;
    currentState = new Uint8Array(stateArraySize);
    stateBitMasks = new Uint8Array(stateArraySize);
    previousStateChksum = 0;
    computeStateBitMasks();
}

function computeStateBitMasks() {
    var curOffset = 0;

    for(var i=0; i<dataToAskChain.length; i++) {
        if(dataToAskChain[i] == dataEnum.items) {
            var curOffset = stateDataOffsets[dataEnum.items];
            for(var byteIndex in itemsBitMasks) {
                // in js dict keys are strings
                byteIndexInt = parseInt(byteIndex);
                stateBitMasks[curOffset + byteIndexInt] |= itemsBitMasks[byteIndex];
            }
        } else if(dataToAskChain[i] == dataEnum.boss) {
            var curOffset = stateDataOffsets[dataEnum.boss];
            for(var bossName in bossBitMasks) {
                stateBitMasks[curOffset + bossBitMasks[bossName]["byteIndex"]] |= bossBitMasks[bossName]["bitMask"];
            }
        } else if(dataToAskChain[i] == dataEnum.map) {
            var curOffset = stateDataOffsets[dataEnum.map];
            if(area) {
                // loop on areaAccessPoints
                for(var apName in areaAccessPoints[logic]) {
                    var apData = areaAccessPoints[logic][apName];
                    stateBitMasks[curOffset + apData["byteIndex"] + mapOffsetEnum[apData["area"]]] |= apData["bitMask"];
                }
            }
            if(boss) {
                // loop on bossAccessPoints
                for(var apName in bossAccessPoints[logic]) {
                    var apData = bossAccessPoints[logic][apName];
                    stateBitMasks[curOffset + apData["byteIndex"] + mapOffsetEnum[apData["area"]]] |= apData["bitMask"];
                }
            }
            if(doorsRando) {
                for(var doorName in doorsScreen[logic]) {
                    var doorData = doorsScreen[logic][doorName];
                    stateBitMasks[curOffset + doorData["byteIndex"] + mapOffsetEnum[doorData["area"]]] |= doorData["bitMask"];
                }
            }
            if(hasNothing) {
                for(var locName in nothingScreens[logic]) {
                    var locData = nothingScreens[logic][locName];
                    stateBitMasks[curOffset + locData["byteIndex"] + mapOffsetEnum[locData["area"]]] |= locData["bitMask"];
                }
            }
            if(escapeRando) {
                for(var apName in escapeAccessPoints[logic]) {
                    var apData = escapeAccessPoints[logic][apName];
                    stateBitMasks[curOffset + apData["byteIndex"] + mapOffsetEnum[apData["area"]]] |= apData["bitMask"];
                }
            }
        } else if(dataToAskChain[i] == dataEnum.events) {
            var curOffset = stateDataOffsets[dataEnum.events];
            for(var event in eventsBitMasks) {
                stateBitMasks[curOffset + eventsBitMasks[event]["byteIndex"]] |= eventsBitMasks[event]["bitMask"];
            }
        } else if(dataToAskChain[i] === dataEnum.inventory) {
            let curOffset = stateDataOffsets[dataEnum.inventory];
            for(let item in inventoryBitMasks) {
                // If no bit mask defined, this is a two byte quantity (missiles, energy, etc.)
                if (inventoryBitMasks[item]["bitMask"]) {
                    stateBitMasks[curOffset + inventoryBitMasks[item]["byteIndex"]] |= inventoryBitMasks[item]["bitMask"];
                }
                else {
                    let bitOffset = curOffset + inventoryBitMasks[item]["byteIndex"];
                    stateBitMasks[bitOffset] |= 0xFF;
                    stateBitMasks[bitOffset + 1] |= 0xFF;
                }
            }
        }
    }
}

// called after a state upload to rearm the timer
function postAjaxHook() {
    if (window.ajaxChainedActions.length > 0) {
        return
    }

    var duration = Date.now() - transfertStart;
    appendLog(`\u2705 Backend updated in ${duration}ms`);

    resetNextDataChain();
}

function updateGlobalHook(jsonData) {
    // get eventsBitMasks if preset
    if("eventsBitMasks" in jsonData) {
        eventsBitMasks = jsonData["eventsBitMasks"];
    }
}

function resetNextDataChain() {
    cleanupBuffer();
    // start at the beginning of the chain
    dataToAskStep = 0;
    // rearm timer
    timeout = setTimeout(askForData, waitingTime);
}

function askNextData() {
    // reset data vars
    cleanupBuffer();

    dataToAskStep++;

    if(dataToAskStep < dataToAskChain.length) {
        // next step
        askForData();
    } else {
        // we've collected all the required data, check if there's a state change,
        // return true if no state change, so we can rearm the timer
        if(checkCollectedData()) {
            // restart chain
            resetNextDataChain();
        }
    }
}

function checkCollectedData() {
    // populate state
    populateCurrentState();

    // compute crc32
    // TODO::check if we can reuse the same crc32 instance
    var crc32 = new Crc32();
    crc32.update(currentState);
    var newStateChksum = crc32.digest();
    console.log(`State Checksum: ${newStateChksum}`);

    if(newStateChksum == previousStateChksum && newAP == lastAP) {
        appendLog("\u2705 State is the same");

        // rearm the timer for next data retrieval
        return true;
    } else {
        appendLog("\u2705 New state detected");

        previousStateChksum = newStateChksum;

        transfertStart = Date.now();

        // send state to backend
        ajaxCall({action: "import",
                  scope: "dump",
                  stateDataOffsets: JSON.stringify(stateDataOffsets),
                  currentState: jsonArray(currentState),
                  newAP: newAP}, "upload");

        return false;
    }
}

function jsonArray(array) {
    // json.stringify on a uint8array changes it to a dict...
    var ret = '['+array[0];
    for(var i=1; i<array.length; i++) {
        ret += ', '+array[i];
    }
    ret += ']';
    return ret;
}

function populateCurrentState() {
    // reset current state
    currentState.fill(0);

    // add data to state
    for(var j=0; j<dataToAskChain.length; j++) {
        if(dataToAskChain[j] == dataEnum.items) {
            var curOffset = stateDataOffsets[dataToAskChain[j]];
            for(var i=0; i<itemsData.length; i++) {
                currentState[curOffset + i] = itemsData[i] & stateBitMasks[curOffset + i];
            }
        } else if(dataToAskChain[j] == dataEnum.boss) {
            var curOffset = stateDataOffsets[dataEnum.boss];
            for(var i=0; i<bossData.length; i++) {
                currentState[curOffset + i] = bossData[i] & stateBitMasks[curOffset + i];
            }
        } else if(dataToAskChain[j] == dataEnum.map) {
            var curOffset = stateDataOffsets[dataEnum.map];
            for(var i=0; i<mapData.length; i++) {
                currentState[curOffset + i] = mapData[i] & stateBitMasks[curOffset + i];
            }
        } else if(dataToAskChain[j] == dataEnum.events) {
            var curOffset = stateDataOffsets[dataEnum.events];
            for(var i=0; i<eventsData.length; i++) {
                currentState[curOffset + i] = eventsData[i] & stateBitMasks[curOffset + i];
            }
        } else if(dataToAskChain[j] === dataEnum.inventory) {
            let curOffset = stateDataOffsets[dataEnum.inventory];
            for(let i=0; i<inventoryData.length; i++) {
                currentState[curOffset + i] = inventoryData[i] & stateBitMasks[curOffset + i];
            }
        }
    }
}

function sendAutoTrackerMessage(data, newState) {
    socket.send(JSON.stringify(data));

    // update state
    curState = newState;

    // update interface
    setAutoTrackerIcon("statusLoad");
}
