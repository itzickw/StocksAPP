﻿using AIModel;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace AIManager;

internal class ChromaDB
{
    private readonly HttpClient _httpClient;
    //private const string CollectionName = "stock_advice";
    private readonly string CollectionID = "29d040ac-89e2-4d55-9636-ad99f807d627";
    private readonly string ChromaEndpoint = "http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database";

    public ChromaDB(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<string> StoreEmbeddingVector(List<string> chunks, List<string> ids, List<List<float>> embeddings)
    {
        var chromaRequest = new
        {
            embeddings,
            metadatas = ids.Select(_ => new { }).ToArray(), // רשימה של אובייקטים ריקים
            documents = chunks.ToArray(),
            uris = ids.Select(_ => (string)null).ToArray(),
            ids = ids.ToArray()
        };

        var chromaJson = JsonSerializer.Serialize(chromaRequest, new JsonSerializerOptions { WriteIndented = true });
        Console.WriteLine($"ChromaDB Request JSON: {chromaJson}");

        // שליחת הנתונים ל-ChromaDB
        var chromaResponse = await _httpClient.PostAsync(
            $"{ChromaEndpoint}/collections/{CollectionID}/add",
            new StringContent(chromaJson, Encoding.UTF8, "application/json")
        );

        if (!chromaResponse.IsSuccessStatusCode)
        {
            var errorResponse = await chromaResponse.Content.ReadAsStringAsync();
            throw new Exception($"ChromaDB API Error: {chromaResponse.StatusCode}, Response: {errorResponse}");
        }

        return "Document embedded and stored successfully";
    }

    public async Task<ChromaQueryResponse> ChromaQueryGetNearestNeighbors(List<float> questionEmbedding)
    {
        var queryRequest = new
        {
            query_embeddings = new[] { questionEmbedding },  // רשימת ההטמעות לחיפוש
            n_results = 4,  // מספר תוצאות להחזיר
            include = new[] { "metadatas", "documents", "distances" }  // אילו פרטים להחזיר
        };

        var queryResponse = await _httpClient.PostAsync(
            $"{ChromaEndpoint}/collections/{CollectionID}/query",
            new StringContent(
                JsonSerializer.Serialize(queryRequest),
                Encoding.UTF8,
                "application/json"
            )
        );

        var responseBody = await queryResponse.Content.ReadAsStringAsync();

        queryResponse.EnsureSuccessStatusCode();

        var queryResult = await queryResponse.Content.ReadFromJsonAsync<ChromaQueryResponse>();
        return queryResult;
    }
}