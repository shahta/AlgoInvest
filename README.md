# AlgoInvest
This project is inspired by the book "Warren Buffett and the Interpretation of Financial Statements: The Search for the Company with a Durable Competitive Advantage" by David Clark and Mary Buffett. The books enlightens its readers to the things Warren Buffet looks for when he analyzes a companies financial statements. 

The goal of my algorithm is to automate the calculations needed to be done on the entries found on said financial statements (income statement, balance sheet, and cash-flow statements) according to how it is described in the book. Depending on if these calculations meet the criteria prescribed in the book, my program assigns a score for that category. To provide an example, the book explains that a company with a net-income of 40% or higher to total revenue is an excellent sign of a company with a **Durable Competitve Advantage** (referred to as a DCA in the program). So, my program will retrieve the net-income and the total revenue for the specified ticker over the last five years and divide the two values and average them over the last five years. If the resulting value is above 40% the score variable will be incremented by one since it meets the criteria described in the book. If the entry does not meet this criteria then a point is deducted from the total score. For some of the entries, there is no quantitative measure described in the book so I have used reasonably assumed values for these values. The output of the calculation is beautifully printed in the console for the user to read along with if it meets Buffet's criteria or not.

After all the entries are calculated, an analysis is provided should the user ask for it. The analysis is based on if the score meets a certain threshold. These thresholds were determined through evaluating the scores for companies that already have a known DCA (i.e. Coca Cola Company, Microsoft, Moody's Corporation, etc.) The program also plots graphs of the key ratios and key entries to show the user the trends of these values over time. These trend lines aid a user to strengthen their conviction of the company that is being analyzed.

Although this is a great tool for the fundamental analysis of a company, users should use this as a starting point for researching a company that they are interested in purchasing. By no means is this program the end-all and be-all for analyzing the company and its value. Users should also be aware that this program is built for **long-term investing**. Buffet is a man who looks for companies he can hold onto forever so this program is built to analyze companies that fit this criteria. This means that if a company is given an excellent rating may not mean its a great buy for all types of investors. Similarly, if a company is given a poor rating does not necessarily mean that its a terrible stock, it just means that this company may not be a suitable holding for the investor who's in for the long haul. This is why some amazing companies such as Tesla will do poorly against this algorithm since a lot of its financial data does not meet the criteria required for it to be a good long term investment. 

**NOTE: ALL CALCULATIONS ARE OVER A FIVE YEAR PERIOD**

# GENERAL USE
To use this program simply clone this into your working directory. After that, head over to https://financialmodelingprep.com/developer/ to get your API key and paste it into the `KEY` variable of the `Config.ex.py` file. Also change `Config.ex.py` to just `Config.py`.
To evaluate a ticker simply enter `python main.py --ticker ticker`. See below examples for further info.

# DISCLAIMER
This is for educational purposes only. The insight provided by this program is not investment advice and should not be relied upon for any recommnedations. Please use at your own risk. Please do your own research before making any sort of decision. This program is not accountable for any sort of losses or damages incurred.

# EXAMPLES

### 'Excellent' company with a DCA (Moody's Corp.)
![image](https://user-images.githubusercontent.com/68486811/114450423-3795e400-9b93-11eb-802e-139e5dcbc10c.png)
![image](https://user-images.githubusercontent.com/68486811/114450524-5ac09380-9b93-11eb-9ca7-e9712e4ec310.png)


### 'Mediocre' company that has potential (Amazon)
![image](https://user-images.githubusercontent.com/68486811/114458067-f6560200-9b9b-11eb-970e-1c63529d418c.png)
![image](https://user-images.githubusercontent.com/68486811/114458021-edfdc700-9b9b-11eb-8db1-34c1cc656b9b.png)


### 'Terrible' company without a DCA (GameStop _hehe_)
![image](https://user-images.githubusercontent.com/68486811/114457661-847db880-9b9b-11eb-8e7d-db7b5de94e4b.png)
![image](https://user-images.githubusercontent.com/68486811/114457720-94959800-9b9b-11eb-82f4-336a2e56ab83.png)
