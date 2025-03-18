using System.Text;
using System.Text.Json;


namespace GatewayManager
{
    internal class AIAdvisorGateway
    {
        private readonly string AIAdvisorURL = "http://localhost:9050/api/AI/";
        private HttpClient httpClient;

        internal AIAdvisorGateway(HttpClient httpClient)
        {
            this.httpClient = httpClient;
        }

        internal async Task<string> GetAIAdvice(string query)
        {
            var advice = await httpClient.GetAsync($"{ AIAdvisorURL}AI-advice/{query}");
            return await advice.Content.ReadAsStringAsync();
        }
    }
}
