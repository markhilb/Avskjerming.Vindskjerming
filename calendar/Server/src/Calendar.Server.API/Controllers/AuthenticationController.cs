using System;
using System.Security.Claims;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Domain.Authentication.Commands;
using Calendar.Server.Application.Dtos.Authentication;
using MediatR;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace Calendar.Server.API.Controllers
{
    [ApiController]
    [Route("Authentication")]
    public class AuthenticationController : BaseController
    {
        public AuthenticationController(ILogger<BaseController> logger, IMediator mediator) : base(logger, mediator) { }

        [HttpPost("Login")]
        public async Task<ActionResult<bool>> Login([FromBody] LoginDto login, CancellationToken cancellationToken)
        {
            var ok = await _mediator.Send(new LoginCommand { LoginDto = login }, cancellationToken);
            if (ok)
            {
                var claimsIdentity = new ClaimsIdentity(CookieAuthenticationDefaults.AuthenticationScheme);
                var authProps = new AuthenticationProperties
                {
                    IsPersistent = true,
                    IssuedUtc = DateTime.UtcNow,
                    ExpiresUtc = DateTimeOffset.UtcNow.AddYears(100),
                    AllowRefresh = true,
                };

                await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, new ClaimsPrincipal(claimsIdentity), authProps);
            }

            return Ok(ok);
        }

        [HttpPost("Logout")]
        public async Task<IActionResult> Login(CancellationToken cancellationToken)
        {
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            return Ok();
        }

        [HttpGet("IsLoggedIn")]
        public ActionResult<bool> IsLoggedIn(CancellationToken cancellationToken) =>
            Ok(HttpContext.User.Identity.IsAuthenticated);

        [HttpPost("ChangePassword")]
        public async Task<ActionResult<bool>> ChangePassword([FromBody] ChangePasswordDto dto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new ChangePasswordCommand { ChangePasswordDto = dto }, cancellationToken));
    }
}
