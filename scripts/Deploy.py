from scripts.helperScript import getAccount, generateEncode, upgradeCon
from brownie import network, sampCon, sampCon1, ProxyAdmin, TransparentUpgradeableProxy, Contract


def deploy():

    # taking the current network
    curNet = network.show_active()
    # getting the account based on the network
    account = getAccount()

    # deploying first sample contract
    impCon = sampCon.deploy({"from": account})

    # deployin the proxy admin for giving as admin to the proxy contract
    proxyAdmin = ProxyAdmin.deploy({"from": account})

    # the contract is going to give in the proxy contract so there instead of contractor we use initializer 
    initializerEncode = generateEncode()

    # here we giving the implementation contract to the proxy contract
    # in this instead of the proxy admin contract we can give our adddress as the admin
    # here we passing the paramenter (implementation contract, proxy admin contract or your address, initilizer)
    proxyCon = TransparentUpgradeableProxy.deploy(impCon.address, proxyAdmin.address, initializerEncode, {"from": account})

    # getting the contract 
    # here we passing the proxy address and the implementation contract address
    workingCon = Contract.from_abi("Box", proxyCon.address, impCon.abi)

    

    print(f"curNet: {curNet}")
    print(f"account: {account}")
    print(f"initializerEncode: {initializerEncode}")
    print(f"workingCon address: {workingCon}")

    # checking the value in the present proxy contract
    print(f"proxyCon retrive: {workingCon.retrive()}")

    # here we storing the 1 value in the contract
    storeTx = workingCon.store(1, {"from": account})
    # waiting for the transaction to be completed
    storeTx.wait(1)
    print(f"proxyCon retrive: {workingCon.retrive()}")

    # here deploying the second contract
    impCon1 = sampCon1.deploy({"from": account})


    # using this upgrade function we upgrading the implementation contract to the second contract
    # in this we passing the parameter our account, lastest contract going to update, proxy contract, proxy admin contract
    print("upgrading the contract...")
    upgradeTx = upgradeCon(account=account, 
                            implementationCon=impCon1, 
                            proxy=proxyCon, 
                            proxyAdmin=proxyAdmin)
    upgradeTx.wait(1)
    print(f'upgraded successfully: {upgradeTx}')

    
    # getting the contract from the seond contract abi
    workingCon = Contract.from_abi("Box1", proxyCon.address, impCon1.abi)

    # here we retriving the value from the contract becouse if we upgrade contract then also the memory will remain same 
    print(f"proxyCon retrive after upgrading: {workingCon.retrive()}")

    print('incrementing the value...')
    # here we incrementing value in the contract
    incTx = workingCon.increment({"from": account})

    incTx.wait(1)

    print('value incremented ....')

    # here checking the value is incremented in the contract
    print(f"proxyCon retrive: {workingCon.retrive()}")





def main():
    deploy()