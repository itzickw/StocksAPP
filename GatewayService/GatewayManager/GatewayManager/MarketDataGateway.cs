using GatewayModel.Stocks;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace GatewayManager
{
    internal class MarketDataGateway
    {
        private readonly string marketDataServiceURL = "http://localhost:9350/api/MarketData";
        private HttpClient httpClient;

        internal MarketDataGateway(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        internal async Task<CurrentData> GetCurrentStockData(string stockSymbol)
        {
            var stockResponse = await httpClient.GetAsync($"{marketDataServiceURL}/stock-data/{stockSymbol}");

            var response = await stockResponse.Content.ReadAsStringAsync();

            CurrentData currentData = JsonSerializer.Deserialize<CurrentData>(response);
            Console.WriteLine(response);

            if (response == null || currentData.Close == 0)
            {
                throw new Exception("Stock data not found");
            }

            return currentData;
        }

        internal async Task<List<StockPrice>> GetStockHistory(string stockSymbol, int range)
        {
            var stockResponse = await httpClient.GetAsync($"{marketDataServiceURL}/{stockSymbol}/{range}");
            var response = await stockResponse.Content.ReadAsStringAsync();
            return ParseStockHistory(response);        
        }

        internal async Task<List<StockPrice>> GetStockPeriodWeeklyHistory(string stockSymbol, int range, int interval)
        {
            var stockResponse = await httpClient.GetAsync(
                $"{marketDataServiceURL}/weekly-stock-data?symbol={stockSymbol}&days={range}&weeksInterval={interval}");
            var response = await stockResponse.Content.ReadAsStringAsync();
            Console.WriteLine(response); // או לוג אחר לפי הצורך
            return ParseStockHistory(response);
        }

        private static  List<StockPrice> ParseStockHistory(string jsonResponse)
        {
            var stockPrices = new List<StockPrice>();
            var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };

            var jsonData = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>(jsonResponse, options);

            Console.WriteLine("Total records: " + jsonData.Count); // לוג לאיברי ה-JSON

            foreach (var entry in jsonData)
            {
                if (DateTime.TryParseExact(entry.Key, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime date) &&
                    entry.Value.TryGetValue("4. close", out string closePriceStr) &&
                    decimal.TryParse(closePriceStr, NumberStyles.Any, CultureInfo.InvariantCulture, out decimal closePrice))
                {
                    stockPrices.Add(new StockPrice { Date = date, ClosePrice = closePrice });
                }
                else
                {
                    Console.WriteLine($"Failed to parse entry: {entry.Key}"); // לוג לאיברים שלא מצליחים להמיר
                }
            }

            return stockPrices;
        }

    }
}
