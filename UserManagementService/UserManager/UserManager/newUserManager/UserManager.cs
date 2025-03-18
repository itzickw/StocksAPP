using Microsoft.EntityFrameworkCore;
using System.Text.RegularExpressions;
using UserModel.newUser;

namespace UserManager.newUserManager
{
    public class UserManager
    {
        private readonly ApplicationDbContext _context;

        public UserManager(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<bool> RegisterUserAsync(string email, string password)
        {
            if (!IsValidEmail(email))
            {
                throw new ArgumentException("Invalid email format.");
            }

            if (await _context.Users.AnyAsync(u => u.Email == email))
                return false; // המשתמש כבר קיים

            var user = new User { Email = email };
            user.SetPassword(password);

            _context.Users.Add(user);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<UserDto?> GetUserByEmailAndPasswordAsync(string email, string password)
        {
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
            if (user == null || !user.VerifyPassword(password))
            {
                return null; // אימייל לא קיים או סיסמה לא נכונה
            }

            return new UserDto
            {
                Id = user.Id,
                Email = user.Email,
                CreatedAt = user.RegisteredAt
            };
        }

        public bool UpdateUser(string email, string password, string newEmail, string newPassword)
        {
            var user = _context.Users.FirstOrDefault(u => u.Email == email);
            if (user == null || !user.VerifyPassword(password))
            {
                throw new ArgumentException("Invalid email or password.");
            }

            if (!IsValidEmail(newEmail))
            {
                throw new ArgumentException("Invalid email format.");
            }

            user.Email = newEmail;
            user.SetPassword(newPassword);
            _context.SaveChanges();
            return true;
        }

        public bool DeleteUser(string email, string password)
        {
            
            var user = _context.Users.FirstOrDefault(u => u.Email == email);
            if (user == null || !user.VerifyPassword(password))
            {
                return false;
            }

            _context.Users.Remove(user);
            _context.SaveChanges();
            return true;
        }

        public async Task<bool> ValidateUserAsync(string email, string password)
        {
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
            return user != null && user.VerifyPassword(password);
        }

        private bool IsValidEmail(string email)
        {
            return Regex.IsMatch(email, @"^[^@\s]+@[^@\s]+\.[^@\s]+$");
        }
    }
}
