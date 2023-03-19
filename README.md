# HFT Bot

I'm a bit of an idiot, but I wanted a way to download large amounts of kline data.
Through implementing this I'm hoping to larn more about building large python projects.

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

I have found this implementation:
[https://github.com/kmanley/orderbook]

Which is an implementation of this quant cup winner apparently
[https://web.archive.org/web/20141222151051/https://dl.dropboxusercontent.com/u/3001534/engine.c]

Hopefully, I wish to generalise this as much as possible, so that we can spread this out across 2-3 centralised exchanges.
Once this is done, I hope I can set up some way to check the prices for decentralised exchanges.

## Strategies

We could probably implement multiple methods, one that includes using AAVE to manage the assets in a relatively low risk manner.
We would borrow stablecoins to buy back assets we think we want, paying interest on these loans but doing so in the hopes that the price rises. This long only plan will generally try to aim for longer timeframes. Swapping the assets into other high yield assets could also be on the table.

Another strategy we can try to implement is more traditional long/short trading on a decentralised exchange like GMX. This would allow us to utilise leverage, and increase the risk being taken. We could consider this a riskier strategy that we would not generally recommend implementing for more than let's say 25% of your portfolio (arbitrarily).

Another way that we can try to make profits would be to try to perform some form of multi-chain MEV. This is something I'm much less familiar with, but would be a fun learning experience in general.
