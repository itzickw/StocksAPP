using AIManager;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.Configure<ServiceUrlsConfig>(builder.Configuration.GetSection("ServiceUrls"));
builder.Services.AddHttpClient("OllamaEndpoint", client =>
{
    var serviceUrlsConfig = builder.Configuration.GetSection("ServiceUrls").Get<ServiceUrlsConfig>();
    client.BaseAddress = new Uri(serviceUrlsConfig.OllamaEndpoint);
});

builder.Services.AddHttpClient("ChromaEndpoint", client =>
{
    var serviceUrlsConfig = builder.Configuration.GetSection("ServiceUrls").Get<ServiceUrlsConfig>();
    client.BaseAddress = new Uri(serviceUrlsConfig.ChromaEndpoint);
});

builder.Services.AddHttpClient<IAIService, AIService>(client =>
{
    client.Timeout = TimeSpan.FromMinutes(10);
});

builder.Services.AddControllers();
builder.Services.AddHttpClient();

builder.Services.AddControllers();
var app = builder.Build();

//if (app.Environment.IsDevelopment())
//{
//    app.UseSwagger();
//    app.UseSwaggerUI();
//}

app.UseSwagger();
app.UseSwaggerUI();

app.UseRouting();
app.UseAuthorization();
app.MapControllers();

app.UseHttpsRedirection();

app.Run();