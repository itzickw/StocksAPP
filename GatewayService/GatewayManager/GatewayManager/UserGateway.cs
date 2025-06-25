using GatewayModel;
using GatewayModel.User;
using Microsoft.Extensions.Options;
using System.Text;
using System.Text.Json;

namespace GatewayManager
{
    internal class UserGateway
    {
        private readonly string userServiceUrl = "http://localhost:9150/api/Users";
        private readonly string userV2ServiceUrl;
        //private readonly string userV2ServiceUrl = "http://localhost:9150/api/v2/User";

        private readonly HttpClient _httpClient;

        internal UserGateway(HttpClient httpClient, IOptions<ServiceUrlsConfig> serviceUrls)
        {
            _httpClient = httpClient;
            userV2ServiceUrl = serviceUrls.Value.userV2ServiceUrl;
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

        internal async Task<StandardApiResponse> UserRegisterV2(User user)
        {
            try
            {
                var userJson = JsonSerializer.Serialize(user);
                var content = new StringContent(userJson, Encoding.UTF8, "application/json");
                var userResponse = await _httpClient.PostAsync($"{userV2ServiceUrl}/register", content);
                var responseString = await userResponse.Content.ReadAsStringAsync();
                var standardResponse = JsonSerializer.Deserialize<StandardApiResponse>(responseString);

                if (standardResponse == null)
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Gateway Error: User Management Service returned an empty or unparseable response (despite 200 OK)."
                    };
                }

                return standardResponse;
            }
            catch (HttpRequestException ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway communication failed with User Management Service: {ex.Message}. Please try again later."
                };
            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway encountered an unexpected error: {ex.Message}. Check logs for details."
                };
            }
        }



        internal async Task<StandardApiResponse> UserDeleteV2(string email, string password)
        {
            try
            {
                var userResponse = await _httpClient.DeleteAsync($"{userV2ServiceUrl}/delete/{email}/{password}");
                var responseString = await userResponse.Content.ReadAsStringAsync();
                var standardResponse = JsonSerializer.Deserialize<StandardApiResponse>(responseString);
                if (standardResponse == null)
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Gateway Error: User Management Service returned an empty or unparseable response (despite 200 OK)."
                    };
                }
                return standardResponse;
            }
            catch (HttpRequestException ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway communication failed with User Management Service: {ex.Message}. Please try again later."
                };
            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway encountered an unexpected error: {ex.Message}. Check logs for details."
                };
            }
        }

        internal async Task<StandardApiResponse> UserLoginV2(User user)
        {
            try
            {
                var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
                var content = new StringContent(userJson, Encoding.UTF8, "application/json");
                var userResponse = await _httpClient.PostAsync($"{userV2ServiceUrl}/login", content);
                var responseString = await userResponse.Content.ReadAsStringAsync();
                var standardResponse = JsonSerializer.Deserialize<StandardApiResponse>(responseString);
                if (standardResponse == null)
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Gateway Error: User Management Service returned an empty or unparseable response (despite 200 OK)."
                    };
                }
                return standardResponse;
            }
            catch (HttpRequestException ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway communication failed with User Management Service: {ex.Message}. Please try again later."
                };
            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway encountered an unexpected error: {ex.Message}. Check logs for details."
                };
            }
        }

        internal async Task<StandardApiResponse> UserPasswordUpdateV2(UserUpdate user)
        {
            try
            {
                var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
                var content = new StringContent(userJson, Encoding.UTF8, "application/json");
                var userResponse = await _httpClient.PutAsync($"{userV2ServiceUrl}/update-password", content);
                var responseString = await userResponse.Content.ReadAsStringAsync();
                var standardResponse = JsonSerializer.Deserialize<StandardApiResponse>(responseString);
                if (standardResponse == null)
                {
                    return new StandardApiResponse
                    {
                        Success = false,
                        Message = "Gateway Error: User Management Service returned an empty or unparseable response (despite 200 OK)."
                    };
                }
                return standardResponse;
            }
            catch (HttpRequestException ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway communication failed with User Management Service: {ex.Message}. Please try again later."
                };
            }
            catch (Exception ex)
            {
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway encountered an unexpected error: {ex.Message}. Check logs for details."
                };
            }
        }

        internal async Task<StandardApiResponse> UserIDV2(User user)
        {
            try
            {
                string userId = await GetUserID(user);

                return new StandardApiResponse
                {
                    Success = true,
                    Message = "User ID retrieved successfully.", // הודעה חדשה, יותר ספציפית
                    Data = userId // אובייקט אנונימי שמכיל רק את ה-ID
                };
            }

            catch (JsonException ex)
            {
                // טיפול בשגיאות פרסור JSON
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway Error: Failed to parse user service response JSON. Details: {ex.Message}"
                };
            }
            catch (HttpRequestException ex)
            {
                // טיפול בשגיאות HTTP (כמו 4xx, 5xx או בעיות רשת)
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway Error: Communication with User Management Service failed. Details: {ex.Message}"
                };
            }
            catch (Exception ex)
            {
                // טיפול בכל שגיאה אחרת
                return new StandardApiResponse
                {
                    Success = false,
                    Message = $"Gateway Error: An unexpected error occurred. Details: {ex.Message}"
                };
            }
        }

        internal async Task<string> GetUserID(User user)
        {
            var userJson = JsonSerializer.Serialize(user, new JsonSerializerOptions { WriteIndented = true });
            var userResponse = await _httpClient.PostAsync(
                $"{userV2ServiceUrl}/user-details", new StringContent(userJson, Encoding.UTF8, "application/json")
            );
            var responseString = await userResponse.Content.ReadAsStringAsync();

            var standardResponse = JsonSerializer.Deserialize<StandardApiResponse>(responseString);
            return ExtractUaerId(standardResponse).ToString();
        }

        internal int ExtractUaerId(StandardApiResponse standardApiResponse)
        {
            try
            {

                if (standardApiResponse.Success && standardApiResponse.Data != null)
                {
                    // 1. נסה לפרסר את ה-Data ל-JsonElement
                    if (standardApiResponse.Data is JsonElement dataElement)
                    {
                        // 2. נסה למצוא את המאפיין "id" בתוך ה-JsonElement
                        if (dataElement.TryGetProperty("id", out JsonElement idElement))
                        {
                            // 3. חלץ את ה-GUID מה-JsonElement
                            if (idElement.TryGetInt32(out int userIdAsIntd))
                            {
                                return userIdAsIntd;
                            }
                        }
                    }
                }
                throw new Exception("User ID not found in the response data or response was not successful.");
            }
            catch (Exception ex)
            {
                throw new Exception($"Error extracting user ID: {ex.Message}", ex);
            }
        }
    }
}
