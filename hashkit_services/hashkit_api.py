from flask import Flask, url_for, request
from xminer_command import XMinerCommand
import os, json

app_dir = '/home/ubuntu/Hash-Kit/'
application = Flask(__name__, static_folder= app_dir + 'public/')
application.config['UPLOAD_FOLDER'] =  app_dir + 'public/media/'
application.config['SESSION_TYPE'] = 'filesystem'
application.config.from_object(__name__)

if (os.path.exists(app_dir + 'hashkit_resources/ranges.json')):

    pass

else:

    with open(app_dir + 'hashkit_resources/ranges.json', 'w') as hashkit_ip_ranges_file:

        init_json = {}
        json.dump(init_json, hashkit_ip_ranges_file)

@application.route('/', methods=['GET'])
def hashkit_main():

    overheating_items_html = ""
    low_hashrate_items_html = ""
    zeroes_items_html = ""
    timeouts_items_html = ""
    error_miners_html = ""

    with open(app_dir + 'hashkit_resources/overheating.json', 'r') as overheating_file:

        overheating_miners = json.load(overheating_file)

    for om in overheating_miners.keys():

        overheating_items_html = overheating_items_html + '<a href="http://' + om + '"><p class="warning_item">' + om + '</p></a>'

    with open(app_dir + 'hashkit_resources/low_hashrate.json', 'r') as low_hashrate_file:

        low_hashrate_miners = json.load(low_hashrate_file)

    for lh in low_hashrate_miners.keys():

        low_hashrate_items_html = low_hashrate_items_html + '<a href="http://' + lh + '"><p class="warning_item">' + lh + '</p></a>'

    with open(app_dir + 'hashkit_resources/zeroes.json', 'r') as zeroes_file:

        miner_zeroes = json.load(zeroes_file)

    for zi in miner_zeroes.keys():

        zeroes_items_html = zeroes_items_html + '<a href="http://' + zi + '"><p class="warning_item">' + zi + '</p></a>'

    with open(app_dir + 'hashkit_resources/timeouts.json', 'r') as timeouts_file:

        miner_timeouts = json.load(timeouts_file)

    for to in miner_timeouts.keys():

        timeouts_items_html = timeouts_items_html + '<a href="http://' + to + '"><p class="warning_item">' + to + '</p></a>'

    with open(app_dir + 'hashkit_resources/errors.json', 'r') as errors_file:

        miner_errors = json.load(errors_file)

    for em in miner_errors.keys():

        error_miners_html = error_miners_html + '<a href="http://' + em + '"><p class="warning_item">' + em + '</p></a>'

    with open(app_dir + 'hashkit_resources/summaries.json', 'r') as summaries_file:

        farm_summary = json.load(summaries_file)

    total_petahash = farm_summary["total_petahash"]
    total_miners_hashing = farm_summary['total_miners_hashing']
    percentage_miners_hashing = farm_summary['percentage_miners_hashing']
    highest_temperature = farm_summary['highest_temperature']
    lowest_temperature = farm_summary['lowest_temperature']
    timeouts = farm_summary['timeouts']
    overheating = len(overheating_miners.keys())
    low_hashrate = len(low_hashrate_miners.keys())
    zeroes = farm_summary['zeroes']
    error_miner_count = farm_summary['errors']
    average_temperature = (int(highest_temperature) + int(lowest_temperature)) / 2

    with open(app_dir + 'public/pages/hashkit.html', 'r') as ui_code_source:

        ui_code = ui_code_source.read()

    style = url_for('static', filename='styles/hashkit_style.css')
    script = url_for('static', filename='scripts/hashkit_main.js')

    return ui_code.format(style, total_petahash, total_miners_hashing, percentage_miners_hashing, average_temperature, highest_temperature, lowest_temperature, zeroes, zeroes_items_html, timeouts, timeouts_items_html, overheating, overheating_items_html, low_hashrate, low_hashrate_items_html, error_miner_count, error_miners_html, script) 

@application.route('/equery', methods=['POST'])
def expectation_query():

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):

        json_body = request.json

    else:

        return {"status": "Content-Type not supported!"}

    with open(app_dir + 'hashkit_resources/miner_types.json', 'r') as miner_types_file:

        miner_types = json.load(miner_types_file)

    command = json_body['command']

    if (command == 'get'):

        miner_types_dd_list = '<option value="Select Miner Type">Select Miner Type</option>'

        for miner_type in miner_types.keys():

            miner_types_dd_list = miner_types_dd_list + '<option value="' + miner_type + '">' + miner_type + '</option>'

        return {"status": "success", "types": miner_types_dd_list}


    if (command == 'add'):

        selected_miner_type = list(json_body.keys())[0]
        selected_miner_expectations = json_body[selected_miner_type]
        miner_types[selected_miner_type] = selected_miner_expectations

        with open(app_dir + 'hashkit_resources/miner_types.json', 'w') as miner_types_file:

            json.dump(miner_types, miner_types_file)

        return {"status": "success"}

    elif (command == 'rem'):

        range_nicknames = list(json_body['ranges'])

        for range_nickname in range_nicknames:

            del miner_types[range_nickname]

        with open(app_dir + 'hashkit_resources/miner_types.json', 'w') as miner_types_file:

            json.dump(miner_types, miner_types_file)

        return {"status": "success"}

    elif (command == 'exp'):

        miner_expectations = {}

        for miner_expectation in miner_types.keys():

            if miner_types[miner_expectation] != []:

                miner_expectations[miner_expectation] = miner_types[miner_expectation]

        return {"status": "success", "expectations": miner_expectations}

@application.route('/rquery', methods=['POST'])
def range_query():

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):

        json_body = request.json

    else:

        return {"status": "Content-Type not supported!"}

    command = json_body['command']

    with open(app_dir + 'hashkit_resources/ranges.json', 'r') as hashkit_ip_ranges_file:
                            
        hashkit_ip_ranges = json.load(hashkit_ip_ranges_file)

    if (command == 'get'):

        return {"status": "success", "ranges": hashkit_ip_ranges}

    if (command == 'add'):

        range_nickname = list(json_body.keys())[0]
        address_ranges = json_body[range_nickname]

        hashkit_ip_ranges[range_nickname] = address_ranges

        with open(app_dir + 'hashkit_resources/ranges.json', 'w') as hashkit_ip_ranges_file:

            json.dump(hashkit_ip_ranges, hashkit_ip_ranges_file, sort_keys=True)

        return {"status": "success"}

    elif (command == 'rem'):

        range_nicknames = list(json_body['ranges'])

        for range_nickname in range_nicknames:

            del hashkit_ip_ranges[range_nickname]
            
            if os.path.isfile(app_dir + 'hashkit_resources/range_data/' + range_nickname + '.json'):

                os.remove(app_dir + 'hashkit_resources/range_data/' + range_nickname + '.json')

        with open(app_dir + 'hashkit_resources/ranges.json', 'w') as hashkit_ip_ranges_file:

            json.dump(hashkit_ip_ranges, hashkit_ip_ranges_file)

        return {"status": "success"}

    elif (command == 'view'):

        range_nickname = json_body['range_name']

        with open(app_dir + 'hashkit_resources/range_data/' + range_nickname + '.json', 'r') as range_data_file:

            range_data = json.load(range_data_file)

        return {"status": "success", "payload": range_data}

    else:

        return {"status": "invalid command"}

@application.route('/mquery', methods=['POST'])
def miner_query():

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):

        json_body = request.json

    else:

        return 'Content-Type not supported!'

    command = json_body['command']
    return {"status": "invalid command"}