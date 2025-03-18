using MarketDataManager;
using MarketDataModel;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

[ApiController]
[Route("api/[controller]")]
public class MarketDataController : ControllerBase
{    
    private readonly AlphaVantageService _alphaVantageService;

    public MarketDataController(AlphaVantageService alphaVantageService)
    {       
        _alphaVantageService = alphaVantageService;
    }

    [HttpGet("{symbol}/{range}")]
    public async Task<IActionResult> GetStockDailyData(string symbol, int range)
    {
        try
        {
            var data = await _alphaVantageService.GetStockDataForPeriodAsync(symbol, range);
            return Ok(data);
        }
        catch (Exception ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    [HttpGet("stock-data/{symbol}")]
    public async Task<IActionResult> GetStockInterdayData(string symbol)
    {
        try
        {
            var data = await _alphaVantageService.GetRealtimeStockDataAsync(symbol);
            return Ok(data);
        }
        catch (Exception ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    [HttpGet("weekly-stock-data")]
    public async Task<IActionResult> GetStockData(
    [FromQuery] string symbol,
    [FromQuery] int days,
    [FromQuery] int weeksInterval = 1)
    {
        if (string.IsNullOrWhiteSpace(symbol) || days <= 0)
        {
            return BadRequest("Invalid parameters.");
        }

        var result = await _alphaVantageService.GetWeeklyStockDataForPeriodAsync(symbol, days, weeksInterval);

        return Ok(result);
    }
}