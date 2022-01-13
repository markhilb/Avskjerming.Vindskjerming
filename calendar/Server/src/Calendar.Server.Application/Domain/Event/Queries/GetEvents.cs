using Dapper;
using System.Data.Common;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Event;
using Calendar.Server.Application.Dtos.Team;
using System.Collections.Generic;
using Calendar.Server.Application.Dtos.Employee;

namespace Calendar.Server.Application.Domain.Event.Queries
{
    public class GetEventsQuery : IRequest<IEnumerable<EventDto>>
    {
        public EventDto Event { get; set; }
    }

    public class GetEventsHandler : BaseHandler, IRequestHandler<GetEventsQuery, IEnumerable<EventDto>>
    {
        public GetEventsHandler(DbConnection db) : base(db) { }

        public async Task<IEnumerable<EventDto>> Handle(GetEventsQuery query, CancellationToken cancellationToken)
        {
            var sql = @"SELECT *
                        FROM Events e
                        INNER JOIN Teams t ON e.TeamId = t.Id";

            var events = await _db.QueryAsync<EventDto, TeamDto, EventDto>(sql, splitOn: "Id", map: (e, t) => { e.Team = t; return e; });
            foreach (var e in events)
                e.Employees = await GetEmployees(e.Id);

            return events;
        }

        private Task<IEnumerable<EmployeeDto>> GetEmployees(long eventId)
        {
            var sql = @"SELECT e.Id Id,
                               e.Name Name
                        FROM Employees e
                        INNER JOIN EventEmployees em ON em.EmployeeId = e.Id
                        WHERE em.EventId = @EventId";

            return _db.QueryAsync<EmployeeDto>(sql, new { EventId = eventId });
        }
    }
}
