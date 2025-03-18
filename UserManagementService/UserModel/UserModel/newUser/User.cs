using System.Text;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Security.Cryptography;

namespace UserModel.newUser
{
    public class User
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)] // יצירת מזהה ייחודי אוטומטי
        public int Id { get; set; }

        [Required]
        [EmailAddress]
        public string Email { get; set; }

        [Required]
        public string PasswordHash { get; private set; }

        [Required]
        public string Salt { get; private set; }

        public DateTime RegisteredAt { get; set; } = DateTime.UtcNow;

        public void SetPassword(string password)
        {
            Salt = GenerateSalt();
            PasswordHash = HashPassword(password, Salt);
        }

        public bool VerifyPassword(string password)
        {
            string hash = HashPassword(password, Salt);
            return hash == PasswordHash;
        }

        private static string GenerateSalt()
        {
            byte[] saltBytes = new byte[16];
            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(saltBytes);
            }
            return Convert.ToBase64String(saltBytes);
        }

        private static string HashPassword(string password, string salt)
        {
            using (var sha256 = SHA256.Create())
            {
                byte[] combinedBytes = Encoding.UTF8.GetBytes(password + salt);
                byte[] hashBytes = sha256.ComputeHash(combinedBytes);
                return Convert.ToBase64String(hashBytes);
            }
        }
    }
}
