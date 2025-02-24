using StockModel;
using System.Collections.Generic;
using System.Linq;
using System.Transactions;

namespace StockManager
{
    public class StockManager
    {
        private readonly ApplicationDbContext _context;

        public StockManager(ApplicationDbContext context)
        {
            _context = context;
        }

        // קבלת כל העסקאות של לקוח מסוים לפי מזהה לקוח
        public IEnumerable<StockModel.Transaction> GetTransactions(int clientId)
        {
            return _context.Transactions.Where(t => t.ClientId == clientId).ToList();
        }

        // הוספת עסקה חדשה ועדכון כמות המניות בפועל
        public void AddTransaction(StockModel.Transaction transaction)
        {
            if (transaction.Timestamp == null)
                transaction.Timestamp = DateTime.UtcNow;

            _context.Transactions.Add(transaction);
            UpdateStockHoldings(transaction);
            _context.SaveChanges();
        }

        // קבלת מחזיק מניות לפי מזהה לקוח
        public IEnumerable<StockHolding> GetStockHoldings(int clientId)
        {
            return _context.StockHoldings.Where(h => h.ClientId == clientId).ToList();
        }

        // פונקציה לעדכון כמות המניות בפועל
        private void UpdateStockHoldings(StockModel.Transaction transaction)
        {
            var holding = _context.StockHoldings
                .FirstOrDefault(h => h.ClientId == transaction.ClientId && h.StockSymbol == transaction.StockSymbol);

            if (holding == null)
            {
                // אם זה מכירה ואין החזקה קיימת - זו שגיאה
                if (transaction.TransactionType == "Sell")
                {
                    throw new InvalidOperationException("Cannot sell stock that is not held.");
                }

                holding = new StockHolding
                {
                    ClientId = transaction.ClientId,
                    StockSymbol = transaction.StockSymbol,
                    Quantity = transaction.Quantity // קנייה מוסיפה כמות
                };
                _context.StockHoldings.Add(holding);
            }
            else
            {
                if (transaction.TransactionType == "Sell")
                {
                    if (holding.Quantity < transaction.Quantity)
                    {
                        throw new InvalidOperationException("Not enough stock to sell.");
                    }
                    holding.Quantity -= transaction.Quantity; // מכירה מורידה כמות
                    return;
                }
                if (transaction.TransactionType == "Buy")
                {
                    holding.Quantity += transaction.Quantity; // קנייה מוסיפה כמות
                    return;
                }
                else
                {
                    throw new InvalidOperationException("Invalid transaction type.");
                }
            }
        }


        // פונקציה למחיקת כל הנתונים של לקוח מסוים בכל הטבלאות
        public void DeleteClientData(int clientId)
        {
            var transactions = _context.Transactions.Where(t => t.ClientId == clientId).ToList();
            var holdings = _context.StockHoldings.Where(h => h.ClientId == clientId).ToList();

            _context.Transactions.RemoveRange(transactions);
            _context.StockHoldings.RemoveRange(holdings);
            _context.SaveChanges();
        }
    }

}