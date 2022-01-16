using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Dtos.Authentication;
using Calendar.Server.Application.Infrastructure;
using MediatR;

namespace Calendar.Server.Application.Domain.Authentication.Commands
{
    public class LoginCommand : IRequest<bool>
    {
        public LoginDto LoginDto { get; set; }
    }

    public class LoginHandler : BaseHandler, IRequestHandler<LoginCommand, bool>
    {
        public LoginHandler(ISqlSettings settings) : base(settings) { }

        public async Task<bool> Handle(LoginCommand command, CancellationToken cancellationToken)
        {
            var hash = await _db.QuerySingleAsync<string>("SELECT Hash FROM Password");
            return hash == ComputeSHA256Hash(command.LoginDto.Password);
        }
    }
}
