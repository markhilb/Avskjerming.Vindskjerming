using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Dtos.Authentication;
using Calendar.Server.Application.Infrastructure;
using MediatR;

namespace Calendar.Server.Application.Domain.Authentication.Commands
{
    public class ChangePasswordCommand : IRequest<bool>
    {
        public ChangePasswordDto ChangePasswordDto { get; set; }
    }

    public class ChangePasswordHandler : BaseHandler, IRequestHandler<ChangePasswordCommand, bool>
    {
        public ChangePasswordHandler(ISqlSettings settings) : base(settings) { }

        public async Task<bool> Handle(ChangePasswordCommand command, CancellationToken cancellationToken)
        {
            var hash = await _db.QuerySingleAsync<string>("SELECT Hash FROM Password");
            if (hash != ComputeSHA256Hash(command.ChangePasswordDto.OldPassword))
                return false;

            var updatedRows = await _db.ExecuteAsync("UPDATE Password SET Hash = @Hash", new { Hash = ComputeSHA256Hash(command.ChangePasswordDto.NewPassword) });
            return updatedRows == 1;
        }
    }
}
