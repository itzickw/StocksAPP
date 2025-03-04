using AIModel;

namespace AIManager;

public interface IAIService
{
    Task<string> EmbedDocumentAsync(DocumentModel document);
    Task<string> GetAnswerAsync(QueryModel query);
}