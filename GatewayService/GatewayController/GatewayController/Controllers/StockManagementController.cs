using Microsoft.AspNetCore.Mvc;
using GatewayModel.Stocks;
using GatewayModel.User;
using System.ComponentModel.DataAnnotations;

namespace GatewayController.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class StockManagementController : ControllerBase
    {
        private readonly GatewayManager.GatewayManager _gatewayManager;

        public StockManagementController(GatewayManager.GatewayManager gatewayManager)
        {
            _gatewayManager = gatewayManager;
        }

        [HttpGet("{userId}/holding")]
        public async Task<IActionResult> UserStocksHolding(string userId)
        {
            try
            {
                string response = await _gatewayManager.GetUserHoldingStocks(userId);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost("holding")]
        public async Task<IActionResult> UserStocksHolding(User user)
        {
            try
            {
                string id = await _gatewayManager.UserIDV2(user);
                string response = await _gatewayManager.GetUserHoldingStocks(id);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpGet("{userId}/transactions")]
        public async Task<IActionResult> UserTransactions(string userId)
        {
            try
            {
                string response = await _gatewayManager.GetUserTransactions(userId);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost("transactions")]
        public async Task<IActionResult> UserTransactions(User user)
        {
            try
            {
                string id = await _gatewayManager.UserIDV2(user);
                string response = await _gatewayManager.GetUserTransactions(id);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost("transaction")]
        public async Task<IActionResult> MakeTransaction([FromBody] TransactionGet t)
        {
            try
            {
                string response = await _gatewayManager.MakingTransaction(t);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost("transactionByEmail")]
        public async Task<IActionResult> MakeTransaction([FromBody] TransactionGetByMail t)
        {
            try
            {
                string id = await _gatewayManager.UserIDV2(new User(){ Email = t.Email, Password = t.Password });
                TransactionGet transaction = new TransactionGet()
                {
                    ClientId = int.Parse(id),
                    StockSymbol = t.StockSymbol,
                    Quantity = t.Quantity,
                    TransactionType = t.TransactionType
                };

                string response = await _gatewayManager.MakingTransaction(transaction);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
}
