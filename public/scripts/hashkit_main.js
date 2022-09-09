function readCookie(name) {
    
    return (name = new RegExp('(?:^|;\\s*)' + ('' + name).replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&') + '=([^;]*)').exec(document.cookie)) && name[1];

}

var ip_ranges = {};

function getSelExpectations() {

  var miner_type_dd = document.getElementById("miner_type_list");
  var temp_threshold_dd = document.getElementById("temperatures_dd");
  var hashrate_threshold_dd = document.getElementById("hashrates");
  var selected_miner_type = miner_type_dd.options[miner_type_dd.selectedIndex].value;
  var selected_temp_threshold = temp_threshold_dd.options[temp_threshold_dd.selectedIndex].value;
  var selected_hashrate_threshold = hashrate_threshold_dd.options[hashrate_threshold_dd.selectedIndex].value;

  if (selected_miner_type.includes("Select") || selected_temp_threshold.includes("Select") || selected_hashrate_threshold.includes("Select")) {

    alert("You must make a selection for all three expectation fields.")
    return -1

  } else {

    return [JSON.stringify([selected_temp_threshold, selected_hashrate_threshold]), selected_miner_type];

  }

}

function addExpectation() {

  var url = '/equery';
  var expectations_object = getSelExpectations();

  if (expectations_object === -1) {

    return null;

  }

  var selected_miner_type = expectations_object[1];
  var selected_miner_expectations = expectations_object[0];
  var myObj = '{' + JSON.stringify(selected_miner_type) + ': ' + selected_miner_expectations + ',"command": "add"}';
  var data = JSON.parse(myObj);

  fetch(url, {

    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {

      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)

  }).then(response => response.json())
  .then(response => {

    if (response["status"] = "success") {

      alert("Expectation added successfully");
      document.getElementById("miner_type_list").selectedIndex = 0;
      document.getElementById("temperatures_dd").selectedIndex = 0;
      document.getElementById("hashrates").selectedIndex = 0;
      location.reload();

    } else {

      alert("An internal server error occurred, page will refresh");
      location.reload();

    }

  });

}

function getIPRange() {

  const ip_format = /\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/;
  var range_nickname = document.getElementById("n_add").value;
  var start_ip = document.getElementById("s_add").value;
  var end_ip = document.getElementById("e_add").value;

  if (range_nickname === "") {

    return -3;
    
  } else if (start_ip === "" || end_ip === "") {

    return -2;

  } else if (ip_ranges.hasOwnProperty(range_nickname)) {

    return -1;

  } else if (start_ip.match(ip_format) && end_ip.match(ip_format)) {

    return [JSON.stringify([start_ip, end_ip]), range_nickname];

  } else {

    return 0;

  }

}

function addIPRange() {

  var ip_range_info = getIPRange();

  if (ip_range_info === -3) {

    alert("Nickname cannot be blank");
  
  } else if (ip_range_info === -2) {

    alert("IP addresses cannot be blank");
  
  } else if (ip_range_info === -1) {

    alert("Nickname already used");
  
  } else if (ip_range_info === 0) {
  
    alert("Invalid IP address format");
  
  } else {
    
    var url = '/rquery';
    var ip_range = ip_range_info[0];
    var nickname = ip_range_info[1];
    var myObj = '{' + JSON.stringify(nickname) + ': ' + ip_range + ',"command": "add"}';
    var data = JSON.parse(myObj);

    fetch(url, {

      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {

        'Content-Type': 'application/json'

      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
      body: JSON.stringify(data)

    }).then(response => response.json())
    .then(response => {

      if (response["status"] = "success") {

        alert("Range added successfully");
        range_nickname = document.getElementById("n_add").value = "";
        start_ip = document.getElementById("s_add").value = "";
        end_ip = document.getElementById("e_add").value = "";
        location.reload();

      } else {

        alert("An internal server error occurred, page will refresh");
        location.reload();

      }
      
    });

  }

}

function getCheckedExpectations() {

  var range_items = document.getElementById("miner_expectations_container").getElementsByClassName("range_item");
  var sel_range_list = [];
  
  for (i=0; i<range_items.length; i++) {

    var existing_range_item = range_items[i];
    var existing_range_chx_state = existing_range_item.firstChild.checked;

    if (existing_range_chx_state === true) {
      
      sel_range_list.push(existing_range_item.childNodes[1].innerText);

    }

  }

  console.log(sel_range_list);
  return sel_range_list;

}

function getSelRanges() {

  var range_items = document.getElementById("range_container").getElementsByClassName("range_item");
  var sel_range_list = [];
  
  for (i=0; i<range_items.length; i++) {

    var existing_range_item = range_items[i];
    var existing_range_chx_state = existing_range_item.firstChild.checked;

    if (existing_range_chx_state === true) {
      
      sel_range_list.push(existing_range_item.childNodes[1].innerText);

    }

  }

  console.log(sel_range_list);
  return sel_range_list;

}

function delExpectation() {

  var url = "/equery";
  var del_range_list = getCheckedExpectations();
  var myObj = '{"ranges": ' + JSON.stringify(del_range_list) + ',"command": "rem"}';
  var data = JSON.parse(myObj);

  fetch(url, {

    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {

      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)

  }).then(response => response.json())
  .then(response => {

    if (response["status"] = "success") {

      alert("Expectation(s) removed successfully");
      location.reload();

    } else {

      alert("An internal server error occurred, page will refresh");
      location.reload();

    }

  });

}

function delIPRange() {

  var url = "/rquery";
  var del_range_list = getSelRanges();
  var myObj = '{"ranges": ' + JSON.stringify(del_range_list) + ',"command": "rem"}';
  var data = JSON.parse(myObj);

  fetch(url, {

    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {

      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)

  }).then(response => response.json())
  .then(response => {

    if (response["status"] = "success") {

      alert("Range(s) removed successfully");
      location.reload();

    } else {

      alert("An internal server error occurred, page will refresh");
      location.reload();

    }

  });

}

function showHideWarningDetail(e) {

  var target_element_id = e.target.getAttribute("name");;
  var target_element = document.getElementById(target_element_id);

  if (target_element.className !== "warning_detail_active") {

    e.target.innerText = "hide detail";
    target_element.className = "warning_detail_active";

  } else {

    e.target.innerText = "show detail";
    target_element.className = "warning_detail";

  }

}

window.onload = (e) => {

  var temp_threshold_dd = document.getElementById("temperatures_dd");

  for(i=80; i<106; i++) {

    var temp_option = document.createElement("option");
    temp_option.value = i;
    temp_option.innerText = i.toString();
    temp_threshold_dd.appendChild(temp_option);

  }

  var hashrate_threshold_dd = document.getElementById("hashrates");
  
  for(i=1; i<300; i++) {

    var hashrate_option = document.createElement("option");
    hashrate_option.value = i;
    hashrate_option.innerText = i.toString() + " TH/s";
    hashrate_threshold_dd.appendChild(hashrate_option);

  }

  var url = '/rquery';
  var myObj = '{"command": "get"}';
  var data = JSON.parse(myObj);

  fetch(url, {

    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {

      'Content-Type': 'application/json'

    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)

  }).then(response => response.json())
  .then(response => {

    ip_ranges = response["ranges"];
    var range_keys = Object.keys(ip_ranges);

    for (i=0; i<range_keys.length; i++) {
    
      var ip_range = ip_ranges[range_keys[i]];
      var range_container = document.getElementById("range_container");
      var range_item = document.createElement("div");
      var range_checkbox = document.createElement("input");
      var range_label = document.createElement("p");
      var range_addresses = document.createElement("p");
      range_checkbox.type = "checkbox";
      range_checkbox.id = "chx";
      range_checkbox.className = "range_checkbox";
      range_label.innerText = range_keys[i];
      range_addresses.innerText = ip_range.toString().replace(",", " - ");
      range_item.className = "range_item";
      range_label.className = "range_label";
      range_addresses.className = "range_addresses";
      range_item.append(range_checkbox);
      range_item.append(range_label);
      range_item.append(range_addresses);
      range_container.append(range_item);

    }

    var url = '/equery';
    var myObj = '{"command": "get"}';
    var data = JSON.parse(myObj);

    fetch(url, {

      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {

        'Content-Type': 'application/json'

      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
      body: JSON.stringify(data)

    }).then(response => response.json())
    .then(response => {

      miner_types_dd_content = response["types"];
      var miner_type_list_dd = document.getElementById("miner_type_list");
      miner_type_list_dd.innerHTML = miner_types_dd_content;

      var url = '/equery';
      var myObj = '{"command": "exp"}';
      var data = JSON.parse(myObj);

      fetch(url, {

        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {

          'Content-Type': 'application/json'

        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)

      }).then(response => response.json())
      .then(response => {

        miner_expectations_obj = response["expectations"];
        var expectations_types_list = Object.keys(miner_expectations_obj);
        var range_container = document.getElementById("miner_expectations_container");
        console.log(expectations_types_list);
        
        for (i=0; i<expectations_types_list.length; i++) {

          var range_item = document.createElement("div");
          var range_checkbox = document.createElement("input");
          var range_label = document.createElement("p");
          var range_addresses = document.createElement("p");
          range_checkbox.type = "checkbox";
          range_checkbox.id = "chx";
          range_checkbox.className = "range_checkbox";
          range_label.innerText = expectations_types_list[i];
          range_addresses.innerText = "Max Desired Temp: " + miner_expectations_obj[expectations_types_list[i]].toString().replace(",", " C,\n Min Expected Hashrate: ") + " TH/s";
          range_item.className = "range_item";
          range_label.className = "range_label";
          range_addresses.className = "range_addresses";
          range_item.append(range_checkbox);
          range_item.append(range_label);
          range_item.append(range_addresses);
          range_container.append(range_item);

        }

      });

    });

  });

  document.getElementById("add_expectation_button").addEventListener('click', function(e) {

    addExpectation();

  });
  
  document.getElementById("del_expectation_button").addEventListener('click', function(e) {

    delExpectation();

  });

  document.getElementById("add_range_button").addEventListener('click', function(e) {

    addIPRange();

  });
  
  document.getElementById("del_range_button").addEventListener('click', function(e) {

    delIPRange();

  });

  var warning_expanders = document.getElementsByClassName("warning_expander");
  
  for (w=0; w<warning_expanders.length; w++) {

    warning_expanders[w].addEventListener('click', function(e) {

      showHideWarningDetail(e);
  
    });

  }
  
}
