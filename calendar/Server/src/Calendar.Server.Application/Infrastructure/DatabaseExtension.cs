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
        public static void AddSqlSupport(this IServiceCollection services, IConfiguration configuration)
        {
            var sqlSettings = configuration.GetSection("DatabaseSettings");

            SqlMapper.AddTypeMap(typeof(DateTime), DbType.Date);
            // SqlMapper.AddTypeHandler(new DateTimeHandler());
            services.AddScoped((_) => CreateSqlConnection(sqlSettings.Get<SqlSettings>()));
        }

        private static DbConnection CreateSqlConnection(SqlSettings sqlSettings)
        {
            // var sqlConnection = new SqlConnection(sqlSettings.ConnectionString); // TODO: Fix this
            var sqlConnection = new SqlConnection("Server=db,1433; Database=master; User Id=sa; Password=1234abcd<>%&");

            sqlConnection.Open();
            return sqlConnection;
        }
    }
}
