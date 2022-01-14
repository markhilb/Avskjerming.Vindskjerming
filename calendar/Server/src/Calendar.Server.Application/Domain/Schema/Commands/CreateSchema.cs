using Dapper;
using System.Data.Common;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using System;

namespace Calendar.Server.Application.Domain.Schema.Commands
{
    public class CreateSchemaCommand : IRequest<bool>
    {
    }

    public class CreateSchemaHandler : BaseHandler, IRequestHandler<CreateSchemaCommand, bool>
    {
        public CreateSchemaHandler(ISqlSettings settings) : base(settings) { }

        public Task<bool> Handle(CreateSchemaCommand command, CancellationToken cancellationToken)
        {
            return Task.FromResult(true); // TODO: Check if executed correct
        }
    }
}
