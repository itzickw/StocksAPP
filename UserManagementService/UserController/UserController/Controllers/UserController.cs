using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using UserModel;
using UserManager;

[Route("api/[controller]")]
[ApiController]
public class UsersController : ControllerBase
{
    private readonly UserManager.UserManager _userManager;

    public UsersController(UserManager.UserManager userManager)
    {
        _userManager = userManager;
    }

    [HttpPost("register")]
    public async Task<IActionResult> RegisterUser([FromBody] User userDto)
    {
        var result = await _userManager.RegisterUserAsync(userDto.Email, userDto.Password);

        if (result == "User already exists")
            return Conflict(new { message = result });

        if (result.StartsWith("Registration failed"))
            return BadRequest(new { message = result });

        return Ok(new { message = result });
    }

    [HttpGet("callback")]
    public IActionResult Callback([FromQuery] string access_token, [FromQuery] string code)
    {
        if (!string.IsNullOrEmpty(access_token))
        {
            // שמור את ה-token או בצע אימות
            return Ok(new { Token = access_token });
        }
        else if (!string.IsNullOrEmpty(code))
        {
            // אם PropelAuth מחזיר קוד במקום טוקן, בצע קריאה נוספת ל-PropelAuth להמיר את ה-code ל-token
            return Ok(new { Code = code });
        }
        return BadRequest("No token or code received");
    }

    [HttpDelete("delete/{email}")]
    public async Task<IActionResult> DeleteUser(string email)
    {
        Console.WriteLine($"📨 got mail to delete: '{email}'");

        if (string.IsNullOrWhiteSpace(email))
        {
            return BadRequest("❌ Incorrect email address.");
        }

        bool success = await _userManager.DeleteUserAsync(email);

        if (success)
        {
            return Ok("✅ User deleted successfuly.");
        }
        else
        {
            return NotFound("❌ User not found or cannot be deleted.");
        }
    }

    [HttpPut("update-password")]
    public async Task<IActionResult> UpdatePassword([FromBody] User request)
    {
        if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
        {
            return BadRequest("❌ email and new passord are mandetory.");
        }

        bool isUpdated = await _userManager.UpdateUserPasswordAsync(request.Email, request.Password);

        if (!isUpdated)
        {
            return NotFound("❌ User not found or cannot be updated.");
        }

        return Ok("✅ The new password successfuly updated");
    }
}