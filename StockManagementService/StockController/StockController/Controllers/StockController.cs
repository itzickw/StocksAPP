using Microsoft.AspNetCore.Mvc;
using StockModel;
using StockManager;

namespace StockController.Controllers
{
    using Microsoft.AspNetCore.Mvc;
    using StockModel;
    using StockManager;

    [Route("api/[controller]")]
    [ApiController]
    public class StockController : ControllerBase
    {
        private readonly StockManager _stockManager;

        public StockController(StockManager stockManager)
        {
            _stockManager = stockManager;
        }

        // פעולה לקבלת כל העסקאות לפי מזהה לקוח
        [HttpGet("{clientId}/transactions")]
        public IActionResult GetTransactions(int clientId)
        {
            var transactions = _stockManager.GetTransactions(clientId);
            return Ok(transactions);
        }

        [HttpPost("transaction")]
        public IActionResult AddTransaction([FromBody] Transaction transaction)
        {
            if (transaction == null || transaction.Price <= 0 || transaction.Quantity < 1)
            {
                return BadRequest("Invalid transaction data.");
            }

            _stockManager.AddTransaction(transaction);
            return Ok("Transaction added successfully.");
        }


        // פעולה לקבלת מחזיק מניות לפי מזהה לקוח
        [HttpGet("{clientId}/holding")]
        public IActionResult GetStockHolding(int clientId)
        {
            var stockHoldings = _stockManager.GetStockHoldings(clientId);
            return Ok(stockHoldings);
        }

        // פעולה למחיקת כל הנתונים של לקוח מסוים
        [HttpDelete("deleted/{clientId}")]
        public IActionResult DeleteClientData(int clientId)
        {
            _stockManager.DeleteClientData(clientId);
            return Ok(new { message = "Client data deleted successfully." });
        }
    }
}