# Notes

This contains notes for future me, to make sure I understand what I'm trying to do, especially if I'm having to stop for some reason.

## Current thought process

Looking to recreate the test_run function as per the README. This would also involve recreating the way that the dataframes work, and how we add the indicators in as well.

Our next step is now to rebuild the Binance API - so that it is easier to read and the boilerplate is in place so that it can be updated to any exchange easily.
Remembering that the main aim is to be able to create settings well, and knowing that I need to have:

- The ability to manage multiple timeframes.
- The ability to work with multiple assets.
- Easily be able to model statistics. We want to use whatever information we have to map something that's happenning in the future.

---

We want to try to stay as computationally efficient as possible now, especially as we're starting to reach data sizes that might be much more noticeable than before. We currently cannot move from python (it's a personal skill issue), so the next step is to try and optimise the code at the same time.

At the moment, the signals for trading (STOCH RSI k above d) is within the same dataframe as the original data. We will now look to separate those so that the market data and the signals will reside on different Dataframes. As such, we would not only need to rebuild the test_run function but also how we handle databases.

So currently we'd want to:

- Adjust how we add the signals from the settings page to a more easily managed way
- Which therefore would facilitate the change that df_signals goes on their own. Here is some code from ChatGPT: df_signals = pd.DataFrame(index=df_market.index)
- In doing so, I can then use functions like: df_signals['EMA_8_A_EMA_21'] = df_market['EMA_8'] > df_market['EMA_21'] and df_signals['STOCHRSIk_34_34_8_8_XA_STOCHRSId_34_34_8_8'] = (df_market['STOCHRSIk_34_34_8_8'].shift(1) < df_market['STOCHRSId_34_34_8_8'].shift(1)) & (df_market['STOCHRSIk_34_34_8_8'] > df_market['STOCHRSId_34_34_8_8']) to create the df_signals dataframe.
- Once doing so, we can start to rebuild the test_run function to take both of these into account.

---

Alright - so I think I'll create a factory class for the settings and many of the different classes that I have created. In this way, I can dynamically add them when required and actually add a function to save them as well.

When I've done that, I can continue to add functions to the strategy class, to allow it to better manage the overall trading strategy.
