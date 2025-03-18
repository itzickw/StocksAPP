using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;

namespace GatewayController.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AIAdvisorController : ControllerBase
    {
        private readonly GatewayManager.GatewayManager _gatewayManager;

        public AIAdvisorController(GatewayManager.GatewayManager gatewayManager)
        {
            _gatewayManager = gatewayManager;
        }

        [HttpGet("AIadvice/{query}")]
        public async Task<IActionResult> GetAIAdvice(string query)
        {
            try
            {
                string advice = await _gatewayManager.GetAIAdvice(query);
                return Ok(advice);
            }
            catch (Exception ex) { return BadRequest(ex.Message); }
        }

        [HttpGet("based-history-advice/{stockSymbol}")]
        public async Task<IActionResult> GetBasedStockHistoryAdvice(string stockSymbol)
        {
            try
            {
                var advice = await _gatewayManager.GetBasedStockHistoryAdvice(stockSymbol);
                return Ok(advice);
            }
            catch (Exception ex) { return BadRequest(ex.Message); }
        }
    }
}
