using System;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using MediatR;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.Logging;

namespace Calendar.Server.API.Controllers
{
    [ApiController]
    [Produces("application/json")]
    public class BaseController : Controller
    {
        protected readonly IMediator _mediator;
        private readonly ILogger<BaseController> _logger;

        public BaseController(ILogger<BaseController> logger, IMediator mediator) =>
            (_logger, _mediator) = (logger, mediator);

        public override void OnActionExecuting(ActionExecutingContext context) =>
            _logger.LogInformation($"Entered action: {context.ActionDescriptor.DisplayName} - {DateTime.UtcNow.ToString("o")}");

        protected async Task SetAuthenticated()
        {
            var claims = new[]
            {
                new Claim("IsLoggedIn", true.ToString()),
            };
            var claimsIdentity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);
            var authProps = new AuthenticationProperties
            {
                IsPersistent = true,
                IssuedUtc = DateTime.UtcNow,
                ExpiresUtc = DateTimeOffset.UtcNow.AddYears(100),
                AllowRefresh = true,
            };

            await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, new ClaimsPrincipal(claimsIdentity), authProps);
        }

        protected bool GetAuthenticated() =>
            GetAuthenticated(HttpContext);

        public static bool GetAuthenticated(HttpContext context) =>
            context.User.Claims.FirstOrDefault(c => c.Type == "IsLoggedIn")?.Value != null;
    }
}
