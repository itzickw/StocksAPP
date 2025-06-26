using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net.Http;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using MarketDataModel;

namespace MarketDataManager
{
    public class AlphaVantageService
    {
        private readonly HttpClient _httpClient;
        private readonly string _dailyUrl = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY";
        private readonly string _intradayUrl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY";
        private readonly string _apiKey = "2Y5DWP9YTF6UTM46";
        //private readonly string _apiKey = "E4EW01897YHVDVB5";
        //private readonly string _apiKey = "R5PGW5TWXOVEIYAO";
        public AlphaVantageService(HttpClient httpClient)
        {
            _httpClient = httpClient ?? throw new ArgumentNullException(nameof(httpClient));
        }

        public async Task<Dictionary<string, AlphaVantageDailyStockResult>> GetStockDataAsync(string symbol, string outputsize)
        {
            string url = $"{_dailyUrl}&symbol={symbol}&outputsize={outputsize}&apikey={_apiKey}";
            var response = await _httpClient.GetAsync(url);

            if (!response.IsSuccessStatusCode)
                throw new Exception("Failed to fetch stock data from AlphaVantage");

            var json = await response.Content.ReadAsStringAsync();
            Console.WriteLine("Daily Response: " + json);

            var result = JsonSerializer.Deserialize<TimeSeriesResponse>(json, new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            });

            if (result == null || result.TimeSeries == null)
                throw new Exception("Invalid response format from AlphaVantage");

            return result.TimeSeries;
        }

        public async Task<Dictionary<string, AlphaVantageDailyStockResult>> GetStockDataForPeriodAsync(string symbol, int days)
        {
            string outputsize = days > 100 ? "full" : "compact";
            var timeSeries = await GetStockDataAsync(symbol, outputsize);

            var filteredData = timeSeries
                .Where(kv => DateTime.Parse(kv.Key) >= DateTime.UtcNow.AddDays(-days))
                .ToDictionary(kv => kv.Key, kv => kv.Value);

            return filteredData;
        }

        // פונקציה חדשה לנתוני זמן אמת (intraday)
        public async Task<AlphaVantageDailyStockResult> GetRealtimeStockDataAsync(string symbol, string interval = "1min")
        {
            string url = $"{_intradayUrl}&symbol={symbol}&interval={interval}&apikey={_apiKey}";
            var response = await _httpClient.GetAsync(url);

            if (!response.IsSuccessStatusCode)
                throw new Exception("Failed to fetch realtime stock data from AlphaVantage");

            var json = await response.Content.ReadAsStringAsync();
            Console.WriteLine("Realtime Response: " + json);

            var result = JsonSerializer.Deserialize<AlphaVantageInterdayStockResult>(json, new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            });

            if (result == null || result.TimeSeries == null || !result.TimeSeries.Any())
                throw new Exception("Invalid or empty response from AlphaVantage for realtime data");

            // מחזיר את הנתונים של הנקודה האחרונה (הכי עדכנית)
            var latestEntry = result.TimeSeries.OrderByDescending(kv => DateTime.Parse(kv.Key)).First();
            return latestEntry.Value;
        }

        public async Task<Dictionary<string, AlphaVantageDailyStockResult>> GetWeeklyStockDataForPeriodAsync(string symbol, int days, int daysInterval = 1)
        {
            string outputsize = days > 100 ? "full" : "compact";
            var timeSeries = await GetStockDataAsync(symbol, outputsize);

            var filteredData = timeSeries
                .Where(kv => DateTime.Parse(kv.Key) >= DateTime.UtcNow.AddDays(-days)) // מסנן לפי ימים
                .OrderByDescending(kv => kv.Key) // מסדר את התאריכים בסדר עולה
                .Select((kv, index) => new { Date = kv.Key, Value = kv.Value, Index = index }) // מוסיף אינדקס לכל תאריך
                .Where(x => x.Index % daysInterval == 0) // בוחר כל אינטרבל ימים
                .ToDictionary(x => x.Date, x => x.Value);

            return filteredData;
        }
    }
}