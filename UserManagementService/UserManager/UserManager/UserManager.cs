using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net;
using System.Net.Http.Headers;
using UserModel;

namespace UserManager
{
    public class UserManager
    {
        private readonly HttpClient _httpClient;
        private readonly string _propelAuthUrl = "https://33704590271.propelauthtest.com";
        private readonly string _propelAuthApiKey = "545d6af0e500d797d5b52c051dac0bd7bf6be8721acb6a86274da602d25e4f616d506d502ae4a30de357ff2e0b845c43";

        public UserManager(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }


        public async Task<string?> GetUserIdByEmailAsync(string email)
        {
            var url = $"{_propelAuthUrl}/api/backend/v1/user/email?email={Uri.EscapeDataString(email)}";
            using var request = new HttpRequestMessage(HttpMethod.Get, url);
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _propelAuthApiKey);

            using var response = await _httpClient.SendAsync(request);
            if (!response.IsSuccessStatusCode) return null;

            var jsonResponse = JsonSerializer.Deserialize<JsonElement>(await response.Content.ReadAsStringAsync());
            return jsonResponse.GetProperty("user_id").GetString();
        }



        public async Task<string> RegisterUserAsync(string email, string password)
        {
            // בדיקה אם המשתמש כבר קיים במערכת
            string? existingUserId = await GetUserIdByEmailAsync(email);
            if (existingUserId != null)
            {
                throw new Exception("The user alredy exists");
            }

            var requestBody = new
            {
                email,
                password
            };

            var jsonContent = new StringContent(JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");

            using var request = new HttpRequestMessage(HttpMethod.Post, $"{_propelAuthUrl}/api/backend/v1/user/")
            {
                Content = jsonContent
            };
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _propelAuthApiKey);

            using var response = await _httpClient.SendAsync(request);
            var responseBody = await response.Content.ReadAsStringAsync();

            if (!response.IsSuccessStatusCode)
            {
                throw new Exception($"User registration error: {response.StatusCode} - {responseBody}");
            }

            return responseBody;
        }


        public async Task<bool> DeleteUserAsync(string email)
        {
            try
            {
                // השגת ה- ID של המשתמש לפי האימייל
                string? userId = await GetUserIdByEmailAsync(email);
                Console.WriteLine($"user ID to delete: '{userId}'");
                if (userId == null)
                {
                    //Console.WriteLine("❌ המשתמש לא נמצא, אין צורך למחוק.");
                    return false;
                }

                // שליחת בקשת מחיקה לפי ה-ID
                var request = new HttpRequestMessage(HttpMethod.Delete, $"{_propelAuthUrl}/api/backend/v1/user/{userId}");
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _propelAuthApiKey);

                HttpResponseMessage response = await _httpClient.SendAsync(request);

                if (response.IsSuccessStatusCode)
                {
                    //Console.WriteLine("✅ User deleted successfuly.");
                    return true;
                }
                else
                {
                    string error = await response.Content.ReadAsStringAsync();
                    //Console.WriteLine($"❌ נכשל במחיקת המשתמש: {error}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                //Console.WriteLine($"❌ חריגה אירעה: {ex.Message}");
                return false;
            }
        }

        public async Task<bool> UpdateUserPasswordAsync(string email, string newPassword)
        {
            string? userId = await GetUserIdByEmailAsync(email);

            if (string.IsNullOrEmpty(userId))
            {
                Console.WriteLine("❌ לא נמצא מזהה משתמש עבור האימייל שסופק.");
                return false;
            }

            var requestBody = new
            {
                password = newPassword,
                ask_user_to_update_password_on_login = false
            };

            var jsonContent = new StringContent(JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");

            using var request = new HttpRequestMessage(HttpMethod.Put, $"{_propelAuthUrl}/api/backend/v1/user/{userId}/password")
            {
                Content = jsonContent
            };
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _propelAuthApiKey);

            using var response = await _httpClient.SendAsync(request);
            var responseBody = await response.Content.ReadAsStringAsync();

            Console.WriteLine($"🔵 סטטוס תגובה: {response.StatusCode}");
            Console.WriteLine($"🔵 תוכן תגובה: {responseBody}");

            return response.IsSuccessStatusCode;
        }

    }
}