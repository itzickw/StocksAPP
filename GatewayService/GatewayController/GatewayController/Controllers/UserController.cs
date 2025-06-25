using GatewayModel;
using GatewayModel.User;
using Microsoft.AspNetCore.Mvc;

namespace GatewayController.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UserController : ControllerBase
    {
        private readonly GatewayManager.GatewayManager _gatewayManager;

        public UserController(GatewayManager.GatewayManager gatewayManager)
        {
            _gatewayManager = gatewayManager;
        }

        [HttpGet("Login-URL")]
        public IActionResult LoginUrl()
            => Ok("https://33704590271.propelauthtest.com");


        [HttpPost("Registration")]
        public async Task<IActionResult> Registration([FromBody] User user)
        {
            try
            {
                var result = await _gatewayManager.UserRegister(user);
                return Ok(result);
            }
            catch (Exception ex) { return BadRequest(ex.Message); }
        }

        [HttpPost("V2/Registration")]
        public async Task<IActionResult> Register([FromBody] User user) // שיניתי את שם המתודה ל-Register כדי שתהיה עקבית יותר
        {
            StandardApiResponse result = await _gatewayManager.UserRegisterV2(user);
            return Ok(result);
        }



        [HttpDelete("DeleteUser")]
        public async Task<IActionResult> DeleteUser([FromQuery] string email)
        {
            try
            {
                var result = await _gatewayManager.UserDelete(email);
                return Ok(result);
            }
            catch (Exception ex) { return BadRequest(ex.Message); }
        }

        [HttpDelete("V2/DeleteUser")]
        public async Task<IActionResult> V2DeleteUser([FromQuery] string email, [FromQuery] string password)
        {
            StandardApiResponse result = await _gatewayManager.UserDeleteV2(email, password);
            return Ok(result);
        }

        [HttpPut("UpdatePassword")]
        public async Task<IActionResult> UpdatePassword([FromBody] User user)
        {
            try
            {
                var result = await _gatewayManager.UserPasswordUpdate(user);
                return Ok(result);
            }
            catch (Exception ex) { return BadRequest(ex.Message); }
        }

        [HttpPut("V2/UpdatePassword")]
        public async Task<IActionResult> V2UpdatePassword([FromBody] UserUpdate user)
        {
            StandardApiResponse result = await _gatewayManager.UserPasswordUpdateV2(user);
            return Ok(result);
        }

        [HttpPost("V2/Login")]
        public async Task<IActionResult> V2Login([FromBody] User user)
        {
            StandardApiResponse result = await _gatewayManager.UserLoginV2(user);
            return Ok(result);
        }

        [HttpPost("V2/UserId")]
        public async Task<IActionResult> V2Details([FromBody] User user)
        {
            StandardApiResponse result = await _gatewayManager.UserIDV2(user);
            return Ok(result);
        }

    }
}
