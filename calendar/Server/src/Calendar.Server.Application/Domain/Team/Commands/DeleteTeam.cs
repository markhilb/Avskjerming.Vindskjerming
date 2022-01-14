using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;

namespace Calendar.Server.Application.Domain.Team.Commands
{
    public class DeleteTeamCommand : IRequest<bool>
    {
        public long TeamId { get; set; }
    }

    public class DeleteTeamHandler : BaseHandler, IRequestHandler<DeleteTeamCommand, bool>
    {
        public DeleteTeamHandler(ISqlSettings settings) : base(settings) { }

        public async Task<bool> Handle(DeleteTeamCommand command, CancellationToken cancellationToken)
        {
            var sql = @"UPDATE Teams
                        SET Disabled = 1
                        WHERE Id = @TeamId;";

            var deletedRows = await _db.ExecuteAsync(sql, command);
            return deletedRows == 1;
        }
    }
}
