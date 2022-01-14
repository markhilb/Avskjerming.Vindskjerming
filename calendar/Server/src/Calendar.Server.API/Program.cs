using Calendar.Server.API.Services;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.Configure<SqlSettings>(builder.Configuration.GetSection("DatabaseSettings"));

builder.Services.AddSingleton<ISqlSettings>(s => s.GetRequiredService<IOptions<SqlSettings>>().Value);

builder.Services.AddMediatR(typeof(BaseHandler).Assembly);

builder.Services.AddHostedService<SqlSchemaService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
// #if DEBUG
app.UseSwagger();
app.UseSwaggerUI();
// #endif

app.UseCors(builder =>
{
    builder
    .WithOrigins("http://localhost:4200", "http://localhost:5000", "http://localhost:12000")
    .AllowAnyHeader()
    .AllowAnyMethod()
    .AllowCredentials();
});

app.UseHttpsRedirection();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();
