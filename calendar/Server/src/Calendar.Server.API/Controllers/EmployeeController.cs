using Calendar.Server.Application.Dtos.Employee;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Calendar.Server.Application.Domain.Employee.Commands;
using Calendar.Server.Application.Domain.Employee.Queries;

namespace Calendar.Server.API.Controllers
{
    [ApiController]
    [Route("Employees")]
    public class EmployeeController : BaseController
    {
        public EmployeeController(ILogger<BaseController> logger, IMediator mediator) : base(logger, mediator) {}

        [HttpGet]
        public async Task<ActionResult<IEnumerable<EmployeeDto>>> GetEmployeesAsync(CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new GetEmployeesQuery(), cancellationToken));

        [HttpPost]
        public async Task<ActionResult<long>> CreateEmployee([FromBody] EmployeeDto employeeDto, CancellationToken cancellationToken) =>
            Ok(await _mediator.Send(new CreateEmployeeCommand { Employee = employeeDto }, cancellationToken));

        [HttpPut]
        public ActionResult<bool> UpdateEmployee([FromBody] EmployeeDto employeeDto)
        {
            return Ok(true);
        }

        [HttpDelete("{id}")]
        public ActionResult<bool> DeleteEmployee(long id)
        {
            return Ok(true);
        }
    }
}
