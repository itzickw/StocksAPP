using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StockModel
{
    public class StockHolding
    {
        public int Id { get; set; }
        public int ClientId { get; set; }
        public string StockSymbol { get; set; }  // שונה מ-StockId ל-StockSymbol
        public decimal Quantity { get; set; }
    }

}