using GatewayModel.Stocks;
using Microsoft.AspNetCore.Mvc;

namespace GatewayController.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class StockDataController : ControllerBase
    {
        private readonly GatewayManager.GatewayManager _gatewayManager;

        public StockDataController(GatewayManager.GatewayManager gatewayManager)
        {
            _gatewayManager = gatewayManager;
        }

        [HttpGet("current-data/{symbol}")]
        public async Task<IActionResult> GetCurrentPrice(string symbol)
        {
            try
            {
                decimal price = await _gatewayManager.GetStockPrice(symbol);
                return Ok(price);
            }
            catch (Exception e)
            {
                return BadRequest(e.Message);
            }
        }

        [HttpGet("stock-history/{symbol}/{range}")]
        public async Task<IActionResult> GetStockHistory(string symbol, int range)
        {
            try
            {
                List<StockPrice> data = await _gatewayManager.GetStockHistory(symbol, range);
                return Ok(data);
            }
            catch (Exception e)
            {
                return BadRequest(e.Message);
            }
        }

        [HttpGet("stock-weekly-history")]
        public async Task<IActionResult> GetStockPeriodWeeklyHistory(
            [FromQuery] string symbol, 
            [FromQuery] int range, 
            [FromQuery] int interval)
        {
            try
            {
                List<StockPrice> data = await _gatewayManager.GetStockPeriodWeeklyHistory(symbol, range, interval);
                return Ok(data);
            }
            catch (Exception e)
            {
                return BadRequest(e.Message);
            }
        }
    }
}
