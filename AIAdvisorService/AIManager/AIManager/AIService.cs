using AIModel;
using Azure;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using UglyToad.PdfPig;

namespace AIManager;

public class AIService : IAIService
{
    //private readonly HttpClient _httpClient;
    private readonly OllamaMistral ollamaMistralEmbedding;
    private readonly ChromaDB chromaDBStore;
    private readonly TextProcessing textProcessing;
    public AIService(HttpClient httpClient)
    {
        //_httpClient = httpClient;
        ollamaMistralEmbedding = new OllamaMistral(httpClient);
        chromaDBStore = new ChromaDB(httpClient);
        textProcessing = new TextProcessing();
    }

    public async Task<string> EmbeddingDocumentAsync(string filePath)
    {
        //string content = ExtracrTextFromPdf(document.FilePath);

        var chunks = textProcessing.SplitFileIntoChunksWithOverlap(filePath, 100, 20);
        //SplitTextIntoChunksWithOverlap(content, 100, 20);

        var ids = chunks.Select(_ => Guid.NewGuid().ToString()).ToList();

        var embeddings = await ollamaMistralEmbedding.EmbedDocumentAsync(chunks);

        string result = await chromaDBStore.StoreEmbeddingVector(chunks, ids, embeddings);
        return result;
    }


    public async Task<string> GetAnswerAsync(string query)
    {
        try
        {
            var questionEmbedding = await ollamaMistralEmbedding.QueryEmbedding(query);
            var queryResult = await chromaDBStore.ChromaQueryGetNearestNeighbors(questionEmbedding);
            var context = string.Join("\n", queryResult.Documents[0]);
            var ragPrompt = $"Context: {context}\nQuestion: {query}\nAnswer:";
            Console.WriteLine($"query ragPrompt: {ragPrompt}");
            return await ollamaMistralEmbedding.GetAdvisorAsync(ragPrompt);

            //return await ollamaMistralEmbedding.GetAdvisorAsync(query.Question);
        }
        catch (Exception ex)
        {
            return $"Error getting answer: {ex.Message}";
        }
    }
}