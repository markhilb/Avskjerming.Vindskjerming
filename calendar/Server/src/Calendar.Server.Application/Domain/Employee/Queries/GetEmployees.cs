using Dapper;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;
using Calendar.Server.Application.Dtos.Employee;
using System.Collections.Generic;

namespace Calendar.Server.Application.Domain.Employee.Queries
{
    public class GetEmployeesQuery : IRequest<IEnumerable<EmployeeDto>>
    {
    }

    public class GetEmployeesHandler : BaseHandler, IRequestHandler<GetEmployeesQuery, IEnumerable<EmployeeDto>>
    {
        public GetEmployeesHandler(ISqlSettings settings) : base(settings) { }

        public Task<IEnumerable<EmployeeDto>> Handle(GetEmployeesQuery query, CancellationToken cancellationToken) =>
            _db.QueryAsync<EmployeeDto>("SELECT * FROM Employees WHERE Disabled = 0");
    }
}
