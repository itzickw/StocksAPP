using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace StockModel
{
    public class ApplicationDbContextFactory : IDesignTimeDbContextFactory<ApplicationDbContext>
    {
        public ApplicationDbContext CreateDbContext(string[] args)
        {
            var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
            optionsBuilder.UseSqlServer("workstation id=StockManagementDB.mssql.somee.com;packet size=4096;user id=itzikw_SQLLogin_1;pwd=ogp7prxhn4;data source=StockManagementDB.mssql.somee.com;persist security info=False;initial catalog=StockManagementDB;TrustServerCertificate=True");

            return new ApplicationDbContext(optionsBuilder.Options);
        }
    }
}