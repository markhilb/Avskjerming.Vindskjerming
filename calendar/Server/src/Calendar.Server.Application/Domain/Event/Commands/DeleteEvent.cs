using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;

namespace Calendar.Server.Application.Domain.Event.Commands
{
    public class DeleteEventCommand : IRequest<bool>
    {
        public long EventId { get; set; }
    }

    public class DeleteEventHandler : BaseHandler, IRequestHandler<DeleteEventCommand, bool>
    {
        public DeleteEventHandler(ISqlSettings settings) : base(settings) { }

        public async Task<bool> Handle(DeleteEventCommand command, CancellationToken cancellationToken)
        {
            await DeleteEventEmployees(command.EventId);

            var sql = @"DELETE FROM Events
                        WHERE Id = @EventId";

            var deletedRows = await _db.ExecuteAsync(sql, command);
            return deletedRows == 1;
        }

        private async Task DeleteEventEmployees(long eventId)
        {
            var sql = @"DELETE FROM EventEmployees
                        WHERE EventId = @EventId";

            await _db.ExecuteAsync(sql, new { EventId = eventId });
        }
    }
}
