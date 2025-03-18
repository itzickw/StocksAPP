using Microsoft.AspNetCore.Mvc;
using UserManager.newUserManager;
using System.Threading.Tasks;

namespace newUserController.Controllers
{
    [Route("api/v2/[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly UserManager.newUserManager.UserManager _userManager;

        public UserController(UserManager.newUserManager.UserManager userManager)
        {
            _userManager = userManager;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] UserDto userDto)
        {
            if (await _userManager.RegisterUserAsync(userDto.Email, userDto.Password))
                return Ok(new { message = "User registered successfully" });

            return BadRequest(new { message = "Email already exists" });
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] UserDto userDto)
        {
            if (await _userManager.ValidateUserAsync(userDto.Email, userDto.Password))
            {
                var detailes = await _userManager.GetUserByEmailAndPasswordAsync(userDto.Email, userDto.Password);
                return Ok(detailes);
            }

            return Unauthorized(new { message = "Invalid credentials" });
        }

        [HttpDelete("delete")]
        public IActionResult Delete([FromBody] UserDto userDto)
        {
            if (_userManager.DeleteUser(userDto.Email, userDto.Password))
                return Ok(new { message = "User deleted successfully" });
            return NotFound(new { message = "Invalid email or password" });
        }

        [HttpPost("user-details")]
        public async Task<IActionResult> GetUserDetails([FromBody] UserDto userDto)
        {
            var user = await _userManager.GetUserByEmailAndPasswordAsync(userDto.Email, userDto.Password);
            if (user == null)
                return NotFound(new { message = "Invalid email or password" });
            return Ok(user);
        }

        [HttpPut("update")]
        public Task<IActionResult> UserUpdate([FromBody] UpdateUserDto userDto)
        {
            if (_userManager.UpdateUser(userDto.Email, userDto.Password, userDto.NewEmail, userDto.NewPassword))
                return Task.FromResult<IActionResult>(Ok(new { message = "User updated successfully" }));
            return Task.FromResult<IActionResult>(NotFound(new { message = "Invalid email or password" }));
        }

        public class UserDto
        {
            public string Email { get; set; }
            public string Password { get; set; }
        }

        public class UpdateUserDto
        {
            public string Email { get; set; }
            public string Password { get; set; }
            public string NewEmail { get; set; }
            public string NewPassword { get; set; }
        }
    }
}
