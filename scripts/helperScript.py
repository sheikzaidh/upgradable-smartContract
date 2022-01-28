from brownie import network, config, accounts
import eth_utils

LOCALNAME = ["development", "ganache-cli", "mainnet-fork"]

# function to get the account based on the network and the parmenters
def getAccount(id=None, index=None):
    curNet = network.show_active()
    print(f"curNet: {curNet}")
    if id:
        return accounts.load(id) 
    if index:
        return accounts[index]

    if curNet not in LOCALNAME:
        return config["wallets"]["fromAdd"]
    else:
        return accounts[0]
    
# here we endoing the initializer and the data which we going to provide to the proxy
def generateEncode(initializer=None, *args):
    # if the data and the initializer is available data is encoded and returned
    if len(args) > 0 and initializer:
        return initializer.encode(*args)
    else:
        # if data and the initializer is not available the we encode the empty data using the eth_utils
        return eth_utils.to_bytes(hexstr = "0x")

# this function is used to update the implementation contract in the proxy contract
# here we passing the parameter our account, lastest contract going to update, proxy contract, proxy admin contract, initializer if available, and the data for the initializer
def upgradeCon(account, implementationCon, proxy=None, proxyAdmin=None, initializer=None , *args):
    transCon = ""

    # here one note if there is initailizer in upgrade function we have add "AndCall" because it will call the initializer
    # checking the proxy admin is available 
    if proxyAdmin:
        if initializer:
            intializerEncoded = generateEncode(intializer=None, *args)

            # upgrading based on the proxy admin
            transCon = proxyAdmin.upgradeAndCall(
                                                    proxy.address,
                                                    implementationCon.address,          
                                                    intializerEncoded,
                                                    {"from": account}
                                                )
        else:
            transCon = proxyAdmin.upgrade(
                                            proxy.address,
                                            implementationCon.address,
                                            {"from": account}
                                            )
    else:
        if initializer:
            intializerEncoded = generateEncode(intializer=None, *args)
            # upgrading with respect to proxy
            transCon = proxy.upgradeToAndCall(
                                            implementationCon.address,
                                            intializerEncoded,
                                            {"from": account}
                                            )
        else:
            transCon = proxy.upgradeTo(
                                        implementationCon.address,
                                        {"from": account}
                                        )
    return transCon








