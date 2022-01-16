using Calendar.Server.Application.Dtos.Employee;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Calendar.Server.Application.Domain.Employee.Commands;
using Calendar.Server.Application.Domain.Employee.Queries;
using Microsoft.AspNetCore.Authorization;

namespace Calendar.Server.API.Controllers
{
    [ApiController]
    [Authorize]
    [Route("Employees")]
    public class EmployeeController : BaseController
    {
        public EmployeeController(ILogger<BaseController> logger, IMediator mediator) : base(logger, mediator) { }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<EmployeeDto>>> GetEmployees(CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new GetEmployeesQuery(), cancellationToken));

        [HttpPost]
        public async Task<ActionResult<long>> CreateEmployee([FromBody] EmployeeDto employeeDto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new CreateEmployeeCommand { Employee = employeeDto }, cancellationToken));

        [HttpPut]
        public async Task<ActionResult<bool>> UpdateEmployee([FromBody] EmployeeDto employeeDto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new UpdateEmployeeCommand { Employee = employeeDto }, cancellationToken));

        [HttpDelete("{id}")]
        public async Task<ActionResult<bool>> DeleteEmployee(long id, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new DeleteEmployeeCommand { EmployeeId = id }, cancellationToken));
    }
}
