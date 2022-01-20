using Dapper;
using System.Data.Common;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Team;
using System.Collections.Generic;

namespace Calendar.Server.Application.Domain.Team.Queries
{
    public class GetTeamsQuery : IRequest<IEnumerable<TeamDto>>
    {
    }

    public class GetTeamsHandler : BaseHandler, IRequestHandler<GetTeamsQuery, IEnumerable<TeamDto>>
    {
        public GetTeamsHandler(DbConnection db) : base(db) { }

        public Task<IEnumerable<TeamDto>> Handle(GetTeamsQuery query, CancellationToken cancellationToken) =>
            _db.QueryAsync<TeamDto>("SELECT * FROM Teams WHERE Disabled = 0");
    }
}
