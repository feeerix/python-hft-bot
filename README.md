# HFT Bot

I'm a bit of an idiot, but I wanted a way to download large amounts of kline data.
It's turned out into quite a large project that it seems I basically want to do everything with.

## Current Focus Points

- Double check that backtesting is indeed going correctly
- Update to the latest blockchain data
- Add the ability to check for the earliest and latest times in db
- Integrate the websocket functionality into the model!
- Allow live updates directly from websocket

## Next Goals

- To Effectively "build" strategies, I will need to better abstract and automate the process, such that I could do it from the command line. I will need to build a better system to build the strategies.
- I currently am not able to perform the strategies across multiple assets, including tracking the whole portfolio as well as arbitrage between multiple assets. Implementation of this should also be considered as well.
- Implementing this with websockets, and then allow this to be run 24/7 will then allow the data to be collected whenever the script is running, and dynamically add it to the db as opposed to manually running the command.
- Start to integrate multiple exchanges and add to the database of klines. We will hopefully start to integrate the other exchange details, like funding rate and orderbook information.

## Potential Roadmap

First thing I want to do is to set up the ability to get as much kline data as we can.
This will allow us to potentially check if there is some kind of edge we can find getting data from Binanace, Coinbase and potentially Bybit.
These are exchanges that have a huge amount of liquidity and we can potentially try to track if prices are being led by these exchanges or vice versa.

The next step is to try to implement a way for the bot to implement these trades.
We would also want to implement some way to keep track of performance, of the trades, potentially setting up a web frontend to do so.
Finally, once the logic is set up to make the trades, we'd also want to introduce the ability for potential users to deposit funds so that they can also benefit from these strategies.

We might implement some form of multi-sig that might require some off-chain signatures to manage the assets.
To completely remove the assets, we can say would require TWO signatures from separate wallets that you own. We would be looking to make sure that users are operating with the best security practices, so there would be a multitude of layers of multi-sig requirements for specific types of operations.

Depending on what the bot is doing at the time, and the strategy that has been chosen, it would mean that the funds are pretty much liquid, and that the performance is actually going to be public.
I'd love to monetise this buy implementing a model similar to the 2 and 20 model from a hedge fund, but instead set it at something like 1 and 5.

I also eventually want to run a local orderbook for all of these exchanges.

Hopefully, I wish to generalise this as much as possible, so that we can spread this out across 2-3 centralised exchanges.
Once this is done, I hope I can set up some way to check the prices for decentralised exchanges.

## Strategies

We could probably implement multiple methods, one that includes using AAVE to manage the assets in a relatively low risk manner.
We would borrow stablecoins to buy back assets we think we want, paying interest on these loans but doing so in the hopes that the price rises. This long only plan will generally try to aim for longer timeframes. Swapping the assets into other high yield assets could also be on the table.

Another strategy we can try to implement is more traditional long/short trading on a decentralised exchange like GMX. This would allow us to utilise leverage, and increase the risk being taken. We could consider this a riskier strategy that we would not generally recommend implementing for more than let's say 25% of your portfolio (arbitrarily).

Another way that we can try to make profits would be to try to perform some form of multi-chain MEV. This is something I'm much less familiar with, but would be a fun learning experience in general.
