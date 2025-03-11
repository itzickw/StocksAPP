using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace MarketDataModel
{
    public class AlphaVantageInterdayStockResult
    {
        [JsonPropertyName("Time Series (1min)")] 
        public Dictionary<string, AlphaVantageDailyStockResult> TimeSeries { get; set; }
    }
}
