using System;
using Dapper;
using Calendar.Server.API.Services;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;
using FluentValidation.AspNetCore;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers()
    .AddFluentValidation(c => c.RegisterValidatorsFromAssemblyContaining<EventValidator>());
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.Configure<SqlSettings>(builder.Configuration.GetSection("DatabaseSettings"));
SqlMapper.AddTypeMap(typeof(DateTime), System.Data.DbType.DateTime2);

builder.Services.AddSingleton<ISqlSettings>(s => s.GetRequiredService<IOptions<SqlSettings>>().Value);

builder.Services.AddMediatR(typeof(BaseHandler).Assembly);

builder.Services.AddHostedService<SqlSchemaService>();

builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme).AddCookie(options =>
{
    options.LoginPath = new PathString("/Authentication/Login");
    options.SlidingExpiration = true;
    options.Events.OnRedirectToLogin = context =>
    {
        context.Response.StatusCode = 401;
        return Task.CompletedTask;
    };
});

var app = builder.Build();

// Configure the HTTP request pipeline.
#if DEBUG
app.UseSwagger();
app.UseSwaggerUI();
#endif

app.UseCors(builder =>
{
    builder
#if DEBUG
    .WithOrigins("http://localhost:4200", "http://localhost:5000", "http://localhost:12000")
#else
    .WithOrigins("https://calendar.hilbertsen.com")
#endif
    .AllowAnyHeader()
    .AllowAnyMethod()
    .AllowCredentials();
});

app.UseHttpsRedirection();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();
