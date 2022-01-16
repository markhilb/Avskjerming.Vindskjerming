using System.Data.Common;
using Calendar.Server.Application.Infrastructure;
using Microsoft.Extensions.Hosting;
using System.Threading;
using System.Threading.Tasks;
using Dapper;

namespace Calendar.Server.API.Services
{
    public class SqlSchemaService : IHostedService
    {
        protected readonly DbConnection _db;

        public SqlSchemaService(ISqlSettings settings) =>
            _db = DatabaseExtension.CreateSqlConnection(settings);

        public async Task StartAsync(CancellationToken cancellationToken)
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
                            Color VARCHAR(9),
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
                            Start DATETIME2,
                            ""End"" DATETIME2,
                            TeamId INT NULL FOREIGN KEY (TeamId) REFERENCES Teams(Id),
                        );

                        IF NOT EXISTS (
                            SELECT name
                            FROM sys.tables
                            WHERE name = 'EventEmployees'
                        ) CREATE TABLE EventEmployees (
                            Id INT NOT NULL IDENTITY PRIMARY KEY,
                            EventId INT FOREIGN KEY (EventId) REFERENCES Events(Id),
                            EmployeeId INT FOREIGN KEY (EmployeeId) REFERENCES Employees(Id),
                        );

                        IF NOT EXISTS (
                            SELECT name
                            FROM sys.tables
                            WHERE name = 'Password'
                        ) CREATE TABLE Password (
                            Id INT NOT NULL IDENTITY PRIMARY KEY,
                            Hash VARCHAR(256) NOT NULL,
                        );

                        INSERT INTO Password (Hash)
                        SELECT @Hash
                        WHERE NOT EXISTS (SELECT * FROM Password);";

            await _db.ExecuteAsync(sql, new { Hash = BaseHandler.ComputeSHA256Hash("passord") });
        }

        public Task StopAsync(CancellationToken cancellationToken) =>
            Task.CompletedTask;
    }
}
