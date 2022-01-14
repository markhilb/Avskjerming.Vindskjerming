using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Team;

namespace Calendar.Server.Application.Domain.Team.Commands
{
    public class CreateTeamCommand : IRequest<long>
    {
        public TeamDto Team { get; set; }
    }

    public class CreateTeamHandler : BaseHandler, IRequestHandler<CreateTeamCommand, long>
    {
        public CreateTeamHandler(ISqlSettings settings) : base(settings) { }

        public Task<long> Handle(CreateTeamCommand command, CancellationToken cancellationToken)
        {
            var sql = @"INSERT INTO Teams (
                            Name,
                            PrimaryColor,
                            SecondaryColor
                        ) OUTPUT INSERTED.Id
                        VALUES (
                            @Name,
                            @PrimaryColor,
                            @SecondaryColor
                        );";

            return _db.QuerySingleAsync<long>(sql, command.Team);
        }
    }
}
