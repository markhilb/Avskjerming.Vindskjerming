using System;
using System.Data;
using System.Data.Common;
using System.Data.SqlClient;
using Dapper;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Calendar.Server.Application.Infrastructure
{
    public static class DatabaseExtension
    {
        public static DbConnection CreateSqlConnection(ISqlSettings settings)
        {
            // var sqlConnection = new SqlConnection(sqlSettings.ConnectionString); // TODO: Fix this
            var connection = new SqlConnection("Server=localhost,1433; Database=master; User Id=sa; Password=1234abcd<>%&");

            connection.Open();
            return connection;
        }
    }
}
