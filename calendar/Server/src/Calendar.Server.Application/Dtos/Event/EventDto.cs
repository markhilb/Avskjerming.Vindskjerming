using System;
using System.Collections.Generic;
using Calendar.Server.Application.Dtos.Employee;
using Calendar.Server.Application.Dtos.Team;

namespace Calendar.Server.Application.Dtos.Event
{
    public class EventDto
    {
        public long Id { get; set; }
        public string Title { get; set; }
        public string Details { get; set; }
        public DateTime Start { get; set; }
        public DateTime End { get; set; }
        public long? TeamId { get; set; }
        public TeamDto Team { get; set; }
        public IEnumerable<EmployeeDto> Employees { get; set; }
    }
}
