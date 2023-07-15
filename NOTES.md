# Notes

This contains notes for future me, to make sure I understand what I'm trying to do, especially if I'm having to stop for some reason.

## Current thought process

Looking to recreate the test_run function as per the README. This would also involve recreating the way that the dataframes work, and how we add the indicators in as well.

We want to try to stay as computationally efficient as possible now, especially as we're starting to reach data sizes that might be much more noticeable than before. We currently cannot move from python (it's a personal skill issue), so the next step is to try and optimise the code at the same time.

At the moment, the signals for trading (STOCH RSI k above d) is within the same dataframe as the original data. We will now look to separate those so that the market data and the signals will reside on different Dataframes. As such, we would not only need to rebuild the test_run function but also how we handle databases.

So currently we'd want to:

- Adjust how we add the signals from the settings page to a more easily managed way
- Which therefore would facilitate the change that df_signals goes on their own. Here is some code from ChatGPT: df_signals = pd.DataFrame(index=df_market.index)
- In doing so, I can then use functions like: df_signals['EMA_8_A_EMA_21'] = df_market['EMA_8'] > df_market['EMA_21'] and df_signals['STOCHRSIk_34_34_8_8_XA_STOCHRSId_34_34_8_8'] = (df_market['STOCHRSIk_34_34_8_8'].shift(1) < df_market['STOCHRSId_34_34_8_8'].shift(1)) & (df_market['STOCHRSIk_34_34_8_8'] > df_market['STOCHRSId_34_34_8_8']) to create the df_signals dataframe.
- Once doing so, we can start to rebuild the test_run function to take both of these into account.

---

I must remember that I may want to perform computation on a whole portfolio of assets, throughout time, for multiple data points. It would be a 4 dimensional matrix?

Holy fuck I gotta redo the whole thing.

Overall this will improve the computational efficiency as well as be easier to use.
