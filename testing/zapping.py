import os
import time
from datetime import timedelta
import dotenv
from nostr_sdk import Keys, ClientBuilder, NostrSigner, NostrZapper, NostrWalletConnectUri, PublicKey, ZapEntity, init_logger, LogLevel


dotenv.load_dotenv()

# Init logger
init_logger(LogLevel.INFO)

# Parse NWC uri
NWC = os.getenv("NWC")
print(NWC)
# uri = NostrWalletConnectUri.parse("nostr+walletconnect://..")
uri = NostrWalletConnectUri.parse(NWC)

# Compose client
keys = Keys.generate()
signer = NostrSigner.keys(keys)
zapper = NostrZapper.nwc(uri)
client = ClientBuilder().signer(signer).zapper(zapper).build()

client.add_relay("wss://relay.damus.io")
client.connect()


pk = PublicKey.from_bech32("npub1xegedgkkjf24pl4d76cdwhufacng5hapzjnrtgms3pyhlvmyqj9suym08k")
client.zap(ZapEntity.public_key(pk), 10, None)




# from nostr_sdk import Keys, ClientBuilder, NostrSigner, NostrZapper, NostrWalletConnectUri, PublicKey, ZapEntity, init_logger, LogLevel
# from datetime import timedelta
# import time

# # Init logger
# init_logger(LogLevel.INFO)

# # Parse NWC uri
# uri = NostrWalletConnectUri.parse("nostr+walletconnect://..")

# # Compose client
# keys = Keys.generate()
# signer = NostrSigner.keys(keys)
# zapper = NostrZapper.nwc(uri)
# client = ClientBuilder().signer(signer).zapper(zapper).build()

# client.add_relay("wss://relay.damus.io")
# client.connect()

# pk = PublicKey.from_bech32("npub1drvpzev3syqt0kjrls50050uzf25gehpz9vgdw08hvex7e0vgfeq0eseet")
# client.zap(ZapEntity.public_key(pk), 1000, None)