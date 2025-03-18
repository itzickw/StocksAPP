using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GatewayModel.Stocks
{
    public class TransactionGetByMail
    {
        public string Email { get; set; }
        public string Password { get; set; }
        public string StockSymbol { get; set; }
        public decimal Quantity { get; set; }
        public string TransactionType { get; set; }
    }
}
