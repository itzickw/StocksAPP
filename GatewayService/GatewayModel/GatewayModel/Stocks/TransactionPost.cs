﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GatewayModel.Stocks
{
    public class TransactionPost
    {        
        public int ClientId { get; set; }
        public string StockSymbol { get; set; }
        public decimal Quantity { get; set; }
        public string TransactionType { get; set; }
        public decimal Price { get; set; }
        public DateTime Date { get; set; }
    }
}
