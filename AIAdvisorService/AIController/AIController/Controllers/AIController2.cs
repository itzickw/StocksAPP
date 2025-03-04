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

    [HttpPost("embed")]
    public async Task<IActionResult> EmbedDocument([FromBody] DocumentModel document)
    {
        var result = await _aiService.EmbedDocumentAsync(document);
        return Ok(result);
    }

    [HttpPost("query")]
    public async Task<IActionResult> GetAnswer([FromBody] QueryModel query)
    {
        var answer = await _aiService.GetAnswerAsync(query);
        return Ok(answer);
    }
}