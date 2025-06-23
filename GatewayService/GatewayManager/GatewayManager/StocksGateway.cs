using System.Text;
using System.Text.Json;
using GatewayModel.Stocks;
using Microsoft.Extensions.Options;

namespace GatewayManager
{
    internal class StocksGateway
    {
        //private readonly string stockServiceURL = "http://localhost:9250/api/Stock";
        private readonly string stockServiceURL;
        private readonly HttpClient httpClient;

        internal StocksGateway(HttpClient httpClient, IOptions<ServiceUrlsConfig> serviceUrls)
        {
            this.httpClient = httpClient;
            stockServiceURL = serviceUrls.Value.stockServiceURL;
        }

        internal async Task<string> GetUsrStocksHolding(string userId)
        {
            var stockResponse = await httpClient.GetAsync($"{stockServiceURL}/{userId}/holding");
            return await stockResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> GetUserTransactions(string userId)
        {
            var stockResponse = await httpClient.GetAsync($"{stockServiceURL}/{userId}/transactions");
            return await stockResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> MakingTransaction(int userId, string stockSymbol, decimal quantity, string transactionType, decimal price)
        {
            TransactionPost transaction = new()
            {                
                ClientId = userId,
                StockSymbol = stockSymbol,
                Quantity = quantity,
                TransactionType = transactionType,
                Price = price,
                Date = DateTime.UtcNow
            };

            var jsonTransaction = JsonSerializer.Serialize(transaction);
            var stockResponse = await httpClient.PostAsync(
                $"{stockServiceURL}/transaction", new StringContent(jsonTransaction, Encoding.UTF8, "application/json")
            );

            return await stockResponse.Content.ReadAsStringAsync();
        }
    }
}
