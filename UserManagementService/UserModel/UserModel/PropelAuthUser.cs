using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace UserModel
{
    public class PropelAuthUser
    {
        [JsonPropertyName("user_id")]
        public string? UserId { get; set; }
    }
}