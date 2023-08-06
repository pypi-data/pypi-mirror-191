from __future__ import annotations
import sys
import os
sys.path.append(os.path.dirname('sharingiscaring'))
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
import grpc
import base58
import base64
import datetime as dt
from rich.progress import track
from rich import print
from enum import Enum
from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf import message
import sys
import os



from sharingiscaring.GRPCClient.queries._GetPoolInfo import Mixin as _GetPoolInfo
from sharingiscaring.GRPCClient.queries._GetPoolDelegatorsRewardPeriod import Mixin as _GetPoolDelegatorsRewardPeriod
from sharingiscaring.GRPCClient.queries._GetPassiveDelegatorsRewardPeriod import Mixin as _GetPassiveDelegatorsRewardPeriod
from sharingiscaring.GRPCClient.queries._GetAccountList import Mixin as _GetAccountList
from sharingiscaring.GRPCClient.queries._GetBakerList import Mixin as _GetBakerList
from sharingiscaring.GRPCClient.queries._GetBlocksAtHeight import Mixin as _GetBlocksAtHeight
from sharingiscaring.GRPCClient.queries._GetFinalizedBlocks import Mixin as _GetFinalizedBlocks
from sharingiscaring.GRPCClient.queries._GetInstanceInfo import Mixin as _GetInstanceInfo
from sharingiscaring.GRPCClient.queries._GetInstanceList import Mixin as _GetInstanceList
from sharingiscaring.GRPCClient.queries._GetAnonymityRevokers import Mixin as _GetAnonymityRevokers
from sharingiscaring.GRPCClient.queries._GetIdentityProviders import Mixin as _GetIdentityProviders
from sharingiscaring.GRPCClient.queries._GetPoolDelegators import Mixin as _GetPoolDelegators
from sharingiscaring.GRPCClient.queries._GetPassiveDelegators import Mixin as _GetPassiveDelegators
from sharingiscaring.GRPCClient.queries._GetAccountInfo import Mixin as _GetAccountInfo
from sharingiscaring.GRPCClient.queries._GetBlockInfo import Mixin as _GetBlockInfo
from sharingiscaring.GRPCClient.queries._GetElectionInfo import Mixin as _GetElectionInfo
from sharingiscaring.GRPCClient.queries._GetTokenomicsInfo import Mixin as _GetTokenomicsInfo
from sharingiscaring.GRPCClient.queries._GetPassiveDelegationInfo import Mixin as _GetPassiveDelegationInfo
from sharingiscaring.GRPCClient.queries._GetBlockTransactionEvents import Mixin as _GetBlockTransactionEvents
from sharingiscaring.GRPCClient.queries._GetBlockSpecialEvents import Mixin as _GetBlockSpecialEvents
from sharingiscaring.GRPCClient.queries._GetBlockPendingUpdates import Mixin as _GetBlockPendingUpdates
from sharingiscaring.GRPCClient.queries._GetModuleSource import Mixin as _GetModuleSource




class GRPCClient(
    _GetPoolInfo,
    _GetAccountList,
    _GetBakerList,
    _GetInstanceInfo,
    _GetInstanceList,
    _GetFinalizedBlocks,
    _GetBlocksAtHeight,
    _GetIdentityProviders,
    _GetAnonymityRevokers,
    _GetPassiveDelegationInfo,
    _GetPassiveDelegators,
    _GetPoolDelegators,
    _GetPoolDelegatorsRewardPeriod,
    _GetPassiveDelegatorsRewardPeriod,
    _GetAccountInfo,
    _GetBlockInfo,
    _GetElectionInfo,
    _GetBlockTransactionEvents,
    _GetBlockSpecialEvents,
    _GetBlockPendingUpdates,
    _GetTokenomicsInfo,
    _GetModuleSource
    ):
    
    def __init__(self, host: str='localhost', port: int=20000):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = QueriesStub(self.channel)
        
    
grpcclient = GRPCClient()
# deleg = grpcclient.get_delegators_for_pool(72723, "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# print (deleg)

# pool_info = grpcclient.get_pool_info_for_pool(74936, "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# print (pool_info)

# passive_info = grpcclient.get_passive_delegation_info("affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# print (passive_info)

#76670
# account_info = grpcclient.get_account_info("4qL7HmpqdKpYufCV7EvL1WnHVowy1CrTQS7jfYgef5stzpftwS", 
#                 "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
#72723
# account_info = grpcclient.get_account_info("3BFChzvx3783jGUKgHVCanFVxyDAn5xT3Y5NL5FKydVMuBa7Bm", 
#                 "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# print (account_info)
#delegator
# account_info = grpcclient.get_account_info("4TVoQQ8VRfqjQkG34dXR8NEPHFxQtWyE6ND62YXckJadGxBQsg", 
#                 "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# #passive Delegator
# account_info = grpcclient.get_account_info("3rfJwWcM5AcdpchhXtQ1Zo5aVFjjPpM1DqNT2ucJRLZgu95R7s", 
#                 "af7c0abae81577a9a52621ecfb794a01f1fbb370fe714659f0760644065bdcbd")
# print (account_info)

# # blockInfo
# block_info = grpcclient.get_block_info(
#                 "ee6f396d82bd3615fb74e53681dbacb1f409fba22eaa12fba60941bc3d387f2b")
# print (block_info)

# block_txs = grpcclient.get_block_transaction_events(
#                 "ee6f396d82bd3615fb74e53681dbacb1f409fba22eaa12fba60941bc3d387f2b")


# tokenomicsInfo
# tok_info = grpcclient.get_tokenomics_info(
#                 "af7c0abae81577a9a52621ecfb794a01f1fbb370fe714659f0760644065bdcbd")
# print (tok_info)

#bakery
# account_info = grpcclient.get_account_info("3hzSaiFSz3VWQsr2PYMvA8NYygM4stDmpVzJZbyHwij5cg4v23", 
#                 "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# print (account_info)