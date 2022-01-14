using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Team;

namespace Calendar.Server.Application.Domain.Team.Commands
{
    public class UpdateTeamCommand : IRequest<bool>
    {
        public TeamDto Team { get; set; }
    }

    public class UpdateTeamHandler : BaseHandler, IRequestHandler<UpdateTeamCommand, bool>
    {
        public UpdateTeamHandler(ISqlSettings settings) : base(settings) { }

        public async Task<bool> Handle(UpdateTeamCommand command, CancellationToken cancellationToken)
        {
            var sql = @"UPDATE Teams
                        SET Name = @Name,
                            PrimaryColor = @PrimaryColor,
                            SecondaryColor = @SecondaryColor
                        WHERE Id = @Id;";

            var updatedRows = await _db.ExecuteAsync(sql, command.Team);
            return updatedRows == 1;
        }
    }
}
