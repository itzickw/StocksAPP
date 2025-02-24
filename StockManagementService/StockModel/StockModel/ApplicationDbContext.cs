using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Reflection.Emit;
using System.Transactions;

namespace StockModel
{
    public class ApplicationDbContext : DbContext
    {
        public DbSet<Transaction> Transactions { get; set; }
        public DbSet<StockHolding> StockHoldings { get; set; }

        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        // קונסטרקטור ריק ש-EF Core יכול להשתמש בו בזמן יצירת מיגרציות
        public ApplicationDbContext()
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<StockHolding>()
                .HasKey(s => s.Id);

            modelBuilder.Entity<StockHolding>()
                .Property(s => s.StockSymbol)
                .IsRequired();
        }


        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer("workstation id=StockManagementDB.mssql.somee.com;packet size=4096;user id=itzikw_SQLLogin_1;pwd=ogp7prxhn4;data source=StockManagementDB.mssql.somee.com;persist security info=False;initial catalog=StockManagementDB;TrustServerCertificate=True");
            }
        }
    }
}