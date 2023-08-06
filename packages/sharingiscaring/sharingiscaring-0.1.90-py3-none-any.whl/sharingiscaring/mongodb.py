from enum import Enum
from .mongodb_queries._search_transfers import Mixin as _search_transfers
from .mongodb_queries._subscriptions import Mixin as _subscriptions
from .mongodb_queries._baker_distributions import Mixin as _distributions
from .mongodb_queries._store_block import Mixin as _store_block
from .mongodb_queries._apy_calculations import Mixin as _apy_calculations

from pymongo import MongoClient
from pymongo.collection import Collection
from rich.console import Console
from typing import Dict
from sharingiscaring.tooter import Tooter, TooterType, TooterChannel
console = Console()


class Collections(Enum):
    blocks                          = 'blocks'
    transactions                    = 'transactions'
    instances                       = 'instances'
    modules                         = 'modules'
    messages                        = 'messages'
    paydays                         = 'paydays'
    paydays_performance             = 'paydays_performance'
    paydays_rewards                 = 'paydays_rewards'
    paydays_apy_intermediate        = 'paydays_apy_intermediate'
    paydays_helpers                 = 'paydays_helpers'
    involved_accounts_all           = 'involved_accounts_all'
    involved_accounts_transfer      = 'involved_accounts_transfer'
    involved_contracts              = 'involved_contracts'
    nightly_accounts                = 'nightly_accounts'
    blocks_at_end_of_day            = 'blocks_at_end_of_day'
    helpers                         = 'helpers'
    memo_transaction_hashes         = 'memo_transaction_hashes'

class MongoDB(
    _search_transfers,
    _subscriptions,
    _distributions,
    _store_block,
    _apy_calculations
    ):

    def __init__(self, mongo_config, tooter: Tooter):
        self.tooter: Tooter           = tooter
        
        try:
            con = MongoClient(f'mongodb://admin:{mongo_config["MONGODB_PASSWORD"]}@{mongo_config["MONGO_IP"]}:{mongo_config["MONGO_PORT"]}')
            self.db                                     = con.concordium
            self.testnet_db                              = con.concordium_testnet
            self.mainnet_db                              = con.concordium_mainnet
            self.collection_blocks                      = self.db['blocks']
            self.collection_transactions                = self.db['transactions']
            self.collection_messages                    = self.db['bot_messages']
            self.collection_accounts_involved           = self.db['accounts_involved']
            self.collection_paydays                     = self.db['paydays']
            self.collection_paydays_performance         = self.db['paydays_performance']
            self.collection_paydays_rewards             = self.db['paydays_rewards']
            self.collection_paydays_apy                 = self.db['paydays_apy']
            self.collection_paydays_apy_intermediate    = self.db['paydays_apy_intermediate']

            self.collection_involved_accounts_all       = self.db['involved_accounts_all']
            self.collection_involved_accounts_transfer  = self.db['involved_accounts_transfer']
            self.collection_involved_contracts          = self.db['involved_contracts']
            self.collection_nightly_accounts            = self.db['nightly_accounts']
            self.collection_blocks_at_end_of_day        = self.db['blocks_at_end_of_day']
            self.collection_helpers                     = self.db['helpers']
            self.collection_memo_transaction_hashes     = self.db['memo_transaction_hashes']
            self.collection_blocks_grpc                 = self.db['blocks_grpc']
            self.collection_transactions_grpc           = self.db['transactions_grpc']
            self.collection_instances                   = self.db['instances']

            # MAINNET
            self.mainnet = {}#: Dict(Collections, Collection)
            self.mainnet[Collections.blocks]         = self.mainnet_db['blocks']
            self.mainnet[Collections.transactions]   = self.mainnet_db['transactions']
            self.mainnet[Collections.helpers]        = self.mainnet_db['helpers']
            self.mainnet[Collections.involved_accounts_all]       = self.mainnet_db['involved_accounts_all']
            self.mainnet[Collections.involved_accounts_transfer]  = self.mainnet_db['involved_accounts_transfer']
            self.mainnet[Collections.involved_contracts]          = self.mainnet_db['involved_contracts']
            self.mainnet[Collections.instances]                   = self.mainnet_db['instances']
            self.mainnet[Collections.modules]                     = self.mainnet_db['modules']

            self.mainnet[Collections.paydays]                     = self.mainnet_db['paydays']
            self.mainnet[Collections.paydays_performance]         = self.mainnet_db['paydays_performance']
            self.mainnet[Collections.paydays_rewards]             = self.mainnet_db['paydays_rewards']
            self.mainnet[Collections.paydays_apy_intermediate]    = self.mainnet_db['paydays_apy_intermediate']
            self.mainnet[Collections.paydays_helpers]             = self.mainnet_db['paydays_helpers']

            # TESTNET
            self.testnet={}#: Dict[Collections, Collection] = {}
            self.testnet[Collections.blocks]         = self.testnet_db['blocks']
            self.testnet[Collections.transactions]   = self.testnet_db['transactions']
            self.testnet[Collections.helpers]        = self.testnet_db['helpers']
            self.testnet[Collections.involved_accounts_all]       = self.testnet_db['involved_accounts_all']
            self.testnet[Collections.involved_accounts_transfer]  = self.testnet_db['involved_accounts_transfer']
            self.testnet[Collections.involved_contracts]          = self.testnet_db['involved_contracts']
            
            self.testnet[Collections.instances] = self.testnet_db['instances']
            self.testnet[Collections.modules]   = self.testnet_db['modules']

            # self.collection_transaction_python          = self.db['transaction_python']

            console.log(con.server_info()['version'])
        except Exception as e:
            print (e)
            tooter.send(channel=TooterChannel.NOTIFIER, message=f'BOT ERROR! Cannot connect to MongoDB, with error: {e}', notifier_type=TooterType.MONGODB_ERROR)
            