# tested firmwares:
# stock
# vnish
# should support anything running cgminer

from xminer_command import XMinerCommand
import os, json, time, math

app_dir = '/home/ubuntu/Hash-Kit/'
command = 'stats'

summary = {

    "total_petahash": str(0),
    "total_miners_hashing": str(0),
    "percentage_miners_hashing": str(0) + "%",
    "highest_temperature": str(0),
    "lowest_temperature": str(0),
    "zeroes": str(0),
    "errors": str(0),
    "timeouts": str(0)
    
}

with open(app_dir + 'hashkit_resources/summaries.json', 'w') as summaries_file:

    json.dump(summary, summaries_file)

while True:

    with open(app_dir + 'hashkit_resources/ranges.json', 'r') as hashkit_ip_ranges_file:
                        
        hashkit_ip_ranges = json.load(hashkit_ip_ranges_file)

    with open(app_dir + 'hashkit_resources/miner_types.json', 'r') as miner_types_file:

        miner_types = json.load(miner_types_file)

    total_hashrate_ghs = 0
    total_miners_hashing = 0
    percentage_miners_hashing = 0
    highest_temperature_c = 0
    lowest_temperature_c = 1000
    overheating = 0
    low_hashrate = 0
    timeouts = 0
    zeroes = 0
    problem_miners = 0
    overheating_miners = {}
    low_hashrate_miners = {}
    zeroes_miners = {}
    error_miners = {}
    timeout_addresses = {}

    for range_entity in hashkit_ip_ranges:

        selected_ip_range = hashkit_ip_ranges[range_entity]
        end_of_start_address = int(selected_ip_range[0][selected_ip_range[0].rindex(".") + 1:len(selected_ip_range[0])])
        end_of_end_address = int(selected_ip_range[1][selected_ip_range[1].rindex(".") + 1:len(selected_ip_range[1])])
        start_ip_parts = selected_ip_range[0].split(".")
        start_ip_parts = list(map(int, start_ip_parts))
        end_ip_parts = selected_ip_range[1].split(".")
        end_ip_parts = list(map(int, end_ip_parts))
        section_one_diff = end_ip_parts[0] - start_ip_parts[0] + 1
        section_two_diff = end_ip_parts[1] - start_ip_parts[1] + 1
        section_three_diff = end_ip_parts[2] - start_ip_parts[2] + 1
        section_four_diff = end_ip_parts[3] - start_ip_parts[3] + 1

        for a in range(section_one_diff):

            part_one = start_ip_parts[0] + a

            for b in range(section_two_diff):

                part_two = start_ip_parts[1] + b

                for c in range(section_three_diff):

                    part_three = start_ip_parts[2] + c

                    for d in range(section_four_diff):

                        miner_temp_threshold = 99999999999999999999
                        miner_hashrate_threshold = 0
                        part_four = start_ip_parts[3] + d
                        miner_address = str(part_one) + "." + str(part_two) + "." + str(part_three) + "." + str(part_four)
                        miner_stats = XMinerCommand.command_miner(command, miner_address)

                        if miner_stats == b'timeout':

                            timeouts = timeouts + 1
                            timeout_addresses[miner_address] = ""
                            continue

                        try:

                            miner_stats = miner_stats.replace(b' ', b'')[:-9] + b'}'
                            miner_stats = b'{' + miner_stats[miner_stats.find(b'"STATS"'):]
                            miner_stats_part1_locator = miner_stats[0:miner_stats.rfind(b'{"STATS"') + 2]
                            miner_stats_part1 = miner_stats_part1_locator[0:miner_stats_part1_locator.rfind(b'}')] + b'}]}'
                            miner_stats_part2 = miner_stats[miner_stats.rfind(b'{"STATS"'):][:-2]
                            miner_stats_part1 = miner_stats_part1.decode("utf-8")
                            miner_stats_part1 = json.loads(miner_stats_part1)
                            miner_stats_part1_payload = dict(miner_stats_part1["STATS"][0])
                            miner_type = miner_stats_part1_payload["Type"]
                            formatted_miner_type = ""
                            position = 0

                            for c in miner_type:

                                if position == 0:

                                    formatted_miner_type = formatted_miner_type + c
                                    position = 1
                                    continue

                                if c.isupper() == True:

                                    formatted_miner_type = formatted_miner_type + " " + c
                                
                                else:

                                    formatted_miner_type = formatted_miner_type + c

                            key_match = 0

                            for key in miner_types.keys():

                                if key_match == 1:
                                    continue
                                
                                if key == formatted_miner_type:

                                    key_match = 1

                                    if miner_types[formatted_miner_type] != []:

                                        miner_temp_threshold = miner_types[formatted_miner_type][0]
                                        miner_hashrate_threshold = miner_types[formatted_miner_type][1]

                            if key_match == 0:

                                miner_types[formatted_miner_type] = []

                            miner_stats_part2 = miner_stats_part2.decode("utf-8")
                            miner_stats_part2 = json.loads(miner_stats_part2)
                            current_miner_hashrate = float(miner_stats_part2["GHS5s"])

                            if not math.isclose(current_miner_hashrate, float(0)):

                                total_hashrate_ghs = total_hashrate_ghs + current_miner_hashrate
                                total_miners_hashing = total_miners_hashing + 1

                                if current_miner_hashrate/1000 < int(miner_hashrate_threshold):

                                    low_hashrate = low_hashrate + 1
                                    low_hashrate_miners[miner_address] = miner_type

                                miner_max_temp = 0

                                for field in miner_stats_part2.keys():
                                    
                                    if "temp" in field:

                                        temperature_reading = int(miner_stats_part2[field])

                                        if temperature_reading > 0 and temperature_reading < 255:

                                            if temperature_reading > miner_max_temp:

                                                miner_max_temp = temperature_reading

                                            if temperature_reading > int(miner_temp_threshold):

                                                overheating = overheating + 1

                                                overheating_miners[miner_address] = miner_type

                                if miner_max_temp < lowest_temperature_c:

                                    lowest_temperature_c = miner_max_temp

                                if miner_max_temp > highest_temperature_c:

                                    highest_temperature_c = miner_max_temp

                            elif math.isclose(current_miner_hashrate, float(0)):

                                zeroes = zeroes + 1
                                zeroes_miners[miner_address] = miner_type

                        except:

                            problem_miners = problem_miners + 1
                            error_miners[miner_address] = ""
                            continue

    if lowest_temperature_c == 1000:

        lowest_temperature_c = 0

    active_miners = total_miners_hashing + zeroes + problem_miners

    if active_miners == 0:

        summary = {

            "total_petahash": str(0),
            "total_miners_hashing": str(0),
            "percentage_miners_hashing": str(0) + "%",
            "highest_temperature": str(0),
            "lowest_temperature": str(0),
            "zeroes": str(0),
            "errors": str(0),
            "timeouts": str(0)

        }

        with open(app_dir + 'hashkit_resources/overheating.json', 'w') as overheating_file:

            json.dump({}, overheating_file)

        with open(app_dir + 'hashkit_resources/low_hashrate.json', 'w') as low_hashrate_file:

            json.dump({}, low_hashrate_file)

        with open(app_dir + 'hashkit_resources/zeroes.json', 'w') as zeroes_file:

            json.dump({}, zeroes_file)

        with open(app_dir + 'hashkit_resources/timeouts.json', 'w') as timeouts_file:

            json.dump({}, timeouts_file)

        with open(app_dir + 'hashkit_resources/errors.json', 'w') as errors_file:

            json.dump({}, errors_file)

    else:
        

        total_petahash = round(total_hashrate_ghs/1000/1000, 6)
        percentage_miners_hashing = round((total_miners_hashing / active_miners) * 100, 2)
        summary = {

            "total_petahash": str(total_petahash),
            "total_miners_hashing": str(total_miners_hashing),
            "percentage_miners_hashing": str(percentage_miners_hashing),
            "highest_temperature": str(highest_temperature_c),
            "lowest_temperature": str(lowest_temperature_c),
            "zeroes": str(zeroes),
            "errors": str(problem_miners),
            "timeouts": str(timeouts)

        }

        with open(app_dir + 'hashkit_resources/miner_types.json', 'w') as miner_types_file:

            json.dump(miner_types, miner_types_file)

        with open(app_dir + 'hashkit_resources/overheating.json', 'w') as overheating_file:

            json.dump(overheating_miners, overheating_file)

        with open(app_dir + 'hashkit_resources/low_hashrate.json', 'w') as low_hashrate_file:

            json.dump(low_hashrate_miners, low_hashrate_file)

        with open(app_dir + 'hashkit_resources/zeroes.json', 'w') as zeroes_file:

            json.dump(zeroes_miners, zeroes_file)

        with open(app_dir + 'hashkit_resources/timeouts.json', 'w') as timeouts_file:

            json.dump(timeout_addresses, timeouts_file)

        with open(app_dir + 'hashkit_resources/errors.json', 'w') as errors_file:

            json.dump(problem_miners, errors_file)

    with open(app_dir + 'hashkit_resources/summaries.json', 'w') as summaries_file:

        json.dump(summary, summaries_file)

    time.sleep(1)