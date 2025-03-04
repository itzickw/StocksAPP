using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace AIModel
{
    public class OllamaEmbeddingResponse
    {

        [JsonPropertyName("embedding")]
        public List<float> Embedding { get; set; }
    }
}
