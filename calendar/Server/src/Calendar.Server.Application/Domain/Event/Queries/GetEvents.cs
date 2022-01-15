using Dapper;
using System;
using System.Linq;
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
        public DateTime From { get; set; }
        public DateTime To { get; set; } = DateTime.UtcNow;
    }

    public class GetEventsHandler : BaseHandler, IRequestHandler<GetEventsQuery, IEnumerable<EventDto>>
    {
        public GetEventsHandler(ISqlSettings settings) : base(settings) { }

        public async Task<IEnumerable<EventDto>> Handle(GetEventsQuery query, CancellationToken cancellationToken)
        {
            var sql = @"SELECT *
                        FROM Events e
                        LEFT JOIN Teams t ON e.TeamId = t.Id
                        WHERE e.Start BETWEEN @From AND @To
                           OR e.""End"" BETWEEN @From AND @To
                           OR (e.Start < @From AND e.""End"" > @To)";

            var events = await _db.QueryAsync<EventDto, TeamDto, EventDto>(sql, param: query, splitOn: "Id", map: (e, t) => { e.Team = t; return e; });
            await Task.WhenAll(events.Select(async e => e.Employees = await GetEmployees(e.Id)));

            return events;
        }

        private Task<IEnumerable<EmployeeDto>> GetEmployees(long eventId)
        {
            var sql = @"SELECT e.*
                        FROM Employees e
                        INNER JOIN EventEmployees em ON em.EmployeeId = e.Id
                        WHERE em.EventId = @EventId";

            return _db.QueryAsync<EmployeeDto>(sql, new { EventId = eventId });
        }
    }
}
