using Calendar.Server.Application.Dtos.Team;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Calendar.Server.Application.Domain.Team.Commands;
using Calendar.Server.Application.Domain.Team.Queries;
using Microsoft.AspNetCore.Authorization;

namespace Calendar.Server.API.Controllers
{
    [ApiController]
    [Authorize]
    [Route("Teams")]
    public class TeamController : BaseController
    {
        public TeamController(ILogger<BaseController> logger, IMediator mediator) : base(logger, mediator) { }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<TeamDto>>> GetTeams(CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new GetTeamsQuery(), cancellationToken));

        [HttpPost]
        public async Task<ActionResult<long>> CreateTeam([FromBody] TeamDto teamDto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new CreateTeamCommand { Team = teamDto }, cancellationToken));

        [HttpPut]
        public async Task<ActionResult<bool>> UpdateTeam([FromBody] TeamDto teamDto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new UpdateTeamCommand { Team = teamDto }, cancellationToken));

        [HttpDelete("{id}")]
        public async Task<ActionResult<bool>> DeleteTeam(long id, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new DeleteTeamCommand { TeamId = id }, cancellationToken));
    }
}
