using GatewayModel.Stocks;
using GatewayModel.User;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GatewayManager
{
    public class GatewayManager
    {
        private readonly UserGateway userGateway;
        private readonly StocksGateway stocksGateway;
        private readonly MarketDataGateway marketDataGateway;
        private readonly AIAdvisorGateway aiAdvisorGateway;

        public GatewayManager(HttpClient httpClient)
        {
            userGateway = new UserGateway(httpClient);
            stocksGateway = new StocksGateway(httpClient);
            marketDataGateway = new MarketDataGateway(httpClient);
            aiAdvisorGateway = new AIAdvisorGateway(httpClient);
        }

        public Task<string> UserRegister(User user)
            => userGateway.UserRegister(user);

        public Task<string> UserDelete(string email)
            => userGateway.UserDelete(email);

        public Task<string> UserPasswordUpdate(User user)
            => userGateway.UserPasswordUpdate(user);

        public Task<string> UserRegisterV2(User user)
            => userGateway.UserRegisterV2(user);

        public Task<string> UserDeleteV2(string email, string password)
            => userGateway.UserDeleteV2(email, password);

        public Task<string> UserPasswordUpdateV2(UserUpdate user)
            => userGateway.UserPasswordUpdateV2(user);

        public Task<string> UserLoginV2(User user)
            => userGateway.UserLoginV2(user);

        public Task<string> UserIDV2(User user)
            => userGateway.UserIDV2(user);

        public Task<decimal> GetStockPrice(string stockSymbol)
        {
            CurrentData currentData = marketDataGateway.GetCurrentStockData(stockSymbol).Result;
            return Task.FromResult(currentData.Close);
        }

        public Task<List<StockPrice>> GetStockHistory(string stockSymbol, int range)
            => marketDataGateway.GetStockHistory(stockSymbol, range);

        public Task<List<StockPrice>> GetStockPeriodWeeklyHistory(string stockSymbol, int range, int interval)
            => marketDataGateway.GetStockPeriodWeeklyHistory(stockSymbol, range, interval);


        public Task<string> GetUserHoldingStocks(string userId)
            => stocksGateway.GetUsrStocksHolding(userId);

        public Task<string> GetUserTransactions(string userId)
            => stocksGateway.GetUserTransactions(userId);

        public async Task<string> MakingTransaction(TransactionGet t)
        {
            decimal price = GetStockPrice(t.StockSymbol).Result;
            return await stocksGateway.MakingTransaction(t.ClientId, t.StockSymbol, t.Quantity, t.TransactionType, price);
        }

        public async Task<string> GetAIAdvice(string query)
            => await aiAdvisorGateway.GetAIAdvice(query);

        public async Task<string> GetBasedStockHistoryAdvice(string stockSymbol)
        {
            List<StockPrice> stockPrices = await GetStockHistory(stockSymbol, 99);
            string stockPricesStr = string.Join("; ", stockPrices.Select(sp => $"{sp.Date:yyyy-MM-dd}: Close: {sp.ClosePrice}"));
            string query = $"stock symbol: {stockSymbol}, history: {stockPricesStr}, what is your recommendation based on this history?";
            var respose = await GetAIAdvice(query);
            return respose;
        }


    }
}
