using GatewayManager;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle

builder.Services.Configure<ServiceUrlsConfig>(builder.Configuration.GetSection("ServiceUrls"));
builder.Services.AddScoped<GatewayManager.GatewayManager>();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient<GatewayManager.GatewayManager>(client => {
    var serviceUrlsConfig = builder.Configuration.GetSection("ServiceUrls").Get<ServiceUrlsConfig>();
    client.BaseAddress = new Uri(serviceUrlsConfig.AIAdvisorURL); // ?? ?-appsettings.json ???? ??? AIAdvisor
    client.Timeout = TimeSpan.FromMinutes(10);
} );

builder.Services.AddHttpClient("AIAdvisorHttpClient", client =>
{
    var serviceUrlsConfig = builder.Configuration.GetSection("ServiceUrls").Get<ServiceUrlsConfig>();
    client.BaseAddress = new Uri(serviceUrlsConfig.AIAdvisorURL);
});

builder.Services.AddHttpClient("marketDataServiceHttpClient", client =>
{
    var serviceUrlsConfig = builder.Configuration.GetSection("ServiceUrls").Get<ServiceUrlsConfig>();
    client.BaseAddress = new Uri(serviceUrlsConfig.marketDataServiceURL);
});

builder.Services.AddHttpClient("stockServiceHttpClient", client =>
{
    var serviceUrlsConfig = builder.Configuration.GetSection("ServiceUrls").Get<ServiceUrlsConfig>();
    client.BaseAddress = new Uri(serviceUrlsConfig.stockServiceURL);
});

builder.Services.AddHttpClient("userV2ServiceHttpClient", client =>
{
    var serviceUrlsConfig = builder.Configuration.GetSection("ServiceUrls").Get<ServiceUrlsConfig>();
    client.BaseAddress = new Uri(serviceUrlsConfig.userV2ServiceUrl);
});


var app = builder.Build();

// Configure the HTTP request pipeline.
//if (app.Environment.IsDevelopment())
//{
//    app.UseSwagger();
//    app.UseSwaggerUI();
//}

app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
