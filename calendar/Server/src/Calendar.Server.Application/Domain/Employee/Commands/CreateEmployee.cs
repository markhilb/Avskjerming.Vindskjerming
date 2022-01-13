using Dapper;
using System.Data.Common;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Employee;

namespace Calendar.Server.Application.Domain.Employee.Commands
{
    public class CreateEmployeeCommand : IRequest<long>
    {
        public EmployeeDto Employee { get; set; }
    }

    public class CreateEmployeeHandler : BaseHandler, IRequestHandler<CreateEmployeeCommand, long>
    {
        public CreateEmployeeHandler(DbConnection db) : base(db) { }

        public Task<long> Handle(CreateEmployeeCommand command, CancellationToken cancellationToken)
        {
            var sql = @"INSERT INTO Employees (
                            Name
                        ) OUTPUT INSERTED.Id
                        VALUES (
                            @Name
                        );";

            return _db.QuerySingleAsync<long>(sql, command.Employee);
        }
    }
}