from xminer_wrapper import XMinerWrapper

class XMinerCommand():

    def command_miner(command, miner):

        miner_connection = XMinerWrapper(miner, 4028)
        command_response = miner_connection.issue_command(command)
        return command_response

    def command_miners(command, miners):

        for miner_range in miners:

            for range_id in miner_range:

                for miner_address in miner_range[range_id]:

                    miner_connection = XMinerWrapper(miner_address, 4028)

                    if miner_connection == b'timeout':

                        return b'timeout'
                    
                    else:

                        command_response = miner_connection.issue_command(command)

                    return command_response