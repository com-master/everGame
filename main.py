from tonclient.types import Abi, DeploySet, CallSet, Signer, FunctionHeader, \
    ParamsOfEncodeMessage, ParamsOfProcessMessage, ProcessingResponseType, \
    ProcessingEvent, ParamsOfSendMessage, ParamsOfWaitForTransaction, ClientConfig, \
        BuilderOp, NetworkConfig, ParamsOfRunGet, ParamsOfQuery, ParamsOfGetCodeFromTvc, \
            ParamsOfRunTvm, AccountForExecutor, ParamsOfWaitForCollection, ParamsOfRunExecutor, \
                ParamsOfNaclSignKeyPairFromSecret, KeyPair
from tonclient.client import TonClient
import pyxel
import time
class cords:
    x:int
    y:int

class block:
    owner:str
    types:int

cache_id_block = dict(data=0,time=0)

cache_id_cords = dict(data=0,time=0)

cache_time = 0.5

client = TonClient(config=ClientConfig())

main_address = "0:71e65a4d80a6e58675d8bf6b8d476c6ae14d700d943f243289610a88c95e6d40"

main_abi = Abi.from_path(
            path='main.abi.json')

def get_method(address,get: str,abi):
    call_set = CallSet(
        function_name=get,
        )
    encode_params = ParamsOfEncodeMessage(
        abi=abi,signer=Signer.NoSigner(), address=address,
        call_set=call_set)
    encoded_message = client.abi.encode_message(
        params=encode_params)

    q_params = ParamsOfWaitForCollection(
        collection='accounts', result='id boc',
        filter={'id': {'eq': address}})
    account = client.net.wait_for_collection(params=q_params)

    account_for_executor = AccountForExecutor.Account(
        boc=account.result['boc'], unlimited_balance=True)

    run_params = ParamsOfRunTvm(
        message=encoded_message.message, account=account.result["boc"], abi=abi)
    result = client.tvm.run_tvm(params=run_params)
    return result.decoded.output[get]

def call_method(address,method:str,params:dict):
    call_set = CallSet(
            function_name=method, input=params)
    encode_params = ParamsOfEncodeMessage(
        abi=main_abi, signer=Signer.NoSigner(), address=address,
        call_set=call_set)
    process_params = ParamsOfProcessMessage(
        message_encode_params=encode_params, send_events=False)
    result = client.processing.process_message(
        params=process_params)

    return result



import pyxel


class App:
    def __init__(self):
        pyxel.init(210, 210, title="Hello Pyxel")
        pyxel.load("main.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btn(pyxel.KEY_W):
            call_method(main_address,"_move",dict(id=0,way=0))
        elif pyxel.btn(pyxel.KEY_S):
            call_method(main_address,"_move",dict(id=0,way=1))
        elif pyxel.btn(pyxel.KEY_D):
            call_method(main_address,"_move",dict(id=0,way=2))
        elif pyxel.btn(pyxel.KEY_A):
            call_method(main_address,"_move",dict(id=0,way=3))

    def draw(self):
        pyxel.cls(0)
        if cache_id_block["time"] + cache_time < time.time():
            cache_id_block["data"] = get_method(main_address, "id_block", main_abi)
        
        if cache_id_cords["time"] + cache_time < time.time():
            cache_id_cords["data"] = get_method(main_address, "id_cords", main_abi)
        for i in cache_id_block["data"]:
            pyxel.rect(int(cache_id_cords["data"][i]['x']) * 10,int(cache_id_cords["data"][i]['y']) * 10,10,10,1)
        
        
        
        


App()
