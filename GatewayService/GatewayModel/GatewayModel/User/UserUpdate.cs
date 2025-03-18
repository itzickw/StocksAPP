using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GatewayModel.User
{
    public class UserUpdate
    {
        public string Email { get; set; }
        public string Password { get; set; }
        public string NewEmail { get; set; }
        public string NewPassword { get; set; }
    }
}
