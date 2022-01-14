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
    public class UpdateEventCommand : IRequest<bool>
    {
        public EventDto Event { get; set; }
    }

    public class UpdateEventHandler : BaseHandler, IRequestHandler<UpdateEventCommand, bool>
    {
        public UpdateEventHandler(ISqlSettings settings) : base(settings) { }

        public async Task<bool> Handle(UpdateEventCommand command, CancellationToken cancellationToken)
        {
            var sql = @"UPDATE Events
                        SET Title = @Title,
                            Details = @Details,
                            Start = @Start,
                            ""End"" = @End,
                            TeamId = @TeamId
                        WHERE Id = @Id;";

            var updatedRows = await _db.ExecuteAsync(sql, command.Event);
            await UpdateEventEmployees(command.Event.Id, command.Event.Employees);
            return updatedRows == 1;

        }

        private async Task UpdateEventEmployees(long eventId, IEnumerable<EmployeeDto> employees)
        {
            var delete = @"DELETE FROM EventEmployees
                           WHERE EventId = @EventId";

            await _db.ExecuteAsync(delete, new { EventId = eventId });

            var sql = @"INSERT INTO EventEmployees (
                            EventId,
                            EmployeeId
                        ) VALUES (
                            @EventId,
                            @EmployeeId
                        )";

            await _db.ExecuteAsync(sql, employees.Select(e => new { EventId = eventId, EmployeeId = e.Id }));
        }
    }
}
