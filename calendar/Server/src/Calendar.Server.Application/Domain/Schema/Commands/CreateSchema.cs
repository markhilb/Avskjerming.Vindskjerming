using Dapper;
using System.Data.Common;
using System.Threading;
using System.Threading.Tasks;
using Calendar.Server.Application.Infrastructure;
using MediatR;

namespace Calendar.Server.Application.Domain.Schema.Commands
{
    public class CreateSchemaCommand : IRequest<bool>
    {
    }

    public class CreateSchemaHandler : BaseHandler, IRequestHandler<CreateSchemaCommand, bool>
    {
        public CreateSchemaHandler(DbConnection db) : base(db) { }

        public async Task<bool> Handle(CreateSchemaCommand command, CancellationToken cancellationToken)
        {
            var sql = @"IF NOT EXISTS (
                            SELECT name
                            FROM sys.tables
                            WHERE name = 'Teams'
                        ) CREATE TABLE Teams (
                            Id INT NOT NULL IDENTITY PRIMARY KEY,
                            Name VARCHAR(255),
                            PrimaryColor VARCHAR(9),
                            SecondaryColor VARCHAR(9),
                            Disabled BIT DEFAULT 0
                        );

                        IF NOT EXISTS (
                            SELECT name
                            FROM sys.tables
                            WHERE name = 'Employees'
                        ) CREATE TABLE Employees (
                            Id INT NOT NULL IDENTITY PRIMARY KEY,
                            Name VARCHAR(255),
                            Disabled BIT DEFAULT 0
                        );

                        IF NOT EXISTS (
                            SELECT name
                            FROM sys.tables
                            WHERE name = 'Events'
                        ) CREATE TABLE Events (
                            Id INT NOT NULL IDENTITY PRIMARY KEY,
                            Title VARCHAR(255),
                            Details VARCHAR(255),
                            Start DATETIME,
                            ""End"" DATETIME,
                            TeamId INT FOREIGN KEY (TeamId) REFERENCES Teams(Id),
                        );

                        IF NOT EXISTS (
                            SELECT name
                            FROM sys.tables
                            WHERE name = 'EventEmployees'
                        ) CREATE TABLE EventEmployees (
                            Id INT NOT NULL IDENTITY PRIMARY KEY,
                            EventId INT FOREIGN KEY (EventId) REFERENCES Events(Id),
                            EmployeeId INT FOREIGN KEY (EmployeeId) REFERENCES Employees(Id),
                        );";

            await _db.ExecuteAsync(sql);
            return true; // TODO: Check if executed correct
        }
    }
}
