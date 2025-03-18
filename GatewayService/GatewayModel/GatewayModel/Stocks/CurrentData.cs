using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace GatewayModel.Stocks
{
    public class CurrentData
    {
        [JsonPropertyName("1. open")]
        public string OpenString { get; set; }

        [JsonIgnore]
        public decimal Open => decimal.TryParse(OpenString, NumberStyles.Any, CultureInfo.InvariantCulture, out var result) ? result : 0m;

        [JsonPropertyName("2. high")]
        public string HighString { get; set; }

        [JsonIgnore]
        public decimal High => decimal.TryParse(HighString, NumberStyles.Any, CultureInfo.InvariantCulture, out var result) ? result : 0m;

        [JsonPropertyName("3. low")]
        public string LowString { get; set; }

        [JsonIgnore]
        public decimal Low => decimal.TryParse(LowString, NumberStyles.Any, CultureInfo.InvariantCulture, out var result) ? result : 0m;

        [JsonPropertyName("4. close")]
        public string CloseString { get; set; }

        [JsonIgnore]
        public decimal Close => decimal.TryParse(CloseString, NumberStyles.Any, CultureInfo.InvariantCulture, out var result) ? result : 0m;

        [JsonPropertyName("5. volume")]
        public string VolumeString { get; set; }

        [JsonIgnore]
        public long Volume => long.TryParse(VolumeString, NumberStyles.Any, CultureInfo.InvariantCulture, out var result) ? result : 0;

    }
}
