using Microsoft.EntityFrameworkCore;
using System.Text.RegularExpressions;
using UserModel.newUser;
//using UserModel;

namespace UserManager.newUserManager
{
    public class UserManager
    {
        private readonly ApplicationDbContext _context;

        public UserManager(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<StandardApiResponse> RegisterUserAsync(string email, string password)
        {
            if (!IsValidEmail(email))
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = "Invalid email format."
                };
            }

            if (await _context.Users.AnyAsync(u => u.Email == email))
                return new StandardApiResponse
                {
                    Success = false,
                    Message = "Registration failed: User with this email already exists."
                };

            var user = new User { Email = email };
            user.SetPassword(password);

            try
            {
                _context.Users.Add(user);
                await _context.SaveChangesAsync();

                return new StandardApiResponse
                {
                    Success = true,
                    Message = "User registered successfully."
                    // Data = new { UserId = user.Id } // ניתן להוסיף כאן נתונים אם תרצה
                };
            }

            catch (Exception ex)
            {
                // במקרה של שגיאת DB, עדיין מחזירים StandardApiResponse עם Success=false
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"An error occurred during registration: {ex.Message}"
                };
            }
        }

        public async Task<StandardApiResponse> GetUserByEmailAndPasswordAsync(string email, string password)
        {
            try
            {

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
            if (user == null || !user.VerifyPassword(password))
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = "Invalid email or password."
                };
            }

            return new StandardApiResponse
            {
                Success = true,
                Message = "User successfully retrieved",
                Data = new UserDto
                {
                    Id = user.Id,
                    Email = user.Email,
                    CreatedAt = user.RegisteredAt
                }
            };            
            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"An error occurred while retrieving user: {ex.Message}"
                };
            }
        }

        public async Task<StandardApiResponse> UpdateUser(string email, string password, string newEmail, string newPassword)
        {
            try
            {
                var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
                if (user == null || !user.VerifyPassword(password))
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Invalid email or password."
                    };
                }
                if (!IsValidEmail(newEmail))
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Invalid new email format."
                    };
                }
                user.Email = newEmail;
                user.SetPassword(newPassword);
                await _context.SaveChangesAsync();
                return new StandardApiResponse
                {
                    Success = true,
                    Message = "User updated successfully."
                };
            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"An error occurred while updating user: {ex.Message}"
                };
            }
        }

        public async Task<StandardApiResponse> DeleteUser(string email, string password)
        {
            try
            {
                var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
                if (user == null || !user.VerifyPassword(password))
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Invalid email or password."
                    };
                }
                _context.Users.Remove(user);
                await _context.SaveChangesAsync();
                return new StandardApiResponse
                {
                    Success = true,
                    Message = "User deleted successfully."
                };

            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"An error occurred while deleting user: {ex.Message}"
                };
            }
        }

        public async Task<StandardApiResponse> ValidateUserAsync(string email, string password)
        {
            try
            {
                var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
                if (user == null || !user.VerifyPassword(password))
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Invalid email or password."
                    };
                }
                return new StandardApiResponse
                {
                    Success = true,
                    Message = "User validation successful."
                };
            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"An error occurred during user validation: {ex.Message}"
                };
            }
        }

        private bool IsValidEmail(string email)
        {
            return Regex.IsMatch(email, @"^[^@\s]+@[^@\s]+\.[^@\s]+$");
        }
    }
}
