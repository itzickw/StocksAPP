using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace AIModel
{
    public class ChromaQueryResponse
    {
        [JsonPropertyName("documents")]
        public List<List<string>> Documents { get; set; }

        [JsonPropertyName("distances")]
        public List<List<double>> Distances { get; set; } // רשימת רשימות של double

        [JsonPropertyName("metadatas")]
        public List<List<object>> Metadatas { get; set; }
    }
}
