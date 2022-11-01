const difficulty_by_level = {
    1: 'easy',
    5: 'medium',
    10: 'hard',
    25: 'very hard',
    50: 'hardcore',
    100: 'mania',
    0: 'mania', // unchecked defaults to mania
}

function loadPresetOk(data) {
    $('#presetActionBox').removeClass('preset-loading');
    Object.entries(data.Settings).forEach(([key, value]) => {
        var setting = document.getElementById(key);
        setting.value = value;
        setting.dispatchEvent(new Event('change'));
    })

    Object.entries(data.Knows).forEach(([key, value]) => {
        const [checked, level] = value;
        const checkbox = document.getElementById(key + "_bool");
        if (checkbox.disabled) {
            return;
        }
        checkbox.value = checked ? 'on' : 'off';
        checkbox.checked = checked;
        checkbox.dispatchEvent(new Event('change'));
        checkbox.dispatchEvent(new Event('click'));

        const difficulty = difficulty_by_level[level];
        const selector = `#${key}_diff + .br-widget [data-rating-value="${difficulty}"]`;
        const bar = document.querySelector(selector);
        bar.click();
    })

    Object.entries(data.Controller).forEach(([key, value]) => {
        if (key === "Moonwalk") {
            const checkbox = document.getElementById("Moonwalk");
            checkbox.checked = value;
            checkbox.value = value ? 'on' : 'off';
            return;
        }
        const select = document.getElementById(key);
        select.value = value;
        select.dispatchEvent(new Event('change'));
    })

    loadSkillBar(data.skillBarData);
    drawSkillChart(data.skillBarData);
    verifyPreset(data);
}

function verifyPreset(data_in) {
    const compare = (category, key, value1, value2) => {
        if (value1 !== value2) {
            const text1 = JSON.stringify(value1);
            const text2 = JSON.stringify(value2);
            console.warn(`Mismatch for data.Knows.${key} ${text1} !== ${text2}`);
        }
    }
    const data_out = window.getPresetDataDict();

    Object.entries(data_in.Settings).forEach(([key, value]) => {
        const value_in = data_in.Settings[key];
        const value_out = data_out[key];
        compare('Settings', key, value_in, value_out);
    });

    // these are skipped because they are disabled on front end
    const skip_knows = ['WallJump', 'ShineSpark', 'MidAirMorph', 'CrouchJump'];

    Object.entries(data_in.Knows).forEach(([key, value]) => {
        if (skip_knows.includes(key)) {
            return;
        }
        if (data_in.Knows[key][0]) {
            const bool_in = data_in.Knows[key][0] ? "on" : "off";
            const bool_out = data_out[key + '_bool'];
            compare('Knows', key + '_bool', bool_in, bool_out);

            const diff_in = difficulty_by_level[data_in.Knows[key][1]];
            const diff_out = data_out[key + '_diff'];
            compare('Knows', key + '_diff', diff_in, diff_out);
        } else {
            compare('Knows', key + '_bool', undefined, data_out[key + '_bool']);
            compare('Knows', key + '_diff', undefined, data_out[key + '_diff']);
        }
    });

    Object.entries(data_in.Controller).forEach(([key, value]) => {
        let value_in = data_in.Controller[key];
        const value_out = data_out[key];
        if (key === "Moonwalk") {
            value_in = value_in ? 'on' : 'off';
        }
        compare('Controller', key, value_in, value_out);
    });
}

function loadPreset() {
    $('#flash').hide();
    $('#presetActionBox').addClass('preset-loading');
    var dataDict = {
        preset: document.getElementById("preset").value,
        action: "load",
        currenttab: document.getElementById("currenttab").value,
    };

    // call web service to update the session with the params from the rando preset and update the parameters in the page
    var request = $.ajax({
            url: "/skillPresetActionWebService",
            data: dataDict,
            dataType: "json"
    });

    request.done(loadPresetOk);
    request.fail((e) => {
        const flash = $("#flash");
        flash.text("An error occurred while loading preset. Please refresh the page and try again.");
        flash.show();
    })
}

function loadSkillBar(skillBarData) {
    const id_texts = [
        ['skill-bar__title', skillBarData.custom[0]],
        ['skill-bar__score', skillBarData.custom[1]],
        ['skill-bar__knows-known', skillBarData.knowsKnown],
        ['skill-bar__last-action', skillBarData.lastAction],
    ];
    id_texts.forEach(([id, text]) => {
        $("#"+id).text(text);
    })
}


function drawSkillChart(skillBarData) {
    const rows = [];

    const mult = 2;
    const score = 100 + skillBarData["custom"][1] * mult;
    const lower = 100 + skillBarData["standards"]["newbie"] * mult;
    const upper = 100 + skillBarData["standards"]["samus"] * mult;

    let previousStdScore = lower;
    let previousPreset = 'newbie';
    let stop = false;
    const presets = ['casual', 'regular', 'veteran', 'expert', 'master', 'samus'];
    presets.forEach((preset) => {
        if (stop) {
            return;
        }
        const stdScore = 100 + skillBarData["standards"][preset] * mult;
        if (stdScore <= score) {
            rows.push([ 'Skill', previousPreset, new Date(previousStdScore), new Date(stdScore)]);
        } else {
            rows.push([ 'Skill', previousPreset, new Date(previousStdScore), new Date(score)]);
            stop = true;
        }
        previousStdScore = stdScore;
        previousPreset = preset;
    })

    var container = document.getElementById('timeline');
    container.innerHTML = "";
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    dataTable.addColumn({ type: 'string', id: 'Role' });
    dataTable.addColumn({ type: 'string', id: 'Difficulty' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows(rows);

    var options = {
        hAxis: {
            minValue: new Date(lower),
            maxValue: new Date(upper),
        },
        timeline: { groupByRowLabel: true},
        tooltip: { trigger: 'none' },
        colors: ['#6daa53', '#C1B725', '#e69235', '#d13434', '#123456', '#000000'],
        avoidOverlappingGridLines: false
    };

    window.google.visualization.events.addListener(chart, 'ready', function () {
        // remove haxis label
        var labels = container.getElementsByTagName('text');

        for (let i = 0; i < labels.length; i++) {
            if (labels[i].textContent.substring(0,1) == '0' || labels[i].textContent.substring(0,1) == '1') {
                labels[i].parentNode.removeChild(labels[i]);
                i--;
            }
        }

    });
    chart.draw(dataTable, options);
}


