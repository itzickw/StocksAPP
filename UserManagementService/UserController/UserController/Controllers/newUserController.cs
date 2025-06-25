using Microsoft.AspNetCore.Mvc;
using UserManager.newUserManager;
using System.Threading.Tasks;
using UserModel.newUser;

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
            StandardApiResponse response = await _userManager.RegisterUserAsync(userDto.Email, userDto.Password);
            return Ok(response);
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] UserDto userDto)
        {
            StandardApiResponse response = await _userManager.ValidateUserAsync(userDto.Email, userDto.Password);
            return Ok(response);
        }

        [HttpDelete("delete/{email}/{password}")]
        public async Task<IActionResult> Delete(string email, string password)
        {
            StandardApiResponse response = await _userManager.DeleteUser(email, password);
                return Ok(response);
        }

        [HttpPost("user-details")]
        public async Task<IActionResult> GetUserDetails([FromBody] UserDto userDto)
        {
            StandardApiResponse response = await _userManager.GetUserByEmailAndPasswordAsync(userDto.Email, userDto.Password);
            return Ok(response);
        }

        [HttpPut("update")]
        public async Task<IActionResult> UserUpdate([FromBody] UpdateUserDto userDto)
        {
            StandardApiResponse response = await _userManager.UpdateUser(userDto.Email, userDto.Password, userDto.NewEmail, userDto.NewPassword);
            return Ok(response);
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
