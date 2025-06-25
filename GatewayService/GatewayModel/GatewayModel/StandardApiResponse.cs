using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace GatewayModel
{
    public class StandardApiResponse
    {
        [JsonPropertyName("success")]
        public bool Success { get; set; }

        [JsonPropertyName("message")] // מצביע על השם המדויק ב-JSON
        public string? Message { get; set; } // כאן אתה יכול להשאיר M גדולה ב-C#

        [JsonPropertyName("data")]
        public object? Data { get; set; }
    }
}
