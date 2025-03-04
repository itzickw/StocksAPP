using AIModel;
using System.Text;
using System.Text.Json;


namespace AIManager;

internal class OllamaMistral
{
    private const string OllamaEndpoint = "http://localhost:11434/api/";
    private readonly HttpClient _httpClient;
    public OllamaMistral(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }


    public async Task<List<List<float>>> EmbedDocumentAsync(List<string> chunks)
    {
        try
        {
            var embeddings = await ChunksEmbedding(chunks);

            Console.WriteLine($"Total Chunks: {chunks.Count}, Total Embeddings: {embeddings.Count}");

            if (chunks.Count != embeddings.Count)
                throw new Exception("Mismatch between number of chunks and number of embeddings!");

            return embeddings;
        }
        catch (Exception ex)
        {
            throw new Exception($"Error embedding document: {ex.Message}");
        }
    }


    private async Task<List<List<float>>> ChunksEmbedding(List<string> chunks)
    {
        var embeddings = new List<List<float>>();
        foreach (var chunk in chunks)
        {
            var embeddingRequest = new { model = "mistral:latest", prompt = chunk };

            var jsonContent = JsonSerializer.Serialize(embeddingRequest);

            var response = await _httpClient.PostAsync($"{OllamaEndpoint}embeddings",
                new StringContent(jsonContent, Encoding.UTF8, "application/json"));

            if (!response.IsSuccessStatusCode)
            {
                var errorMessage = await response.Content.ReadAsStringAsync();
                throw new Exception($"Ollama API Error: {response.StatusCode}, Response: {errorMessage}");
            }

            var rawResponse = await response.Content.ReadAsStringAsync();
            Console.WriteLine($"Raw Ollama Embedding Response: {rawResponse}");
            var embeddingResult = JsonSerializer.Deserialize<OllamaEmbeddingResponse>(rawResponse);
            Console.WriteLine($"embeddingResult: {embeddingResult}");
            embeddings.Add(embeddingResult.Embedding);
        }
        return embeddings;
    }

    public async Task<List<float>> QueryEmbedding(string query)
    {
        // יצירת embedding לשאלה
        var embeddingRequest = new
        {
            model = "mistral:latest",
            prompt = query
        };

        var jsonContent = JsonSerializer.Serialize(embeddingRequest);
        var embeddingResponse = await _httpClient.PostAsync($"{OllamaEndpoint}embeddings",
            new StringContent(jsonContent, Encoding.UTF8, "application/json"));

        embeddingResponse.EnsureSuccessStatusCode();
        var embeddingResult = await embeddingResponse.Content.ReadAsStringAsync();
        //var questionEmbedding =
        return JsonSerializer.Deserialize<OllamaEmbeddingResponse>(embeddingResult).Embedding;
    }

    public async Task<string> GetAdvisorAsync(string query)
    {
        var answerRequest = new
        {
            model = "mistral:latest",
            prompt = query,
            stream = false
        };

        var jsonRequest = JsonSerializer.Serialize(answerRequest);
        var content = new StringContent(jsonRequest, Encoding.UTF8, "application/json");

        var answerResponse = await _httpClient.PostAsync($"{OllamaEndpoint}generate", content);

        if (!answerResponse.IsSuccessStatusCode)
        {
            throw new Exception($"Ollama API Error: {answerResponse.StatusCode}");
        }

        string jsonResponse = await answerResponse.Content.ReadAsStringAsync();
        var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        var result = JsonSerializer.Deserialize<AIResponse>(jsonResponse, options);

        return result?.Response ?? "No response from AI";
    }
}

