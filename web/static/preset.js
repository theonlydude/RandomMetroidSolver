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
  Object.entries(data.Settings).forEach(([key, value]) => {
    document.getElementById(key).value = value
  })

  const levels = []
  const is_checked = {}
  const not_checked = {}
  Object.entries(data.Knows).forEach(([key, value]) => {
    const [checked, level] = value
    const checkbox = document.getElementById(key + "_bool")
    if (checkbox.disabled) {
      return
    }
    if (!checked) {
      is_checked[level] = true
    } else {
      not_checked[level] = true
    }
    checkbox.checked = checked
    checkbox.dispatchEvent(new Event('change'));

    const difficulty = difficulty_by_level[level]
    const selector = `#${key}_diff + .br-widget [data-rating-value="${difficulty}"]`
    const bar = document.querySelector(selector)
    bar.click()

    Object.entries(data.Controller).forEach(([key, value]) => {
      if (key === "Moonwalk") {
        document.getElementById("Moonwalk").checked = value === "on"
        return
      }
      const select = document.getElementById(key)
      select.value = value
      select.dispatchEvent(new Event('change'));
    })

  })
  verifyPreset(data)
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
    const value_in = data_in.Settings[key]
    const value_out = data_out[key]
    compare('Settings', key, value_in, value_out)
  });

  // these are skipped because they are disabled on front end
  const skip_knows = ['WallJump', 'ShineSpark', 'MidAirMorph', 'CrouchJump']

  Object.entries(data_in.Knows).forEach(([key, value]) => {
    if (skip_knows.includes(key)) {
      return
    }
    if (data_in.Knows[key][0]) {
      const bool_in = data_in.Knows[key][0] ? "on" : "off"
      const bool_out = data_out[key + '_bool']
      compare('Knows', key + '_bool', bool_in, bool_out)

      const diff_in = difficulty_by_level[data_in.Knows[key][1]]
      const diff_out = data_out[key + '_diff']
      compare('Knows', key + '_diff', diff_in, diff_out)
    } else {
      compare('Knows', key + '_bool', undefined, data_out[key + '_bool'])
      compare('Knows', key + '_diff', undefined, data_out[key + '_diff'])
    }
  });

  Object.entries(data_in.Controller).forEach(([key, value]) => {
    let value_in = data_in.Controller[key]
    const value_out = data_out[key]
    if (key === "Moonwalk") {
      value_in = value_in ? 'on' : 'off'
    }
    compare('Controller', key, value_in, value_out)
  });
}

function loadPreset() {
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

  request.done(loadPresetOk)
  request.fail((e) => console.error(e));
}