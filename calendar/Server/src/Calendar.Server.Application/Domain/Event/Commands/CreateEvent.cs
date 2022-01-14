using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Event;
using System.Data;
using System.Collections.Generic;
using Calendar.Server.Application.Dtos.Employee;
using System.Linq;

namespace Calendar.Server.Application.Domain.Event.Commands
{
    public class CreateEventCommand : IRequest<long>
    {
        public EventDto Event { get; set; }
    }

    public class CreateEventHandler : BaseHandler, IRequestHandler<CreateEventCommand, long>
    {
        public CreateEventHandler(ISqlSettings settings) : base(settings) { }

        public async Task<long> Handle(CreateEventCommand command, CancellationToken cancellationToken)
        {
            var sql = @"INSERT INTO Events (
                            Title,
                            Details,
                            Start,
                            ""End"",
                            TeamId
                        ) OUTPUT INSERTED.Id
                        VALUES (
                            @Title,
                            @Details,
                            @Start,
                            @End,
                            @TeamId
                        );";

            var id = await _db.QuerySingleAsync<long>(sql, command.Event);
            await InsertEventEmployees(id, command.Event.Employees);
            return id;

        }

        private Task InsertEventEmployees(long eventId, IEnumerable<EmployeeDto> employees)
        {
            var sql = @"INSERT INTO EventEmployees (
                            EventId,
                            EmployeeId
                        ) VALUES (
                            @EventId,
                            @EmployeeId
                        )";

            return _db.ExecuteAsync(sql, employees.Select(e => new { EventId = eventId, EmployeeId = e.Id }));
        }
    }
}
