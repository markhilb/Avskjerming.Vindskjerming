using System;
using MediatR;
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
    }
}
