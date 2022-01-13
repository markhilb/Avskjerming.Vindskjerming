using Dapper;
using System.Data.Common;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Employee;

namespace Calendar.Server.Application.Domain.Employee.Commands
{
    public class UpdateEmployeeCommand : IRequest<bool>
    {
        public EmployeeDto Employee { get; set; }
    }

    public class UpdateEmployeeHandler : BaseHandler, IRequestHandler<UpdateEmployeeCommand, bool>
    {
        public UpdateEmployeeHandler(DbConnection db) : base(db) { }

        public async Task<bool> Handle(UpdateEmployeeCommand command, CancellationToken cancellationToken)
        {
            var sql = @"UPDATE Employees
                        SET Name = @Name
                        WHERE Id = @Id;";

            var updatedRows = await _db.ExecuteAsync(sql, command.Employee);
            return updatedRows == 1;
        }
    }
}
