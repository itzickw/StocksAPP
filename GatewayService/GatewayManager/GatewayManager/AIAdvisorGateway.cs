using Microsoft.Extensions.Options;
using System.Text;
using System.Text.Json;


namespace GatewayManager
{
    internal class AIAdvisorGateway
    {
        //private readonly string AIAdvisorURL = "http://localhost:9050/api/AI/";
        private readonly string AIAdvisorURL;
        private HttpClient httpClient;

        internal AIAdvisorGateway(HttpClient httpClient, IOptions<ServiceUrlsConfig> serviceUrlsOptions)
        {
            this.httpClient = httpClient;
            AIAdvisorURL = serviceUrlsOptions.Value.AIAdvisorURL;
        }

        internal async Task<string> GetAIAdvice(string query)
        {
            var advice = await httpClient.GetAsync($"{ AIAdvisorURL}AI-advice/{query}");
            return await advice.Content.ReadAsStringAsync();
        }
    }
}
