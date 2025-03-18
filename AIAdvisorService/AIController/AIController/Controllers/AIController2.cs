using AIManager;
using AIModel;
using Microsoft.AspNetCore.Mvc;

namespace AIConsultingServer.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AIController : ControllerBase
{
    private readonly IAIService _aiService;

    public AIController(IAIService aiService)
    {
        _aiService = aiService;
    }

    [HttpPost("file-embedding")]
    public async Task<IActionResult> EmbedDocument(string filePath)
    {
        var result = await _aiService.EmbeddingDocumentAsync(filePath);
        return Ok(result);
    }

    [HttpGet("AI-advice/{query}")]
    public async Task<IActionResult> GetAnswer(string query)
    {
        var answer = await _aiService.GetAnswerAsync(query);
        return Ok(answer);
    }
}