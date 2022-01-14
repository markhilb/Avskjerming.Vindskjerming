using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using System;

namespace Calendar.Server.Application.Domain.Employee.Commands
{
    public class DeleteEmployeeCommand : IRequest<bool>
    {
        public long EmployeeId { get; set; }
    }

    public class DeleteEmployeeHandler : BaseHandler, IRequestHandler<DeleteEmployeeCommand, bool>
    {
        public DeleteEmployeeHandler(ISqlSettings settings) : base(settings) { }

        public async Task<bool> Handle(DeleteEmployeeCommand command, CancellationToken cancellationToken)
        {
            var sql = @"UPDATE Employees
                        SET Disabled = 1
                        WHERE Id = @EmployeeId;";

            var deletedRows = await _db.ExecuteAsync(sql, command);
            Console.WriteLine(deletedRows);
            return deletedRows == 1;
        }
    }
}
