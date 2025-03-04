using AIModel;

namespace AIManager;

public interface IAIService
{
    Task<string> EmbeddingDocumentAsync(string filePath);
    Task<string> GetAnswerAsync(string query);
}