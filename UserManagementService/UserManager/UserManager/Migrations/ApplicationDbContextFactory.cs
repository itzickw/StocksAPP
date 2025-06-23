using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using UserManager.newUserManager; // עדכן לפי ה־namespace שלך

public class ApplicationDbContextFactory : IDesignTimeDbContextFactory<ApplicationDbContext>
{
    public ApplicationDbContext CreateDbContext(string[] args)
    {
        var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();

        // 🔴 כאן הכנס את ה-Connection String שלך ישירות
        var connectionString = "workstation id=StockManagementDB.mssql.somee.com;packet size=4096;user id=itzikw_SQLLogin_1;pwd=ogp7prxhn4;data source=StockManagementDB.mssql.somee.com;persist security info=False;initial catalog=StockManagementDB;TrustServerCertificate=True";
        optionsBuilder.UseSqlServer(connectionString);

        return new ApplicationDbContext(optionsBuilder.Options);
    }
}
