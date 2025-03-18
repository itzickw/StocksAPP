using GatewayModel.User;
using System.Text;
using System.Text.Json;

namespace GatewayManager
{
    internal class UserGateway
    {
        private readonly string userServiceUrl = "http://localhost:9150/api/Users";
        private readonly string userV2ServiceUrl = "http://localhost:9150/api/v2/User";

        private readonly HttpClient _httpClient;

        internal UserGateway(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        internal async Task<string> UserRegister(User user)
        {
            //User user = new User
            //{
            //    Email = email,
            //    Password = password
            //};

            var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });

            var userResponse = await _httpClient.PostAsync(
                $"{userServiceUrl}/register", new StringContent(userJson, Encoding.UTF8, "application/json")
            );

            return await userResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> UserDelete(string email)
        {
            var userResponse = await _httpClient.DeleteAsync($"{userServiceUrl}/delete/{email}");
            return await userResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> UserPasswordUpdate(User user)
        {
            //User user = new User
            //{
            //    Email = email,
            //    Password = password
            //};
            var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
            var userResponse = await _httpClient.PutAsync(
                $"{userServiceUrl}/update-password", new StringContent(userJson, Encoding.UTF8, "application/json")
            );
            return await userResponse.Content.ReadAsStringAsync();
        }

        //========================================      v2 funcs    ========================================================

        internal async Task<string> UserRegisterV2(User user)
        {
            var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
            var userResponse = await _httpClient.PostAsync(
                $"{userV2ServiceUrl}/register", new StringContent(userJson, Encoding.UTF8, "application/json")
            );
            return await userResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> UserDeleteV2(string email, string password)
        {
            var userResponse = await _httpClient.DeleteAsync($"{userV2ServiceUrl}/delete/{email}/{password}");
            return await userResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> UserLoginV2(User user)
        {

            var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
            var userResponse = await _httpClient.PostAsync(
                $"{userV2ServiceUrl}/login", new StringContent(userJson, Encoding.UTF8, "application/json")
            );
            return await userResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> UserPasswordUpdateV2(UserUpdate user)
        {
            var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
            var userResponse = await _httpClient.PutAsync(
                $"{userV2ServiceUrl}/update-password", new StringContent(userJson, Encoding.UTF8, "application/json")
            );
            return await userResponse.Content.ReadAsStringAsync();
        }

        internal async Task<string> UserIDV2(User user)
        {
            var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
            var userResponse = await _httpClient.PostAsync(
                $"{userV2ServiceUrl}/user-details", new StringContent(userJson, Encoding.UTF8, "application/json")
            );

            using (JsonDocument doc = JsonDocument.Parse(await userResponse.Content.ReadAsStringAsync()))
            {
                if (doc.RootElement.TryGetProperty("id", out JsonElement idElement))
                {
                    return idElement.ToString(); // מחזיר רק את ה-ID כמחרוזת
                }
            }
            return await userResponse.Content.ReadAsStringAsync();
        }
    }
}
