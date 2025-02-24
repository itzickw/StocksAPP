using System.Security.Cryptography;
using UserManager;
using Microsoft.IdentityModel.Tokens;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;

var builder = WebApplication.CreateBuilder(args);


// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient<UserManager.UserManager>(); // ????? ?? UserManager ?-Service

var rsa = RSA.Create();
rsa.ImportFromPem(@"-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxBodQO1w24R6s3Yqrr9L
XdAcyvzjvApxHLUqFSsAN/Rzlrxcna1sUCOHHQKwJck47jp2/SfsucsibCAgoxiP
w68iBAqZOg6M7sD/goUhMl+BjI3wY0m4C6xEWVTukqZWmRMA0EvxdqVXJodbeTGe
CcGkjIGj0njOw3kN5SZNZOZvVcP6lKn/CntrIlE11iw99xPQgBu/96/wX3aRpqta
SeCdA1Tux6h0beh6e7TwSqIsgN/DpjwpV99X73SI/WPntdM8JLj/CjKAeNC60YzU
y8i3X/M2x3J44A29k7JwNGRw7Lj5vKbsT9Fy8TjverjyDPPBNJ4Blq0mkzjD8KMj
iwIDAQAB
-----END PUBLIC KEY-----
");

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
}).AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateAudience = false,
        ValidAlgorithms = new List<string>() { "RS256" },
        ValidIssuer = "https://33704590271.propelauthtest.com",
        IssuerSigningKey = new RsaSecurityKey(rsa),
    };
});


var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();