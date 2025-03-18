using System;
using System.Globalization;

namespace GatewayModel.Stocks
{
    public class StockPrice
    {
        public DateTime Date { get; set; }
        public decimal ClosePrice { get; set; }

        public override string ToString()
        {
            return $"Date: {Date:yyyy-MM-dd}, Price: {ClosePrice.ToString(CultureInfo.InvariantCulture)}";
        }
    }
}
