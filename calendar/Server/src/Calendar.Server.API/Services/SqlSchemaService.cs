using Calendar.Server.Application.Domain.Schema.Commands;
using MediatR;
using Microsoft.Extensions.Hosting;
using System.Threading;
using System.Threading.Tasks;

namespace Calendar.Server.API.Services
{
    public class SqlSchemaService : IHostedService
    {
        protected readonly IMediator _mediator;

        public SqlSchemaService(IMediator mediator) =>
            _mediator = mediator;

        public async Task StartAsync(CancellationToken cancellationToken) =>
            await _mediator.Send(new CreateSchemaCommand(), cancellationToken);

        public Task StopAsync(CancellationToken cancellationToken) =>
            Task.CompletedTask;
    }
}
