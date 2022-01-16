using Calendar.Server.Application.Dtos.Event;
using Calendar.Server.Application.Domain.Event.Commands;
using Calendar.Server.Application.Domain.Event.Queries;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using Microsoft.AspNetCore.Authorization;

namespace Calendar.Server.API.Controllers
{
    [ApiController]
    [Authorize]
    [Route("Events")]
    public class EventController : BaseController
    {
        public EventController(ILogger<BaseController> logger, IMediator mediator) : base(logger, mediator) { }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<EventDto>>> GetEvents(
                [FromQuery] DateTime from, [FromQuery] DateTime to, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new GetEventsQuery { From = from, To = to }, cancellationToken));

        [HttpPost]
        public async Task<ActionResult<long>> CreateEvent([FromBody] EventDto eventDto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new CreateEventCommand { Event = eventDto }, cancellationToken));

        [HttpPut]
        public async Task<ActionResult<bool>> UpdateEvent([FromBody] EventDto eventDto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new UpdateEventCommand { Event = eventDto }, cancellationToken));

        [HttpDelete("{id}")]
        public async Task<ActionResult<bool>> DeleteEvent(long id, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new DeleteEventCommand { EventId = id }, cancellationToken));
    }
}
